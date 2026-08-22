# Video 7 narration script

This production script is transcribed from the `\note{...}` blocks in
`video7.tex`, following `SCRIPT_TRANSCRIPTION.md`. Each `Read` direction expands
only the newly revealed slide material; all other spoken words preserve the
authored note in source order. Page 20 preserves an incomplete authored cue,
which is flagged with a `\gpt` comment in the source.

## Page 001: Title

Narration:
Welcome to the seventh video lecture for ECE 586, Vector Space Methods. Today, we'll discuss the ideas of completeness and contraction.

## Page 002: 2.1.3: Completeness (overlay 1 of 3)

Narration:
A metric space X comma d is said to be complete if every Cauchy sequence in X comma d converges to a limit x in X. Completeness is very useful property for analysis and, thus, researchers prefer to setup problems in complete spaces if possible.

## Page 003: 2.1.3: Completeness (overlay 2 of 3)

Narration:
Consider the sequence x sub n in the rational numbers defined by x-one equal to two and x sub n plus one equal to one half x sub n plus one over x sub n. For this sequence, one can show that the absolute value of x sub n minus the square root of two tends to zero. Since the square root of two is not rational, however, this shows the standard metric space of rationals is not complete.

## Page 004: 2.1.3: Completeness (overlay 3 of 3)

Narration:
I should note that the standard metric space of real numbers is a complete metric space. This can be proven by starting with Zermelo-Fraenkel, Z F, set theory and associating the real numbers with Cauchy sequences of rational numbers. The proof of this is not covered in this class but is available on the website.

## Page 005: 2.1.3: Dense Subsets (overlay 1 of 4)

Narration:
A subset-A of a metric space X comma d is dense in X if every x in X is a limit point of the set A. This is equivalent to the closure of-A being equal to X.

## Page 006: 2.1.3: Dense Subsets (overlay 2 of 4)

Narration:
The rational numbers are a dense subset of the real numbers because every real number is the limit of a sequence of rational numbers. Later, we will see that having a countable dense subset can be useful when proving things.

## Page 007: 2.1.3: Dense Subsets (overlay 3 of 4)

Narration:
The completion of a metric space X comma d sub X consists of a complete metric space Y comma d sub Y, and an isometry phi from X to Y, such that phi of X is a dense subset of Y. Moreover, the completion is unique up to isometry. For example, think of X as the rational numbers, Y as the real numbers, and phi as the mapping that embeds the rational numbers in the real numbers. I should also note that an isometry is a function between metric spaces that preserves pairwise distances.

## Page 008: 2.1.3: Dense Subsets (overlay 4 of 4)

Narration:
For example, if a metric space is not complete, then some of its natural limit points have been left out. This can be repaired by creating new points associated with Cauchy sequences that don't converge.

## Page 009: 2.1.3: A Space of Continuous Functions (overlay 1 of 3)

Narration:
Let X equal C of the interval from negative one to one be the space of continuous functions that map the interval from negative one to one to the real numbers and satisfy norm f sub two less than infinity, where norm f sub two denotes the L-two norm: norm f sub two is defined as the square root of the integral from negative one to one of the absolute value of f of t squared, d t. This set forms a metric space X comma d when equipped with the distance d of f comma g, defined as norm f minus g sub two, which equals the square root of the integral from negative one to one of the absolute value of f of t minus g of t squared, d t. Now, consider the sequence of functions f sub n of t given by: zero for t in the interval from negative one to negative one over n; n t over two plus one half for t in the interval from negative one over n to one over n, with both endpoints excluded; and one for t in the interval from one over n to one.

## Page 010: 2.1.3: A Space of Continuous Functions (overlay 2 of 3)

Narration:
This figure shows the first few functions in the sequence and we see it's a sequence of continuous functions converging to the step function. The key problem is that the limit function is not continuous and therefore not in the set X.

## Page 011: 2.1.3: A Space of Continuous Functions (overlay 3 of 3)

Narration:
Analytically, this is a Cauchy sequence in X comma d. But, it does not converge to a continuous function in C of the interval from negative one to one.

## Page 012: 2.1.3: Contractions on Metric Spaces (overlay 1 of 2)

Narration:
Let A be a subset of a metric space X comma d, and f from X to X be a function. Then, f is a contraction on-A if f of-A is contained in-A and there exists a constant gamma less than one such that d of f of x comma f of y is less than or equal to gamma d of x comma y for all x and y in-A.

## Page 013: 2.1.3: Contractions on Metric Spaces (overlay 2 of 2)

Narration:
Consider the metric space X equal to the interval from zero to one with absolute distance. Define f from X to X with f of x equal to one minus one half x, and observe that d of f of x comma f of y equals the absolute value of f of x minus f of y, which equals one half times the absolute value of x minus y. Thus, f is a contraction on X with contraction coefficient one half. The figure shows the graph of f.

## Page 014: 2.1.3: Contraction Mapping Theorem

Narration:
First, we look at the figure. It illustrates a function f that is a contraction on the closed subset-A, which is outlined in blue. Because of this, the image of-A under f, which is outlined in purple, lies inside of-A. Likewise, the image of the set f of-A under f, which is outlined in red, lies inside the set f of-A. Now, look at the theorem. Contraction Mapping Theorem. Let X comma d be a complete metric space and f be a contraction on a closed subset-A contained in X. Then, f has a unique fixed point x-star in-A such that f of x-star equals x-star, and the sequence x sub n plus one equals f of x sub n converges to x-star from any initial x-one in-A. Also, x sub n satisfies the error bounds, for contraction coefficient gamma: d of x-star comma x sub n is less than or equal to gamma to the power n minus one times d of x-star comma x-one; and d of x-star comma x sub n plus one is less than or equal to d of x sub n comma x sub n plus one times gamma over one minus gamma. If this process were continued, the image of-A under the n-fold composition of f with itself would shrink to the fixed point x-star.

## Page 015: 2.1.3: Concrete Example of the Contraction Mapping Theorem (overlay 1 of 6)

Narration:
Let X equal the interval from zero to one and define f from X to X via f of x equal to cosine of x. Cosine of x is plotted in red and, for the definition to make sense, one first needs to check that cosine of x is in the interval from zero to one whenever x is in the interval from zero to one.

## Page 016: 2.1.3: Concrete Example of the Contraction Mapping Theorem (overlay 2 of 6)

Narration:
The red curve above proves this numerically. Analytically, we see that cosine of the interval from zero to one equals the interval from cosine of one to one, because cosine of x is decreasing on the interval from zero to pi.

## Page 017: 2.1.3: Concrete Example of the Contraction Mapping Theorem (overlay 3 of 6)

Narration:
To show that cosine of x is a contraction, we use the mean value theorem: f of y minus f of x equals y minus x times f prime of t for some t in the interval from x to y.

## Page 018: 2.1.3: Concrete Example of the Contraction Mapping Theorem (overlay 4 of 6)

Narration:
Next, we consider the derivative and note that f prime of t equals negative sine of t, and sine of the interval from zero to one equals the interval from zero to sine of one, with sine of one approximately zero point eight four.

## Page 019: 2.1.3: Concrete Example of the Contraction Mapping Theorem (overlay 5 of 6)

Narration:
This implies that the absolute value of cosine of y minus cosine of x is less than or equal to zero point eight five times the absolute value of y minus x. This implies f of x is a contraction on the interval from zero to one.

## Page 020: 2.1.3: Concrete Example of the Contraction Mapping Theorem (overlay 6 of 6)

Narration:
Thus, the contraction mapping theorem implies that the sequence

## Page 021: 2.1.3: Applications of the Contraction Mapping Theorem (overlay 1 of 3)

Narration:
Picard's uniqueness theorem for differential equations. Differential equation y prime of t equals f of t comma y of t, for t in the interval from a to b, with y of a equal to y-naught. Assume f of t comma y is Lipschitz continuous in y for t in the interval from a to b. Then, the solution y of t exists and is unique for t in the interval from a to b. There is an optional homework problem that outlines this proof for a special case of this theorem.

## Page 022: 2.1.3: Applications of the Contraction Mapping Theorem (overlay 2 of 3)

Narration:
Implicit function theorem. Let f from R to the n cross R to the m into R to the m be continuously differentiable on an open set A. Let g from R to the n into R to the m be defined implicitly by f of x comma g of x equal to zero. For x-naught in-A, assume f of x-naught comma y-naught equals zero and the y-Jacobian is invertible at x-naught comma y-naught. Then, g of x exists and is unique in some neighborhood of x-naught. which provides a method prove the local uniqueness of a function that is defined implicitly.

## Page 023: 2.1.3: Applications of the Contraction Mapping Theorem (overlay 3 of 3)

Narration:
Dynamic Programming for a Markov Decision Process, M D P. State-action s comma a defines probability p of s-prime given s comma a, and reward R of s comma a. Finite state plus discounted reward implies a unique stationary optimal policy. This is related to reinforcement learning and other methods by which computers can learn to play video games.

## Page 024: Next Steps

Narration:
Here are some options to continue learning this material. To continue studying after this video: try the suggested reading, Course Notes E F 2.1.6. Or the optional reading, M M A 2.1. Also, look at the problems in Assignment 3. That's it for today. So, I'll see you next time.
