Subject: Maths
Exam style: IOQM / RMO (algebra, greatest integer function)
Concept tested: Equations with the floor function ⌊x⌋: fix n = ⌊x⌋, solve, then check n ≤ x < n + 1
Hook line (top of slide, <=8 words): Not a quadratic. Don't trust x = 1, 4!
Question: Find the sum of the squares of ALL real numbers x satisfying
x² − 5⌊x⌋ + 4 = 0
(⌊x⌋ = greatest integer ≤ x.)
Options (A-D, or "integer answer"): integer answer
Answer: 34
Solution (3-6 short lines, for next day's post/caption):
Let n = ⌊x⌋. Then x² = 5n − 4, so n ≥ 1 and x > 0, which means x = √(5n − 4).
Need n ≤ x < n + 1, i.e. n² ≤ 5n − 4 < (n + 1)².
Left part: n² − 5n + 4 ≤ 0 ⇒ 1 ≤ n ≤ 4. Right part always holds.
n = 1, 2, 3, 4 give x = 1, √6, √11, 4 (each has ⌊x⌋ = n ✅).
Sum of squares = 1 + 6 + 11 + 16 = 34.
Why it's tricky (common trap): Treating ⌊x⌋ as x turns it into x² − 5x + 4 = 0, giving only x = 1 and 4 and the answer 17. The two irrational roots √6 and √11 are missed. Some also wrongly keep negative roots −√(5n−4), but those have ⌊x⌋ < 0.
Caption (2-3 lines + "Comment your answer 👇"):
Looks like a simple quadratic. It isn't. 😏
How many solutions did you find? Answer tomorrow!
Comment your answer 👇
Diagram needed? (describe, or "no"): no
