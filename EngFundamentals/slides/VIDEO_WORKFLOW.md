# Flipped-classroom video workflow

## Current production path

Qwen3-TTS on the Duke DCC is the production audio backend. From this directory, the normal command is:

```sh
make video VIDEO=0
```

`make video`, `make video-qwen`, `make qwen-video`, and `make video-qwen-remote` all build the canonical remote-backed file `build/video0/video0_qwen3-clone-coben.mp4`. The Makefile checks the remote speech cache before requesting a GPU. A fully cached build skips DCC and SSH entirely; otherwise it starts or reuses the service, opens the tunnel, generates only missing speech, and stops the job when finished.

Local Qwen/MPS is retained only for debugging:

```sh
make video-qwen-local VIDEO=0
```

Local output and caches include the device name, for example `video0_qwen3-local-mps-coben.mp4` and `audio/qwen3-local-mps-coben/`. They cannot satisfy a remote cache lookup or overwrite the canonical production video.

## Goals

1. Keep each Beamer source authoritative for slide content and synchronized speaker notes.
2. Keep reviewed narration editable as ordinary Markdown, with one beat per rendered overlay page.
3. Reuse accepted speech while allowing text, timing, pronunciation, and individual seeds to change incrementally.
4. Make remote GPU allocation, authentication, tunneling, logging, and cleanup automatic.
5. Preserve page audio losslessly until one final AAC encode.

## Source and generated files

- `videoN.tex` is the authoritative Beamer deck and contains `\note` speaker notes.
- `scripts/videoN.md` is the reviewed narration. Each `## Page NNN:` section maps to one overlay page.
- `SCRIPT_TRANSCRIPTION.md` is the normative procedure for expanding the
  authored notes into that reviewed narration without adding prose.
- `audio_config.json` defines timing and the local and remote backend defaults.
- `pronunciations.json` is the shared pronunciation lexicon.
- `build/videoN/slides.pdf` is the linked slide deck for distribution, while
  `build/videoN/video-slides.pdf` is the link-decoration-free deck rasterized
  for video production.
- `build/videoN/beats.jsonl` is generated from the reviewed Markdown and records frames, overlays, chunks, pauses, and seed overrides.
- `build/videoN/audio/qwen3-remote-VOICE/speech/` is the content-addressed production speech cache.
- `build/videoN/audio/qwen3-remote-VOICE/timed/` contains page WAVs assembled from speech and exact PCM silence.
- `build/videoN/audio/qwen3-local-DEVICE-VOICE/` is reserved for local debugging.
- `build/videoN/video-work/PROFILE/narration.wav` is the lossless concatenation of every timed page WAV.
- `build/videoN/video-work/PROFILE/segments/` contains video-only H.264 page segments.
- `build/videoN/videoN_qwen3-clone-VOICE.mp4` is the canonical remote-backed production video.
- `build/videoN/logs/audio-PROFILE.log` records generation and cache decisions.
- `build/videoN/logs/dcc-PROFILE.log` records DCC submission, readiness, tunnel, and service diagnostics.

Generated files live under `build/`, except for the legacy PDFs maintained by `make slides`.

## Pipeline

1. The reviewed Markdown is transcribed from the embedded speaker notes using
   `SCRIPT_TRANSCRIPTION.md`. This alignment and exact-`Read` expansion step
   requires source-aware review; `extract-script` provides diagnostics but does
   not author or approve production narration.
2. `script_to_beats.py` validates that the reviewed Markdown has one beat per rendered Beamer page and expands explicit pause and seed markers.
3. `generate_audio.py --check-speech-cache` computes every speech fingerprint without loading a model. If all files exist, no DCC service is started.
4. On a cache miss, the DCC controller asks Slurm for non-submitting start estimates for every configured GPU candidate, chooses the best performance-adjusted estimate, submits that request, waits for the model to become ready, and creates an authenticated SSH tunnel at `http://127.0.0.1:8765`.
5. Only missing speech chunks are sent to the warm Qwen service. Accepted WAVs remain content-addressed and are reused by later builds.
6. Page-level timed WAVs are assembled from cached speech plus exact lead, tail, and internal silence. Timing-only changes never rerun TTS.
7. `render_video.py` allocates frames from cumulative audio time so 30-fps rounding cannot accumulate across pages. Page segments contain video only.
8. All timed WAVs are concatenated losslessly into one PCM `narration.wav`. FFmpeg encodes this continuous track to AAC exactly once while muxing the final MP4.

When its target is out of date, the final MP4 is re-encoded; an already-current
MP4 is left untouched. Unchanged speech, timed WAVs, rendered frames, and video
segments are reused where their fingerprints or state still match.

## DCC service setup

The service definition is in `/Users/hpfister/github/pfistergroup/agents/dcc/services/qwen3-tts/service.json`.

- Model: `Qwen/Qwen3-TTS-12Hz-1.7B-Base`
- Voice cloning: Coben reference, x-vector mode
- Preferred runtime: BF16 with SDPA on CUDA
- Candidate GPUs: RTX 5000 Ada in `gpu-common` or `scavenger-gpu`, A5000 in
  `gpu-common`, and RTX 2080 in `gpu-common`
- RTX 2080 fallback: FP16 with SDPA because Turing does not provide native BF16
- CPU and memory: 4 CPUs and 32 GB
- Time limit: 2 hours
- Environment and caches: `/work/hp83/dcc-ai/`
- Durable model and voice assets: `/hpc/group/pfisterlab/hp83/dcc-ai/`

No H200 is needed for this 1.7B service. Before submission, the controller runs
`sbatch --test-only` for all enabled candidates. It ranks the reported start
times after adding configurable performance penalties: zero for either RTX
5000 Ada request, three minutes for A5000, and thirty minutes for RTX 2080.
Thus, the 2080 is used only when its shorter queue wait outweighs its slower
generation. The controller records the selected partition, GPU, dtype, estimate,
and job ID in its remote state. The controller uses the SSH host `dcc`; the
local shell alias `cluster` is not required by the Makefile.

Inspect the current decision without submitting a job:

```sh
make dcc-qwen-plan
```

By default, the job and tunnel stop after generation. Keep a service warm across several commands with:

```sh
make video VIDEO=0 DCC_QWEN_AUTOSTOP=0
```

Stop it explicitly with:

```sh
make dcc-qwen-stop
```

## Commands

Run commands from `EngFundamentals/slides/`:

```sh
./makeslides 0
make review VIDEO=0
make extract-script VIDEO=0
make beats VIDEO=0
make audio VIDEO=0
make video VIDEO=0
make video-slides VIDEO=0
```

Useful explicit variants are:

```sh
make video-qwen VIDEO=0          # canonical remote build
make qwen-video VIDEO=0          # alias for video-qwen
make video-qwen-remote VIDEO=0   # explicit remote alias
make video-qwen-local VIDEO=0    # local MPS debugging only
make video-say VIDEO=0           # fast macOS say preview
make dcc-qwen-plan               # compare live GPU candidates; submit nothing
```

For a pronunciation-only diagnostic, use `make pronunciation-test BACKEND=say` or the local Qwen target `make pronunciation-qwen QWEN_DEVICE=cpu`.

## Voice reference and cloning mode

The default reference is the 29.49-second, mono, 16-bit, 44.1-kHz PCM `coben_hold_tight_ch1_first29_hp3.wav` recording derived from the previous ISIT deck. The production service keeps a copy under group storage and handles its input resampling. No exact transcript was found beside the recording, so both local and remote configuration use reference-audio-only x-vector cloning.

For an authorized reference with an exact transcript, local debugging can use ICL mode:

```sh
make video-qwen-local VIDEO=0 QWEN_CLONE_MODE=icl \
  QWEN_REF_AUDIO=voices/reference.wav \
  QWEN_REF_TEXT_FILE=voices/reference.txt
```

Changing a model, voice, reference, cloning mode, language, text, pronunciation, or seed changes the speech fingerprint. Remote identity is additionally pinned by `QWEN_REMOTE_SERVICE_ID`; bump it when the server-side model or voice changes.

## Seeds and alternate takes

The default Qwen seed is `42` in `audio_config.json`. An individual page can request a different cached take:

```text
Narration:
[[seed 17]]
The narration for this page begins here.
```

The marker is removed before synthesis and applies to every chunk on that page. Changing it invalidates only that page's Qwen speech. `QWEN_SEED=17` changes the command-wide default and therefore invalidates every chunk that does not have a page override.

Seeds stabilize cache identity, but they do not make output identical across MPS, CPU, and CUDA. The local MPS backend has produced divergent WAVs from repeated nominally identical runs and is not used for production.

## Institution customization

Edit `institution.tex` to set the shared Beamer values `\univ`, `\mascot`, and
`\city`. Videos 0--4 load this file directly; later videos, chapter decks, and
FAQ documents receive it through `macros.tex`. Institution names in slide
sources should use these commands rather than literal university text.

Narration Markdown uses the matching tokens `{{univ}}`, `{{mascot}}`, and
`{{city}}`. `script_to_beats.py` reads their values from the same
`institution.tex` file, expands the tokens before synthesis, and rejects
unknown or malformed tokens. This keeps visible examples and Qwen narration
synchronized when the course moves to another university. The display value
`Durham, NC` is spoken as “Durham, North Carolina” through the shared `NC`
pronunciation entry.

## Translating Beamer speaker notes

The complete rules and audit checklist are in `SCRIPT_TRANSCRIPTION.md`. The
central rule is that `\note{...}` is an already-authored script, including the
title note. In a note enumeration, each note item normally controls the matched
main slide-body reveal. `Read.` means to speak that newly revealed bullet,
subitems, and displayed mathematics exactly; it does not mean to summarize the
visible slide, reread earlier overlays, or create a smoother explanation. Then
all words following `Read.` are spoken unchanged and in source order.

The rendered PDF establishes the visual states, while the note establishes the
speech. Count mismatches must be mapped explicitly. Preserve extra authored
cues as extra chunks, flag missing cues, and preserve incomplete notes rather
than completing them. Equations may be rendered into faithful spoken
mathematics, but their logical content and scope may not be changed.

This transcription is the judgment-bearing part of the workflow. An LLM can
help perform and audit it, but it is constrained extraction rather than
creative narration. After the reviewed Markdown exists, Make and the Python
tools deterministically handle variables, cache fingerprints, pauses, audio
generation, synchronization, and final rendering.

## Pronunciation authoring

Keep narration readable and add whole words or phrases to `pronunciations.json`:

```json
{
  "term": "ECE 586",
  "spoken": "E C E five eighty-six",
  "test_text": "Welcome to ECE 586."
}
```

Optional backend-specific values override `spoken`, while `ipa` documents the intent. Longer matches take priority. Metadata records source text, synthesis text, and every applied entry.

Stress-sensitive words can be written syllabically in `spoken`, for example
`orthogonal` as `or-THOG-uh-nul`. When spelling alone is ambiguous by part of
speech, prefer phrase entries: `graduates this term`, `graduates and passes`,
and `graduates nor passes` force the verb pronunciation, while noun phrases
such as `the graduates` and adjectival phrases such as `graduate students`
remain untouched.

## Spoken variables: the letter "a" versus the article "a"

English writes the indefinite article and the name of the first letter with the
same character, and Qwen has to guess which one is meant. It guesses from what
follows: if the next word could begin a noun phrase, it reads the schwa article
("uh"), otherwise it reads the letter name ("ay"). Set and function variables sit
in exactly the position an article occupies, so the default guess is usually
wrong. `A union B` is heard as "uh union B", `a comma b` as "uh comma b", and
`for a in A` as "for uh in A".

This cannot be repaired in `pronunciations.json`. Lexicon entries match whole
words, so an `a` entry would rewrite every genuine article in every deck. Fix it
in the narration text, using the first technique below that works.

**1. Rewrite so the bare variable disappears.** Always the best fix, because it
also helps a listener who cannot see the slide:

| Instead of | Write |
|---|---|
| Two sets are disjoint if A intersect B equals the empty set | Two sets are called disjoint if their intersection equals the empty set |
| bracket a is the set of x in A such that x tilde a | the equivalence class containing-a is defined as the set of x in-A such that x tilde a |
| N equals the set of x in Z such that x is at least one | The natural numbers consist of all integers that are at least one |
| f inverse of the set containing f of x equals the set containing x | the inverse image of a singleton set containing f of x is the singleton set containing x |

**2. Bind the letter to its neighbours with hyphens.** A hyphenated span is one
token, so no article reading is available. Hyphenate toward the adjacent
function word — the preposition, conjunction, or operator name — not across a
whole clause: `A-union-B`, `A-cross-B`, `A-minus-B`, `A-complement`, `x-in-A`,
`not-in-B`, `of-A`, `on-A`, `contains-A`, `a-comma-b`, `a-in-A`, `A-sub x`,
`A-to-the power n`, `a-not-in A`.

**3. Break the phrase with a comma or semicolon** where hyphenating would fuse
too many words: `A relation; tilde; between elements of A`, or
`let A be a set of people; and; let P of x y be the statement`. A semicolon also
buys a short prosodic pause, which helps when the letter is a list item:
`the set containing a-c; a-d; b-c; and b-d`.

**4. Say "capital A" or "lowercase a"** when the case distinction matters to the
listener as well as to the synthesizer, as on video 3 page 9: `the logical
statement "a is a member of the set capital A"`.

### Where the risk actually is

The hazard is a lone `a` or `A` followed by a word that can head a noun phrase.
Operator names are the worst offenders because most of them are also nouns:
*union*, *cross*, *complement*, *subset*, *minus*, *intersection*.

Low-risk positions need no markup, and hyphenating them only makes the script
harder to read:

- before a verb — `A equals B`, `A is not empty`, `A contains all elements`;
- at the end of a clause — `the set only containing a.`;
- inside a spelled-out list of letters — `a, e, i, o, and u`;
- after a determiner or noun — `the set A`, `the image of A under f`.

Sentence-initial position is the most dangerous of all, since real sentences
routinely start with an article. Do not open a beat with a bare variable; add
the lead-in that videos 3 and 4 now use — "Now, we consider ...", "We say ...",
"The set ..." — and hyphenate what follows.

### Related single-letter hazards

The same class of failure affects any variable whose name is also a common word.
Watch `I` for an index set, which competes with the pronoun (video 3 page 34
writes `for all alpha in-I`); `U` for a universal set, which is heard as "you";
and `R` for a range or the reals, which is heard as "are". The same three
techniques apply, in the same order of preference.

Each of these edits changes the narration text and therefore the speech
fingerprint, so only the edited page is resynthesized; every other cached chunk
is reused.

## Pause authoring

Automatic defaults are defined in `audio_config.json`:

| Boundary | Tail on current page | Lead on next page | Total silence |
|---|---:|---:|---:|
| Ordinary overlay | 0.65 s | 0.20 s | 0.85 s |
| New slide | 1.40 s | 0.50 s | 1.90 s |

The final page has a 1.25-second tail. Put `Pause-after: 2.5` before `Narration:` to override one page's tail. Insert `[[pause 0.8]]` or `[[pause 0.8s]]` for exact internal silence. Punctuation remains responsible for ordinary sentence-level prosody.

## Logging and failure diagnosis

Remote generation prints cache hits, generated chunks, request latency, audio duration, and real-time factor. The local audio log contains full Python tracebacks. On a remote failure, the Makefile also appends scheduler status and the last 200 lines of the Slurm service log. The server log records request queue time, synthesis time, generated duration, and server-side tracebacks without recording the bearer token.

## Reliable remote runs

- Run `make video-qwen VIDEO=N` in a persistent terminal when it will take more than a few minutes, and poll that terminal rather than starting a new invocation. DCC allocation, service readiness, and synthesis can outlive a short-lived command runner.
- The controller's Slurm `--test-only` result is only a scheduling estimate. Let the configured controller select one of `scavenger`, `common`, and `rtx2080`; do not cancel and requeue a healthy request merely because an estimate is pessimistic or changes.
- After cancelling a run, wait until the controller status reports a terminal state before resubmitting. A job in `COMPLETING` is still live to the controller and an immediate retry can be rejected as already stopping.
- With the normal `DCC_QWEN_AUTOSTOP=1`, a successful build deliberately finishes by stopping the remote service. A final Slurm state such as `CANCELLED ...` after local encoding is therefore normal cleanup, not a failed narration run.

## Incremental regeneration and listening

The build is deliberately granular. A change to pause markers rebuilds timing and affected video segments but does not resynthesize speech. A change to the narration, a pronunciation override, or a per-clip seed resynthesizes only the changed speech fingerprints; unchanged clips are reused from the content-addressed cache. A slide-only edit recompiles the PDF and rerenders the affected video pages without requiring Qwen when the narration fingerprint is unchanged.

After an incremental Qwen run, audition the clips that were actually resynthesized before reviewing the complete video. The newest run in `build/videoN/logs/audio-qwen3-remote-coben.log` is delimited by a `=== ... Remote Qwen audio run ===` marker; its `synthesizing` entries identify the page and chunk. Match those entries to `page`, `chunk`, and `speech_file` in `build/videoN/audio/qwen3-remote-coben/metadata.json`, then listen in page/chunk order. This avoids confusing older log entries with the current run and makes pronunciation or voice-quality checks much faster.

## Post-build acceptance checks

For a completed remote build, verify the following before treating it as the new reference video:

1. The automatic local speech-cache preflight reports no missing cache entries. This check runs before a GPU is requested and does not contact DCC when every speech fingerprint is already cached.
2. The timed page WAVs concatenate byte-for-byte to `build/videoN/video-work/qwen3-remote-coben/narration.wav`; the audio should be mono, 16-bit PCM, at 24 kHz.
3. `ffprobe` reports the expected H.264 video (908x510 at 30 fps) and AAC mono 24-kHz audio. Audio and video durations may differ by at most one video frame because of encoding.
4. Use `ffmpeg`'s `volumedetect` when a narration refresh changes apparent loudness, and inspect the final MP4 as well as the newly synthesized clips.
5. Record the resulting duration, cache/generation counts, and hash in `VIDEO_RESULTS.md` after a material refresh.

## Editing cycle

1. Review `videoN.tex` and source-only `\gpt` comments in its `\note` blocks.
2. Build `make review VIDEO=N` and verify page order and overlay states.
3. Transcribe and audit `scripts/videoN.md` with `SCRIPT_TRANSCRIPTION.md`.
   Expand every `Read.` from the matched new reveal, retain all authored note
   text unchanged and in order, and add no narration.
4. Run `make beats VIDEO=N` before synthesis to validate the Markdown/page map.
5. Update `pronunciations.json`, pauses, and per-page seeds as needed.
6. Run `make video VIDEO=N`. Only changed speech should require DCC inference.
7. Inspect the canonical `videoN_qwen3-clone-coben.mp4` and record significant decisions in `VIDEO_RESULTS.md`.

## Known limitations

- Local MPS inference is useful for experiments but is not production-reliable for this workflow.
- Changing the slide PDF still rerenders all PDF pages; speech remains cached.
- A new remote model or server-side voice must use a new `QWEN_REMOTE_SERVICE_ID` to avoid reusing incompatible speech.
