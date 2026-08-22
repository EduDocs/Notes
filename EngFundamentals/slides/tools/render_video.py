#!/usr/bin/env python3
"""Render a slide PDF and synchronized WAV files into an incremental MP4."""

import argparse
import hashlib
import json
import math
import re
import shutil
import subprocess
import wave
from pathlib import Path


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def pdf_pages(path: Path, pdfinfo: str) -> int:
    result = subprocess.run([pdfinfo, str(path)], check=True, capture_output=True, text=True)
    match = re.search(r"^Pages:\s+(\d+)", result.stdout, re.M)
    if not match:
        raise RuntimeError("could not read PDF page count")
    return int(match.group(1))


def write_text_if_changed(path: Path, text: str) -> None:
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return
    path.write_text(text, encoding="utf-8")


def rendered_frames(directory: Path) -> list:
    def page_number(path: Path) -> int:
        match = re.search(r"-(\d+)$", path.stem)
        return int(match.group(1)) if match else -1
    return sorted(directory.glob("page-*.png"), key=page_number)


def wav_duration(path: Path) -> float:
    with wave.open(str(path), "rb") as source:
        return source.getnframes() / source.getframerate()


def concatenate_wavs(files: list, output: Path) -> None:
    """Join compatible PCM WAVs without resampling, filtering, or lossy encoding."""
    if not files:
        raise ValueError("cannot concatenate an empty WAV list")
    temporary = output.with_name(output.stem + ".tmp.wav")
    expected = None
    try:
        with wave.open(str(temporary), "wb") as target:
            for path in files:
                with wave.open(str(path), "rb") as source:
                    parameters = (
                        source.getnchannels(),
                        source.getsampwidth(),
                        source.getframerate(),
                        source.getcomptype(),
                    )
                    if expected is None:
                        expected = parameters
                        channels, sample_width, sample_rate, compression = parameters
                        if compression != "NONE":
                            raise ValueError("narration WAVs must use uncompressed PCM")
                        target.setnchannels(channels)
                        target.setsampwidth(sample_width)
                        target.setframerate(sample_rate)
                        target.setcomptype("NONE", "not compressed")
                    elif parameters != expected:
                        raise ValueError(
                            "narration WAV format differs for {}: expected {}, got {}".format(
                                path, expected, parameters
                            )
                        )
                    target.writeframes(source.readframes(source.getnframes()))
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)


def allocate_frame_counts(durations: list, fps: int) -> list:
    """Round cumulative boundaries so frame error cannot accumulate page by page."""
    counts = []
    cumulative_seconds = 0.0
    previous_boundary = 0
    for index, duration in enumerate(durations):
        cumulative_seconds += duration
        if index + 1 == len(durations):
            boundary = math.ceil(cumulative_seconds * fps)
        else:
            boundary = int(cumulative_seconds * fps + 0.5)
        count = boundary - previous_boundary
        if count <= 0:
            raise ValueError("every narration page must occupy at least one video frame")
        counts.append(count)
        previous_boundary = boundary
    return counts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--dpi", type=int, default=144)
    parser.add_argument("--fps", type=int, default=30)
    args = parser.parse_args()

    ffmpeg = shutil.which("ffmpeg")
    pdftoppm = shutil.which("pdftoppm")
    pdfinfo = shutil.which("pdfinfo")
    missing = [name for name, value in (("ffmpeg", ffmpeg), ("pdftoppm", pdftoppm), ("pdfinfo", pdfinfo)) if not value]
    if missing:
        raise SystemExit("missing required command(s): " + ", ".join(missing))

    metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
    pages = pdf_pages(args.pdf, pdfinfo)
    if pages != len(metadata):
        raise SystemExit("PDF has {} pages but narration has {} beats".format(pages, len(metadata)))
    if [item["page"] for item in metadata] != list(range(1, pages + 1)):
        raise SystemExit("narration page numbers are not contiguous")

    frames_dir = args.work_dir / "frames"
    segments_dir = args.work_dir / "segments"
    frames_dir.mkdir(parents=True, exist_ok=True)
    segments_dir.mkdir(parents=True, exist_ok=True)
    render_state_path = args.work_dir / "render_state.json"
    render_state = {"pdf_sha256": sha256(args.pdf), "dpi": args.dpi, "pages": pages}
    old_render_state = json.loads(render_state_path.read_text()) if render_state_path.exists() else None
    frames = rendered_frames(frames_dir)
    if old_render_state != render_state or len(frames) != pages:
        for frame in frames_dir.glob("page-*.png"):
            frame.unlink()
        subprocess.run(
            [pdftoppm, "-png", "-r", str(args.dpi), str(args.pdf), str(frames_dir / "page")],
            check=True,
        )
        render_state_path.write_text(json.dumps(render_state, indent=2) + "\n")
        frames = rendered_frames(frames_dir)
    if len(frames) != pages:
        raise SystemExit("Poppler rendered {} frames for a {}-page PDF".format(len(frames), pages))

    audio_files = []
    audio_durations = []
    for item in metadata:
        audio = Path(item["file"])
        if not audio.exists():
            raise SystemExit("missing audio for page {}: {}".format(item["page"], audio))
        audio_files.append(audio)
        audio_durations.append(wav_duration(audio))
    frame_counts = allocate_frame_counts(audio_durations, args.fps)

    narration = args.work_dir / "narration.wav"
    concatenate_wavs(audio_files, narration)

    segment_config = {"encoder": "ffmpeg-libx264-v3-video-only-exact-frames", "fps": args.fps}
    config_path = args.work_dir / "segment_config.json"
    old_config = json.loads(config_path.read_text()) if config_path.exists() else None
    force_segments = old_config != segment_config
    config_path.write_text(json.dumps(segment_config, indent=2) + "\n")

    rebuilt = 0
    segments = []
    segment_state_path = args.work_dir / "segment_state.json"
    old_segment_state = (
        json.loads(segment_state_path.read_text(encoding="utf-8"))
        if segment_state_path.exists()
        else {}
    )
    segment_state = {}
    for item, frame, frame_count in zip(metadata, frames, frame_counts):
        page = item["page"]
        segment = segments_dir / "segment_{:03d}.mp4".format(page)
        state = {
            "frame_sha256": sha256(frame),
            "frames": frame_count,
        }
        segment_state[str(page)] = state
        if force_segments or not segment.exists() or old_segment_state.get(str(page)) != state:
            subprocess.run(
                [ffmpeg, "-y", "-loglevel", "error", "-loop", "1", "-framerate", str(args.fps),
                 "-i", str(frame), "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
                 "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-tune", "stillimage",
                 "-pix_fmt", "yuv420p", "-an", "-frames:v", str(frame_count),
                 "-movflags", "+faststart", str(segment)],
                check=True,
            )
            rebuilt += 1
        segments.append(segment)
    write_text_if_changed(segment_state_path, json.dumps(segment_state, indent=2) + "\n")

    valid_segments = set(segments)
    for segment in segments_dir.glob("segment_*.mp4"):
        if segment not in valid_segments:
            segment.unlink()

    concat = args.work_dir / "concat.txt"
    concat_text = "".join("file '{}'\n".format(str(segment.resolve()).replace("'", "'\\''")) for segment in segments)
    write_text_if_changed(concat, concat_text)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary_output = args.output.with_suffix(".tmp.mp4")
    subprocess.run(
        [ffmpeg, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(concat),
         "-i", str(narration), "-map", "0:v:0", "-map", "1:a:0",
         "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
         "-r", str(args.fps), "-c:a", "aac", "-b:a", "192k", "-af", "apad", "-shortest",
         "-movflags", "+faststart", str(temporary_output)],
        check=True,
    )
    temporary_output.replace(args.output)
    print("video: {} segments rebuilt, {} reused; wrote {}".format(rebuilt, pages - rebuilt, args.output))


if __name__ == "__main__":
    main()
