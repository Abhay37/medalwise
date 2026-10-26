# Medalwise autopost (Instagram + Facebook)

A free GitHub Actions job (`.github/workflows/autopost.yml`) runs every 15 minutes. It publishes every post in `schedule.json` whose time has passed, through the official Meta Graph API, and records the result in `state.json`. Nothing is posted twice, and posts more than 6 hours late are skipped rather than flooding the feed.

## एक बार का setup (Rishi के लिए, हिंदी में)

**भाग 1: Meta App बनाना**

1. Laptop पर https://developers.facebook.com खोलें और उसी Facebook account से login करें जो Medalwise Page का admin है।
2. ऊपर **My Apps** → **Create App** दबाएँ।
3. App का नाम `Medalwise Poster` रखें और email `medalwise@gmail.com` डालें।
4. Use case पूछे तो ये दोनों चुनें: **"Manage everything on your Page"** और **"Manage messaging & content on Instagram"**। Business portfolio पूछे तो Medalwise वाला चुनें, या "I don't want to connect" चुनें।
5. **Create App** दबाएँ और password डालें। App "Development" mode में ही रहने दें, क्योंकि अपने खुद के Page पर post करने के लिए यही काफ़ी है।

**भाग 2: चाबी (token) निकालना**

6. ऊपर **Tools** → **Graph API Explorer** खोलें।
7. दाईं ओर **Meta App** में `Medalwise Poster` चुनें।
8. **Permissions** में ये सब जोड़ें: `pages_show_list`, `pages_read_engagement`, `pages_manage_posts`, `instagram_basic`, `instagram_content_publish`, `business_management`।
9. **Generate Access Token** दबाएँ। जो popup खुले, उसमें Medalwise Page और @medalwise.in दोनों पर tick करें और Continue दबाएँ।
10. Token के बगल में नीला **ⓘ** दबाएँ → **Open in Access Token Tool** → नीचे **Extend Access Token** दबाएँ। जो नया लंबा token दिखे, उसे copy करें।
11. Graph API Explorer पर वापस आएँ। Token वाले box में यह लंबा token paste करें, ऊपर query box में `me/accounts` लिखें और **Submit** दबाएँ।
12. नतीजे में Medalwise वाले हिस्से में `"access_token": "EAA..."` होगा। उसे पूरा copy करें। यही Page की चाबी है, और यह expire नहीं होती।

**भाग 3: चाबी GitHub में रखना (chat में मत भेजिए)**

13. https://github.com/Abhay37/medalwise/settings/secrets/actions खोलें → **New repository secret** दबाएँ।
14. Name में `META_PAGE_TOKEN` लिखें, Secret में step 12 वाली चाबी paste करें और **Add secret** दबाएँ।

**भाग 4: जाँच**

15. https://github.com/Abhay37/medalwise/actions/workflows/autopost.yml खोलें → **Run workflow** → mode में `check` चुनें → फिर से **Run workflow** दबाएँ।
16. एक मिनट में हरा ✓ आए तो सब ठीक है, और log में Page और @medalwise.in का नाम दिखेगा। लाल ✗ आए तो Claude को बताइए।

## schedule.json format

```json
{
  "posts": [
    {
      "id": "2026-10-27-maths-reel",
      "time": "2026-10-27T20:00:00+05:30",
      "type": "reel",
      "media": "autopost/media/2026-10-27-maths.mp4",
      "caption": "Caption with #hashtags",
      "networks": ["instagram", "facebook"]
    }
  ]
}
```

- `id`: unique; the log in `state.json` is keyed by it.
- `time`: ISO time with offset (IST is `+05:30`).
- `type`: `reel` (mp4), `image` (jpg or png; Instagram does not accept other formats), or `story`.
- `media`: a path in this repo (served from GitHub Pages) or any public https URL.
- `networks`: defaults to both.
- Optional `cover`: public image URL for a Reel cover.

Instagram's API allows 100 published posts per 24 hours. Reels need 9:16 mp4 (H.264, AAC), 3 to 90 seconds. Music must already be in the video, because library songs cannot be attached through the API.

## Manual runs

Actions → Social autopost → Run workflow, with mode `check` (test the token), `dry` (list what would post) or `run` (post now).
