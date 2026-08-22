#!/usr/bin/env python3
"""Generate cached speech and separately timed page audio for slide videos."""

import argparse
import hashlib
import json
import logging
import os
import random
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


DEFAULT_QWEN_MODEL = (
    "/Users/hpfister/.cache/huggingface/hub/"
    "models--Qwen--Qwen3-TTS-12Hz-1.7B-Base/"
    "snapshots/fd4b254389122332181a7c3db7f27e918eec64e3"
)
DEFAULT_QWEN_REF_AUDIO = (
    "/Users/hpfister/overleaf/qary_bpqm_slides_isit26/video_work/voices/"
    "coben_hold_tight_ch1_first29.wav"
)

LOGGER = logging.getLogger("generate_audio")
CACHE_MISS_EXIT_CODE = 10


def configure_logging(log_file, verbose: bool) -> None:
    LOGGER.handlers.clear()
    LOGGER.setLevel(logging.DEBUG)
    LOGGER.propagate = False
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S")

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG if verbose else logging.INFO)
    console.setFormatter(formatter)
    LOGGER.addHandler(console)

    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        LOGGER.addHandler(file_handler)
        LOGGER.info("Detailed log: %s", log_file.resolve())


def preview(text: str, limit: int = 90) -> str:
    compact = " ".join(text.split())
    return compact if len(compact) <= limit else compact[: limit - 1] + "…"


def digest(data: dict) -> str:
    payload = json.dumps(data, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def file_digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_beats(path: Path) -> list:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_if_changed(path: Path, text: str) -> None:
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def file_duration(path: Path, ffprobe: str) -> float:
    result = subprocess.run(
        [ffprobe, "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


class PronunciationLexicon:
    def __init__(self, path: Path):
        data = load_json(path)
        self.version = data.get("version", 1)
        self.entries = data.get("entries", [])
        terms = []
        self.by_term = {}
        for entry in self.entries:
            term = entry.get("term", "")
            if not term or not entry.get("spoken"):
                raise ValueError("every pronunciation entry needs term and spoken values")
            if term in self.by_term:
                raise ValueError("duplicate pronunciation term: " + term)
            self.by_term[term] = entry
            terms.append(term)
        terms.sort(key=len, reverse=True)
        self.pattern = None
        if terms:
            alternatives = "|".join(re.escape(term) for term in terms)
            self.pattern = re.compile(r"(?<!\w)(?:" + alternatives + r")(?!\w)")

    def expand(self, text: str, backend: str) -> tuple:
        applied = []
        if self.pattern is None:
            return text, applied

        def replacement(match):
            term = match.group(0)
            entry = self.by_term[term]
            spoken = entry.get(backend, entry["spoken"])
            applied.append({
                "term": term,
                "spoken": spoken,
                "ipa": entry.get("ipa"),
            })
            return spoken

        return self.pattern.sub(replacement, text), applied


class SayBackend:
    def __init__(self, args, signature):
        self.args = args
        self.signature = signature

    def synthesize(self, text: str, output: Path, instruction=None, seed=None) -> None:
        aiff = output.with_name(output.stem + ".tmp.aiff")
        temporary = output.with_name(output.stem + ".tmp.wav")
        try:
            subprocess.run(
                [self.args.say, "-v", self.signature["voice"], "-r", str(self.signature["rate"]),
                 "-o", str(aiff), text],
                check=True,
            )
            subprocess.run(
                [self.args.ffmpeg, "-y", "-loglevel", "error", "-i", str(aiff),
                 "-ar", str(self.signature["sample_rate"]), "-ac", "1", "-c:a", "pcm_s16le", str(temporary)],
                check=True,
            )
            temporary.replace(output)
        finally:
            aiff.unlink(missing_ok=True)
            temporary.unlink(missing_ok=True)


class QwenBackend:
    def __init__(self, args, signature):
        os.environ.setdefault("NUMBA_CACHE_DIR", "/private/tmp/qwen3tts_numba_cache")
        import torch
        from qwen_tts import Qwen3TTSModel

        self.args = args
        self.signature = signature
        self.torch = torch
        self.np = __import__("numpy")
        self.sf = __import__("soundfile")
        print("Loading Qwen3 TTS model from {}".format(signature["model"]), flush=True)
        self.model = Qwen3TTSModel.from_pretrained(
            signature["model"],
            device_map=args.qwen_device_map,
            dtype=torch.float32,
            local_files_only=True,
        )
        print(
            "Building Qwen voice-clone prompt from {} ({})".format(
                signature["reference_audio"], signature["clone_mode"]
            ),
            flush=True,
        )
        self.voice_clone_prompt = self.model.create_voice_clone_prompt(
            ref_audio=signature["reference_audio"],
            ref_text=signature["reference_text"] or None,
            x_vector_only_mode=signature["clone_mode"] == "x-vector",
        )

    def synthesize(self, text: str, output: Path, instruction=None, seed=None) -> None:
        raw = output.with_name(output.stem + ".raw.wav")
        temporary = output.with_name(output.stem + ".tmp.wav")
        try:
            if instruction:
                raise ValueError(
                    "Qwen Base voice cloning does not accept an instruction; "
                    "express delivery through narration text and punctuation instead"
                )
            if seed is None:
                raise ValueError("Qwen synthesis requires an explicit seed")
            random.seed(seed)
            self.np.random.seed(seed % (2**32))
            self.torch.manual_seed(seed)
            wavs, sample_rate = self.model.generate_voice_clone(
                text=text,
                language=self.signature["language"],
                voice_clone_prompt=self.voice_clone_prompt,
            )
            wav = self.np.asarray(wavs[0], dtype=self.np.float32)
            self.sf.write(raw, wav, sample_rate)
            subprocess.run(
                [self.args.ffmpeg, "-y", "-loglevel", "error", "-i", str(raw),
                 "-ar", str(self.signature["sample_rate"]), "-ac", "1", "-c:a", "pcm_s16le", str(temporary)],
                check=True,
            )
            temporary.replace(output)
        finally:
            raw.unlink(missing_ok=True)
            temporary.unlink(missing_ok=True)


class QwenRemoteBackend:
    def __init__(self, args, signature):
        self.args = args
        self.signature = signature
        self.token = os.environ.get(signature["token_env"], "")
        if not self.token:
            raise SystemExit(
                "Qwen remote token is missing; export {}".format(signature["token_env"])
            )
        LOGGER.info(
            "Remote Qwen service: %s (service %s, token from %s)",
            signature["url"],
            signature["service_id"],
            signature["token_env"],
        )

    def synthesize(self, text: str, output: Path, instruction=None, seed=None) -> None:
        temporary = output.with_name(output.stem + ".tmp.wav")
        try:
            if instruction:
                raise ValueError(
                    "Qwen Base voice cloning does not accept an instruction; "
                    "express delivery through narration text and punctuation instead"
                )
            if seed is None:
                raise ValueError("Qwen synthesis requires an explicit seed")
            payload = json.dumps({
                "text": text,
                "language": self.signature["language"],
                "seed": seed,
            }).encode("utf-8")
            request = urllib.request.Request(
                self.signature["url"].rstrip("/") + "/v1/audio/speech",
                data=payload,
                headers={
                    "Authorization": "Bearer " + self.token,
                    "Content-Type": "application/json",
                },
                method="POST",
            )
            started = time.perf_counter()
            LOGGER.debug(
                "POST %s/v1/audio/speech (seed=%s, language=%s, %d characters)",
                self.signature["url"].rstrip("/"),
                seed,
                self.signature["language"],
                len(text),
            )
            try:
                with urllib.request.urlopen(request, timeout=self.signature["timeout_seconds"]) as response:
                    audio = response.read()
                    status = getattr(response, "status", 200)
            except urllib.error.HTTPError as error:
                detail = error.read().decode("utf-8", errors="replace")
                raise RuntimeError("Qwen remote HTTP {}: {}".format(error.code, detail)) from error
            except urllib.error.URLError as error:
                raise RuntimeError("Qwen remote service is unavailable: {}".format(error.reason)) from error
            elapsed = time.perf_counter() - started
            LOGGER.debug(
                "Remote response HTTP %s: %d bytes in %.2fs", status, len(audio), elapsed
            )
            if not audio.startswith(b"RIFF"):
                raise RuntimeError("Qwen remote service did not return a WAV file")
            temporary.write_bytes(audio)
            temporary.replace(output)
        finally:
            temporary.unlink(missing_ok=True)


def qwen_seed(args, settings: dict) -> int:
    default_seed = args.qwen_seed if args.qwen_seed is not None else settings.get("seed", 0)
    try:
        default_seed = int(default_seed)
    except (TypeError, ValueError):
        raise SystemExit("Qwen seed must be an integer")
    if not 0 <= default_seed <= 2**63 - 1:
        raise SystemExit("Qwen seed must be between 0 and 2^63-1")
    return default_seed


def resolve_settings(args, config: dict) -> tuple:
    sample_rate = args.sample_rate or int(config.get("sample_rate", 24000))
    if args.backend == "say":
        settings = config.get("say", {})
        signature = {
            "engine": "macos-say-v2",
            "voice": args.voice or settings.get("voice", "Alex"),
            "rate": args.rate or int(settings.get("rate", 175)),
            "sample_rate": sample_rate,
        }
    elif args.backend == "qwen3-remote":
        settings = config.get("qwen3_remote", {})
        default_seed = qwen_seed(args, settings)
        service_id = args.qwen_remote_service_id or settings.get("service_id", "")
        if not service_id:
            raise SystemExit(
                "Qwen remote service_id is required so cached speech identifies the remote model and voice"
            )
        signature = {
            "engine": "qwen3-remote-v1",
            "service_id": service_id,
            "url": args.qwen_remote_url or settings.get("url", "http://127.0.0.1:8765"),
            "voice_name": args.qwen_voice_name or settings.get("voice_name", "coben"),
            "language": args.qwen_language or settings.get("language", "English"),
            "token_env": args.qwen_remote_token_env or settings.get("token_env", "DCC_TTS_TOKEN"),
            "timeout_seconds": (
                args.qwen_remote_timeout
                if args.qwen_remote_timeout is not None
                else float(settings.get("timeout_seconds", 600))
            ),
            "default_seed": default_seed,
            "sample_rate": sample_rate,
        }
    else:
        settings = config.get("qwen3", {})
        default_seed = qwen_seed(args, settings)
        reference_audio = Path(
            args.qwen_ref_audio or settings.get("reference_audio", DEFAULT_QWEN_REF_AUDIO)
        ).expanduser().resolve()
        if not reference_audio.is_file():
            raise SystemExit("Qwen reference audio was not found: {}".format(reference_audio))
        clone_mode = args.qwen_clone_mode or settings.get("clone_mode", "x-vector")
        reference_text_file_value = args.qwen_ref_text_file or settings.get("reference_text_file", "")
        if reference_text_file_value:
            reference_text_file = Path(reference_text_file_value).expanduser().resolve()
            if not reference_text_file.is_file():
                raise SystemExit(
                    "Qwen reference transcript was not found: {}".format(reference_text_file)
                )
            reference_text = reference_text_file.read_text(encoding="utf-8").strip()
            reference_text_source = str(reference_text_file)
        else:
            reference_text = (
                args.qwen_ref_text
                if args.qwen_ref_text is not None
                else settings.get("reference_text", "")
            )
            reference_text_source = "inline" if reference_text else "none"
        if clone_mode == "icl" and not reference_text.strip():
            raise SystemExit(
                "Qwen ICL cloning requires the exact reference-audio transcript in "
                "reference_text or --qwen-ref-text"
            )
        signature = {
            "engine": "qwen3-base-voice-clone-v1",
            "model": args.qwen_model or settings.get("model", DEFAULT_QWEN_MODEL),
            "device_map": args.qwen_device_map,
            "dtype": "float32",
            "voice_name": args.qwen_voice_name or settings.get("voice_name", "coben"),
            "language": args.qwen_language or settings.get("language", "English"),
            "clone_mode": clone_mode,
            "reference_audio": str(reference_audio),
            "reference_audio_sha256": file_digest(reference_audio),
            "reference_text": reference_text,
            "reference_text_source": reference_text_source,
            "default_seed": default_seed,
            "sample_rate": sample_rate,
        }
    return signature, sample_rate


def resolve_timing(beat: dict, index: int, count: int, timing: dict) -> tuple:
    if beat.get("lead_in_seconds") is not None:
        lead = float(beat["lead_in_seconds"])
    elif beat.get("starts_new_slide"):
        lead = float(timing["new_slide_lead_seconds"])
    else:
        lead = float(timing["overlay_lead_seconds"])

    if beat.get("pause_after_seconds") is not None:
        tail = float(beat["pause_after_seconds"])
        tail_source = "page override"
    elif index + 1 == count:
        tail = float(timing["final_tail_seconds"])
        tail_source = "final page"
    elif beat.get("ends_slide"):
        tail = float(timing["slide_tail_seconds"])
        tail_source = "slide boundary"
    else:
        tail = float(timing["overlay_tail_seconds"])
        tail_source = "overlay boundary"
    if lead < 0 or tail < 0:
        raise ValueError("pause durations cannot be negative")
    return lead, tail, tail_source


def speech_plan(args, signature: dict, lexicon: PronunciationLexicon, beat: dict, chunk: dict) -> dict:
    synthesis_text, applied = lexicon.expand(chunk["text"], args.backend)
    instruction = beat.get("instruction")
    generation_seed = None
    if args.backend in ("qwen3", "qwen3-remote"):
        generation_seed = beat.get("seed")
        if generation_seed is None:
            generation_seed = signature["default_seed"]
    descriptor = {
        "schema": 1,
        "backend": signature,
        "text": synthesis_text,
        "instruction": instruction,
    }
    if generation_seed is not None:
        descriptor["seed"] = generation_seed
    return {
        "synthesis_text": synthesis_text,
        "pronunciations": applied,
        "instruction": instruction,
        "seed": generation_seed,
        "fingerprint": digest(descriptor),
    }


def cache_inventory(args, signature: dict, lexicon: PronunciationLexicon, beats: list) -> dict:
    fingerprints = []
    for beat in beats:
        for chunk in beat.get("chunks", [{"text": beat["text"], "pause_after_seconds": 0.0}]):
            fingerprints.append(speech_plan(args, signature, lexicon, beat, chunk)["fingerprint"])
    unique = set(fingerprints)
    cached = set()
    if not args.force_speech:
        cached = {
            fingerprint
            for fingerprint in unique
            if (args.output_dir / "speech" / (fingerprint + ".wav")).is_file()
        }
    return {
        "chunks": len(fingerprints),
        "unique": len(unique),
        "cached": len(cached),
        "missing": len(unique - cached),
    }


def ensure_silence(directory: Path, seconds: float, sample_rate: int, ffmpeg: str) -> Path:
    milliseconds = int(round(seconds * 1000))
    path = directory / "silence_{:06d}ms.wav".format(milliseconds)
    if path.exists():
        return path
    directory.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.stem + ".tmp.wav")
    subprocess.run(
        [ffmpeg, "-y", "-loglevel", "error", "-f", "lavfi", "-i",
         "anullsrc=channel_layout=mono:sample_rate={}".format(sample_rate),
         "-t", "{:.6f}".format(seconds), "-ar", str(sample_rate), "-ac", "1",
         "-c:a", "pcm_s16le", str(temporary)],
        check=True,
    )
    temporary.replace(path)
    return path


def concatenate_audio(files: list, output: Path, sample_rate: int, ffmpeg: str) -> None:
    temporary = output.with_name(output.stem + ".tmp.wav")
    command = [ffmpeg, "-y", "-loglevel", "error"]
    for path in files:
        command.extend(["-i", str(path)])
    inputs = "".join("[{}:a]".format(index) for index in range(len(files)))
    command.extend([
        "-filter_complex", inputs + "concat=n={}:v=0:a=1[out]".format(len(files)),
        "-map", "[out]", "-ar", str(sample_rate), "-ac", "1", "-c:a", "pcm_s16le", str(temporary),
    ])
    subprocess.run(command, check=True)
    temporary.replace(output)


def run(args) -> int:
    started = time.perf_counter()
    LOGGER.info(
        "Audio generation starting: backend=%s, output=%s", args.backend, args.output_dir.resolve()
    )

    if not args.ffmpeg or not args.ffprobe:
        raise SystemExit("ffmpeg and ffprobe are required")
    if args.backend == "say" and not Path(args.say).exists():
        raise SystemExit("macOS say was not found")

    config = load_json(args.config)
    timing = config.get("timing", {})
    required_timing = {
        "overlay_lead_seconds", "new_slide_lead_seconds", "overlay_tail_seconds",
        "slide_tail_seconds", "final_tail_seconds",
    }
    missing_timing = sorted(required_timing - set(timing))
    if missing_timing:
        raise SystemExit("audio config lacks timing field(s): " + ", ".join(missing_timing))
    signature, sample_rate = resolve_settings(args, config)
    lexicon = PronunciationLexicon(args.lexicon)
    beats = load_beats(args.beats)
    inventory = cache_inventory(args, signature, lexicon, beats)
    LOGGER.info(
        "Speech cache: %d chunks, %d unique, %d cached, %d missing",
        inventory["chunks"], inventory["unique"], inventory["cached"], inventory["missing"],
    )
    if args.check_speech_cache:
        if inventory["missing"]:
            LOGGER.info("Cache preflight: DCC synthesis is required")
            return CACHE_MISS_EXIT_CODE
        LOGGER.info("Cache preflight: complete; no DCC service is needed")
        return 0

    LOGGER.info("Loaded %d narrated pages at %d Hz", len(beats), sample_rate)

    speech_dir = args.output_dir / "speech"
    timed_dir = args.output_dir / "timed"
    silence_dir = args.output_dir / "silence"
    speech_dir.mkdir(parents=True, exist_ok=True)
    timed_dir.mkdir(parents=True, exist_ok=True)
    old = {}
    if args.metadata.exists():
        old = {item["page"]: item for item in load_json(args.metadata)}

    backend = None
    speech_changed = 0
    speech_reused = 0
    timed_changed = 0
    timed_reused = 0
    metadata = []
    chunk_number = 0
    total_chunks = inventory["chunks"]

    for index, beat in enumerate(beats):
        page = int(beat["page"])
        lead, tail, tail_source = resolve_timing(beat, index, len(beats), timing)
        sequence = []
        chunks_metadata = []
        speech_fingerprints = []
        speech_duration = 0.0

        if lead > 0:
            sequence.append(ensure_silence(silence_dir, lead, sample_rate, args.ffmpeg))

        chunks = beat.get("chunks", [{"text": beat["text"], "pause_after_seconds": 0.0}])
        for chunk_index, chunk in enumerate(chunks, start=1):
            chunk_number += 1
            plan = speech_plan(args, signature, lexicon, beat, chunk)
            synthesis_text = plan["synthesis_text"]
            applied = plan["pronunciations"]
            instruction = plan["instruction"]
            generation_seed = plan["seed"]
            speech_fingerprint = plan["fingerprint"]
            speech_path = speech_dir / (speech_fingerprint + ".wav")
            synth_elapsed = None
            if args.force_speech or not speech_path.exists():
                LOGGER.info(
                    "[%d/%d] page %d chunk %d: synthesizing %r",
                    chunk_number, total_chunks, page, chunk_index, preview(synthesis_text),
                )
                if backend is None:
                    LOGGER.info("Initializing %s backend", args.backend)
                    backend_started = time.perf_counter()
                    if args.backend == "say":
                        backend = SayBackend(args, signature)
                    elif args.backend == "qwen3":
                        backend = QwenBackend(args, signature)
                    else:
                        backend = QwenRemoteBackend(args, signature)
                    LOGGER.info("Backend ready in %.2fs", time.perf_counter() - backend_started)
                synth_started = time.perf_counter()
                backend.synthesize(
                    synthesis_text,
                    speech_path,
                    instruction=instruction,
                    seed=generation_seed,
                )
                synth_elapsed = time.perf_counter() - synth_started
                speech_changed += 1
            else:
                speech_reused += 1
                LOGGER.debug(
                    "[%d/%d] page %d chunk %d: cache hit %s (%r)",
                    chunk_number, total_chunks, page, chunk_index,
                    speech_fingerprint[:12], preview(synthesis_text),
                )
            duration = file_duration(speech_path, args.ffprobe)
            if synth_elapsed is not None:
                LOGGER.info(
                    "[%d/%d] generated %.2fs of audio in %.2fs (%.2fx real time)",
                    chunk_number, total_chunks, duration, synth_elapsed,
                    synth_elapsed / duration if duration else 0.0,
                )
            speech_duration += duration
            sequence.append(speech_path)
            internal_pause = float(chunk.get("pause_after_seconds", 0.0))
            if internal_pause > 0:
                sequence.append(ensure_silence(silence_dir, internal_pause, sample_rate, args.ffmpeg))
            speech_fingerprints.append(speech_fingerprint)
            chunks_metadata.append({
                "source_text": chunk["text"],
                "synthesis_text": synthesis_text,
                "pronunciations": applied,
                "instruction": instruction,
                "seed": generation_seed,
                "speech_file": str(speech_path.resolve()),
                "speech_fingerprint": speech_fingerprint,
                "speech_duration_seconds": round(duration, 3),
                "pause_after_seconds": internal_pause,
            })

        if tail > 0:
            sequence.append(ensure_silence(silence_dir, tail, sample_rate, args.ffmpeg))

        timed_descriptor = {
            "schema": 1,
            "speech_fingerprints": speech_fingerprints,
            "lead_in_seconds": lead,
            "internal_pauses": [item["pause_after_seconds"] for item in chunks_metadata],
            "tail_seconds": tail,
            "sample_rate": sample_rate,
        }
        timed_fingerprint = digest(timed_descriptor)
        timed_path = timed_dir / "page_{:03d}.wav".format(page)
        prior = old.get(page, {})
        if args.force_timing or not timed_path.exists() or prior.get("timed_fingerprint") != timed_fingerprint:
            concatenate_audio(sequence, timed_path, sample_rate, args.ffmpeg)
            timed_changed += 1
            LOGGER.debug("page %d: rebuilt timed audio", page)
        else:
            timed_reused += 1
            LOGGER.debug("page %d: reused timed audio", page)
        duration = file_duration(timed_path, args.ffprobe)
        metadata.append({
            "page": page,
            "frame_index": beat.get("frame_index"),
            "frame": beat.get("frame", beat.get("slide", "")),
            "overlay": beat.get("overlay", 1),
            "overlay_count": beat.get("overlay_count", 1),
            "slide": beat.get("frame", beat.get("slide", "")),
            "starts_new_slide": beat.get("starts_new_slide", False),
            "ends_slide": beat.get("ends_slide", False),
            "next_starts_new_slide": index + 1 < len(beats) and beats[index + 1].get("starts_new_slide", False),
            "file": str(timed_path.resolve()),
            "duration_seconds": round(duration, 3),
            "speech_duration_seconds": round(speech_duration, 3),
            "lead_in_seconds": lead,
            "tail_seconds": tail,
            "tail_source": tail_source,
            "internal_pause_seconds": round(sum(item["pause_after_seconds"] for item in chunks_metadata), 3),
            "seed_override": beat.get("seed"),
            "chunks": chunks_metadata,
            "backend": signature,
            "timed_fingerprint": timed_fingerprint,
            "fingerprint": timed_fingerprint,
        })

    valid_pages = {item["page"] for item in metadata}
    for wav in timed_dir.glob("page_*.wav"):
        match = re.search(r"(\d+)$", wav.stem)
        if match and int(match.group(1)) not in valid_pages:
            wav.unlink()
    for legacy in args.output_dir.glob("page_*.wav"):
        legacy.unlink()

    write_if_changed(
        args.metadata,
        json.dumps(metadata, indent=2, ensure_ascii=False) + "\n",
    )
    total = sum(item["duration_seconds"] for item in metadata)
    speech_total = sum(item["speech_duration_seconds"] for item in metadata)
    LOGGER.info(
        "Complete in %.2fs: speech %d synthesized/%d reused; timing %d rebuilt/%d reused; "
        "%.1fs speech, %.1fs total",
        time.perf_counter() - started,
        speech_changed, speech_reused, timed_changed, timed_reused, speech_total, total,
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", choices=("say", "qwen3", "qwen3-remote"), default="say")
    parser.add_argument("--beats", type=Path, required=True)
    parser.add_argument("--config", type=Path, default=Path("audio_config.json"))
    parser.add_argument("--lexicon", type=Path, default=Path("pronunciations.json"))
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--sample-rate", type=int)
    parser.add_argument("--force-speech", action="store_true")
    parser.add_argument("--force-timing", action="store_true")
    parser.add_argument(
        "--check-speech-cache",
        action="store_true",
        help="report whether synthesis is needed and exit 10 when speech is missing",
    )
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--log-file", type=Path)
    parser.add_argument("--say", default=shutil.which("say") or "/usr/bin/say")
    parser.add_argument("--voice")
    parser.add_argument("--rate", type=int)
    parser.add_argument("--qwen-model")
    parser.add_argument("--qwen-voice-name")
    parser.add_argument("--qwen-language")
    parser.add_argument("--qwen-ref-audio")
    parser.add_argument("--qwen-ref-text")
    parser.add_argument("--qwen-ref-text-file")
    parser.add_argument("--qwen-clone-mode", choices=("x-vector", "icl"))
    parser.add_argument("--qwen-seed", type=int)
    parser.add_argument("--qwen-device-map", default="mps")
    parser.add_argument("--qwen-remote-url")
    parser.add_argument("--qwen-remote-service-id")
    parser.add_argument("--qwen-remote-token-env")
    parser.add_argument("--qwen-remote-timeout", type=float)
    parser.add_argument("--ffmpeg", default=shutil.which("ffmpeg"))
    parser.add_argument("--ffprobe", default=shutil.which("ffprobe"))
    args = parser.parse_args()
    configure_logging(args.log_file, args.verbose)
    try:
        return run(args)
    except KeyboardInterrupt:
        LOGGER.error("Audio generation interrupted")
        raise
    except SystemExit as error:
        LOGGER.error("Audio generation stopped: %s", error)
        raise
    except Exception:
        LOGGER.exception("Audio generation failed")
        if args.log_file:
            LOGGER.error("Failure details were written to %s", args.log_file.resolve())
        raise


if __name__ == "__main__":
    raise SystemExit(main())
