#!/usr/bin/env python3
"""Convert narration Markdown into structured, page-synchronized JSONL beats."""

import argparse
import json
import re
from pathlib import Path


HEADING_RE = re.compile(r"^## Page (\d+):\s*(.+?)\s*$", re.M)
OVERLAY_RE = re.compile(r"^(.*?)\s+\(overlay\s+(\d+)\s+of\s+(\d+)\)$", re.I)
PAUSE_RE = re.compile(
    r"\[\[pause\s+([0-9]+(?:\.[0-9]+)?)\s*s?\s*\]\]",
    re.I,
)
SEED_RE = re.compile(r"\[\[seed\s+([0-9]+)\s*\]\]", re.I)
FIELD_RE = re.compile(r"^([A-Za-z][A-Za-z-]*):\s*(.*?)\s*$", re.M)
VARIABLE_DEF_RE = re.compile(
    r"\\providecommand\s*\{\\([A-Za-z][A-Za-z0-9]*)\}\s*\{([^{}]*)\}"
)
VARIABLE_TOKEN_RE = re.compile(r"\{\{\s*([A-Za-z][A-Za-z0-9]*)\s*\}\}")


def write_if_changed(path: Path, text: str) -> None:
    if path.exists() and path.read_text(encoding="utf-8") == text:
        path.touch()
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def optional_seconds(value: str, page: int, field: str):
    value = value.strip().lower()
    if not value or value == "auto":
        return None
    if value.endswith("s"):
        value = value[:-1].strip()
    try:
        seconds = float(value)
    except ValueError:
        raise SystemExit("page {} has invalid {} value: {}".format(page, field, value))
    if seconds < 0:
        raise SystemExit("page {} has negative {} value".format(page, field))
    return seconds


def load_variables(path) -> dict:
    if path is None:
        return {}
    source = path.read_text(encoding="utf-8")
    variables = {}
    for name, value in VARIABLE_DEF_RE.findall(source):
        value = value.replace(r"\xspace", "").replace(r"\&", "&").replace("~", " ")
        variables[name] = " ".join(value.split())
    if not variables:
        raise SystemExit("no \\providecommand variables found in {}".format(path))
    return variables


def expand_variables(text: str, variables: dict, page: int) -> str:
    def replacement(match):
        name = match.group(1)
        if name not in variables:
            raise SystemExit("page {} uses unknown narration variable {{{{{}}}}}".format(page, name))
        return variables[name]

    expanded = VARIABLE_TOKEN_RE.sub(replacement, text)
    if "{{" in expanded or "}}" in expanded:
        raise SystemExit("page {} contains a malformed narration variable".format(page))
    return expanded


def narration_chunks(narration: str, page: int) -> list:
    unparsed = PAUSE_RE.sub("", narration)
    if "[[pause" in unparsed.lower():
        raise SystemExit("page {} contains a malformed pause marker".format(page))

    chunks = []
    cursor = 0
    for match in PAUSE_RE.finditer(narration):
        text = " ".join(narration[cursor:match.start()].split())
        if not text:
            raise SystemExit("page {} has a pause marker without preceding speech".format(page))
        chunks.append({"text": text, "pause_after_seconds": float(match.group(1))})
        cursor = match.end()
    remainder = " ".join(narration[cursor:].split())
    if remainder:
        chunks.append({"text": remainder, "pause_after_seconds": 0.0})
    if not chunks:
        raise SystemExit("page {} narration is empty".format(page))
    return chunks


def narration_seed(narration: str, page: int) -> tuple:
    matches = list(SEED_RE.finditer(narration))
    unparsed = SEED_RE.sub("", narration)
    if "[[seed" in unparsed.lower():
        raise SystemExit("page {} contains a malformed seed marker".format(page))
    if len(matches) > 1:
        raise SystemExit("page {} contains more than one seed marker".format(page))
    if not matches:
        return narration, None

    match = matches[0]
    if narration[:match.start()].strip():
        raise SystemExit(
            "page {} seed marker must appear before the narration text".format(page)
        )
    seed = int(match.group(1))
    if seed > 2**63 - 1:
        raise SystemExit("page {} seed is larger than 2^63-1".format(page))
    cleaned = " ".join((narration[:match.start()] + narration[match.end():]).split())
    return cleaned, seed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--variables", type=Path)
    args = parser.parse_args()

    source = args.source.read_text(encoding="utf-8")
    variables = load_variables(args.variables)
    headings = list(HEADING_RE.finditer(source))
    if not headings:
        raise SystemExit("no '## Page NNN:' sections found")

    beats = []
    frame_index = 0
    previous = None
    for index, heading in enumerate(headings):
        page = int(heading.group(1))
        expected = index + 1
        if page != expected:
            raise SystemExit("expected page {}, found page {}".format(expected, page))
        display_title = heading.group(2)
        overlay_match = OVERLAY_RE.match(display_title)
        if overlay_match:
            frame = overlay_match.group(1).strip()
            overlay = int(overlay_match.group(2))
            overlay_count = int(overlay_match.group(3))
        else:
            frame = display_title.strip()
            overlay = 1
            overlay_count = 1

        if overlay == 1:
            frame_index += 1
        else:
            if previous is None or previous[0] != frame or overlay != previous[1] + 1:
                raise SystemExit("page {} has a noncontiguous overlay sequence".format(page))
            if overlay_count != previous[2]:
                raise SystemExit("page {} changes the overlay count within a frame".format(page))
        if not 1 <= overlay <= overlay_count:
            raise SystemExit("page {} has invalid overlay metadata".format(page))
        previous = (frame, overlay, overlay_count)

        stop = headings[index + 1].start() if index + 1 < len(headings) else len(source)
        section = source[heading.end():stop]
        marker = re.search(r"^Narration:\s*$", section, re.M)
        if not marker:
            raise SystemExit("page {} has no Narration: block".format(page))
        field_text = section[:marker.start()]
        fields = {name.lower(): value for name, value in FIELD_RE.findall(field_text)}
        unknown = sorted(set(fields) - {"pause-after", "lead-in", "instruction"})
        if unknown:
            raise SystemExit("page {} has unknown field(s): {}".format(page, ", ".join(unknown)))

        narration = section[marker.end():].strip()
        narration = " ".join(narration.split())
        narration = expand_variables(narration, variables, page)
        if not narration or "[Write narration" in narration or "[Read the" in narration:
            raise SystemExit("page {} narration still contains a draft placeholder".format(page))
        narration, seed = narration_seed(narration, page)
        chunks = narration_chunks(narration, page)
        beats.append({
            "page": page,
            "frame_index": frame_index,
            "frame": frame,
            "overlay": overlay,
            "overlay_count": overlay_count,
            "starts_new_slide": overlay == 1,
            "ends_slide": overlay == overlay_count,
            "display_title": display_title,
            "slide": frame,
            "text": narration,
            "chunks": chunks,
            "pause_after_seconds": optional_seconds(fields.get("pause-after", "auto"), page, "Pause-after"),
            "lead_in_seconds": optional_seconds(fields.get("lead-in", "auto"), page, "Lead-in"),
            "instruction": fields.get("instruction") or None,
            "seed": seed,
        })

    payload = "".join(json.dumps(beat, ensure_ascii=False) + "\n" for beat in beats)
    write_if_changed(args.output, payload)
    print("wrote {} narration beats across {} frames to {}".format(len(beats), frame_index, args.output))


if __name__ == "__main__":
    main()
