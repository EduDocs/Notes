#!/usr/bin/env python3
"""Create short structured beats for auditioning every pronunciation entry."""

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("lexicon", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    data = json.loads(args.lexicon.read_text(encoding="utf-8"))
    entries = data.get("entries", [])
    if not entries:
        raise SystemExit("pronunciation lexicon has no entries")
    beats = []
    for index, entry in enumerate(entries, start=1):
        term = entry["term"]
        text = entry.get("test_text") or "The term is {}.".format(term)
        beats.append({
            "page": index,
            "frame_index": index,
            "frame": "Pronunciation: " + term,
            "overlay": 1,
            "overlay_count": 1,
            "starts_new_slide": True,
            "ends_slide": True,
            "display_title": "Pronunciation: " + term,
            "slide": "Pronunciation: " + term,
            "text": text,
            "chunks": [{"text": text, "pause_after_seconds": 0.0}],
            "pause_after_seconds": 0.6,
            "lead_in_seconds": 0.15,
            "instruction": None,
        })
    payload = "".join(json.dumps(beat, ensure_ascii=False) + "\n" for beat in beats)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(payload, encoding="utf-8")
    print("wrote {} pronunciation tests to {}".format(len(beats), args.output))


if __name__ == "__main__":
    main()
