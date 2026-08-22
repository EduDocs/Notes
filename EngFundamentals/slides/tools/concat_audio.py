#!/usr/bin/env python3
"""Concatenate timed WAV files listed in narration metadata."""

import argparse
import json
import shutil
import subprocess
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("metadata", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise SystemExit("ffmpeg is required")
    items = json.loads(args.metadata.read_text(encoding="utf-8"))
    files = [Path(item["file"]) for item in items]
    if not files or not all(path.exists() for path in files):
        raise SystemExit("metadata contains missing audio files")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_name(args.output.stem + ".tmp.wav")
    command = [ffmpeg, "-y", "-loglevel", "error"]
    for path in files:
        command.extend(["-i", str(path)])
    inputs = "".join("[{}:a]".format(index) for index in range(len(files)))
    command.extend([
        "-filter_complex", inputs + "concat=n={}:v=0:a=1[out]".format(len(files)),
        "-map", "[out]", "-c:a", "pcm_s16le", str(temporary),
    ])
    subprocess.run(command, check=True)
    temporary.replace(args.output)
    print("wrote pronunciation reel to {}".format(args.output))


if __name__ == "__main__":
    main()
