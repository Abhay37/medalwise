#!/usr/bin/env python3
"""Publish due posts from autopost/schedule.json to Instagram and Facebook.

Uses the Meta Graph API with one Page access token (env META_PAGE_TOKEN), and
optionally the YouTube Data API v3 for Shorts (env YT_CLIENT_ID, YT_CLIENT_SECRET,
YT_REFRESH_TOKEN; posts list "youtube" in networks).
Run by .github/workflows/autopost.yml every 15 minutes. Standard library only.

  python3 autopost/post.py check      # verify the token, Page and Instagram link
  python3 autopost/post.py run        # publish everything that is due
  python3 autopost/post.py run --dry  # show what would be published
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "config.json")
SCHEDULE = os.path.join(HERE, "schedule.json")
STATE = os.path.join(HERE, "state.json")


def load(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default


def save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


class GraphError(Exception):
    pass


class Graph:
    def __init__(self, token, version):
        self.token = token
        self.base = "https://graph.facebook.com/" + version + "/"

    def call(self, method, path, **params):
        params["access_token"] = self.token
        data = urllib.parse.urlencode(params).encode()
        url = self.base + path
        if method == "GET":
            req = urllib.request.Request(url + "?" + data.decode())
        else:
            req = urllib.request.Request(url, data=data, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            try:
                err = json.load(e).get("error", {})
                msg = err.get("error_user_msg") or err.get("message") or str(err)
            except Exception:
                msg = str(e)
            raise GraphError(msg) from None


def use_page_token(g, cfg):
    """Accept either a Page token or a long-lived user token in META_PAGE_TOKEN.

    With a user token, ask Meta for the Page's own token and use that instead.
    The token is never printed.
    """
    try:
        page_token = g.call("GET", cfg["facebook_page_id"], fields="access_token").get("access_token")
    except GraphError:
        return
    if page_token:
        g.token = page_token


def media_url(cfg, media):
    """A full URL is used as is; a repo path is served from GitHub Pages."""
    if media.startswith("http://") or media.startswith("https://"):
        return media
    return cfg["media_base_url"].rstrip("/") + "/" + media.lstrip("/")


def ig_user_id(g, cfg):
    page = g.call("GET", cfg["facebook_page_id"], fields="name,instagram_business_account{id,username}")
    acct = page.get("instagram_business_account")
    if not acct:
        raise GraphError("The Facebook Page has no linked Instagram Business or Creator account.")
    return acct["id"], acct.get("username", ""), page.get("name", "")


def publish_instagram(g, ig_id, post, url):
    kind = post.get("type", "image")
    caption = post.get("caption", "")
    if kind == "reel":
        params = {"media_type": "REELS", "video_url": url, "caption": caption, "share_to_feed": "true"}
        if post.get("cover"):
            params["cover_url"] = post["cover"]
    elif kind == "story":
        params = {"media_type": "STORIES"}
        params["video_url" if url.lower().endswith(".mp4") else "image_url"] = url
    else:
        params = {"image_url": url, "caption": caption}
    container = g.call("POST", ig_id + "/media", **params)["id"]
    # Videos are processed asynchronously; images are usually ready at once.
    for _ in range(60):
        status = g.call("GET", container, fields="status_code,status").get("status_code")
        if status == "FINISHED":
            break
        if status in ("ERROR", "EXPIRED"):
            raise GraphError("Instagram could not process the media (" + status + ").")
        time.sleep(10)
    else:
        raise GraphError("Instagram media was still processing after 10 minutes.")
    media_id = g.call("POST", ig_id + "/media_publish", creation_id=container)["id"]
    link = g.call("GET", media_id, fields="permalink").get("permalink", "")
    return link or media_id


def publish_facebook(g, page_id, post, url):
    caption = post.get("caption", "")
    if url.lower().endswith(".mp4"):
        vid = g.call("POST", page_id + "/videos", file_url=url, description=caption)["id"]
        return "https://www.facebook.com/" + vid
    res = g.call("POST", page_id + "/photos", url=url, caption=caption)
    return "https://www.facebook.com/" + res.get("post_id", res.get("id", ""))


class YouTube:
    """Uploads Shorts with the YouTube Data API v3 (env YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN)."""

    def __init__(self):
        self.client_id = os.environ.get("YT_CLIENT_ID", "").strip()
        self.client_secret = os.environ.get("YT_CLIENT_SECRET", "").strip()
        self.refresh_token = os.environ.get("YT_REFRESH_TOKEN", "").strip()
        self.access = None

    def ready(self):
        return bool(self.client_id and self.client_secret and self.refresh_token)

    def _request(self, req):
        try:
            return urllib.request.urlopen(req, timeout=300)
        except urllib.error.HTTPError as e:
            try:
                body = json.load(e)
                err = body.get("error")
                msg = err.get("message") if isinstance(err, dict) else (body.get("error_description") or err)
            except Exception:
                msg = str(e)
            raise GraphError("YouTube: " + str(msg)) from None

    def token(self):
        if self.access is None:
            data = urllib.parse.urlencode({
                "client_id": self.client_id, "client_secret": self.client_secret,
                "refresh_token": self.refresh_token, "grant_type": "refresh_token",
            }).encode()
            with self._request(urllib.request.Request("https://oauth2.googleapis.com/token", data=data)) as r:
                self.access = json.load(r)["access_token"]
        return self.access

    def channel(self):
        req = urllib.request.Request(
            "https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true",
            headers={"Authorization": "Bearer " + self.token()})
        with self._request(req) as r:
            items = json.load(r).get("items", [])
        if not items:
            raise GraphError("YouTube: this Google account has no channel.")
        return items[0]["snippet"].get("title", ""), items[0]["id"]

    def upload(self, video, title, description):
        meta = json.dumps({
            "snippet": {"title": title, "description": description, "categoryId": "27"},
            "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False},
        }).encode()
        req = urllib.request.Request(
            "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
            data=meta, method="POST", headers={
                "Authorization": "Bearer " + self.token(),
                "Content-Type": "application/json; charset=UTF-8",
                "X-Upload-Content-Type": "video/mp4",
                "X-Upload-Content-Length": str(len(video)),
            })
        with self._request(req) as r:
            location = r.headers["Location"]
        put = urllib.request.Request(location, data=video, method="PUT", headers={
            "Authorization": "Bearer " + self.token(), "Content-Type": "video/mp4"})
        with self._request(put) as r:
            vid = json.load(r)["id"]
        return "https://youtube.com/shorts/" + vid


def video_bytes(cfg, media):
    """Read the mp4 from the checkout when it is a repo path, otherwise download it."""
    if not media.startswith(("http://", "https://")):
        path = os.path.join(os.path.dirname(HERE), media.lstrip("/"))
        if os.path.exists(path):
            with open(path, "rb") as f:
                return f.read()
    with urllib.request.urlopen(media_url(cfg, media), timeout=300) as r:
        return r.read()


def shorts_text(post):
    """Title: the caption's first line plus #Shorts (max 100 chars). Description: the caption."""
    caption = post.get("caption", "")
    clean = caption.replace("<", "").replace(">", "")
    hook = post.get("yt_title") or next((l.strip() for l in clean.splitlines() if l.strip()), "Medalwise")
    tag = " #Shorts"
    if len(hook) + len(tag) > 100:
        hook = hook[:100 - len(tag) - 1].rstrip() + "…"
    return hook + tag, clean[:4900]


def publish_youtube(yt, cfg, post):
    if not post.get("media", "").lower().endswith(".mp4"):
        raise GraphError("YouTube needs an mp4 video.")
    title, desc = shorts_text(post)
    return yt.upload(video_bytes(cfg, post["media"]), title, desc)


def parse_time(s):
    t = datetime.fromisoformat(s)
    if t.tzinfo is None:
        raise ValueError("time needs a timezone offset, e.g. 2026-10-27T20:00:00+05:30")
    return t


def check(g, cfg):
    me = g.call("GET", "me", fields="id,name")
    ig_id, username, page_name = ig_user_id(g, cfg)
    print("Token works for:", me.get("name"), "(" + me.get("id", "") + ")")
    print("Facebook Page:", page_name, cfg["facebook_page_id"])
    print("Instagram:", "@" + username, ig_id)
    try:
        lim = g.call("GET", ig_id + "/content_publishing_limit", fields="quota_usage,config")
        print("Instagram posts used in the last 24 h:", json.dumps(lim.get("data", lim)))
    except GraphError as e:
        print("Could not read the publishing limit:", e)
    yt = YouTube()
    if yt.ready():
        title, cid = yt.channel()
        print("YouTube channel:", title, cid)
    else:
        print("YouTube: not set up (add YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN secrets).")


def run(g, cfg, dry):
    schedule = load(SCHEDULE, {"posts": []})["posts"]
    state = load(STATE, {})
    now = datetime.now(timezone.utc)
    late = timedelta(hours=cfg.get("skip_if_late_hours", 6))
    ig = None
    yt = YouTube()
    changed = False
    for post in schedule:
        pid = post["id"]
        when = parse_time(post["time"])
        if when > now:
            continue
        done = state.setdefault(pid, {})
        for net in post.get("networks", ["instagram", "facebook"]):
            if done.get(net, {}).get("status") in ("published", "skipped"):
                continue
            if now - when > late:
                done[net] = {"status": "skipped", "reason": "more than %s hours late" % cfg.get("skip_if_late_hours", 6), "at": now.isoformat()}
                print("SKIP", pid, net, "(too late)")
                changed = True
                continue
            if net == "youtube" and not yt.ready():
                print("WAIT", pid, net, "(YouTube secrets not added yet)")
                continue
            url = media_url(cfg, post["media"])
            if dry:
                print("WOULD POST", pid, net, url)
                continue
            try:
                if net == "instagram":
                    if ig is None:
                        ig = ig_user_id(g, cfg)[0]
                    link = publish_instagram(g, ig, post, url)
                elif net == "facebook":
                    link = publish_facebook(g, cfg["facebook_page_id"], post, url)
                elif net == "youtube":
                    link = publish_youtube(yt, cfg, post)
                else:
                    raise GraphError("unknown network " + net)
                done[net] = {"status": "published", "link": link, "at": now.isoformat()}
                print("POSTED", pid, net, link)
            except GraphError as e:
                tries = done.get(net, {}).get("tries", 0) + 1
                # Retried on the next runs; given up after max_tries so one bad post can't block the rest.
                status = "skipped" if tries >= cfg.get("max_tries", 3) else "retry"
                done[net] = {"status": status, "error": str(e), "tries": tries, "at": now.isoformat()}
                print("ERROR", pid, net, e)
            changed = True
    if changed and not dry:
        save(STATE, state)
    errors = [p + "/" + n for p, nets in state.items() for n, v in nets.items() if v.get("status") == "retry"]
    return 1 if errors else 0


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "run"
    cfg = load(CONFIG, {})
    token = os.environ.get("META_PAGE_TOKEN", "").strip()
    if not token:
        msg = "META_PAGE_TOKEN is not set. Add it under repo Settings > Secrets and variables > Actions."
        if mode == "check":
            sys.exit(msg)
        # Scheduled runs stay green until the token is added, so nobody gets failure emails.
        print(msg, "Nothing posted.")
        return
    g = Graph(token, cfg.get("graph_version", "v23.0"))
    try:
        use_page_token(g, cfg)
        if mode == "check":
            check(g, cfg)
        else:
            sys.exit(run(g, cfg, "--dry" in sys.argv))
    except GraphError as e:
        sys.exit("Meta API error: " + str(e))


if __name__ == "__main__":
    main()
