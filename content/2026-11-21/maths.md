Subject: Maths
Exam style: IOQM / RMO (number theory)
Concept tested: Legendre's formula for the power of a prime in n!, applied to a composite base (12 = 2² · 3)
Hook line (top of slide, <=8 words): Trailing zeros, but in base 12!
Question: When 2026! is written in base 12, how many zeros does it end with?
Options (A-D, or "integer answer"): integer answer
Answer: 1009
Solution (3-6 short lines, for next day's post/caption):
Each trailing zero in base 12 needs one factor 12 = 2² · 3.
Power of 3 in 2026! = ⌊2026/3⌋ + ⌊2026/9⌋ + … = 675 + 225 + 75 + 25 + 8 + 2 = 1010.
Power of 2 in 2026! = 1013 + 506 + 253 + 126 + 63 + 31 + 15 + 7 + 3 + 1 = 2018.
Each 12 uses TWO 2s, so 2s allow only ⌊2018/2⌋ = 1009 twelves; 3s allow 1010.
Zeros = min(1009, 1010) = 1009.
Why it's tricky (common trap): In base 10, the bigger prime 5 is always the bottleneck, so students assume 3 limits here and answer 1010. But 12 needs 2², so the 2s run out first. Others answer 505 (the base-10 count) or 2018.
Caption (2-3 lines + "Comment your answer 👇"):
You know trailing zeros in base 10. Base 12 has a twist. 🔄
Which prime runs out first, 2 or 3? Answer tomorrow!
Comment your answer 👇
Diagram needed? (describe, or "no"): no
