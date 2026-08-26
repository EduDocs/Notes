# Video workflow results and decisions

## Video 0: course introduction

### Current production status

- Source: `video0.tex`
- Beamer frames: 8
- Overlay-aware pages: 27
- Reviewed narration: `scripts/video0.md`
- Production backend: remote Qwen3-TTS on Duke DCC CUDA
- Model: `Qwen/Qwen3-TTS-12Hz-1.7B-Base`
- Voice: Coben hp3 reference, x-vector cloning
- Service identity: `qwen3-tts-1.7b-base-coben-hp3-xvector-v1`
- Canonical output: `build/video0/video0_qwen3-clone-coben.mp4` (the filename
  describes the cloned voice; its production audio profile is remote)
- Canonical audio metadata: `build/video0/audio/qwen3-remote-coben/metadata.json`

The production video has 32 speech chunks across 27 pages, 547.04 seconds of
speech, and 585.89 seconds of timed PCM narration. The current H.264/AAC MP4 is
585.90 seconds at 30 fps and approximately 10.57 MiB.

`make video`, `make video-qwen`, `make qwen-video`, and `make video-qwen-remote` all produce the canonical file from remote audio. Local generation is isolated behind `make video-qwen-local` and writes a device-labeled debug output instead.

### Remote automation status

- Speech-cache preflight: implemented. A fully cached build does not start DCC or open a tunnel.
- Incremental generation: implemented at speech-chunk granularity.
- Automatic service lifecycle: implemented, including deployment, Slurm submission, readiness wait, authenticated tunnel, token retrieval, and cleanup.
- Failure reporting: implemented in local audio/DCC logs with Python tracebacks, scheduler state, the remote service tail, and server-side request timing.
- Storage: environment and caches under `/work/hp83/dcc-ai/`; durable model and voice assets under `/hpc/group/pfisterlab/hp83/dcc-ai/`.
- Default allocation: one scavenger RTX 5000 Ada, 4 CPUs, 32 GB, and a 2-hour limit. H200 resources are not needed.

### Remote versus local Qwen findings

The local and remote paths use the same 1.7B Qwen model, Qwen-TTS `0.1.1`, and Transformers `4.57.3`. They differ in execution stack:

- Local: PyTorch `2.12.1`, float32, MPS or CPU.
- DCC: PyTorch `2.13.0+cu130`, BF16, CUDA 13, SDPA.

The page-21 artifact was present in a local/MPS speech WAV and absent from the remote/CUDA WAV. Repeating the same local MPS request with the same model, text, prompt, and seed did not reproduce the same file: the original was 9.04 seconds and the rerun was 8.24 seconds with a different hash and opening envelope. A local CPU control had a clean opening like CUDA. This points to MPS numerical or sampling nondeterminism rather than a weaker model.

Decision: remote CUDA is the production backend. Local caches include the device name and cannot be reused by remote builds. MPS remains available only for debugging.

### Rendering and audio-concatenation correction

The earlier renderer created an AAC-bearing MP4 segment for every page. Two effects accumulated at boundaries:

1. Rounding every page independently to 30 fps shortened the timeline by about 210 ms by page 21.
2. Per-segment AAC encoder delay moved that page's valid audio roughly another 107 ms earlier.

The old canonical example therefore placed the beginning of page 21 about 317 ms ahead of its intended PCM position. The audio itself correlated with the source clip; the assembly pipeline had moved it.

The current renderer instead:

- allocates video frames from cumulative narration time, keeping every boundary within half a frame rather than accumulating error;
- creates video-only page segments;
- concatenates all timed page WAV data losslessly into `video-work/PROFILE/narration.wav`; and
- AAC-encodes that continuous PCM track exactly once during final muxing.

The corrected local test placed the page-21 prefix at 419.290 seconds, exactly
matching its PCM timeline. The pre-hp2 canonical remote video placed the
corresponding remote page-21 prefix at 421.120 seconds with correlation
`0.99989` to the remote source WAV.

### Performance measurements

A three-prompt benchmark used the same 1.7B model, reference, seed, and text:

| Metric | Local MPS | Warm DCC RTX 5000 Ada |
|---|---:|---:|
| Model/backend initialization | 10.13 s | already warm |
| Synthesis time | 65.10 s | 21.70 s |
| Generated speech | 18.16 s | 19.04 s |
| Weighted real-time factor | 3.59 | 1.14 |
| Generator end-to-end time | 76.38 s | 22.58 s |

Warm DCC inference was about three times faster. The measured cold service startup was about 79 seconds, including a 4-second Slurm wait, so local execution can still be faster for only a few short experimental clips. The DCC service wins when startup is amortized across a lecture or several jobs.

An incremental production run reused 28 chunks and synthesized four changed chunks. A separate fully cached Make test reused all test clips in 0.40 seconds without contacting DCC.

### Pronunciation and timing state

- Shared lexicon entries include `Pfister`, `ECE 586`, `ECE`, `AI`, `Qwen`, `PAF`, `EF`, `Socrates`, `ex falso quodlibet`, `Euclid`, `Cantor`, `Cauchy`, `orthogonal`, three verb-specific `graduates` phrases, and `NC`. `Orthogonality` is deliberately left in its standard spelling for Qwen.
- The default seed is `42`; the reviewed script uses page overrides including 43, 44, 45, and 47.
- Current timed narration contains 7.8 seconds of page lead, 27.6 seconds of page tail, and 3.45 seconds of explicit internal pauses.
- Timing-only changes rebuild timed WAVs and affected video state without regenerating speech.
- The voice reference is `coben_hold_tight_ch1_first29_hp3.wav`, a 29.49-second,
  mono, 16-bit, 44.1-kHz PCM recording. No exact transcript is available, so
  x-vector mode remains the production default.

### Content review carried forward

The slide and note review identified these authorial issues for future revision:

1. Correct and properly scale the matrix perturbation bound in Example Problem 1.
2. Distinguish metric-space distance from the more general notion of topology.
3. Add differentiability, or use subgradients, in the tangent-line bound for a convex function.
4. Make mathematical maturity an explicit learning goal and simplify the dense major-topics slide.
5. Replace several dated or informal phrases and fix the noted grammar and typography.

All 27 slide states were previously rendered and visually inspected. No clipped audience-facing content was found. Example Problem 2 reports a small vertical overflow, but its rendered content remains visible.

### Current operational decision

Use the remote-backed canonical video for production. Preserve backend-specific caches for correctness and debugging, but do not use local/MPS output as the canonical file. Revisit local generation only if PyTorch/Qwen adds a demonstrably stable MPS path or a targeted reproducibility fix is found.

## Videos 1--4: first production batch

### Completed outputs

All four videos were initially built on 2026-08-01 with remote Qwen3-TTS, the
Coben x-vector voice, and default seed 42. Video 3 was refreshed on 2026-08-06
and Video 1 was regenerated with the hp2 Coben reference on 2026-08-22; the
table reports the current outputs.

| Video | Frames | Overlay pages / clips | Speech | Timed narration | Canonical MP4 | Size |
|---|---:|---:|---:|---:|---:|---:|
| 1: Propositional Logic | 8 | 28 pages / 33 clips | 452.96 s | 487.66 s | 487.67 s | 8.51 MB |
| 2: Predicate Logic | 8 | 29 pages / 30 cues | 675.44 s | 710.29 s | 710.30 s | 12.98 MB |
| 3: Set Theory | 10 | 39 pages / 52 clips | 635.92 s | 686.22 s | 686.23 s | 13.16 MB |
| 4: Relations and Functions | 9 | 29 pages / 39 clips | 497.84 s | 538.04 s | 538.07 s | 10.79 MB |

The canonical files are:

- `build/video1/video1_qwen3-clone-coben.mp4`
- `build/video2/video2_qwen3-clone-coben.mp4`
- `build/video3/video3_qwen3-clone-coben.mp4`
- `build/video4/video4_qwen3-clone-coben.mp4`

### Script and overlay decisions

The reviewed scripts are `scripts/video1.md` through `scripts/video4.md`. Every
rendered overlay page has one narration beat. In video 2, each legacy `Read.`
command is expanded by first speaking the matched newly revealed slide text
and then retaining the additional explanation following `Read.` in the note.

The rendered PDFs are the authority for visual states, and the embedded
speaker notes are the sole authority for narration. The extractor now detects
internal overlays even when a frame has no explicit frame-level overlay range,
so it reports the validated counts of 28, 29, 39, and 29 pages. The production
scripts match those PDFs exactly.

Videos 3 and 4 were retranscribed after the video 2 correction. No mathematical
corrections or explanatory transitions were inserted into the spoken scripts.
A blanket `Read.` applies separately to each reveal, and a reveal with no note
cue falls back only to its displayed text. Existing mathematical or grammatical
concerns remain source-only `\gpt` comments for the author to resolve. Video 4
still contains the literal incomplete note text `Here...` on pages 20 and 23;
that phrase is preserved in the audio and flagged in `video4.tex` rather than
being completed speculatively. Its four-overlay “Applying Functions to Sets
(2)” frame has three cues, so page 25 reads only its fourth reveal.

### Pronunciation and timing

The shared lexicon was expanded for these lectures with `PAF`, `EF`,
`Socrates`, `ex falso quodlibet`, `Euclid`, `Cantor`, and `Cauchy`. The readable
spellings remain in Markdown; the phonetic substitutions appear only in the
Qwen request text. All 127 current clips in this batch use seed 42, and no per-page
reseeds have yet been selected.

Video 1 and video 2 each use a two-second slide-tail override after a reflection
question. All other transitions use the shared timing configuration: 0.2-second
overlay lead, 0.5-second new-slide lead, 0.65-second overlay tail, 1.4-second
slide tail, and 1.25-second final tail.

### Automated QA

- Production PDF pages and Markdown beats agree exactly for all four videos.
- No unexpanded `Read.` commands remain. Video 4 intentionally retains the two
  incomplete authored `Here...` cues described above.
- Every timed page WAV is mono, 16-bit, 24 kHz, with exact digital silence in
  its configured lead and tail regions.
- The final files are H.264 at 908 by 510 and 30 fps, with mono 24-kHz AAC.
- MP4 durations agree with cumulative PCM narration to within one video frame.
- Remote logs contain no failed requests, HTTP errors, or tracebacks.
- A cache-only verification after the video 2 narration correction reused all
  30 current video 2 speech chunks and all 29 timed page WAVs, skipped the DCC
  allocation entirely, and left its MP4 unchanged.
- After the latest builds, final AAC peak levels are -0.4 dBFS for video 3 and
  -0.2 dBFS for video 4. Their mean levels are -16.0 and -16.2 dBFS,
  respectively.

The automated checks establish synchronization and file integrity, but an
author listening pass remains the acceptance test for pronunciation, emphasis,
and occasional Qwen voice variation. A problematic page can be regenerated by
adding `[[seed N]]` immediately after its `Narration:` marker and rerunning the
normal video target; all unaffected speech remains cached.

## Institution and pronunciation update

The slide tree now has a shared `institution.tex` with `\univ`, `\mascot`, and
`\city`. All 49 existing author blocks use `\univ`; the university examples in
video 1 and the chapter-1 deck use `\univ` and `\city`. Narration for videos 0
and 1 uses `{{univ}}` and `{{city}}`, which the beat parser expands from the
same TeX file. Representative builds of video 5, `slides_ch1.tex`, and
`faq3.tex` confirmed that both direct and `macros.tex`-based inclusion paths
compile.

The Qwen pronunciation layer sends `or-THOG-uh-nul` for “orthogonal” and
leaves “orthogonality” in its standard spelling. Phrase-specific entries send the
verb in “graduates this term,” “graduates and passes,” and “graduates nor passes” as
`GRAD-joo-ates`, without changing noun or adjective uses of “graduate.” Video 0
was rebuilt with seven current-script chunks synthesized and 25 reused. Video
1 was brought fully current, then three narration typos found during generation
were corrected and regenerated. Its final cache contains all 29 current chunks,
and the remote service was stopped after completion.

## Video 2 source-owned speaker-note correction

`scripts/video2.md` was retranscribed from the embedded `\note{...}` blocks,
including the title-page note. `Read.` now expands only to the exact matched
reveal; every word before or after it comes directly from the note, in source
order. No explanatory prose or transitions were added. Source wording was
preserved even where an existing `\gpt` comment identifies a typo or
mathematical issue for later author editing.

The “Multiple Quantifiers” frame contains six authored note cues but only five
rendered visual overlays. Both source cues are retained as two speech chunks on
the final visual state, separated by 0.5 seconds. The diagnostic note extractor
now detects this mismatch, preserves the title note, distinguishes `\item`
from `\itemsep`, and labels all `Read` replacements as exact rather than
inviting natural-language rewriting.

The `Socrates` lexicon entry sends `SOCK-rah-teez` to Qwen. The latest
source-faithful remote rebuild has 29 pages and 30 authored speech cues, 711.60
seconds of speech, 746.45 seconds of timed narration, a 746.47-second video,
and a size of 15.57 MB. A final pass reused all 30 speech chunks without
requesting DCC.

## Videos 0--2 recompilation after availability-aware scheduling

On 2026-08-02, videos 0--2 were rebuilt sequentially. Video 0 reused all 32
speech chunks without requesting a GPU or rewriting an already-current MP4.
The live Slurm selector chose an RTX
5000 Ada in `gpu-common` for the remaining work; video 1 synthesized four
changed chunks and reused 25, while video 2 synthesized 18 changed chunks and
reused 12. A final cache preflight found zero missing chunks for all three
videos. PDF pages, metadata pages, and MP4 timing agree, and the service job was
cancelled after the batch.

## Video 0 provenance and splice audit

The cached result used during the 2026-08-02 batch was audited after the build
to determine whether it predated the remote-generation and audio-splicing
corrections. It did not, so no additional regeneration was needed.

- All 32 current speech chunks across 27 pages are referenced by metadata whose
  backend is `qwen3-remote-v1` and whose service identity is
  `qwen3-tts-1.7b-base-coben-xvector-v1`.
- The canonical `video0_qwen3-clone-coben.mp4` was assembled after the current
  remote metadata and continuous narration WAV. The `clone` output tag denotes
  the voice-cloning mode; it does not indicate local generation.
- Concatenating the PCM payloads of the 27 timed page WAVs reproduces
  `video-work/qwen3-remote-coben/narration.wav` byte for byte. Both have PCM
  SHA-256 `2cf16903c5a530e9804976f8ab26680199117a7439b8c4d9b08199e2c12f1b87`.
- The continuous WAV is 587.25 seconds. The canonical 30-fps MP4 is 587.2667
  seconds, and its decoded AAC track correlates with the complete narration WAV
  at `0.9998919` with zero measured sample offset. This is the expected result
  of one final AAC encode, not per-page AAC splicing.

The audit therefore confirms both corrected components requested for video 0:
remote CUDA speech generation and lossless full-WAV assembly before the single
final AAC encode.

## Speaker-note transcription rules

The source-faithful corrections made while preparing videos 2--4 are now
captured normatively in `SCRIPT_TRANSCRIPTION.md` and summarized in
`VIDEO_WORKFLOW.md`. In particular, a note item containing `Read.` directs the
producer to read the corresponding main reveal exactly and then speak all
additional note text unchanged. It is not a prompt to paraphrase the slide or
invent narration. The specification also covers the title note, numbered and
parenthetical read directions, persistent versus newly revealed material,
cue/overlay count mismatches, incomplete notes, faithful spoken mathematics,
and the narrow role of production-only pause, pronunciation, and seed markers.

## Video 3 script refresh

Video 3 was refreshed again on 2026-08-07 after an edit to `scripts/video3.md`.
The reviewed script maps 39 overlay pages across 10 frames and contains 52
speech chunks. The incremental build synthesized 2 changed chunks, reused 50,
rebuilt 2 timed page WAVs, and reused 37.

The availability-aware controller selected an immediately available RTX 2080 in
`gpu-common` using FP16. Both synthesis requests completed without an HTTP
error, traceback, or timeout. The current script produces 635.92 seconds of
speech and 686.22 seconds of timed narration; the audio phase completed in 97
seconds. Automatic cleanup stopped the tunnel and cancelled the service job
after synthesis.

The final render rebuilt 2 video segments and reused 37. The 39 page WAVs
concatenate byte-for-byte into the 686.22-second continuous narration WAV,
whose PCM SHA-256 is
`31ab1ea80cb19a955cbde185f87e639cb432d9d702eabae48f18ab7231b8ab03`.
The canonical H.264/AAC output is 686.23 seconds, 908 by 510 at 30 fps, with
mono 24-kHz audio, a maximum volume of -0.3 dB, mean volume of -16.1 dB, and a
size of 13.16 MB. A final cache preflight found all 52 chunks present and
required no DCC service.

## Video 4 remote refresh

Video 4 was refreshed on 2026-08-07 from the reviewed source-faithful script.
It has 29 overlay pages and 39 speech chunks. The incremental build synthesized
4 chunks, reused 35, rebuilt 2 timed page WAVs, and reused 27.

The availability-aware controller selected an immediately available RTX 5000
Ada in `gpu-common` using BF16. All requests completed without retries, HTTP
errors, tracebacks, or timeouts. The build produced 497.84 seconds of speech
and 538.04 seconds of timed narration in 39 seconds of audio work; automatic
cleanup stopped the tunnel and cancelled the service job afterward.

The 29 timed page WAVs concatenate byte-for-byte into the continuous narration
WAV, with PCM SHA-256
`9ad2ca5459a089876ef6514844d1782151fef60e46468ad664eed23aeb6274fe`.
The canonical H.264/AAC video is 538.07 seconds at 908 by 510 and 30 fps, with
mono 24-kHz audio, a maximum volume of -0.3 dB, mean volume of -16.2 dB, and a
size of 10.79 MB. A final cache preflight found all 39 speech chunks present and
required no DCC service.

## Video 5 first production cut

Video 5 was built on 2026-08-08 from the reviewed, source-faithful script. It
has 30 overlay pages across 9 frames and 34 speech chunks. Three unclosed
`\\note{...}` blocks in `video5.tex` were repaired so the review and
link-decoration-free production PDFs would compile; the authored narration
was not changed.

The first remote build synthesized all 34 chunks and rebuilt all 30 timed page
WAVs. The availability-aware controller selected an immediately available RTX
2080 in `gpu-common` using FP16. Every request returned successfully, without
retries, HTTP errors, tracebacks, or timeouts. The build produced 714.60 seconds
of speech and 751.36 seconds of timed narration. Automatic cleanup closed the
SSH tunnel and cancelled service job 51499873 after synthesis.

The 30 timed page WAV payloads concatenate byte-for-byte into the continuous
narration WAV, whose PCM SHA-256 is
`22a320ce8104a1ba0c9504e8c79dcf75885245a9d0c7733ce043affc9dd90140`.
The canonical H.264/AAC output is 751.3667 seconds at 908 by 510 and 30 fps,
with mono 24-kHz audio, a maximum AAC volume of -0.4 dB, a mean volume of
-16.5 dB, and a size of 15.39 MB. Its file SHA-256 is
`21f11584a663abe19852e8ccc85d2639fcfc4678c17613445b83cda7ed0693a5`.
A full FFmpeg decode completed without errors, and start, middle, and end frames
were visually inspected. A final cache preflight reused all 34 speech chunks
and all 30 timed page WAVs without requesting a DCC service.

The first cut intentionally preserves the authored page-28 narration. The
existing review comment in `video5.tex` flags its claims about complements of
open intervals and the Cantor set as mathematically garbled: every closed set
is trivially a union of closed sets, while the likely intended claim concerns
closed intervals. This wording should be corrected and page 28 regenerated
before final publication.

## Video 0 hp2 voice regeneration

Video 0 was regenerated on 2026-08-22 with the authorized
`coben_hold_tight_ch1_first29_hp2.wav` x-vector reference. The reference is a
29.49-second mono, 16-bit, 44.1-kHz PCM file with SHA-256
`e7e1abcc34ccad5eebb27121fcfa929d2a2200ed9d95a37fff1c13a0c53c7742`.
The local and durable DCC copies have identical hashes. The new production
service identity is `qwen3-tts-1.7b-base-coben-hp2-xvector-v1`, so none of the
old-voice speech cache was eligible for reuse.

Before regeneration, the current `qwen3-remote-coben` speech/timed cache,
continuous narration, audio/DCC logs, and canonical MP4 were copied to
`build/video0/backups/2026-08-22-pre-hp2/`. The verified backup contains 86
files and occupies 101 MB. Its prior canonical MP4, narration WAV, and metadata
SHA-256 values are respectively
`ba62e1a3a1e5c155170815a75ff823cbe2d08711c6b9fd0f6b748e97534e7a5b`,
`ed1b0b92f0e4cdb486710ffb9c1302d7baacd2bc2aca1fc3813a8613d7a57281`,
and `66f238fccefed81b28336640fe844ff595431d8b246181bab8146b720d982dff`.

The existing scratch environment had partial purge damage. Conda Doctor found
missing files in ten packages, including 2,707 ncurses files. It was preserved
as `/work/hp83/dcc-ai/envs/qwen3-tts-damaged-2026-08-22`, and the controller's
Slurm preparation path built a clean replacement. Conda Doctor reports no
missing package files in the replacement environment.

The clean remote run selected an RTX 5000 Ada in `gpu-common` using BF16. It
synthesized all 32 chunks and rebuilt all 27 timed pages without a failed
request, HTTP error, or retry. The hp2 output contains 534.32 seconds of speech
and 573.17 seconds of timed PCM narration. The 27 page WAV payloads concatenate
byte-for-byte into the continuous narration WAV, whose PCM SHA-256 is
`faba67949d883f06cf32748b90a74bdb3b0df0201f38321fabbf493e6f59aea3`.

The regenerated canonical MP4 is 573.20 seconds, 10.87 MB, H.264 at 908 by 510
and 30 fps, with mono 24-kHz AAC. Its SHA-256 is
`3dfb355eab6bc5767c05d44db4566b1e7971357993df4df0ca3e73758da721d8`.
A full FFmpeg decode completed without error, and representative start, middle,
and end frames were visually inspected. The video and audio stream durations
differ by 0.016 seconds, within one 30-fps frame. A final cache-only run reused
all 32 speech chunks and 27 timed page WAVs without requesting DCC.

The hp2 result is materially quieter than the prior production: the final AAC
has mean volume -25.9 dBFS and peak -3.6 dBFS, versus -16.3 dBFS mean and 0.0
dBFS peak for the backed-up PCM narration. No normalization was applied, so the
voice trial remains a direct result of the new reference and existing pipeline.

## Video 0 script and pronunciation refresh

Video 0 was incrementally rebuilt on 2026-08-22 after revisions to
`scripts/video0.md`. The `orthogonality` pronunciation request was simplified
from `or-thog-uh-NAL-uh-tee` to `or-thog-uh-nality` to avoid the previous
exaggerated, unstable output. Cache preflight identified eight missing chunks:
the revised script on pages 4, 7--9, 15, 22, and 25, plus page 16 for the new
pronunciation spelling.

The RTX 5000 Ada BF16 run synthesized those 8 chunks and reused the other 24.
It rebuilt 8 timed pages and reused 19; the video renderer rebuilt 12 segments
and reused 15. All synthesis requests returned successfully without retries,
HTTP errors, or tracebacks, and automatic cleanup stopped the service after the
run. The current output contains 539.60 seconds of speech and 578.45 seconds of
timed narration.

The 27 current page WAV payloads concatenate byte-for-byte into the continuous
narration WAV, whose PCM SHA-256 is
`864253f9559b8966157e586ac6bd72be105d210f7325010284b8f3974a0797e7`.
The current canonical MP4 is 578.4667 seconds, 10.94 MB, H.264 at 908 by 510
and 30 fps, with mono 24-kHz AAC. Its SHA-256 is
`d7307483e7d527d0ef630a588a67ba87e61f33e07a34e5fa47c7462dbbfa7629`.
A full FFmpeg decode completed without error; video and audio stream durations
differ by 0.0347 seconds, approximately one 30-fps frame. A final cache-only
run reused all 32 chunks and all 27 timed pages without requesting DCC.

The page-16 pronunciation audition clip is
`build/video0/review-clips/page16-orthogonality-hp2.wav`, SHA-256
`061b8e7072e6e6c9c95c832c33684afe0b3f0a60ae43ac3345e63d9b0788282b`.
The final AAC level remains -25.9 dBFS mean and -3.6 dBFS peak; no normalization
was introduced during this incremental refresh.

## Video 0 standard-spelling pronunciation regeneration

Video 0 was rebuilt again on 2026-08-22 after removing the `orthogonality`
lexicon override. Qwen therefore received the literal standard spelling
`orthogonality` on page 16. Cache preflight found four missing chunks: page 16
for this pronunciation retry and the still-pending authored script edits on
pages 17, 19, and 22. The selected RTX 2080 FP16 run synthesized those four
chunks, reused 28, rebuilt four timed pages, and reused 23. The renderer rebuilt
six video segments and reused 21. All requests returned HTTP 200 without
retries, timeouts, or tracebacks; automatic cleanup closed the tunnel and
cancelled service job 52997358.

The result contains 547.04 seconds of speech and 585.89 seconds of timed PCM
narration. Concatenating the 27 timed page WAV payloads reproduces the
continuous narration byte-for-byte; both have PCM SHA-256
`ffeae834bb2537fe58bd2229b3b4f9bc138e3392a243ea3a135b8f5b32b9f3b7`.
The canonical MP4 is 585.90 seconds, 11,087,050 bytes, H.264 at 908 by 510 and
30 fps, with mono 24-kHz AAC. Its SHA-256 is
`3103bd4f4c1dd849652848114f5a5f8d0fcc247929b270a5692503fbcf65b628`.
A full FFmpeg decode completed without error; its video and audio streams differ
by 1 ms. The AAC level is -26.0 dBFS mean and -3.6 dBFS peak.

A final cache-only run reused all 32 speech chunks and all 27 timed pages and
did not request a DCC allocation. Stable review copies of the four changed raw
speech clips are in `build/video0/review-clips/` with page-specific filenames.

## Video 1 hp2 voice regeneration

Video 1 was regenerated on 2026-08-22 with the Coben hp2 x-vector reference
and service identity `qwen3-tts-1.7b-base-coben-hp2-xvector-v1`. Before the
refresh, its former remote audio cache, timed WAVs, continuous narration WAV,
logs, and canonical MP4 were copied to
`build/video1/backups/2026-08-22-pre-hp2/`. The verified backup has 149 files,
occupies 96 MB, and preserves the prior canonical MP4, narration WAV, and
metadata SHA-256 values:
`53604817cf9eaf9c822c938c3178d8da0b523e248ea1077be62fc3612ff5c4e6`,
`3a602cb1bb665e3e489ccc41cc6e8208d0c845a17596fdbddea48a482ac124f9`, and
`c16d23c6a454ddc693ddbd653cbd2548a9344880ba8a235862cdd06916532a8f`.

The new service selected an RTX 5000 Ada in `gpu-common` with BF16 and SDPA.
It synthesized all 29 speech chunks and rebuilt all 28 timed pages; the video
renderer rebuilt all 28 video segments. All requests returned HTTP 200 without
retries, timeouts, or tracebacks, and automatic cleanup cancelled service job
53006348 after synthesis.

The hp2 result contains 450.72 seconds of speech and 484.62 seconds of timed
PCM narration. Concatenating all 28 timed page WAV payloads reproduces the
continuous narration byte-for-byte; both have PCM SHA-256
`5c9f0e3ad334def8d4064b3fc06e6aa446aedf2c948cba919ba802c8960bbcca`.
The canonical H.264/AAC MP4 is 484.6333 seconds at 908 by 510 and 30 fps, with
mono 24-kHz AAC, a mean volume of -25.8 dBFS, and a peak of -3.9 dBFS. Its
file SHA-256 is
`a6bb09c69e95ace5a1170604470860200bd8d55e96dcc281b3bfadbfb2dfd713`.
The video and audio streams differ by 25 ms, within one 30-fps frame; a full
FFmpeg decode completed without error. A final cache-only run reused all 29
speech chunks and all 28 timed pages without requesting a DCC allocation.

## Video 1 script refresh and Page 3 alternate take

Video 1 was rebuilt on 2026-08-22 after the current reviewed-script edits and
a new Page 3 alternate take. Page 3 retains the authored text, but uses the
page-local Qwen seed `43` rather than the default `42` to obtain a fresh take
of “recorded for a course at Duke University.” The current script also changed
pages 7, 9, 13--16, 20--22, 24, 26, and 27; its current `graduates` lexicon
entry also changed page 19. The remote run synthesized 14 clips and reused 15,
rebuilt 14 timed pages and reused 14, and rebuilt 21 video segments while
reusing seven. The RTX 5000 Ada BF16 requests completed without retries,
timeouts, or tracebacks, and cleanup cancelled service job 53007758.

The current result has 436.64 seconds of speech and 470.54 seconds of timed
PCM narration. The 28 page WAV payloads concatenate byte-for-byte to the
continuous narration WAV, with PCM SHA-256
`2e3d076838a558ff44d3aeb4ba7e24140864ce1fc57ead12faba9a35592cb19e`.
The canonical MP4 is 470.5667 seconds, 8,603,460 bytes, H.264 at 908 by 510
and 30 fps, with mono 24-kHz AAC. Its SHA-256 is
`2ee48cdac07e6b2434d1cc4d9055b0622e450e5ee6653e8975660ab22137059d`.
Its mean and peak AAC levels are -25.4 dBFS and -3.5 dBFS. A full FFmpeg decode
completed without error; the MP4 duration differs from the PCM narration by
27 ms, within one 30-fps frame. A final cache-only run reused all 29 clips and
all 28 timed pages without requesting DCC. Stable copies of the 14 regenerated clips are in
`build/video1/review-clips/`.

## Video 1 current-script regeneration

Video 1 was incrementally regenerated on 2026-08-22 from the next set of
authored script and pronunciation edits. The current build synthesized 11
speech clips, reused 18, rebuilt 11 timed pages, and reused 17; the renderer
rebuilt 12 video segments and reused 16. The availability-aware controller
selected an immediately available RTX 5000 Ada in `scavenger-gpu` with BF16.
All requests completed without retries, timeouts, or tracebacks, and automatic
cleanup cancelled service job 53020708.

The current result contains 439.04 seconds of speech and 472.94 seconds of
timed PCM narration. The 28 timed page WAVs concatenate byte-for-byte into the
continuous narration WAV, with PCM SHA-256
`7b817e96d813c2605fe08adbf736e1f04ed852b7c2c8e13c1b52474e8204777e`.
The canonical H.264/AAC MP4 is 472.9667 seconds, 8,644,316 bytes, at 908 by
510 and 30 fps, with mono 24-kHz AAC. Its SHA-256 is
`c625457bad1eb881d13ca4bc8e520d7db7241f3e180a496f85f4e8d99b0ea6a1`.
Full FFmpeg decoding completed without error; a final cache-only run reused all
29 speech chunks and all 28 timed pages without requesting DCC.

## Video 1 split-cue regeneration

Video 1 was incrementally regenerated on 2026-08-22 from the latest authored
script and pronunciation edits. The current script has 33 speech chunks across
28 rendered overlay pages. The production run synthesized nine changed chunks,
reused 24, rebuilt five timed pages, and reused 23; the renderer rebuilt seven
video segments and reused 21. The availability-aware controller selected an RTX
5000 Ada in `scavenger-gpu` with BF16. All requests completed without retries,
timeouts, HTTP errors, or tracebacks, and automatic cleanup cancelled service
job 53036809.

The current result contains 453.12 seconds of speech and 487.82 seconds of
timed PCM narration. Concatenating the 28 timed page WAV payloads reproduces
the continuous narration WAV byte-for-byte; both have PCM SHA-256
`c463b57e6188bad81b267237464cbffa2bffd3a7fefb059badef4d731c5c284e`.
The canonical H.264/AAC MP4 is 487.8333 seconds, 8,873,695 bytes, at 908 by
510 and 30 fps, with mono 24-kHz AAC. Its SHA-256 is
`9b086e85331668263b9a6e1e6ca262007ea9b1469ada13b235f9b142b9b8e5bb`.
Full FFmpeg decoding completed without error; the final AAC level is -25.6 dBFS
mean and -3.9 dBFS peak. A final cache-only run reused all 33 speech chunks and
all 28 timed pages without requesting DCC.

## Video 1 conditional and meta-statement refresh

Video 1 was incrementally regenerated on 2026-08-23 after the current edits to
the Page 20 conditional examples and two Page 26 meta-statement cues. The
remote production run synthesized five speech chunks, reused 28, rebuilt two
timed pages, and reused 26; the renderer rebuilt four video segments and reused
24. The controller selected an RTX 5000 Ada in `scavenger-gpu` with BF16, and
automatic cleanup cancelled service job 53039028. The successful remote run had
no request retries, timeouts, HTTP errors, or tracebacks.

The result contains 452.96 seconds of speech and 487.66 seconds of timed PCM
narration. The continuous narration WAV has SHA-256
`f097ef02f7bbc0b734e89fcfbbd8f070be84457780cbafadc2dc4363e3ec030f`.
The canonical H.264/AAC MP4 is 487.6667 seconds, 8,925,888 bytes, at 908 by
510 and 30 fps, with mono 24-kHz AAC. Its SHA-256 is
`791ee51f6cd3983d18d618521e08c7d77e72bef99170367cabca874d5ce0fdfc`.
Full FFmpeg decoding completed without error; the audio and video streams differ
by 30 ms, within one 30-fps frame. The final AAC level is -25.7 dBFS mean and
-3.9 dBFS peak. A final cache-only verification reused all 33 speech chunks and
all 28 timed pages without requesting DCC. Stable review copies of the five
regenerated clips are in `build/video1/review-clips/latest-2026-08-23/`.

## Video 2 hp2 voice regeneration

Video 2 was regenerated on 2026-08-23 with the Coben hp2 x-vector reference
and service identity `qwen3-tts-1.7b-base-coben-hp2-xvector-v1`. Before the
refresh, the prior-voice remote audio cache, video-work state, logs, and
canonical MP4 were copied to `build/video2/backups/2026-08-23-pre-hp2/`. The
verified backup contains 223 files and occupies 222 MB; its preserved MP4,
narration WAV, and metadata SHA-256 values are respectively
`2b3dac998a2d7e7abfa64ff4f122465711fe04d2d14c52bb4e0b8d8b1ddf3860`,
`7eb33010103b9008cc498cc48327d6512c998a9766499388be71a032bf6557ff`, and
`5fc4af4e50e53431b4c9d52d9cade00c06a3e11cb7dccd93cdac72e3f1e16d43`.

All 30 current speech chunks were newly synthesized and all 29 timed pages and
video segments were rebuilt. The availability-aware controller selected an
immediately available RTX 2080 in `gpu-common` with FP16 and SDPA; all remote
requests succeeded without retries, timeouts, HTTP errors, or tracebacks, and
automatic cleanup cancelled service job 53127465.

The hp2 result contains 675.44 seconds of speech and 710.29 seconds of timed
PCM narration. The continuous narration WAV has SHA-256
`daf61065612a2c785512fc3e33343a39cfdf1076dcdb0f78c662d48ce6904ac6`.
The canonical H.264/AAC MP4 is 710.3000 seconds, 13,615,511 bytes, at 908 by
510 and 30 fps, with mono 24-kHz AAC. Its SHA-256 is
`4e8e947873edd499f0f018e23ef30af563c8536bcaf35f013b3619bfcb77faf2`.
Full FFmpeg decoding completed without error; audio and video stream durations
differ by 28 ms, within one 30-fps frame. The final AAC level is -25.6 dBFS
mean and -3.5 dBFS peak. A final cache-only run reused all 30 clips and all 29
timed pages without requesting DCC.

## Video 2 hp3 voice regeneration

Video 2 was regenerated on 2026-08-24 with the Coben hp3 x-vector reference
`coben_hold_tight_ch1_first29_hp3.wav`. The 29.49-second mono, 16-bit,
44.1-kHz PCM reference was uploaded to
`/hpc/group/pfisterlab/hp83/dcc-ai/voices/` and verified there with SHA-256
`eee11132b2cb130a97ae3042419a510be6d948dec563641b89847eac3d662aa3`.
The service identity was bumped to
`qwen3-tts-1.7b-base-coben-hp3-xvector-v1`, so none of the hp2 speech cache
was eligible for reuse.

The first build exposed a malformed `[[pause 0,2]]` marker on Page 7 of
`scripts/video2.md`; it was corrected to `[[pause 0.2]]` before synthesis.
The clean run selected an RTX 5000 Ada in `gpu-common` with BF16 and SDPA,
synthesized all 31 chunks, and rebuilt all 29 timed pages without HTTP errors
or retries. It produced 698.3 seconds of speech and 733.4 seconds of timed
PCM narration. The continuous narration WAV has SHA-256
`f703ebed07d7a7cd8fd3b815cd900f343a68c680fdd9ff1c4eb8630f80a1b48e`.

The canonical H.264/AAC MP4 is 733.4000 seconds, 12,894,254 bytes, at 908 by
510 and 30 fps. Its SHA-256 is
`61eae84b33d25a9dc7641c96675203b90ce5d771b8e1075de023744f5c6df551`.
Automatic cleanup stopped the DCC service after synthesis.
