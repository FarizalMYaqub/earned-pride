#!/usr/bin/env python3
"""One quiet line of earned pride for make.fun.

The entry is a single sentence about Jun, eight years old, who
has stuttered through every school assembly for a year and now
reads the morning announcements to the whole school. The pride
is never named: it sits in the last detail, that he never once
looks down at his shoes. This program checks the sentence
against the house gate (UTF-8 text, one line, 1 to 240
characters) and writes it to /output/entry.txt, where the
house judge reads it two at a time against the other entries.
"""

import sys
from pathlib import Path

GATE_MIN_CHARS = 1
GATE_MAX_CHARS = 240
OUTPUT_FILE = Path("/output/entry.txt")

LINE = (
    "After a year of stuttering through every assembly, "
    "eight-year-old Jun read the morning announcements to the "
    "whole school without once looking down at his shoes."
)


def gate_check(line):
    """Refuse any line the house gate would refuse.

    The gate only takes UTF-8 text of 1 to 240 characters that
    is not only whitespace, on a single line. Anything outside
    that never reaches the judge, so fail here instead.
    """
    stripped = line.strip()
    if len(stripped) < GATE_MIN_CHARS:
        raise SystemExit("entry line must not be empty")
    if len(line) > GATE_MAX_CHARS:
        raise SystemExit(
            f"entry line is {len(line)} characters, "
            f"gate allows at most {GATE_MAX_CHARS}"
        )
    if "\n" in stripped or "\r" in stripped:
        raise SystemExit("entry line must stay on one line")
    if stripped != line:
        raise SystemExit("entry line must not lead or trail with space")
    try:
        stripped.encode("utf-8")
    except UnicodeEncodeError:
        raise SystemExit("entry line must be UTF-8 text")
    return stripped


def write_entry(line):
    """Write the gated line to /output/entry.txt as UTF-8."""
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(gate_check(line), encoding="utf-8")


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if argv:
        raise SystemExit("usage: python3 main.py (no arguments)")
    write_entry(LINE)
    print(f"wrote {len(LINE)} characters to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
