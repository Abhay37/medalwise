Subject: Maths
Exam style: AMC 12 / IOQM (algebra, polynomials)
Concept tested: Newton's sums: power sums of roots via the recurrence from the polynomial itself (no need to find the roots)
Hook line (top of slide, <=8 words): Can't find the roots? You don't need to!
Question: Let a, b, c be the roots of x³ − 3x + 1 = 0. Find a⁵ + b⁵ + c⁵.
Options (A-D, or "integer answer"): integer answer
Answer: −15
Solution (3-6 short lines, for next day's post/caption):
Each root satisfies r³ = 3r − 1, so multiplying by r^(k−3): r^k = 3r^(k−2) − r^(k−3).
Add over a, b, c (with S_k = a^k + b^k + c^k): S_k = 3S_(k−2) − S_(k−3).
Vieta: S_0 = 3, S_1 = 0, S_2 = 0² − 2(−3) = 6.
S_3 = 3·0 − 3 = −3, S_4 = 3·6 − 0 = 18, S_5 = 3·(−3) − 6 = −15.
Answer: −15 (all three roots are real, so this is a plain real-number sum).
Why it's tricky (common trap): The roots are ugly (≈ 1.532, 0.347, −1.879), so students try to estimate them. Others use the shortcut S_5 = S_2 · S_3 = 6 · (−3) = −18, which ignores all the cross terms. Sign errors in Vieta (S_2 = −6) are another common slip.
Caption (2-3 lines + "Comment your answer 👇"):
Three ugly roots, one clean answer. ✨
Find a⁵ + b⁵ + c⁵ without solving the cubic. Answer tomorrow!
Comment your answer 👇
Diagram needed? (describe, or "no"): no
