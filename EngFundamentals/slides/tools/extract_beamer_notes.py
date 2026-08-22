#!/usr/bin/env python3
"""Extract Beamer speaker notes into a page-synchronized Markdown draft."""

import argparse
import re
from pathlib import Path


def balanced_argument(text: str, command_start: int) -> tuple:
    brace = text.find("{", command_start)
    if brace < 0:
        raise ValueError("command has no opening brace")
    depth = 0
    for index in range(brace, len(text)):
        if text[index] == "{" and (index == 0 or text[index - 1] != "\\"):
            depth += 1
        elif text[index] == "}" and (index == 0 or text[index - 1] != "\\"):
            depth -= 1
            if depth == 0:
                return text[brace + 1:index], index + 1
    raise ValueError("unbalanced braces")


def remove_commands(text: str, command: str) -> str:
    needle = "\\" + command
    while True:
        start = text.find(needle)
        if start < 0:
            return text
        _, end = balanced_argument(text, start)
        text = text[:start] + text[end:]


def clean_note(text: str) -> str:
    text = re.sub(r"\\\\\s*\[[^]]*\]", " ", text)
    text = re.sub(r"\\vspace\b\{[^{}]*\}", " ", text)
    text = re.sub(r"\\setlength\s*\\[A-Za-z@]+\s*\{[^{}]*\}", " ", text)
    text = re.sub(r"\\setlength\b(?:\{[^{}]*\}){2}", " ", text)
    text = re.sub(r"\\(scriptsize|footnotesize|color\{[^{}]*\})", " ", text)
    return " ".join(text.split())


def strip_latex_comments(text: str) -> str:
    lines = []
    for line in text.splitlines():
        for index, character in enumerate(line):
            if character != "%":
                continue
            backslashes = 0
            cursor = index - 1
            while cursor >= 0 and line[cursor] == "\\":
                backslashes += 1
                cursor -= 1
            if backslashes % 2 == 0:
                line = line[:index]
                break
        lines.append(line)
    return "\n".join(lines)


def remove_if_false_blocks(text: str) -> str:
    """Remove simple inactive ``\\iffalse ... \\fi`` source blocks."""
    return re.sub(r"\\iffalse\b.*?\\fi\b", "", text, flags=re.S)


def remove_balanced_commands(text: str, command: str) -> str:
    needle = "\\" + command
    while True:
        start = text.find(needle)
        if start < 0:
            return text
        _, end = balanced_argument(text, start)
        text = text[:start] + text[end:]


def overlay_count(frame: str) -> int:
    """Infer rendered overlays from frame and reveal specifications."""
    visual = remove_balanced_commands(frame, "note")
    visual = remove_balanced_commands(visual, "gpt")
    maximum = 1
    for specification in re.findall(r"<([^<>]+)>", visual):
        for number in re.findall(r"\d+", specification):
            maximum = max(maximum, int(number))
    return maximum


def frame_title(frame: str) -> str:
    title_match = re.search(r"\\frametitle\{([^{}]*)\}", frame)
    if title_match:
        return clean_note(title_match.group(1))
    argument_match = re.match(r"\s*(?:\[[^]]*\])?\s*\{([^{}]*)\}", frame)
    if argument_match:
        return clean_note(argument_match.group(1))
    return "Title"


def note_items(note: str) -> list:
    note = remove_commands(note, "gpt")
    start = note.find("\\begin{enumerate}")
    end = note.rfind("\\end{enumerate}")
    body = note[start:end] if start >= 0 and end >= 0 else note
    # The boundary is essential: ``\\itemsep`` is formatting, not a note item.
    matches = list(re.finditer(r"\\item(?![A-Za-z@])(?:\s*\[[^]]*\])?\s*", body))
    if not matches:
        cleaned = clean_note(body)
        return [cleaned] if cleaned else []
    items = []
    for index, match in enumerate(matches):
        stop = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        items.append(clean_note(body[match.end():stop]))
    return items


def narration_draft(note: str) -> str:
    pattern = re.compile(
        r"(?i)\bread(?:\s+(bullets?|[0-9]+(?:-[0-9]+)?))?\s*\.{0,3}"
    )

    def replace(match: re.Match) -> str:
        qualifier = match.group(1)
        if qualifier and qualifier[0].isdigit():
            return "[READ DISPLAYED ITEM(S) {} EXACTLY.]".format(qualifier)
        if qualifier:
            return "[READ THE MATCHED VISIBLE SLIDE BULLETS EXACTLY.]"
        return "[READ THE MATCHED NEWLY REVEALED SLIDE TEXT EXACTLY.]"

    return pattern.sub(replace, note).strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    text = strip_latex_comments(args.source.read_text(encoding="utf-8"))
    text = remove_if_false_blocks(text)
    frames = re.findall(r"\\begin\{frame\}(.*?)\\end\{frame\}", text, flags=re.S)
    output = [
        "# Extracted narration draft for " + args.source.name,
        "",
        "> Generated from Beamer `\\note` blocks. `\\gpt` comments are excluded. "
        "Replace each bracketed `Read` instruction with the matched displayed text exactly. "
        "Do not paraphrase, summarize, or add narration; preserve all note text that follows it.",
        "",
    ]
    page = 1
    for frame_number, frame in enumerate(frames, start=1):
        title = frame_title(frame)
        overlays = overlay_count(frame)
        note_start = frame.find("\\note{")
        items = []
        if note_start >= 0:
            note, _ = balanced_argument(frame, note_start)
            items = note_items(note)

        if len(items) != overlays:
            output.extend([
                "> **Synchronization warning:** frame `{}` has {} rendered overlay(s) "
                "but {} speaker-note cue(s). Map the cues explicitly; do not discard or "
                "invent narration.".format(title, overlays, len(items)),
                "",
            ])

        for overlay in range(1, overlays + 1):
            item = items[overlay - 1] if overlay <= len(items) else ""
            output.extend([
                "## Page {:03d}: {} (overlay {}/{})".format(page, title, overlay, overlays),
                "",
                "Source note:",
                item or "[No speaker note found for this overlay.]",
                "",
                "Narration:",
                narration_draft(item) or "[Write narration for this overlay.]",
                "",
            ])
            page += 1

        for cue_number, item in enumerate(items[overlays:], start=overlays + 1):
            output.extend([
                "### Additional speaker-note cue {} after the final rendered overlay".format(cue_number),
                "",
                "Source note:",
                item,
                "",
                "Narration:",
                narration_draft(item),
                "",
            ])

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(output), encoding="utf-8")
    print("wrote {} pages to {}".format(page - 1, args.output))


if __name__ == "__main__":
    main()
