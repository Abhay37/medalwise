Subject: Maths
Exam style: IOQM / RMO (number theory)
Concept tested: gcd(2^a − 1, 2^b − 1) = 2^gcd(a, b) − 1 (Euclid's algorithm on exponents)
Hook line (top of slide, <=8 words): Two giant numbers. One tiny GCD.
Question: Find gcd(2^2026 − 1, 2^1518 − 1).
(Each number has more than 450 digits. No calculator!)
Options (A-D, or "integer answer"): integer answer
Answer: 3
Solution (3-6 short lines, for next day's post/caption):
Key fact: 2^a − 1 = 2^(a−b)·(2^b − 1) + (2^(a−b) − 1).
So gcd(2^a − 1, 2^b − 1) = gcd(2^(a−b) − 1, 2^b − 1): Euclid's algorithm works on the exponents!
Hence gcd(2^a − 1, 2^b − 1) = 2^gcd(a, b) − 1.
gcd(2026, 1518): 2026 − 1518 = 508, 1518 = 2·508 + 502, 508 − 502 = 6, 502 = 83·6 + 4, gcd(6, 4) = 2.
Answer = 2² − 1 = 3.
Why it's tricky (common trap): Both numbers are odd and "look" unrelated, so many say 1. Others write 2^gcd(a,b) and answer 4, forgetting the −1, or think the gcd must be huge like 2^508 − 1.
Caption (2-3 lines + "Comment your answer 👇"):
450+ digit numbers, and the answer fits on your fingers. ✋
Find the GCD without a calculator. Answer tomorrow!
Comment your answer 👇
Diagram needed? (describe, or "no"): no
