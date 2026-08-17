# Video 4 narration script

This production script is transcribed from the `\note{...}` blocks in
`video4.tex`, following `SCRIPT_TRANSCRIPTION.md` and the house style set by
`scripts/video0.md` through `scripts/video2.md`. Each `Read.` expands to the
newly revealed slide material, rendered as natural spoken mathematics; every
other spoken word comes from the embedded note, in source order.

Two frames — "1.5: Functions" and "1.5: Properties of Functions" — have no
authored note items, so each beat reads only its own newly revealed text. The
relation symbol is spoken as "tilde"; see the `\claude` comment in the source
if you prefer a different spoken form. Pages 20 and 23 carry the incomplete
authored cue "Here ..."; it is preserved rather than completed, and both are
flagged in the source.

## Page 001: Title

Narration:
Welcome to the fourth video lecture for ECE 586, Vector-Space Methods. Today, we’ll discuss equivalence relations and functions.

## Page 002: 1.4: Cartesian Products and Abstract Relations (overlay 1 of 2)

Pause-after: 1

Narration:
Now let's consider sets of tuples and vectors.; For sets A-and-B, the Cartesian product A-cross B is the set of ordered pairs. Thus, A-cross-B is defined as the set of pairs a-comma-b such that a-in-A and b-in-B.; For n-tuples from the same set, we write A-to-the power n to denote the n-fold product of A with itself. [[pause 0.5]] For example, if A-is the set containing a-and-b, and B is the set containing c-and-d, then-A cross-B is the set containing a-c; a-d; b-c; and b-d. [[pause 0.5]] A, squared, which is A, cross-A, is the set containing a, a; a, b; b-a; and b-b. [[pause 0.5]] And-A cubed equals the set shown on the last line.

## Page 003: 1.4: Cartesian Products and Abstract Relations (overlay 2 of 2)

Narration:
A relation; tilde; between elements of A is defined by a subset R of A cross A. Specifically, we say the relation x tilde y holds if and only if the pair x comma y is in R. Relations are abstractions of binary comparisons like equals, less than, greater than, less than or equal to, and greater than or equal to.

## Page 004: 1.4: Properties of Relations (overlay 1 of 5)

Narration:
The relation tilde on-A is said to be reflexive if; x tilde x holds for all x in-A. That is, for all x in-A, the pair x comma x is in R. [[pause 0.5]] It is symmetric if; whenever x tilde y, then y tilde x, for all x and y in-A. [[pause 0.5]] It is transitive if; whenever x tilde y; and y tilde z; then x tilde z.

## Page 005: 1.4: Properties of Relations (overlay 2 of 5)

Pause-after: 2.5

Narration:
It is an equivalence relation if it is reflexive, symmetric, and transitive. For example, let A be a set of people; and; let P of x y be the statement “x has the same birthday, month and day, as y.” Define the relation tilde such that x tilde y holds if and only if P of x y is true. Then, R equals the set of pairs x comma y in-A cross-A such that P of x y is true.

## Page 006: 1.4: Properties of Relations (overlay 3 of 5)

Narration:
This partitions-A into disjoint equivalence classes: the equivalence class containing-a is defined as the set of x in-A such that x tilde a. Thus, the-a inside square brackets denotes the set of all elements that are equivalent to a. These definitions imply that each element is in exactly one equivalence class.

## Page 007: 1.4: Properties of Relations (overlay 4 of 5)

Narration:
For example, tilde has an equivalence class for each day of the year for which someone in A has a birthday.

## Page 008: 1.4: Properties of Relations (overlay 5 of 5)

Narration:
The set of equivalence classes for tilde is called its quotient set and denoted by A-slash tilde. This is the collection of subsets that partition A.

## Page 009: 1.5: Functions (overlay 1 of 7)

Narration:
A function f from X to Y is defined by a subset F of X cross Y such that the set of y-values achieved by each x (denoted by A-sub x) has exactly one element. The value of f at x in X, denoted f of x, is the unique element in A sub x.

## Page 010: 1.5: Functions (overlay 2 of 7)

Narration:
Now, we can unpack this definition. A function f mapping X to Y assigns one value, f of x; which lives in Y, to each x in X.

## Page 011: 1.5: Functions (overlay 3 of 7)

Narration:
The notation f from X to Y identifies the domain X and the codomain Y.

## Page 012: 1.5: Functions (overlay 4 of 7)

Narration:
The range of f is the subset of Y achieved by f;  In math, it is the set of y in Y; such that there exists x in X; with y equal to f of x.

## Page 013: 1.5: Functions (overlay 5 of 7)

Narration:
Since the term codomain is uncommon, people sometimes use the term range instead of codomain, either intentionally or unintentionally.

## Page 014: 1.5: Functions (overlay 6 of 7)

Narration:
In basic math, functions are often described by graphs and formulas. This leads students to picture only “nice” functions.

## Page 015: 1.5: Functions (overlay 7 of 7)

Narration:
For example, Cauchy published an incorrect proof of the false assertion that; “a sequence of continuous functions converging everywhere has a continuous limit.”

## Page 016: 1.5: Properties of Functions (overlay 1 of 3)

Narration:
Two functions are equal if they have the same domain, codomain, and value for all elements of the domain.

## Page 017: 1.5: Properties of Functions (overlay 2 of 3)

Narration:
A function f from X to Y is called one-to-one, or injective, if, for all x and x prime in X; if f of x equals f of x prime, then x equals x prime; [[pause 0.4]] It is called onto, or surjective, if its range equals Y; [[pause 0.4]] It is called a one-to-one correspondence, or bijective, if it is both one-to-one, and onto.

## Page 018: 1.5: Properties of Functions (overlay 3 of 3)

Narration:
A bijective function has a unique inverse function, f inverse mapping Y to X, satisfying: for all x in X, f inverse of f of x equals x; and, for all y in Y, f of f inverse of y equals y; [[pause 0.4]] Any one-to-one function f from X to Y automatically defines a bijective function g from X to R; where R is the range of f, and g of x equals, f of x, for all x in X; [[pause 0.4]] This allows one to define an inverse function closely related to a one-to-one function.

## Page 019: 1.5: Applying Functions to Sets (1) (overlay 1 of 3)

Narration:
For f mapping X to Y and a subset-A of X, the image of A under f is the set of y in Y such that there exists x in-A with f of x equal to y.; In shorthand, we can write this as the set of f of x values achieved by all x in A.

## Page 020: 1.5: Applying Functions to Sets (1) (overlay 2 of 3)

Pause-after: 1

Narration:
This figure illustrates an f that maps the point x to the point y and maps the set A to the set f of-A.

## Page 021: 1.5: Applying Functions to Sets (1) (overlay 3 of 3)

Narration:
This implies that the range of f can be written simply as the image of X under f.

## Page 022: 1.5: Applying Functions to Sets (2) (overlay 1 of 4)

Narration:
The preimage, or inverse image; of a subset C of Y is defined by: f inverse of C equals the set of x in X such that f of x is in C.

## Page 023: 1.5: Applying Functions to Sets (2) (overlay 2 of 4)

Narration:
This figure illustrates an f whose preimage of a singleton y equals the singleton x.  Similarly, we show a case where the preimage of f of-A equals not just A but also the set B.

## Page 024: 1.5: Applying Functions to Sets (2) (overlay 3 of 4)

Narration:
Allowing set-valued images means the set-valued inverse always exists.

## Page 025: 1.5: Applying Functions to Sets (2) (overlay 4 of 4)

Pause-after: 0.5

Narration:
For a one-to-one f, the inverse image of a singleton set containing f of x is the singleton set containing x.

## Page 026: 1.5: Applying Functions to Sets (3) (overlay 1 of 3)

Narration:
In general, one can show that the inverse image of f-of-A contains-A, and f of f inverse of B is contained in B. These expressions hold because f can only compress sets; that is, it can map different inputs to the same value, while the inverse image can only expand sets, that is, it can map a singleton to multiple values.

## Page 027: 1.5: Applying Functions to Sets (3) (overlay 2 of 3)

Narration:
The left figure shows a function f from the real numbers to the real numbers defined by f of x equals x squared; let A equal the interval from one to two, and notice that B, which is f of A, equals the interval from one to four. But, f inverse of B equals the union of intervals; from minus two to minus one and from one to two which is a proper superset of A.

## Page 028: 1.5: Applying Functions to Sets (3) (overlay 3 of 3)

Narration:
The right figure shows a function f from the real numbers to the real numbers defined by f of x equals x squared plus one; Let B equal the interval from zero to two, and notice that A, which is f inverse of B, equals the interval from minus one to one. But, f of A, which is f of the interval from minus one to one, equals the interval from one to two, which is a proper subset of B.

## Page 029: Next Steps

Narration:
Here are some options to continue learning this material. To continue studying after this video, try the suggested reading: Course Notes EF 1.5. Or the optional reading: PAF Sections 4.1 through 5.3. Also, look at the problems in Assignment 2. [[pause 0.5]] That’s it for today. So, I’ll see you next time.
