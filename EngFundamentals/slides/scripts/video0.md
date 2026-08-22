# Video 0 narration script

This is the reviewed production narration derived from the speaker notes in
`video0.tex`. Each section corresponds to exactly one page of the overlay-aware slide
PDF. The word “Read” has been expanded, and displayed mathematics has been rewritten
for speech. Edit this file when improving narration; use `make extract-script VIDEO=0`
to regenerate a diagnostic draft from the LaTeX notes without overwriting this file.
Revise it alongside the slide content before rebuilding the production video.
Use `Pause-after: N` before `Narration:` to override the automatic trailing pause
for one page.  Use `[[pause N]]` or `[[pause Ns]]` inside narration for an exact deliberate pause in seconds.
Pronunciation substitutions belong in `pronunciations.json`, not in this readable script.
Qwen uses the default seed in `audio_config.json`. To retry one page with a different
take, put `[[seed N]]` immediately after that page's `Narration:` line.
The production build is `make video VIDEO=0`; it generates missing Qwen speech on the
Duke DCC and writes `build/video0/video0_qwen3-clone-coben.mp4`. The local MPS path is
debug-only and must be requested explicitly with `make video-qwen-local VIDEO=0`.

## Page 001: Title

Narration:
[[seed 43]]
 Hello! I'm Henry Pfister. And this is the course introduction video for ECE 586, Vector-Space Methods. For everyone who is new to {{univ}}, let me start by saying welcome. It's nice to have you watching. [[pause 0.5]] By the end of this short video, you should have a reasonable understanding of the purpose and organization of this course and how to prepare for each class meeting.

## Page 002: Overview

Narration:
[[seed 44]]
 Engineering uses science and mathematics to invent, design, and build things that solve problems and achieve practical goals. From a mathematical perspective, engineering represents the world using vectors and analyzes it using logic, linear algebra, and optimization. This class is essentially an applied math class designed for graduate engineers in data science, signal processing, and quantum computing. Its goal is to refresh and extend your undergraduate knowledge of linear systems, vector spaces, matrices, and optimization.

## Page 003: Major Topics

Narration:
[[seed 43]]
 Here is a list of the major topics covered in this course: logic and set theory; metric spaces and topology; linear algebra, including normed and inner-product spaces; approximation and projection; the four fundamental subspaces via singular value decomposition; and optimization in vector spaces.
[[pause 0.5]]
 Applications include iterative algorithms, spaces of functions, Markov chains, machine learning, dimensionality reduction, and duality bounds in convex optimization. [[pause 0.75]] Don't worry if you don't know some of these words yet.
[[pause 0.5]]
 At the end of the course, they will all be familiar.    Next; I'll present three example problems that the course will cover in detail.

## Page 004: Example Problem 1 (overlay 1 of 7)

Narration:
[[seed 47]]
The first example concerns approximation error in linear systems. Suppose you know that a vector b satisfies A x equals b, for an invertible matrix A;
To be concrete; picture real three-dimensional vectors and a three-by-three matrix.

## Page 005: Example Problem 1 (overlay 2 of 7)

Narration:
To compute x, you could multiply both sides by A inverse. This gives A inverse b equals A inverse A x, which equals x. For this example, I'm assuming everyone is familiar with matrix inversion. If that concept is rusty for you, don't worry. It will be reviewed later, and all concepts used in this class will be defined precisely.

## Page 006: Example Problem 1 (overlay 3 of 7)

Pause-after: 2.5

Narration:
[[seed 45]]
But, what if A is not known perfectly? This happens frequently in practical problems. Pause for a moment and think about what could go wrong.

## Page 007: Example Problem 1 (overlay 4 of 7)

Narration:
Let's assume that we know A-hat equals A plus E, where the error matrix E is small. The key question is how we should define small;
In this course, that question will be considered in some detail.

## Page 008: Example Problem 1 (overlay 5 of 7)

Narration:
Now we can compute x hat as-A hat, inverse times b. But what can we say about x minus x hat? Given A-hat, we can compute an estimate, but we need to understand the difference between that estimate and the true value.

## Page 009: Example Problem 1 (overlay 6 of 7)

Narration:
Metric spaces formalize distance and closeness in the field of topology.  To answer the above question, one can define distances between objects; In particular, we want distances between vectors and distances between matrices. From these, we can also define lengths of those objects.

## Page 010: Example Problem 1 (overlay 7 of 7)

Narration:
[[seed 43]]
 Using these distances, we can define a constant depending on A-hat and b such that the distance between x and x hat is at most that constant times the distance between A and A-hat. We can view the latter distance as the length of the error matrix E. The expression is intended to show that the solution error shrinks as the matrix error shrinks. Bounds of this kind allow system designers to understand how much error can be tolerated.

## Page 011: Example Problem 2 (overlay 1 of 6)

Narration:
Our second example is the approximation of functions by simpler functions. Suppose you want to find a third-order polynomial that gives a good approximation of a function f of x on the interval from zero to one.

## Page 012: Example Problem 2 (overlay 2 of 6)

Narration:
A key question is: what do we mean by good? Should we use maximum error, average error, or something else? As in the previous example, we have to decide how to measure error, or closeness. For instance, any function lying between the dashed red curves has maximum error less than zero point one.

## Page 013: Example Problem 2 (overlay 3 of 6)

Narration:
[[seed 43]]
 A standard approach is to minimize the mean squared error. Here, we minimize over four polynomial coefficients the integral, from zero to one, of the squared difference between f of x and the polynomial. This choice is mathematically convenient because it has a simple solution.

## Page 014: Example Problem 2 (overlay 4 of 6)

Narration:
[[seed 43]]
Given f of x, one can solve this via optimization. If you do this, the expressions simplify nicely. The resulting polynomial is plotted in green.

## Page 015: Example Problem 2 (overlay 5 of 6)

Narration:
This course will show that there is also a simple, intuitive approach. "And, we will explore the geometric reason why the problem simplifies."

## Page 016: Example Problem 2 (overlay 6 of 6)

Narration:
The solution comes from orthogonality and linear algebra. We compute the four coefficients using four linear equations, one for each value of k from zero through three. The integral of the polynomial times x to the k equals the integral of f of x times x to the k. The left-hand side determines a matrix that does not depend on f, so its inverse can be precomputed. "The right-hand side determines a vector that summarizes the particular function f."

## Page 017: Example Problem 3 (overlay 1 of 6)

Narration:
Our third example concerns convex optimization. Consider a real function f of x on the real interval from a to b. We will use the displayed curve as a running example.

## Page 018: Example Problem 3 (overlay 2 of 6)

Narration:
A chord of f is a line connecting the points x comma f of x, and y comma f of y. The chord with x equal to zero and y equal to one point five is shown in green.

## Page 019: Example Problem 3 (overlay 3 of 6)

Narration:
The function is convex if all chords lie above the function. More precisely, for lambda between zero and one, f of lambda x plus one minus lambda times y is at most lambda f of x plus one minus lambda times f of y. The left side is the function value at a point between x and y. The right side is the height of the chord at that same point. From this definition, the example function is convex.

## Page 020: Example Problem 3 (overlay 4 of 6)

Pause-after: 3.0

Narration:
[[seed 43]]
 Convexity implies that all local minima have the same minimum value. Try drawing a function with two distinct local minima and then checking whether it is convex.

## Page 021: Example Problem 3 (overlay 5 of 6)

Narration:
 Can we compute a simple lower bound on the minimum value? Picture simple functions that could be used to lower-bound f of x.

## Page 022: Example Problem 3 (overlay 6 of 6)

Narration:
"Yes."  A convex function also lies above any tangent line. For any x naught in the interval, the minimum of f is at least the minimum, over the interval, of the tangent-line expression f of x naught plus x minus x naught times f prime of x naught. By minimizing this simpler affine function, we obtain a lower bound. Convexity is important in advanced mathematics because these ideas extend naturally to functions that map multidimensional vectors to real numbers.

## Page 023: Course Overview and Philosophy (overlay 1 of 3)

Narration:
The first course theme is the language of mathematics. Engineering has many subfields in which new ideas are described in the language of abstract mathematics. A key goal is to learn this language and its vocabulary in order to read and understand papers, textbooks, and AI responses in these subfields.

## Page 024: Course Overview and Philosophy (overlay 2 of 3)

Narration:
The second theme is standard theorems and their proof. Our focus is on the mathematical foundations of engineering analysis. Proofs illustrate mathematical reasoning and show why results are true. The emphasis is on general techniques that extend to advanced problems.

## Page 025: Course Overview and Philosophy (overlay 3 of 3)

Narration:
Assignments provide the practice needed to build these skills. Written homework builds knowledge of definitions and techniques, while computer assignments demonstrate practical applications. Think of these as training for a sport: each workout provides a small gain, but consistent effort leads to significant improvement over time; "Although some material is challenging, historically most students have become proficient in most of the topics."

## Page 026: Learning Strategies (overlay 1 of 2)

Narration:
"Here are the course elements."   The syllabus lists lecture and video topics by date, along with homework. The course notes give a detailed description of the content. Flipped class videos provide a slide-based introduction to the notes. Lectures target questions and answers about the videos and notes, together with some group work on example problems. Discussion sessions will be mandatory and focus on live problem solving without computers.

## Page 027: Learning Strategies (overlay 2 of 2)

Narration:
I recommend watching the flipped video first and then reading the matching course notes. Afterward, try the homework while referring to the notes as needed. If you are stuck for more than thirty minutes on a question, ask for a hint by email or on the web. Visit office hours for additional help. Most importantly, watch the video before the class meeting. [[pause 1.2s]] Thanks for your attention. I look forward to seeing everybody during our first class.
