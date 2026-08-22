SHELL := /bin/bash

VIDEO ?= 0
PYTHON ?= python3
BACKEND ?= qwen3-remote
VOICE ?= Alex
RATE ?= 175
QWEN_PYTHON ?= /Users/hpfister/anaconda3/envs/qwen3tts/bin/python
QWEN_MODEL ?= /Users/hpfister/.cache/huggingface/hub/models--Qwen--Qwen3-TTS-12Hz-1.7B-Base/snapshots/fd4b254389122332181a7c3db7f27e918eec64e3
QWEN_VOICE ?= coben
QWEN_REF_AUDIO ?= /Users/hpfister/overleaf/qary_bpqm_slides_isit26/video_work/voices/coben_hold_tight_ch1_first29_hp2.wav
QWEN_CLONE_MODE ?=
QWEN_REF_TEXT ?=
QWEN_REF_TEXT_FILE ?=
QWEN_DEVICE ?= mps
QWEN_SEED ?=
QWEN_REMOTE_URL ?= http://127.0.0.1:8765
QWEN_REMOTE_SERVICE_ID ?= qwen3-tts-1.7b-base-coben-hp2-xvector-v1
QWEN_REMOTE_TOKEN_ENV ?= DCC_TTS_TOKEN
QWEN_REMOTE_TIMEOUT ?= 600
DCC_GPU_ROOT ?= /Users/hpfister/github/pfistergroup/agents/dcc
DCC_QWEN_CONTROLLER ?= $(DCC_GPU_ROOT)/skills/dcc-gpu-service/scripts/dcc_service.py
DCC_QWEN_CONFIG ?= $(DCC_GPU_ROOT)/services/qwen3-tts/service.json
DCC_QWEN_START_WAIT ?= 600
DCC_QWEN_PREPARE_WAIT ?= 10800
DCC_QWEN_AUTOSTOP ?= 1
DCC_QWEN_COMMAND = $(PYTHON) "$(DCC_QWEN_CONTROLLER)" --config "$(DCC_QWEN_CONFIG)"
AUDIO_CONFIG ?= audio_config.json
LEXICON ?= pronunciations.json
INSTITUTION ?= institution.tex
SLIDE_SHARED_DEPS := $(INSTITUTION) macros.tex

BASE := video$(VIDEO)
SOURCE := $(BASE).tex
SCRIPT := scripts/$(BASE).md
BUILD_DIR := build/$(BASE)
SLIDES_PDF := $(BUILD_DIR)/slides.pdf
VIDEO_SLIDES_PDF := $(BUILD_DIR)/video-slides.pdf
HANDOUT_PDF := $(BUILD_DIR)/handout.pdf
REVIEW_PDF := $(BUILD_DIR)/review-notes.pdf
BEATS := $(BUILD_DIR)/beats.jsonl

ifeq ($(BACKEND),say)
AUDIO_PYTHON := $(PYTHON)
AUDIO_PROFILE := say-$(VOICE)-$(RATE)
OUTPUT_TAG := say
AUDIO_ARGS := --backend say --voice "$(VOICE)" --rate $(RATE)
else ifeq ($(BACKEND),qwen3)
AUDIO_PYTHON := $(QWEN_PYTHON)
AUDIO_PROFILE := qwen3-local-$(QWEN_DEVICE)-$(QWEN_VOICE)
OUTPUT_TAG := qwen3-local-$(QWEN_DEVICE)-$(QWEN_VOICE)
AUDIO_ARGS := --backend qwen3 --qwen-model "$(QWEN_MODEL)" --qwen-voice-name "$(QWEN_VOICE)" --qwen-ref-audio "$(QWEN_REF_AUDIO)" --qwen-device-map "$(QWEN_DEVICE)"
ifneq ($(strip $(QWEN_CLONE_MODE)),)
AUDIO_ARGS += --qwen-clone-mode "$(QWEN_CLONE_MODE)"
endif
ifneq ($(strip $(QWEN_REF_TEXT)),)
AUDIO_ARGS += --qwen-ref-text "$(QWEN_REF_TEXT)"
endif
ifneq ($(strip $(QWEN_REF_TEXT_FILE)),)
AUDIO_ARGS += --qwen-ref-text-file "$(QWEN_REF_TEXT_FILE)"
endif
ifneq ($(strip $(QWEN_SEED)),)
AUDIO_ARGS += --qwen-seed "$(QWEN_SEED)"
endif
QWEN_REF_PREREQ := $(QWEN_REF_AUDIO)
else ifeq ($(BACKEND),qwen3-remote)
AUDIO_PYTHON := $(PYTHON)
AUDIO_PROFILE := qwen3-remote-$(QWEN_VOICE)
OUTPUT_TAG := qwen3-clone-$(QWEN_VOICE)
AUDIO_ARGS := --backend qwen3-remote --qwen-remote-url "$(QWEN_REMOTE_URL)" --qwen-remote-service-id "$(QWEN_REMOTE_SERVICE_ID)" --qwen-remote-token-env "$(QWEN_REMOTE_TOKEN_ENV)" --qwen-remote-timeout "$(QWEN_REMOTE_TIMEOUT)" --qwen-voice-name "$(QWEN_VOICE)"
ifneq ($(strip $(QWEN_SEED)),)
AUDIO_ARGS += --qwen-seed "$(QWEN_SEED)"
endif
else
$(error Unsupported BACKEND '$(BACKEND)'; choose say, qwen3, or qwen3-remote)
endif

AUDIO_DIR := $(BUILD_DIR)/audio/$(AUDIO_PROFILE)
AUDIO_META := $(AUDIO_DIR)/metadata.json
VIDEO_FILE := $(BUILD_DIR)/$(BASE)_$(OUTPUT_TAG).mp4
AUDIO_LOG_DIR := $(BUILD_DIR)/logs
AUDIO_LOG := $(AUDIO_LOG_DIR)/audio-$(AUDIO_PROFILE).log
DCC_QWEN_LOG := $(AUDIO_LOG_DIR)/dcc-$(AUDIO_PROFILE).log

SLIDE_TOOL := tools/build_beamer.py
EXTRACT_TOOL := tools/extract_beamer_notes.py
BEATS_TOOL := tools/script_to_beats.py
AUDIO_TOOL := tools/generate_audio.py
VIDEO_TOOL := tools/render_video.py
LEXICON_BEATS_TOOL := tools/lexicon_to_beats.py
CONCAT_AUDIO_TOOL := tools/concat_audio.py
AUDIO_GENERATE_COMMAND = $(AUDIO_PYTHON) $(AUDIO_TOOL) --beats $(BEATS) --config $(AUDIO_CONFIG) --lexicon $(LEXICON) --output-dir $(AUDIO_DIR) --metadata "$(AUDIO_META)" --log-file "$(AUDIO_LOG)" $(AUDIO_ARGS)

PRON_BUILD_DIR := build/pronunciation
PRON_BEATS := $(PRON_BUILD_DIR)/beats.jsonl
PRON_AUDIO_DIR := $(PRON_BUILD_DIR)/audio/$(AUDIO_PROFILE)
PRON_META := $(PRON_AUDIO_DIR)/metadata.json
PRON_REEL := $(PRON_BUILD_DIR)/pronunciation_$(OUTPUT_TAG).wav

.PHONY: all slides video-slides handout review extract-script script beats audio audio-say audio-qwen audio-qwen-local audio-qwen-remote dcc-qwen-plan dcc-qwen-ready dcc-qwen-stop pronunciation-test pronunciation-say pronunciation-qwen pronunciation-qwen-remote video video-say video-qwen qwen-video video-qwen-local video-qwen-remote clean help FORCE

all: slides

help:
	@echo "make slides VIDEO=0        Build linked slide and handout PDFs"
	@echo "make video-slides VIDEO=0  Build link-decoration-free slides for video rendering"
	@echo "make review VIDEO=0        Build notes with visible GPT review comments"
	@echo "make extract-script VIDEO=0  Extract a diagnostic narration draft"
	@echo "make beats VIDEO=0         Validate the reviewed Markdown narration"
	@echo "make audio VIDEO=0         Generate/reuse layered audio (BACKEND=say, qwen3, or qwen3-remote)"
	@echo "make video VIDEO=0         Assemble the synchronized MP4"
	@echo "make video-qwen VIDEO=0    Build the canonical Qwen video with remote DCC audio"
	@echo "make qwen-video VIDEO=0    Alias for video-qwen"
	@echo "make video-qwen-local VIDEO=0  Debug the local Qwen/MPS backend (separate output)"
	@echo "make video-qwen-remote VIDEO=0  Explicit alias for the canonical remote build"
	@echo "make dcc-qwen-plan          Compare live Slurm candidates without submitting a job"
	@echo "make pronunciation-test    Build a WAV reel for every lexicon entry"
	@echo "Say settings: VOICE=Alex RATE=175"
	@echo "Qwen settings: QWEN_VOICE=coben QWEN_REF_AUDIO=... QWEN_CLONE_MODE=icl QWEN_REF_TEXT_FILE=... QWEN_DEVICE=mps QWEN_SEED=0"
	@echo "Remote Qwen: cache preflight, token, tunnel, and cleanup are automatic; bump QWEN_REMOTE_SERVICE_ID when model/voice changes"
	@echo "DCC lifecycle: automatic by default; set DCC_QWEN_AUTOSTOP=0 to keep the service warm"
	@echo "Logs: $(AUDIO_LOG_DIR)/audio-*.log locally and dcc-*.log for Slurm/tunnel diagnostics"

$(BUILD_DIR):
	mkdir -p "$@"

$(SLIDES_PDF): $(SOURCE) $(SLIDE_TOOL) $(SLIDE_SHARED_DEPS) | $(BUILD_DIR)
	$(PYTHON) $(SLIDE_TOOL) --source $(SOURCE) --mode slides --output "$@"

$(VIDEO_SLIDES_PDF): $(SOURCE) $(SLIDE_TOOL) $(SLIDE_SHARED_DEPS) | $(BUILD_DIR)
	$(PYTHON) $(SLIDE_TOOL) --source $(SOURCE) --mode video --output "$@"

$(HANDOUT_PDF): $(SOURCE) $(SLIDE_TOOL) $(SLIDE_SHARED_DEPS) | $(BUILD_DIR)
	$(PYTHON) $(SLIDE_TOOL) --source $(SOURCE) --mode handout --output "$@"

$(REVIEW_PDF): $(SOURCE) $(SLIDE_TOOL) $(SLIDE_SHARED_DEPS) | $(BUILD_DIR)
	$(PYTHON) $(SLIDE_TOOL) --source $(SOURCE) --mode review --output "$@"

$(BASE)_s.pdf: $(SLIDES_PDF)
	cp "$<" "$@"

$(BASE)_h.pdf: $(HANDOUT_PDF)
	cp "$<" "$@"

slides: $(BASE)_s.pdf $(BASE)_h.pdf
video-slides: $(VIDEO_SLIDES_PDF)
handout: $(HANDOUT_PDF)
review: $(REVIEW_PDF)

extract-script: $(SOURCE) $(EXTRACT_TOOL) | $(BUILD_DIR)
	$(PYTHON) $(EXTRACT_TOOL) $(SOURCE) $(BUILD_DIR)/notes-extracted.md

script: extract-script

$(BEATS): $(SCRIPT) $(BEATS_TOOL) $(INSTITUTION) | $(BUILD_DIR)
	$(PYTHON) $(BEATS_TOOL) $(SCRIPT) "$@" --variables "$(INSTITUTION)"

beats: $(BEATS)

dcc-qwen-plan:
	$(DCC_QWEN_COMMAND) plan

dcc-qwen-ready:
	@mkdir -p "$(AUDIO_LOG_DIR)"
	@set -o pipefail; { \
		echo "=== $$(date '+%Y-%m-%d %H:%M:%S') DCC Qwen startup ==="; \
		echo "[DCC 1/3] Checking the runtime/model, probing Slurm, and requesting the best GPU candidate..."; \
		set +e; \
		$(DCC_QWEN_COMMAND) ensure --prepare-if-missing --prepare-wait "$(DCC_QWEN_PREPARE_WAIT)" --wait "$(DCC_QWEN_START_WAIT)"; \
		rc=$$?; \
		set -e; \
		if [ $$rc -ne 0 ]; then \
			echo "DCC startup failed; collecting scheduler status and the remote service log..."; \
			$(DCC_QWEN_COMMAND) status || true; \
			$(DCC_QWEN_COMMAND) logs --lines 200 || true; \
			$(DCC_QWEN_COMMAND) stop || true; \
			exit $$rc; \
		fi; \
		echo "[DCC 2/3] Opening the authenticated SSH tunnel on $(QWEN_REMOTE_URL)..."; \
		set +e; \
		$(DCC_QWEN_COMMAND) tunnel; \
		rc=$$?; \
		set -e; \
		if [ $$rc -ne 0 ]; then \
			echo "Tunnel setup failed; collecting the remote service log..."; \
			$(DCC_QWEN_COMMAND) status || true; \
			$(DCC_QWEN_COMMAND) logs --lines 200 || true; \
			$(DCC_QWEN_COMMAND) stop || true; \
			exit $$rc; \
		fi; \
		echo "[DCC 3/3] Qwen is warm and ready for synthesis."; \
	} 2>&1 | tee -a "$(DCC_QWEN_LOG)"

dcc-qwen-stop:
	$(DCC_QWEN_COMMAND) stop

$(AUDIO_META): FORCE $(BEATS) $(AUDIO_TOOL) $(AUDIO_CONFIG) $(LEXICON) $(QWEN_REF_PREREQ)
ifeq ($(BACKEND),qwen3-remote)
	@mkdir -p "$(AUDIO_LOG_DIR)"
	@set -Eeuo pipefail; \
		service_attached=0; \
		cleanup() { \
			rc=$$?; \
			trap - EXIT; \
			if [ $$rc -ne 0 ]; then \
				echo "Remote audio generation failed (exit $$rc); collecting diagnostics..." | tee -a "$(AUDIO_LOG)"; \
				{ $(DCC_QWEN_COMMAND) status || true; $(DCC_QWEN_COMMAND) logs --lines 200 || true; } 2>&1 | tee -a "$(AUDIO_LOG)" || true; \
			fi; \
			if [ $$service_attached -eq 1 ] && [ "$(DCC_QWEN_AUTOSTOP)" = "1" ]; then \
				echo "Stopping the SSH tunnel and DCC job (DCC_QWEN_AUTOSTOP=1)..." | tee -a "$(AUDIO_LOG)"; \
				$(DCC_QWEN_COMMAND) stop 2>&1 | tee -a "$(AUDIO_LOG)" || true; \
			elif [ $$service_attached -eq 1 ]; then \
				echo "Leaving the DCC service warm (DCC_QWEN_AUTOSTOP=0)." | tee -a "$(AUDIO_LOG)"; \
			fi; \
			exit $$rc; \
		}; \
		trap cleanup EXIT; \
		echo "=== $$(date '+%Y-%m-%d %H:%M:%S') Remote Qwen audio run ===" | tee -a "$(AUDIO_LOG)"; \
		echo "Checking the remote speech cache before requesting a GPU..." | tee -a "$(AUDIO_LOG)"; \
		set +e; \
		$(AUDIO_GENERATE_COMMAND) --check-speech-cache --verbose; \
		preflight_rc=$$?; \
		set -e; \
		if [ $$preflight_rc -eq 10 ]; then \
			echo "Speech is missing; starting or reusing the DCC Qwen service..." | tee -a "$(AUDIO_LOG)"; \
			$(MAKE) --no-print-directory dcc-qwen-ready VIDEO=$(VIDEO) BACKEND=$(BACKEND); \
			service_attached=1; \
			token="$$($(DCC_QWEN_COMMAND) token)"; \
			export $(QWEN_REMOTE_TOKEN_ENV)="$$token"; \
			unset token; \
		elif [ $$preflight_rc -ne 0 ]; then \
			exit $$preflight_rc; \
		else \
			echo "All speech is cached; skipping the DCC allocation and tunnel." | tee -a "$(AUDIO_LOG)"; \
		fi; \
		$(AUDIO_GENERATE_COMMAND) --verbose
else
	@mkdir -p "$(AUDIO_LOG_DIR)"
	@$(AUDIO_GENERATE_COMMAND)
endif

audio: $(AUDIO_META)

audio-say:
	$(MAKE) audio VIDEO=$(VIDEO) BACKEND=say VOICE="$(VOICE)" RATE=$(RATE)

audio-qwen:
	$(MAKE) audio-qwen-remote VIDEO=$(VIDEO) QWEN_VOICE="$(QWEN_VOICE)" QWEN_REMOTE_URL="$(QWEN_REMOTE_URL)" QWEN_REMOTE_SERVICE_ID="$(QWEN_REMOTE_SERVICE_ID)" QWEN_REMOTE_TOKEN_ENV="$(QWEN_REMOTE_TOKEN_ENV)" QWEN_REMOTE_TIMEOUT="$(QWEN_REMOTE_TIMEOUT)" QWEN_SEED="$(QWEN_SEED)"

audio-qwen-local:
	$(MAKE) audio VIDEO=$(VIDEO) BACKEND=qwen3 QWEN_VOICE="$(QWEN_VOICE)" QWEN_REF_AUDIO="$(QWEN_REF_AUDIO)" QWEN_CLONE_MODE="$(QWEN_CLONE_MODE)" QWEN_REF_TEXT="$(QWEN_REF_TEXT)" QWEN_REF_TEXT_FILE="$(QWEN_REF_TEXT_FILE)" QWEN_DEVICE="$(QWEN_DEVICE)" QWEN_MODEL="$(QWEN_MODEL)" QWEN_SEED="$(QWEN_SEED)"

audio-qwen-remote:
	$(MAKE) audio VIDEO=$(VIDEO) BACKEND=qwen3-remote QWEN_VOICE="$(QWEN_VOICE)" QWEN_REMOTE_URL="$(QWEN_REMOTE_URL)" QWEN_REMOTE_SERVICE_ID="$(QWEN_REMOTE_SERVICE_ID)" QWEN_REMOTE_TOKEN_ENV="$(QWEN_REMOTE_TOKEN_ENV)" QWEN_REMOTE_TIMEOUT="$(QWEN_REMOTE_TIMEOUT)" QWEN_SEED="$(QWEN_SEED)"

$(PRON_BEATS): $(LEXICON) $(LEXICON_BEATS_TOOL)
	$(PYTHON) $(LEXICON_BEATS_TOOL) $(LEXICON) "$@"

$(PRON_META): FORCE $(PRON_BEATS) $(AUDIO_TOOL) $(AUDIO_CONFIG) $(LEXICON) $(QWEN_REF_PREREQ)
	$(AUDIO_PYTHON) $(AUDIO_TOOL) --beats $(PRON_BEATS) --config $(AUDIO_CONFIG) --lexicon $(LEXICON) --output-dir $(PRON_AUDIO_DIR) --metadata "$@" $(AUDIO_ARGS)

$(PRON_REEL): $(PRON_META) $(CONCAT_AUDIO_TOOL)
	$(PYTHON) $(CONCAT_AUDIO_TOOL) $(PRON_META) "$@"

pronunciation-test: $(PRON_REEL)
	@echo "Built $(PRON_REEL)"

pronunciation-say:
	$(MAKE) pronunciation-test BACKEND=say VOICE="$(VOICE)" RATE=$(RATE)

pronunciation-qwen:
	$(MAKE) pronunciation-test BACKEND=qwen3 QWEN_VOICE="$(QWEN_VOICE)" QWEN_REF_AUDIO="$(QWEN_REF_AUDIO)" QWEN_CLONE_MODE="$(QWEN_CLONE_MODE)" QWEN_REF_TEXT="$(QWEN_REF_TEXT)" QWEN_REF_TEXT_FILE="$(QWEN_REF_TEXT_FILE)" QWEN_DEVICE="$(QWEN_DEVICE)" QWEN_MODEL="$(QWEN_MODEL)" QWEN_SEED="$(QWEN_SEED)"

pronunciation-qwen-remote:
	$(MAKE) pronunciation-test BACKEND=qwen3-remote QWEN_VOICE="$(QWEN_VOICE)" QWEN_REMOTE_URL="$(QWEN_REMOTE_URL)" QWEN_REMOTE_SERVICE_ID="$(QWEN_REMOTE_SERVICE_ID)" QWEN_REMOTE_TOKEN_ENV="$(QWEN_REMOTE_TOKEN_ENV)" QWEN_REMOTE_TIMEOUT="$(QWEN_REMOTE_TIMEOUT)" QWEN_SEED="$(QWEN_SEED)"

$(VIDEO_FILE): $(VIDEO_SLIDES_PDF) $(AUDIO_META) $(VIDEO_TOOL)
	$(PYTHON) $(VIDEO_TOOL) --pdf $(VIDEO_SLIDES_PDF) --metadata $(AUDIO_META) --work-dir $(BUILD_DIR)/video-work/$(AUDIO_PROFILE) --output "$@"

video: $(VIDEO_FILE)
	@echo "Built $(VIDEO_FILE)"

video-say:
	$(MAKE) video VIDEO=$(VIDEO) BACKEND=say VOICE="$(VOICE)" RATE=$(RATE)

video-qwen:
	$(MAKE) video-qwen-remote VIDEO=$(VIDEO) QWEN_VOICE="$(QWEN_VOICE)" QWEN_REMOTE_URL="$(QWEN_REMOTE_URL)" QWEN_REMOTE_SERVICE_ID="$(QWEN_REMOTE_SERVICE_ID)" QWEN_REMOTE_TOKEN_ENV="$(QWEN_REMOTE_TOKEN_ENV)" QWEN_REMOTE_TIMEOUT="$(QWEN_REMOTE_TIMEOUT)" QWEN_SEED="$(QWEN_SEED)"

qwen-video: video-qwen

video-qwen-local:
	$(MAKE) video VIDEO=$(VIDEO) BACKEND=qwen3 QWEN_VOICE="$(QWEN_VOICE)" QWEN_REF_AUDIO="$(QWEN_REF_AUDIO)" QWEN_CLONE_MODE="$(QWEN_CLONE_MODE)" QWEN_REF_TEXT="$(QWEN_REF_TEXT)" QWEN_REF_TEXT_FILE="$(QWEN_REF_TEXT_FILE)" QWEN_DEVICE="$(QWEN_DEVICE)" QWEN_MODEL="$(QWEN_MODEL)" QWEN_SEED="$(QWEN_SEED)"

video-qwen-remote:
	$(MAKE) video VIDEO=$(VIDEO) BACKEND=qwen3-remote QWEN_VOICE="$(QWEN_VOICE)" QWEN_REMOTE_URL="$(QWEN_REMOTE_URL)" QWEN_REMOTE_SERVICE_ID="$(QWEN_REMOTE_SERVICE_ID)" QWEN_REMOTE_TOKEN_ENV="$(QWEN_REMOTE_TOKEN_ENV)" QWEN_REMOTE_TIMEOUT="$(QWEN_REMOTE_TIMEOUT)" QWEN_SEED="$(QWEN_SEED)"

FORCE:

clean:
	rm -rf "$(BUILD_DIR)"
