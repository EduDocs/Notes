# Video 1 narration script

This reviewed script maps one narration beat to each rendered overlay page of
`video1.tex`. Slide equations and symbols are written as they should be spoken.
Use `[[pause N]]` for exact internal silence and place `[[seed N]]` immediately
after `Narration:` when a page needs an alternate Qwen take.

## Page 001: Title

Narration:
Welcome to the first flipped class video for ECE 586, Vector-Space Methods. Today, we will discuss the first course topic: propositional logic. We will define the basic logical operations and then use them to build conditional, compound, and meta-level statements.

## Page 002: 1: Logic (overlay 1 of 7)

Narration:
Statements, also called propositions, are the fundamental objects of propositional logic. A statement is a declarative sentence that is true or false, but not both.

## Page 003: 1: Logic (overlay 2 of 7)

Narration:
[[seed 43]]
For example, “This video was recorded for a course at {{univ}}” is a statement, and it is true.

## Page 004: 1: Logic (overlay 3 of 7)

Narration:
The sentence “The real number square root of two is rational” is also a statement, but it is false.

## Page 005: 1: Logic (overlay 4 of 7)

Narration:
In contrast, “Wash your hands before dinner” is not a statement because it does not assert something that is true or false. In English, it is a directive sentence.

## Page 006: 1: Logic (overlay 5 of 7)

Narration:
We can form new statements from existing ones using expressions such as and, or, not, if-then, and if and only if. The first three should be familiar from digital logic.

## Page 007: 1: Logic (overlay 6 of 7)

Pause-after: 2.0

Narration:
Consider the statement: “{{univ}} is in {{city}}, or all real numbers are rational.” Is this statement true or false? [[pause 0.4]] The statement is true because a logical ore is true when at least one of its component statements is true.

## Page 008: 1: Logic (overlay 7 of 7)

Narration:
From now on, we will use capital letters such as P, Q, and R to denote abstract statements. Each letter represents a proposition that has a truth value.

## Page 009: 1.1: Basic Definitions (overlay 1 of 4)

Narration:
The conjunction of P and Q is written P-and-Q in English. It is true only when P and Q are both true and it is false otherwise. It is denoted symbolically by P wedge Q, where wedge is a symbol that looks like an upside-down V.

## Page 010: 1.1: Basic Definitions (overlay 2 of 4)

Narration:
The disjunction of P and Q is written P-or-Q in English. It is true when at least one of the two statements is true and it is false only when both are false. It is denoted symbolically by P vee Q where vee is a symbol that looks like a V.

## Page 011: 1.1: Basic Definitions (overlay 3 of 4)

Narration:
The negation of P, written not P or symbolically negation P, reverses its truth value. It is true when P is false and false when P is true.

## Page 012: 1.1: Basic Definitions (overlay 4 of 4)

Narration:
Truth tables summarize these definitions. Each row lists one possible assignment of truth values to the input propositions. The conjunction column is true only in the first row, the disjunction column is false only in the last row, and negation exchanges true and false.

## Page 013: 1.2: Conditional Statements (1) (overlay 1 of 4)

Narration:
The conditional connective “if P, then Q” in English is denoted symbolically by P-right-arrow-Q. It is false only in the case where P is true and Q is false. In every other row of the truth table, it is true. [[pause 0.4]] P is called the antecedent and Q is called the consequent.

## Page 014: 1.2: Conditional Statements (1) (overlay 2 of 4)

Narration:
The last two rows may initially seem surprising because, when P is false, some people guess that the truth value should be undefined.  But, the values shown here are universally accepted in logic.

## Page 015: 1.2: Conditional Statements (1) (overlay 3 of 4)

Narration:
Intuitively, one can think of "If P, then Q" as a promise that Q is true whenever P is true. When P is false, there is no violation and the promise is kept by default. This situation is often called vacuous truth.

## Page 016: 1.2: Conditional Statements (1) (overlay 4 of 4)

Narration:
Suppose a friend promises that, “If it is sunny tomorrow, I will ride my bike.”, and we say their statement is true if they keep their promise. If it rains and they don't ride their bike, then most people would agree that they've kept their promise.

## Page 017: 1.2: Conditional Statements (2) (overlay 1 of 4)

Narration:
The biconditional statement “P if and only if Q” in English is denoted symbolically by P-left-right-arrow-Q. It is true exactly when P and Q have the same truth value. Thus, it is true when both are true and also when both are false.

## Page 018: 1.2: Conditional Statements (2) (overlay 2 of 4)

Narration:
The biconditional has the same truth values as the conjunction of the two directions: If P, then Q; and if Q, then P. Thus, the phrase “if and only if” asserts conditional connectives in both directions.

## Page 019: 1.2: Conditional Statements (2) (overlay 3 of 4)

Narration:
For example, consider the statement “John graduates this term if and only if he passes this class.” As a formal biconditional, it is true when John both graduates and passes, and it is also true when John neither graduates nor passes.

## Page 020: 1.2: Conditional Statements (2) (overlay 4 of 4)

Narration:
Two variations of the statement,"if P, then Q", have standard names. [[pause 0.2]] Its converse is "if Q, then P"; [[pause 0.2]] Its contrapositive is the statement, "if not-Q, then not-P". [[pause 0.2]] A conditional is logically equivalent to its contrapositive but, in general, it is not equivalent to its converse.

## Page 021: 1.2: Compound Statements (overlay 1 of 2)

Narration:
It is also useful to consider compound logical statements like the conjunction of, “if P, then R”, with “Q or not R.” In this case, its truth value depends on the three propositions P, Q, and R.

## Page 022: 1.2: Compound Statements (overlay 2 of 2)

Narration:
[[seed 47]]
In general, there is a mechanical, though tedious, way to construct a truth table. First list all eight assignments of truth values to P, Q, and R. Then, continue by filling any column whose values are determined by previously filled entries. Note that, the numbers at the bottom give an order in which the displayed columns can be filled.

## Page 023: 1.2: Meta Statements (overlay 1 of 5)

Narration:
A meta statement is a logical statement about logical statements. It describes how the truth of a compound expression behaves across all possible valuations of its propositional variables.

## Page 024: 1.2: Meta Statements (overlay 2 of 5)

Narration:
For example, a tautology is a compound statement that is true for every valuation of its variables. For example, P or not P or Q is always true, because either P or not P must be true, regardless of Q.

## Page 025: 1.2: Meta Statements (overlay 3 of 5)

Narration:
A contradiction is a compound statement that is false for every valuation. The expression P and not-P and Q is always false because P and not-P can never both be true.

## Page 026: 1.2: Meta Statements (overlay 4 of 5)

Narration:
The implication R implies S is a meta statement denoted symbolically by a double-arrow from R to S. It asserts that the ordinary conditional connective "if R, then S" is a tautology. The example given is known by the latin name modus ponens. [[pause 0.2]] In English, suppose we know that the conditional connective, "if P, then Q", is true and we also know that, "P is true". Then, it must follow that Q is true. [[pause 0.2]] Since this reasoning holds for all truth values of P and Q, this is a tautology and we use the double arrow to identify this as an implication.

## Page 027: 1.2: Meta Statements (overlay 5 of 5)

Narration:
The equivalence, "R is equivalent to S", is denoted symbolically by the two-sided (or left-right) double-arrow. It asserts that, "the biconditional between R and S", is a tautology. For example, "if P, then Q" is logically equivalent to "not-P or Q". In other words, the two compound statements have identical truth values in every row.  More generally, a single arrow forms a statement whose truth depends on other statements whereas a double arrow asserts that a statement is true in all cases.

## Page 028: Next Steps

Narration:
To continue studying after this video, reed Sections 1 through 1.2.2 of the course notes. The optional reading in Sections 1.1 through 2.6 of PAF is also useful. Also, look at the problems in Assignment 1. [[pause 0.5]] This completes the presentation.
