# Video 3 narration script

This production script is transcribed from the `\note{...}` blocks in
`video3.tex`, following `SCRIPT_TRANSCRIPTION.md` and the house style set by
`scripts/video0.md` through `scripts/video2.md`. Each `Read.` expands to the
newly revealed slide material, rendered as natural spoken mathematics; every
other spoken word comes from the embedded note, in source order. Authored
paragraph breaks (`\\ [2mm]`) become `[[pause 0.5]]`. Three frames carry a
single blanket `Read.` for many overlays; that direction is applied reveal by
reveal, so each beat reads only its own newly displayed material.

## Page 001: Title

Narration:
Welcome to the third video lecture for ECE 586, Vector-Space Methods. Today, we’ll discuss set theory.

## Page 002: 1.4: Set Theory (overlay 1 of 9)

Narration:
Set theory is the foundation, along with logic, of all modern mathematics.

## Page 003: 1.4: Set Theory (overlay 2 of 9)

Narration:
Numbers, relations, functions, and so on, are all defined using set theory.

## Page 004: 1.4: Set Theory (overlay 3 of 9)

Narration:
But, it’s not as simple as one would hope because naive approaches are inconsistent. That is, for some P, the definitions imply P and not P.

## Page 005: 1.4: Set Theory (overlay 4 of 9)

Narration:
Axiomatic approaches avoid contradictions but are overly complicated.

## Page 006: 1.4: Set Theory (overlay 5 of 9)

Narration:
Thus, we use naive set theory, which defines the operations of set theory without worrying about paradoxes. This is sufficient for this course.

## Page 007: 1.4: Set Theory (overlay 6 of 9)

Narration:
In Naive set theory, a set is defined as “any collection of objects, mathematical or otherwise.” For example, consider “the set of all books published in 2007.”

## Page 008: 1.4: Set Theory (overlay 7 of 9)

Narration:
Objects in a set are called elements, or members, of the set.

## Page 009: 1.4: Set Theory (overlay 8 of 9)

Narration:
The logical statement “a is a member of the set capital A” is denoted “a in A.”

## Page 010: 1.4: Set Theory (overlay 9 of 9)

Narration:
Its negation, “a is not a member of the set capital A,” is denoted “a-not-in A.”

## Page 011: 1.4: Using Set Theory (overlay 1 of 7)

Narration:
Defining sets. One can present a set by listing its elements. For the standard English vowels, A equals the set containing a, e, i, o, and u.

## Page 012: 1.4: Using Set Theory (overlay 2 of 7)

Narration:
Element order is irrelevant: the set containing i, o, u, a, and e is the same as the set A. Repeated elements have no effect: the presentation a, e, i, o, u, e, and o is the same as the set A.

## Page 013: 1.4: Using Set Theory (overlay 3 of 7)

Narration:
A singleton is a set containing exactly one element, such as the set only containing a.

## Page 014: 1.4: Using Set Theory (overlay 4 of 7)

Narration:
Standard sets are written with blackboard bold letters: the integers are denoted by Z, the real numbers by R, and the complex numbers by C.

## Page 015: 1.4: Using Set Theory (overlay 5 of 7)

Narration:
To construct new sets from old sets, one often uses set-builder notation: where; for a logical predicate P of x, defined for x in X, “A is the set of elements in X such that P of x is true” is denoted by A equals the set of x in X such that P of x.

## Page 016: 1.4: Using Set Theory (overlay 6 of 7)

Narration:
If no x in X satisfies P of x, then the result is the empty set.

## Page 017: 1.4: Using Set Theory (overlay 7 of 7)

Narration:
For example, from the integers, one can get the natural numbers and the positive prime numbers. The natural numbers consist of all integers that are at least one. [[pause 0.8]] The positive prime numbers consist of all integers that are at least one and prime.

## Page 018: 1.4: Set Properties (overlay 1 of 5)

Narration:
Cardinality. For a set-A, its cardinality, denoted by absolute-value of-A, is the number of elements in A. The cardinality of the set containing a, e, i, o, and u is five.

## Page 019: 1.4: Set Properties (overlay 2 of 5)

Narration:
If there is a one-to-one correspondence between A and the natural numbers, then A is called countably infinite and the cardinality of A is infinity.

## Page 020: 1.4: Set Properties (overlay 3 of 5)

Narration:
For example, the set of rational numbers, Q, is defined as the set of q in the real numbers such that there exists a natural number n for which n times q is an integer. This set is countably infinite. For example, for all natural numbers n,we can list the rationals m over n with the absolute value of m at most n squared.

## Page 021: 1.4: Set Properties (overlay 4 of 5)

Narration:
If the cardinality of A-is infinity but A is not countably infinite, then A is uncountably-infinite.

## Page 022: 1.4: Set Properties (overlay 5 of 5)

Narration:
For example, the real numbers are uncountably infinite by Cantor’s diagonal argument. This is not covered in this class, but it is worth googling if you haven’t seen it.

## Page 023: 1.4: Venn Diagrams

Narration:
Here, we see Venn diagrams for some standard set operations. The sets A-and-B are represented by overlapping circles. Starting at the top left graphic, we see the union of A-and-B, which contains all elements in either A-or-B. [[pause 0.5]] Looking at the top right graphic, we see the intersection of A-and-B, which contains elements that are in both A-and-B. [[pause 0.5]] Moving to the bottom right graphic, we see the set difference A-minus-B, which contains all elements that are in-A and not-in-B. [[pause 0.5]] Finally, in the bottom left graphic, we see the complement of-A, which contains all elements in the universal set U except those in-A.

## Page 024: 1.4: From Logic to Set Theory (overlay 1 of 4)

Narration:
Now, we discuss operations on sets. The union of A-and-B, denoted A-union-B, is the set of elements in either A-or-B. Logically, that means x in A-union-B; if and only if x-in-A or x-in-B. Here and below, we use the notation for equivalence because this biconditional holds for all x, A, and B.

## Page 025: 1.4: From Logic to Set Theory (overlay 2 of 4)

Narration:
The intersection of A-and-B, denoted A-intersect-B, is the set of elements in both A-and-B.; Logically, that means x-in-A intersect B; if and only if x-in-A and x-in-B.

## Page 026: 1.4: From Logic to Set Theory (overlay 3 of 4)

Narration:
The set difference A-minus-B (also denoted A backslash B), is the set of elements in-A but not-in-B.; Logically, that means x-in A-minus-B if and only if x-in-A and x not-in B.

## Page 027: 1.4: From Logic to Set Theory (overlay 4 of 4)

Narration:
The complement of-A, denoted-A-soup c, for an implied universal set U, equals U-minus-A.; Logically, that means x in A-complement if and only if x is not-in-A.

## Page 028: 1.4: Relationships Between Sets (overlay 1 of 4)

Narration:
Now, we consider relationships between sets A and B. We say A equals B if both sets have the same elements. [[pause 0.5]] Logically, “A equals B” is equivalent to: for all x, x in A if and only if x in B. The “for all x” refers to all x in the implied universal set. However, for this operation, we could also write “for all x in-A union B” without changing the meaning.

## Page 029: 1.4: Relationships Between Sets (overlay 2 of 4)

Narration:
We say A is a subset of B, denoted A subset-equal B, if all elements in A are also in B.; Logically, “A subset B” is equivalent to: for all x, if x in A, then x in B. The quantifier “for all x” refers to all x in the implied universal set. Though, writing “for all x in A” instead wouldn’t change the meaning. 

## Page 030: 1.4: Relationships Between Sets (overlay 3 of 4)

Narration:
We say A is a proper subset of B, denoted-A proper-subset B, if A is a subset of B and A is not equal to B. In this case, there must be some element in B that is not in A.

## Page 031: 1.4: Relationships Between Sets (overlay 4 of 4)

Narration:
Two sets are called disjoint if their intersection equals the empty set.

## Page 032: 1.4: De Morgan, Infinite Operations, and Negation (overlay 1 of 3)

Narration:
De-Morgan’s rule says the negation of “P or Q” equals “not P and not Q” with P and Q denoting the statements “x in A” and “x in B” respectively. [[pause 0.5]] This implies that the complement of-A union-B equals A-complement intersect B-complement. This is because membership in the complement of a set is logically the same as negation of membership in that set.

## Page 033: 1.4: De Morgan, Infinite Operations, and Negation (overlay 2 of 3)

Narration:
Now, we see that infinite unions and intersections have relatively simple definitions. [[pause 0.5]] Let S sub alpha denote a collection of sets indexed by alpha in I.; The first equation says the infinite union of the collection contains x if x in S-alpha for some alpha in I. This matches our intuition that the union contains all elements that are in any of the sets. [[pause 0.5]] Similarly, the second equation says the infinite intersection of the collection contains x only if x in S-alpha for all alpha in I. This matches our intuition that the intersection contains an element if and only if it is in all the sets.

## Page 034: 1.4: De Morgan, Infinite Operations, and Negation (overlay 3 of 3)

Narration:
Now, we can apply De-Morgan’s identity by translating to logic, negating, and mapping back to set theory. First, we see that x is in the infinite union if and only if there exists alpha in I such that x in S alpha. [[pause 0.5]] Since the logical negation of this statement is, for all alpha in-I, x is not in S alpha, [[pause 0.5]] it follows that x is in the complement of the infinite union; if and only if; it is in the infinite intersection; of the complements; of the sets in the collection.

## Page 035: 1.4: Foundations of Set Theory (overlay 1 of 4)

Narration:
Naive set theory allows one to define any set described by a sentence. Russell’s paradox is a famous example that exposed a major problem with naive set theory. [[pause 0.5]] Let R be the set of sets that do not include themselves as members. This set exists in naive set theory, simply because it is described by the above sentence. The paradox arises from the fact that this definition leads to the logical contradiction: R is not in R if and only if R is in R. [[pause 0.5]] In particular, the set-builder construction implies that, if a set does not include itself as a member, then it must be in R. Also, if R includes itself as a member, then logically it cannot be in R.

## Page 036: 1.4: Foundations of Set Theory (overlay 2 of 4)

Narration:
In naive set theory, there are sets that contain themselves. For example, consider the “set of all sets” or the “set of abstract ideas.” But, this is not allowed in axiomatic set theory.

## Page 037: 1.4: Foundations of Set Theory (overlay 3 of 4)

Narration:
What does Russell’s paradox show? It shows that naive set theory is not consistent because it allows constructions leading to contradictions. It is avoided in axiomatic formulations by restricting constructions. It also implies that Russel's set R cannot exist in any consistent set theory.

## Page 038: 1.4: Foundations of Set Theory (overlay 4 of 4)

Narration:
This class will use naive set theory while avoiding such statements.

## Page 039: Next Steps

Narration:
Here are some options to continue learning this material. To continue studying after this video, try the suggested reading: Course Notes EF 1.4. Or the optional reading: PAF Sections 3.1 through 3.5. Also, look at the problems in Assignment 2. [[pause 0.5]] That’s it for today. So, I’ll see you next time.
