# Video 6 narration script

This production script is transcribed from the `\note{...}` blocks in
`video6.tex`, following `SCRIPT_TRANSCRIPTION.md`. Each `Read` direction expands
only the newly revealed slide material; all other spoken words preserve the
authored note in source order. The rendered deck has 24 pages. Dormant source
after the first `\end{document}` is not part of this production.

## Page 001: Title

Narration:
Welcome to the sixth video lecture for ECE 586, Vector Space Methods. Today, we'll discuss properties of real numbers and continuity of functions.

## Page 002: 2.1.4: Properties of Real Numbers (overlay 1 of 4)

Narration:
Suppose we include the natural boundary values for the real numbers. This gives the extended real numbers R-bar, defined as the real numbers union the set containing infinity and negative infinity. R-bar forms a metric space with metric d sub R-bar of x comma y, defined as the absolute value of x over one plus the absolute value of x, minus y over one plus the absolute value of y. Using this metric, one can verify that... x sub n tends to infinity is equivalent to: for every M greater than zero, there exists N in the natural numbers such that, for all n greater than N, x sub n is greater than M. This implies that all elements in the tail of the sequence are larger than any fixed real number.

## Page 003: 2.1.4: Properties of Real Numbers (overlay 2 of 4)

Narration:
The supremum, or least upper bound, of X contained in the real numbers is denoted sup X and equals the smallest extended real number M in R-bar such that x is less than or equal to M for all x in X.

## Page 004: 2.1.4: Properties of Real Numbers (overlay 3 of 4)

Narration:
Supremum sequence lemma. Let X be a metric space and f from X to the real numbers be a function mapping X to the real numbers. Let M equal the supremum of f of-A for some non-empty A contained in X. Then, there exists a sequence x-one, x-two, and so on, in-A such that the limit, as n tends to infinity, of f of x sub n equals M. This is an important concept in analysis that will later allow us to exploit compactness.

## Page 005: 2.1.4: Properties of Real Numbers (overlay 4 of 4)

Narration:
In the live session, we will sketch a proof of this.

## Page 006: 2.1.4: More Properties of Real Numbers (overlay 1 of 4)

Narration:
The maximum of X contained in the real numbers, denoted max X, is the largest value contained in the set. It equals the supremum if sup X is in X, and it is undefined otherwise.

## Page 007: 2.1.4: More Properties of Real Numbers (overlay 2 of 4)

Narration:
X equal to the interval from one, inclusive, to two, exclusive, contained in the real numbers, has sup X equal to two and max X undefined. For f of x equal to one over two minus x, f of X equals the interval from one to infinity, and the supremum of f of X equals infinity.

## Page 008: 2.1.4: More Properties of Real Numbers (overlay 3 of 4)

Narration:
The infimum and minimum are the natural minimal quantities associated with the supremum and maximum. Infimum: inf X equals negative the supremum of negative-X, where negative-X is the set of x in the real numbers such that negative x is in X. Minimum: min X equals negative the maximum of negative-X, if it exists. Supremum and infimum are always well-defined but may equal plus or minus infinity.

## Page 009: 2.1.4: More Properties of Real Numbers (overlay 4 of 4)

Narration:
A bounded non-decreasing sequence in the real numbers converges to its supremum. Sketch proof and application to sums on the board. This result says that a non-decreasing sequence must converge if it is bounded.

## Page 010: 2.1.2: Continuity (overlay 1 of 3)

Narration:
For real functions, I'm guessing that most of you have already seen the definition of continuity in a calculus class. Now, we consider functions between metric spaces and discuss the natural extension of that concept. Let f from X to Y be a function between metric spaces X comma d sub X, and Y comma d sub Y. The function f is continuous at x-naught in X if, for any epsilon greater than zero, there exists a delta greater than zero such that, for all x in X satisfying d sub X of x-naught comma x less than delta, we find d sub Y of f of x-naught comma f of x less than epsilon.

## Page 011: 2.1.2: Continuity (overlay 2 of 3)

Narration:
A very nice result in topology is that continuity has an equivalent definition based on convergence. In practice, this viewpoint is often more useful. If f is continuous at x-naught, then f of x sub n tends to f of x-naught for all sequences x-one, x-two, and so on, in X such that x sub n tends to x-naught. Conversely, if f of x sub n tends to f of x-naught for all sequences x-one, x-two, and so on, in X such that x sub n tends to x-naught, then f is continuous at x-naught.

## Page 012: 2.1.2: Continuity (overlay 3 of 3)

Narration:
f is called continuous if it is continuous at all x-naught in X. f is uniformly continuous if delta can be chosen independently of x-naught. In particular, the definition of continuous chooses x-naught before delta. Thus, the value of delta is allowed to depend on x-naught. If that dependence can be removed, then the function is uniformly continuous.

## Page 013: Continuous vs. Uniformly Continuous (overlay 1 of 4)

Narration:
Let X equal the interval from zero, exclusive, to one, inclusive, and Y equal the interval from one to infinity, be subsets of the standard metric space of real numbers. Let f from X to Y be defined by f of x equal to one over x. Is this function continuous? What could go wrong? It's pretty clear that this function is problematic for small values of x because it becomes unbounded as x tends to zero.

## Page 014: Continuous vs. Uniformly Continuous (overlay 2 of 4)

Narration:
For all x-naught in X and epsilon greater than zero, we can choose delta equal to epsilon x-naught squared over one plus epsilon x-naught, and observe that: the absolute value of one over x minus one over x-naught equals the absolute value of x-naught minus x over x times x-naught, which is less than the quantity epsilon x-naught squared over one plus epsilon x-naught, divided by x-naught times the quantity x-naught minus epsilon x-naught squared over one plus epsilon x-naught. This equals epsilon over the product of one plus epsilon x-naught and the quantity one minus epsilon x-naught over one plus epsilon x-naught, which equals epsilon. But, you can check the math and see that f is continuous all the same.

## Page 015: Continuous vs. Uniformly Continuous (overlay 3 of 4)

Narration:
It is uniformly continuous? Where could something go wrong? Small values of x are again problematic and f becomes less and less continuous as x tends to zero. This will imply that f is not uniformly continuous.

## Page 016: Continuous vs. Uniformly Continuous (overlay 4 of 4)

Narration:
Negating the definition of uniformly continuous gives: there exists epsilon greater than zero such that, for every delta greater than zero, there exist x-naught in X and x in X such that the absolute value of x minus x-naught is less than delta, and the absolute value of f of x minus f of x-naught is at least epsilon. If epsilon equals one, x-naught equals the minimum of one half and delta over two, and x equals two x-naught, then the absolute value of x minus x-naught equals x-naught, which is less than or equal to delta over two, and: the absolute value of one over x minus one over x-naught equals the absolute value of x-naught minus x over x times x-naught, which equals x-naught over x times x-naught, which equals one over x, which equals the maximum of one and one over delta, and is at least one. Now, you can check the math to see that f is not uniformly continuous.

## Page 017: Uniformly Continuous vs. Lipschitz Continuous (overlay 1 of 4)

Narration:
In engineering mathematics, most functions satisfy a strong form of continuity known as... A function f from X to Y is called Lipschitz continuous on-A contained in X if there is a constant L in the real numbers such that d sub Y of f of x comma f of y is less than or equal to L times d sub X of x comma y for all x and y in-A. For example, this holds if the function's derivative exists and is bounded on-A.

## Page 018: Uniformly Continuous vs. Lipschitz Continuous (overlay 2 of 4)

Narration:
As an example, ... Let X equal the interval from zero to one, and Y equal the interval from zero to one, be subsets of the standard metric space of real numbers. Let f from X to Y be defined by f of x equal to the square root of x. Is this function Lipschitz continuous? What could go wrong? Again, something is happening at x equals zero.

## Page 019: Uniformly Continuous vs. Lipschitz Continuous (overlay 3 of 4)

Narration:
We can... lower bound the Lipschitz constant via x maps to z squared, and y maps to z squared plus z: L is greater than or equal to the supremum, over distinct x and y in X, of the absolute value of square root y minus square root x over the absolute value of y minus x. This is greater than or equal to the supremum, over z in the interval from zero, exclusive, to one half, inclusive, of the square root of z squared plus z minus the square root of z squared, divided by z squared plus z minus z squared. This is greater than or equal to the supremum, over the same z, of one over square root z minus one. Since the last expression equals infinity, this function is not Lipschitz continuous. Actually, this conclusion follows immediately from the fact that its first derivative is infinite at x equals zero.

## Page 020: Uniformly Continuous vs. Lipschitz Continuous (overlay 4 of 4)

Narration:
As an exercise, take a moment now to decide if you think this function is uniformly continuous.

## Page 021: 2.1.5: Sequences of Functions (overlay 1 of 3)

Narration:
Let X comma d sub X, and Y comma d sub Y, be metric spaces, and let f sub n from X to Y, for n in the natural numbers, be a sequence of functions mapping X to Y. The sequence f sub n converges pointwise to f from X to Y if, for all x in X, the limit as n tends to infinity of f sub n of x equals f of x. This is the standard notion of convergence for sequences of functions.

## Page 022: 2.1.5: Sequences of Functions (overlay 2 of 3)

Narration:
The sequence f sub n converges uniformly to f from X to Y if: for every epsilon greater than zero, there exists N in the natural numbers such that, for all n greater than N and all x in X, d sub Y of f sub n of x comma f of x is less than epsilon. This is a stronger notion of convergence that can be quite useful.

## Page 023: 2.1.5: Sequences of Functions (overlay 3 of 3)

Narration:
In particular, we have the following theorem... If each f sub n is continuous and the sequence f sub n converges uniformly to f from X to Y, then the limit function f is continuous. This is the standard mechanism by which a sequence of continuous functions converges to a continuous function.

## Page 024: Next Steps

Narration:
Here are some options to continue learning this material. To continue studying after this video: try the suggested reading, Course Notes E F 2.1.3 through 2.1.5. Or the optional reading, M M A 2.1. Also, look at the problems in Assignment 3. That's it for today. So, I'll see you next time.
