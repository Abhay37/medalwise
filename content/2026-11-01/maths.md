Subject: Maths
Exam style: IOQM / RMO (algebra, polynomials)
Concept tested: Polynomial remainder using complex cube roots of unity (ω² + ω + 1 = 0, ω³ = 1)
Hook line (top of slide, <=8 words): Power 2026, but the answer is tiny!
Question: What is the remainder when (x + 1)^2026 is divided by x² + x + 1?
Options (A-D, or "integer answer"):
A) x + 1
B) −x − 1
C) 1
D) x
Answer: B) −x − 1
Solution (3-6 short lines, for next day's post/caption):
Remainder has degree < 2, so write it as ax + b. Plug in ω, a root of x² + x + 1 (ω³ = 1).
ω + 1 = −ω², so (ω + 1)^2026 = (−ω²)^2026 = ω^4052 (2026 is even, so the minus sign goes).
4052 = 3·1350 + 2, so ω^4052 = ω² = −1 − ω.
So aω + b = −ω − 1, which gives a = −1, b = −1 (ω is not real). Remainder = −x − 1.
Why it's tricky (common trap): Students see 2026 ≡ 1 (mod 3) and jump to x + 1 (option A), forgetting that ω + 1 = −ω², which doubles the power to 4052. Others write ω² as the "answer" but forget to turn it back into −x − 1.
Caption (2-3 lines + "Comment your answer 👇"):
A degree-2026 polynomial shrinks to just two terms. 🤯
Roots of unity do the magic. A, B, C or D? Answer tomorrow!
Comment your answer 👇
Diagram needed? (describe, or "no"): no
