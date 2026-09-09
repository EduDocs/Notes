# Video 5 narration script

This production script is transcribed from the `\note{...}` blocks in
`video5.tex`, following `SCRIPT_TRANSCRIPTION.md` and the house style set by
`scripts/video0.md` through `scripts/video2.md`. Each `Read.` expands to the
newly revealed slide material, rendered as natural spoken mathematics; every
other spoken word comes from the embedded note, in source order. Authored
paragraph breaks (`\\ [2mm]`) and lettered sub-arguments become `[[pause 0.5]]`.

The 30-page map below is derived from the frame overlay specifications in
`video5.tex`, not from a rendered PDF. Confirm it with `make beats VIDEO=5`
against the audience PDF before synthesis. `MMA` needs an entry in
`pronunciations.json`; one has been added.

## Page 001: Title

Narration:
Welcome to the fifth video lecture for ECE 586, Vector Space Methods. Today, we’ll discuss metric spaces and topology.

## Page 002: 2.1: Introduction (overlay 1 of 6)

Narration:
What is topology and why do we study it? It is the study of geometric properties preserved by continuous deformations. It allows one to define abstract notions of proximity and distance.

## Page 003: 2.1: Introduction (overlay 2 of 6)

Narration:
Engineers approximate real things by mathematical objects. Here are two questions that topology can help answer. [[pause 0.2]] First, can a matrix A be approximated closely by a lower-rank matrix? [[pause 0.2]] Second, can a function f of x be approximated well by a degree-two polynomial?

## Page 004: 2.1: Introduction (overlay 3 of 6)

Narration:
In engineering, a topology is typically defined using a metric. Thus, this course will focus on metric spaces.

## Page 005: 2.1: Introduction (overlay 4 of 6)

Narration:
A metric space, X comma d, is a set X along with a metric d of x-y. The quantity d of x-y is called the distance between the points x and y. This definition is a useful abstraction of spaces with some notion of distance between any two points.

## Page 006: 2.1: Introduction (overlay 5 of 6)

Narration:
A metric on a set X is a function d from X-cross-X to the real numbers with the following properties. [[pause 0.2]] First, “d of x-y is greater than or equal to zero” for all x and y in X, with equality if and only if x equals y. This is called non-negativity. [[pause 0.2]] Second, “d of x-y equals d of y-x” for all x and y in X. This is called symmetry. These rules can be seen as an abstraction of Euclidean space, whose notion of distance retains some key properties of Euclidean distance.

## Page 007: 2.1: Introduction (overlay 6 of 6)

Narration:
Third, “d of x-y plus d of y-z is greater than or equal to d of x-z” for all x, y, and z in X. This is called the triangle inequality. For example, suppose x is where you work, z is where you live, and y is where you buy groceries. Then the triangle inequality abstracts the idea that stopping by the store on your way home cannot make your trip home shorter.

## Page 008: 2.1: Standard Examples of Metric Spaces (overlay 1 of 3)

Narration:
First, consider the real numbers, X equals R, with the absolute distance d of x-y equal to the absolute value of x minus y. This example is the standard foundation for real analysis. Non-negativity holds because the absolute value of a number is non-negative and equals zero if and only if that number is zero. Symmetry holds because swapping x and y doesn’t change the absolute value. The triangle inequality follows because “the absolute value of x minus z” equals “the absolute value of the quantity x minus y, plus the quantity y minus z,” which is less than or equal to “the absolute value of x minus y, plus the absolute value of y minus z.”

## Page 009: 2.1: Standard Examples of Metric Spaces (overlay 2 of 3)

Narration:
Next, consider real n-dimensional vectors, X equals R to the n, with the Euclidean distance as our metric. Non-negativity and symmetry are immediate; the triangle inequality is a bit harder and will be shown later.

## Page 010: 2.1: Standard Examples of Metric Spaces (overlay 3 of 3)

Narration:
Finally, consider the set of continuous functions f from the interval a to b into the real numbers, with the metric d of f g equal to the maximum, over x in the interval a to b, of the absolute value of f of x minus g of x. For this metric, many of the properties are inherited from the absolute distance inside the maximum. In particular, properties one and two follow naturally. For the triangle inequality, we observe that: [[pause 0.5]] the absolute difference between f of x and h of x is unchanged by adding and subtracting g of x inside the absolute value, [[pause 0.5]] the absolute value of the sum of two numbers is upper bounded by the sum of their absolute values, [[pause 0.5]] the maximum of the sum of two functions is only increased by maximizing them separately.

## Page 011: 2.1: Important Concepts in Metric Spaces (overlay 1 of 3)

Narration:
First, consider the set of points with distance less than epsilon from a point x. This is called the open ball of radius epsilon centered at x, and it is given by B sub d of x-comma-epsilon: the set of y in X such that d of x-y is less than epsilon. This is illustrated in the figure. [[pause 0.2]] The statement denoted P says that every point in this open ball has a smaller open ball around it that lies entirely inside the original ball. You will be asked to prove this in the homework.

## Page 012: 2.1: Important Concepts in Metric Spaces (overlay 2 of 3)

Narration:
Next, consider an infinite list x-one, x-two, x-three, and so on, of points in X. [[pause 0.3]] Formally, this is a sequence x sub i in X for i in the natural numbers. This is equivalent to x sub i equal to f of i where f is a function from the natural numbers to X. [[pause 0.2]] For example, for X equal to the real numbers and d of x-y equal to the absolute value of x minus y, let x sub n equal one plus one over n, all raised to the power n. It is well-known that this sequence converges to the constant e. A sequence is also illustrated in the figure.

## Page 013: 2.1: Important Concepts in Metric Spaces (overlay 3 of 3)

Pause-after: 0.5

Narration:
Finally, consider a sequence of points that approaches another point. Formally, a sequence x sub n converges to x in X, denoted x sub n arrow x, if, for any epsilon greater than zero, there is a natural number M such that d of x-comma-x sub n is less than epsilon for all n greater than M. In the figure, one can imagine the example sequence converging to the point x.

## Page 014: 2.1: Convergence: Examples and Counterexamples (overlay 1 of 5)

Narration:
A sequence x-one, x-two, and so on, in X comma d is a Cauchy sequence if, for any epsilon greater than zero, there is a natural number N, which may depend on epsilon, such that, for all m and n greater than N, d of x sub m comma x sub n is less than epsilon. For the real numbers, you’ve probably seen this definition before in a calculus class.

## Page 015: 2.1: Convergence: Examples and Counterexamples (overlay 2 of 5)

Narration:
The following theorem states that every convergent sequence is a Cauchy sequence. The proof will be given in the lecture. This means that the tail of a convergent sequence contains only points that are close to each other.

## Page 016: 2.1: Convergence: Examples and Counterexamples (overlay 3 of 5)

Narration:
What about the converse? In calculus and real analysis, it is also common to prove convergence by showing a sequence is Cauchy.

## Page 017: 2.1: Convergence: Examples and Counterexamples (overlay 4 of 5)

Narration:
But this does not work in all metric spaces. Here is a counterexample. Take the metric space X-comma-d with the rationals, X equals Q, and d of x-y equal to the absolute value of x minus y. Take the sequence with x-one equal to two and x sub n plus one equal to f of x sub n, defined as one half x sub n plus one over x sub n, which is rational. One can show that x sub n is a Cauchy sequence and that the absolute value of x sub n minus the square root of two converges to zero.

## Page 018: 2.1: Convergence: Examples and Counterexamples (overlay 5 of 5)

Narration:
But, according to the definitions, x sub n does not converge! This is because convergence requires that the limit is in X, but we know the the square root of two is not rational. Later, we will see that the converse is true for complete metric spaces.

## Page 019: 2.1.1: Metric Topology (overlay 1 of 3)

Narration:
In mathematics, a topology is a collection of “open” sets satisfying certain properties. It’s likely that many of you have been exposed informally to the idea of open and closed sets, such as intervals of real numbers. In this class, we will make these notions precise for metric spaces. Let W be a subset of a metric space X comma d. The set W is called open if, for every w-naught in W, there is an epsilon greater than zero such that the open ball of radius epsilon around w-naught is a subset of W.

## Page 020: 2.1.1: Metric Topology (overlay 2 of 3)

Narration:
A subset W of X comma d is closed if its complement, W complement equals X minus W, is open.

## Page 021: 2.1.1: Metric Topology (overlay 3 of 3)

Narration:
Based on these definitions, one can prove the following theorem. [[pause 0.2]] First, the empty set and X are open sets. [[pause 0.2]] Second, any union of open sets is open. [[pause 0.2]] Third, any finite intersection of open sets is open. These results will be proven in class or in homework problems.

## Page 022: 2.1.1: Interior, Limit points, and Closure (overlay 1 of 6)

Narration:
[[seed 43]]
Sometimes it is useful to consider only the points in a set that are not part of a boundary. This is called the interior of the set and, formally, for a metric space X comma d and a subset W of X: a point w-naught in W is in the interior of W, denoted W with a superscript circle, if there is a delta greater than zero such that the open ball of radius delta around w-naught is a subset of W. Thus, w-naught is surrounded by an open ball in W.

## Page 023: 2.1.1: Interior, Limit points, and Closure (overlay 2 of 6)

Narration:
It is also useful to consider points that can be approached by non-trivial sequences from a set. These points are called limit points. Formally, a point x-naught in X is a limit point of W if there is a sequence of distinct elements, w-one, w-two, and so on, in W, that converges to x-naught.

## Page 024: 2.1.1: Interior, Limit points, and Closure (overlay 3 of 6)

Narration:
It can also be useful to consider a set along with all additional points lying on its boundary. The resulting set is called the closure and, formally, a point x-naught in X is in the closure of W, denoted W with an overbar, if, for all delta greater than zero, there is a w-naught in W such that d of x-naught comma w-naught is less than delta. This implies that x-naught is arbitrarily close to points in W.

## Page 025: 2.1.1: Interior, Limit points, and Closure (overlay 4 of 6)

Narration:
These sets have a few nice properties. For example, one can show that the interior is open.

## Page 026: 2.1.1: Interior, Limit points, and Closure (overlay 5 of 6)

Narration:
One can also show that W is closed if and only if it contains all of its limit points.

## Page 027: 2.1.1: Interior, Limit points, and Closure (overlay 6 of 6)

Narration:
Lastly, one can show that the closure of W equals the union of W and all its limit points, and is thus closed.

## Page 028: A Few More Things (overlay 1 of 2)

Narration:
Consider the standard metric space of real numbers R. Any open set can be written as a countable disjoint union of open intervals. But, what about closed sets? For closed sets, De Morgan’s law implies that any closed set can be written as the countable disjoint intersection of closed intervals. But, exotic sets like the Cantor set show that they cannot be written as the countable union of closed sets. In higher dimensions, a connected set that is not a ball cannot be written as the countable union of disjoint closed balls.

## Page 029: A Few More Things (overlay 2 of 2)

Narration:
For a subset W of X, the boundary of W is the closure minus the interior. Thus, the closure is the union of the set and its boundary. In the figure, the boundary is the union of the dashed and solid lines. Alternatively, a point x in X is on the boundary of W if, for all delta greater than zero, an open ball of radius delta around x contains a point in W and a point not in W. Thus, boundary points are either in the set and arbitrarily close to points outside the set, or outside the set and arbitrarily close to points inside the set.

## Page 030: Next Steps

Narration:
Here are some options to continue learning this material. To continue studying after this video, try the suggested reading: Course Notes E F two point one through two point one point two. Or the optional reading: M M A two point one. Also, look at the problems in Assignment three. [[pause 0.5]] That’s it for today. So, I’ll see you next time.
