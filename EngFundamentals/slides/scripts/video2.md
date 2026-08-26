# Video 2 narration script

This production script is transcribed from the `\note{...}` blocks in
`video2.tex`. Each `Read.` directive is replaced by the corresponding revealed
slide item; all other spoken words come from the embedded notes. Use `[[seed N]]`
immediately after `Narration:` to request an alternate remote-Qwen take.

## Page 001: Title

Narration:
Welcome to the second video lecture for ECE 586, Vector-Space Methods. Today, we’ll conclude our unit on logic with a discussion of predicate logic.

## Page 002: 1.2.2: Propositions and Predicates (overlay 1 of 3)

Narration:
The logical system we discussed last time is called propositional logic.

## Page 003: 1.2.2: Propositions and Predicates (overlay 2 of 3)

Narration:
Propositional logic has some limitations. For example, if “Socrates is a person” and “Every person is mortal,” then, we also know that “Socrates is mortal” but, in propositional logic, there is no way to formally deduce this by combining the statements. Thus, propositional logic does not enable one to efficiently reason about large sets of objects.

## Page 004: 1.2.2: Propositions and Predicates (overlay 3 of 3)

Narration:
To overcome this, we use predicate logic. [[pause 0.6]] Let "the universe", you, be a collection of elements and P of x be a statement that can be applied to any x in you. [[pause 0.2]] For example, P of x equals “x has four tires” for the collection U of all vehicles. [[pause 0.2]] Statement P of x is called a predicate and x is called a free variable. Predicate logic allows one to apply statements to sets of objects.

## Page 005: 1.2.2: Quantifiers (overlay 1 of 4)

Narration:
Quantifiers allow statements about collections of elements.; Continuing with our example P of x, consider the universal quantifier: for all x in U, P of x, which gives “All vehicles have four tires”.; Likewise, the existential quantifier: there exists x in U, P of x, gives “There is a vehicle with four tires”. Notice that quantified predicates are really propositional statements that no longer depend on the free variable.; Next, universal instantiation is the inference from x-not in U and, for all x in U, P of x to P of x-not. For example, if my car is x-not in U and "All vehicles have 4 tires", then "My car has 4 tires". Finally, existential generalization is the inference that "U not empty", and "for all x in U, P of x", implies that "there exists x in U, P of x".; In the last two cases, we use the notation for implication because these apply to any collection U and predicate P.

## Page 006: 1.2.2: Quantifiers (overlay 2 of 4)

Narration:
Consider the negation of quantified statements and notice that exactly one of these is true.; "for all x-in-U, P-of-x", or "there exists x in U", such that "not P-of-x". [[pause 0.2]] Continuing the example, this means exactly one of these is true: “all vehicles have four tires” or “there exists a vehicle that does not have four tires.”

## Page 007: 1.2.2: Quantifiers (overlay 3 of 4)

Pause-after: 3.0

Narration:
Thus, they are logical negations of each other and we observe that: the negation of, "for all x in U, P of x", is equivalent to, "there exists x in U such that not P-of-x."; [[pause 0.2]] Likewise, the negation of, "there exists x in U such that P of x", is equivalent to, "for all x in U, not P-of-x."; If you think about it, these two rules hold naturally based on the English terms “for all” and “there exist”.; [[pause 0.3]] Here, we use the notation for equivalence because these statements hold for any collection U and predicate P. [[pause 0.3]] Now, for our running example of U and P of x, consider rephrasing the four associated statements as English sentences. I’ll give you a few seconds to pause the video and try this.

## Page 008: 1.2.2: Quantifiers (overlay 4 of 4)

Narration:
For example, “Not all vehicles have four tires” is equivalent to “There is a vehicle that does not have four tires.”; and  “There does not exist a vehicle with four tires” is equivalent to “All vehicles do not have four tires.”

## Page 009: 1.2.2: Multiple Quantifiers (overlay 1 of 5)

Narration:
Now, consider the predicate P of x-y with two free variables, x and y. For example, Let I be a collection of images and C be a collection of colors. Define predicate P of x y equals “x contains y” for x in I, and y in C.

## Page 010: 1.2.2: Multiple Quantifiers (overlay 2 of 5)

Narration:
“For all x in I and all y in C, P of x y” means “All images in I, contain all colors in C.”

## Page 011: 1.2.2: Multiple Quantifiers (overlay 3 of 5)

Narration:
“For all x in I, there exists y in C such that P of x y” means “All images in I, contain a color in C.”

## Page 012: 1.2.2: Multiple Quantifiers (overlay 4 of 5)

Narration:
In “there exists why-in-you, such that P of x y”, x is a free variable and y is a bound variable. An expression like this doesn’t have a truth value until a specific x is chosen or a quantifier is added.  Multiple quantifiers can be applied one at a time and each changes a free variable into a bound variable.

## Page 013: 1.2.2: Multiple Quantifiers (overlay 5 of 5)

Narration:
Consider negation with multiple quantifiers by applying negation sequentially: This gives, "for all x in I and all y in C, P of x y", is equivalent to, "for all x in I, open parenthesis, for all y in C, P of x y, close parenthesis". [[pause 0.2]] For example, the negation of, for all x in I and for all y in C, P of x y, is equivalent to, there exists x in I and y in C, such that not P of x y. [[pause 0.2]] Likewise, the negation of, there exists x in I, such that, for all y in C, P of x y, is equivalent to, for all x in I, there exists y in C, such that not P of x y. [[pause 0.2]] These rules follow from the single-quantifier case because quantifiers can be considered one at a time.

## Page 014: 1.2.2: Relationships Between Multiple Quantifiers (overlay 1 of 6)

Narration:
Implications and equivalences, assuming I and C are not empty. "For all x in I and all y in C, P of x y", is equivalent to. "for all y in C and all, x in I, P of x y". [[pause 0.2]] Thus, switching the order of the universal quantifiers doesn’t matter.

## Page 015: 1.2.2: Relationships Between Multiple Quantifiers (overlay 2 of 6)

Narration:
Likewise, there exists x in I and y in C, such that P of x y, is equivalent to, there exists y in C and x in I, such that P of x y. [[pause 0.2]] Likewise, switching the order of the existential quantifiers doesn’t matter.

## Page 016: 1.2.2: Relationships Between Multiple Quantifiers (overlay 3 of 6)

Narration:
For all x in I and all y in C, P of x y, implies, there exists x in I, such that, for all y in C, P of x y, since I is not empty. Changing a universal quantifier to an existential quantifier only weakens the statement.

## Page 017: 1.2.2: Relationships Between Multiple Quantifiers (overlay 4 of 6)

Narration:
There exists x in I such that, "for all y in C, P of x y" implies, "for all y in C, there exists x in I", "such that P of x y". [[pause 0.2]] This implication is more subtle.; consider our example where P of x y equals "image x contains color y". The statement, there exists x, for all y, requires an image for each color. Thus, an image of a rainbow suffices because it can be chosen for all colors. [[pause 0.2]] More generally, if there is a single x-naught such that P of x-naught y holds for all y, then for all y, we can choose that x equals x-naught so that P of x y holds.

## Page 018: 1.2.2: Relationships Between Multiple Quantifiers (overlay 5 of 6)

Narration:
There are eight possible choices for the order and type of quantifiers. First, choose the order in which to quantify variables. Then, for each variable, choose “for all” or “there exists.”

## Page 019: 1.2.2: Relationships Between Multiple Quantifiers (overlay 6 of 6)

Narration:
These results and their symmetric pairs can be visualized with the following diagram.  The first row says: "for all x, for all y, P of x y" [[pause 0.1]] implies "there exists x, for all y, P of x y" [[pause 0.1]] which implies "for all why, there exists x, P of x y" [[pause 0.1]] which implies "There exists why and x, P of x y". [[pause 0.4]] The first column notes that for all x, for all why, P of x y, is equivalent to, for all why, for all x, P of x y.; The second row shows the same chain of inference with x and y switched in the quantifiers.

## Page 020: Axiomatic Formulations (overlay 1 of 3)

Narration:
“Ex falso quodlibet” is Latin for “from falsehood, anything.” Observe that, if  "P and not-P, then Q", is true regardless of Q. This shows that, if a logical system accepts both P and not P as true, then one can use this argument to prove any Q. Thus, logicians are careful to avoid contradictions. Fortunately, propositional logic has an axiomatic formulation that is consistent, complete, and decidable.

## Page 021: Axiomatic Formulations (overlay 2 of 3)

Narration:
What do these words mean in logic? Consistent means that implications of axioms do not contain a contradiction. Complete means that all valid implications follow from the axioms. Decidable means there is a terminating algorithm that determines if any implication is valid or not. Axiomatic formulations of mathematics allow one to enumerate all statements that follow from applying some set of axioms. I do want to emphasize that this is not a class on mathematical logic and we will not discuss axiomatic formulations for more than these few minutes in the entire class. Propositional logic is decidable because any finite implication can be tested by building a truth table including all the variables in its compound statements.

## Page 022: Axiomatic Formulations (overlay 3 of 3)

Narration:
Consider first-order predicate logic. Its axiomatic formulation is consistent, complete, and semidecidable. Semidecidable means there is an algorithm that determines the truth of any postulated implication, if it terminates. But, termination in finite time is guaranteed only if the postulate is true. I should mention here that first-order essentially means that the axioms allow quantifiers over variables but they do not allow quantifiers over predicates. For example, statements starting with “for all predicates P of x” are not valid statements in first-order predicate logic.

## Page 023: 1.3: Strategies for Proofs (overlay 1 of 6)

Narration:
An important part of abstract mathematics is reading and understanding proofs. Intuition and proof work together. Intuition identifies what might be true and why. Rigorous proofs verify and communicate that intuition. A proof is a sequence of verifiable steps from assumptions to conclusion. Definitions map between words and symbols. For example, the predicate P-of-x asserting “x is even” encodes the definition of even. You are likely taking this class because you already have good engineering intuition, about what is true and why. A key goal of this class is to improve your skill at communicating that intuition in mathematical proofs.

## Page 024: 1.3: Strategies for Proofs (overlay 2 of 6)

Narration:
Now, we list types of proof for "if P, then Q". First, a direct proof assumes P true and give steps that lead to Q.

## Page 025: 1.3: Strategies for Proofs (overlay 3 of 6)

Narration:
Then, we have proof by contrapositive which proves the equivalent statement, "if not Q, then not P".; This works because the contrapositive statement is equivalent to "if P, then Q" and it is useful because it may be more natural to verify.

## Page 026: 1.3: Strategies for Proofs (overlay 4 of 6)

Narration:
Next, we have proof by contradiction which observes that the negation of "if P, then Q" is equivalent to P and not-Q. Thus, one supposes that P is true and Q is false and then gives steps leading to a contradiction. Proof by contradiction is sometimes easier because one starts by assuming more, namely that P is true and Q is false.

## Page 027: 1.3: Strategies for Proofs (overlay 5 of 6)

Narration:
Finally, we have proof by induction which says, for a predicate P-of-n, prove "for all n in the natural numbers, P of n" by establishing the base case "P of one" and the inductive hypothesis, "for all n in the natural numbers, if P of n, then P of n-plus-one". Induction is a powerful way to rapidly verify infinitely many statements. [[pause 0.3]] Many of you are familiar with some or all of these approaches. In this class, you will gain more experience with these techniques.

## Page 028: 1.3: Strategies for Proofs (overlay 6 of 6)

Narration:
The following examples will be presented in the live session. Euclid’s proof of “if x squared equals two and x is real, then x is not rational” via contradiction. And, P-of-n asserting "the sum, from eye equal one to n, of eye is equal to one half of n squared plus n”; via induction.

## Page 029: Next Steps

Narration:
To continue studying after this video: Try the suggested reading: Course Notes E F one point two point two through one point three. Or the optional reading: P A F one point one through two point six. Also, look at the problems in Assignment one. That’s it for today. So, I’ll see you next time.
