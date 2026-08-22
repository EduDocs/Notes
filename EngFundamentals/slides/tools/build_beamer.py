#!/usr/bin/env python3
"""Build one reproducible Beamer PDF variant without modifying the source file."""

import argparse
import re
import shutil
import subprocess
from pathlib import Path


CLASS_RE = re.compile(r"\\documentclass\[([^]]*)\]\{beamer\}")


def transformed_source(source: str, mode: str) -> str:
    match = CLASS_RE.search(source)
    if not match:
        raise ValueError("expected a Beamer \\documentclass with options")

    options = [part.strip() for part in match.group(1).split(",") if part.strip()]
    additions = {
        "slides": ["hide notes"],
        "video": ["hide notes"],
        "notes": ["notes"],
        "handout": ["handout"],
        "review": ["notes"],
    }[mode]
    for option in additions:
        if option not in options:
            options.append(option)

    replacement = "\\documentclass[{}]{{beamer}}".format(",".join(options))
    result = CLASS_RE.sub(lambda _: replacement, source, count=1)
    if mode == "video":
        # This PDF is rasterized by render_video.py. Sources can use this
        # marker to hide PDF-only link decorations in rendered video frames.
        result = "\\def\\videoexport{}\n" + result
    if mode == "review":
        result = "\\def\\enablegptcomments{}\n" + result
        review_template = r"""
% Use the full notes panel for editorial review; the standard template reserves
% substantial space for a miniature slide and clips long GPT comments.
\setbeamertemplate{note page}{%
  \begingroup
  \let\normalsize\relax
  \let\small\relax
  \let\footnotesize\relax
  \let\scriptsize\relax
  \fontsize{4.5}{5.2}\selectfont
  \insertnote
  \endgroup
}
"""
        result = result.replace("\\begin{document}", review_template + "\n\\begin{document}", 1)
    return result


def write_if_changed(path: Path, text: str) -> None:
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--mode", choices=("slides", "video", "notes", "handout", "review"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    source = args.source.resolve()
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    generated_tex = output.with_suffix(".tex")
    write_if_changed(generated_tex, transformed_source(source.read_text(encoding="utf-8"), args.mode))

    latexmk = shutil.which("latexmk")
    if not latexmk:
        raise SystemExit("latexmk was not found on PATH")

    command = [
        latexmk,
        "-pdf",
        "-silent",
        "-shell-escape",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
        "-outdir=" + str(output.parent),
        str(generated_tex),
    ]
    subprocess.run(command, cwd=source.parent, check=True)

    built_pdf = output.parent / (generated_tex.stem + ".pdf")
    if built_pdf != output:
        shutil.copy2(built_pdf, output)


if __name__ == "__main__":
    main()
