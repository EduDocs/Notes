# Speaker-note transcription specification

This file defines how to turn the embedded Beamer speaker notes in
`videoN.tex` into the reviewed production script `scripts/videoN.md`. It is a
source-faithful transcription task, not a narration-writing task.

## Sources of authority

- The `\note{...}` block is the sole authority for what is spoken. This
  includes the note attached to the title page.
- The rendered overlay PDF is the authority for what is visible at each
  narration beat.
- The TeX source is used to associate note items with slide-body reveals, but
  the rendered PDF must confirm the actual page order and reveal state.
- Existing `\gpt` comments identify possible author edits; they do not
  authorize changing the spoken script. Until the instructor edits the source,
  preserve its wording.

An LLM may align cues with reveals, expand `Read` directions, render notation
as faithful spoken mathematics, and detect mismatches. It must not summarize,
paraphrase, improve, correct, smooth, elaborate, or add transitions.

## Normal frame-by-frame procedure

1. Compile the audience slides and speaker notes. Enumerate the audience PDF
   pages in order, including every overlay state.
2. Put the title-page note in page 1 of the Markdown script. Do not skip it
   because it is outside the main lecture frames.
3. For each Beamer frame, identify the material newly revealed on each overlay.
   Earlier material that remains visible is not new material.
4. Read the frame's `\note{...}` block in source order. In the common pattern
   `\begin{enumerate}[<alert@+>]`, note item 1 controls reveal 1, note item 2
   controls reveal 2, and so on. A note item maps to the corresponding main
   slide-body reveal, not merely to the nearest string in the TeX file.
5. Replace every `Read.` with the exact newly revealed main bullet and any
   displayed subitems or equations belonging to that reveal, in display order.
   Do not speak the word “Read.” Do not reread persistent material from earlier
   overlays unless the note explicitly directs it.
6. After expanding `Read.`, append every authored word that follows it exactly
   where it occurs. Thus, `Read. Additional sentence.` means “speak the matched
   reveal exactly, then speak `Additional sentence.` exactly.” The additional
   sentence supplements the reveal; it does not replace it.
7. Preserve authored prose before, between, and after multiple `Read` commands
   in its original order. Forms such as `Read 0`, `read 1-2`, or a parenthetical
   `(read ...)` refer to the specified displayed entries at that exact position
   in the note.
8. Convert TeX notation only into a faithful audible rendering. Preserve
   quantifier order, negation scope, implication direction, parentheses when
   needed for scope, labels, and the order of displayed expressions. This is
   pronunciation of notation, not an opportunity to explain or restate it.
9. Copy the result into the matching `## Page NNN:` section of
   `scripts/videoN.md`. Institution-dependent text uses `{{univ}}`,
   `{{mascot}}`, and `{{city}}` so the spoken and displayed versions share the
   values in `institution.tex`.

## Special cases and count mismatches

- A single blanket `Read.` associated with a multi-overlay frame applies
  reveal by reveal. Each beat reads only its own newly displayed material.
- If there are more authored cues than rendered overlays, retain every cue in
  source order. Multiple speech chunks may share the final visual state, as in
  video 2. Do not discard or merge cues merely to make the counts equal.
- If an overlay has no authored cue, flag the source with a `\gpt` comment. The
  conservative production fallback is to read only that overlay's newly
  revealed text; do not invent an explanation.
- If a note is incomplete, preserve the incomplete wording and flag it. Do not
  finish the instructor's sentence.
- If the intended cue-to-reveal mapping is genuinely ambiguous, stop and ask
  the instructor. A plausible new script is not a substitute for the embedded
  one.
- TeX layout commands such as `\vspace`, `\setlength`, and `\itemsep` are never
  narration and must not be mistaken for note items.

## Production annotations

Pause, seed, and pronunciation controls are production metadata rather than
new narration:

- `Pause-after: S` changes the silence after one page.
- `[[pause S]]` inserts exact internal silence between authored speech chunks.
- `[[seed N]]` selects an alternate Qwen take without changing the words.
- `pronunciations.json` changes synthesis spelling or phonetics while the
  readable Markdown remains faithful to the note.

These annotations may control delivery, but they must not alter, replace, or
silently repair the authored script.

## Required audit before synthesis

- Every rendered audience page has a Markdown page entry in the same order.
- Every `\note` cue, including the title note, is represented exactly once.
- No literal or bracketed `Read` instruction remains in production narration.
- Each expanded `Read` matches only its associated newly revealed material.
- All prose around `Read` commands remains present and in source order.
- Cue/overlay count mismatches and incomplete notes are documented, not hidden.
- Mathematical speech preserves the displayed statement's content and scope.
- Any words not traceable to a note or an exact displayed reveal are removed.

`make extract-script VIDEO=N` is a diagnostic aid for locating notes and count
mismatches. Its output is not automatically a production script; the reviewed
Markdown must pass the source-and-overlay audit above.
