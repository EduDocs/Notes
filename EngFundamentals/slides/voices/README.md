# Voice-reference assets

The production Qwen voice clone uses this authorized sample from the previous slide project:

`/Users/hpfister/overleaf/qary_bpqm_slides_isit26/video_work/voices/coben_hold_tight_ch1_first29_hp3.wav`

It is a 29.49-second, mono, 16-bit, 44.1-kHz PCM WAV. The local source is not duplicated here. The DCC deployment copies it to durable group storage at:

`/hpc/group/pfisterlab/hp83/dcc-ai/voices/coben_hold_tight_ch1_first29_hp3.wav`

The production server and `qwen3-tts-1.7b-base-coben-hp3-xvector-v1` service identity are pinned to that remote asset. If the server-side reference, model, cloning mode, or voice changes, update the service configuration and bump `QWEN_REMOTE_SERVICE_ID` so old speech cannot be reused under an incompatible identity.

No exact transcript was found beside the sample. The workflow therefore defaults to Qwen's `x-vector` mode. Local debugging can audition an authorized reference with an exact transcript by setting `QWEN_REF_AUDIO`, `QWEN_REF_TEXT` or `QWEN_REF_TEXT_FILE`, and `QWEN_CLONE_MODE=icl`.

Remote CUDA is the production path. Local MPS generation has produced divergent output from nominally identical seeded runs, so local and remote speech caches remain deliberately separate.
