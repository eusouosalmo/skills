#!/usr/bin/env python3
"""Flags the mechanical voice failures in a text written as eusouosalmo.

Usage: check-voice.py <file> --register spoken|written

Checks, one finding per line as "line N: rule: excerpt":
  - characters the voice never uses: em dash, en dash, unicode arrows,
    the ellipsis character, emoji;
  - the expressions in ../assets/ai-tells.tsv;
  - the register: "você"/"seu"/"sua" in spoken text (review each one: an
    impersonal "você" as subject is fine), "tu"/"teu"/"tua" and catchphrases
    in written text, filler words in spoken text.

Exit 0: nothing found. 1: findings printed. 2: usage or file error.
Needs: Python 3.8+, standard library only.
"""

import argparse
import re
import sys
from pathlib import Path

TELLS_FILE = Path(__file__).resolve().parent.parent / "assets" / "ai-tells.tsv"

# Characters the voice never uses, in any register (issue #6: no emoji, no dash).
CHARS = [
    ("em or en dash", re.compile("[\\u2013\\u2014]")),
    ("unicode arrow", re.compile("[\\u2190-\\u21FF\\u27F0-\\u27FF\\u2900-\\u297F\\u2B00-\\u2BFF]")),
    ("ellipsis character", re.compile("\\u2026")),
    # Pictographs, symbols, dingbats and flags.
    ("emoji", re.compile("[\\U0001F000-\\U0001FAFF\\u2600-\\u27BF]")),
]

WORD = r"(?<![\wÀ-ÿ])({})(?![\wÀ-ÿ])"

REGISTER = {
    # Spoken: the viewer is "tu". Filler appears on its own when recording,
    # so it never goes into the text.
    "spoken": [
        ("'você' in spoken register (fine only if impersonal)", re.compile(WORD.format("você|vocês|seu|sua|seus|suas"), re.I)),
        ("filler word", re.compile(WORD.format("basicamente|né"), re.I)),
    ],
    # Written: the reader is "você", with no catchphrase.
    "written": [
        ("'tu' in written register", re.compile(WORD.format("tu|teu|tua|teus|tuas"), re.I)),
        ("catchphrase in written register", re.compile(WORD.format("macho|bora lá|pô|ó"), re.I)),
    ],
}


def load_tells():
    tells = []
    try:
        lines = TELLS_FILE.read_text(encoding="utf-8").splitlines()
    except OSError as err:
        sys.exit(f"check-voice: cannot read {TELLS_FILE}: {err}")
    for n, line in enumerate(lines, 1):
        if not line.strip() or line.startswith("#"):
            continue
        pattern = line.split("\t")[0]
        try:
            tells.append(("AI tell", re.compile(pattern, re.I | re.M)))
        except re.error as err:
            sys.exit(f"check-voice: bad regex on line {n} of {TELLS_FILE}: {err}")
    return tells


def main():
    parser = argparse.ArgumentParser(description="Flag mechanical voice failures.")
    parser.add_argument("file")
    parser.add_argument("--register", required=True, choices=sorted(REGISTER))
    args = parser.parse_args()

    try:
        text = Path(args.file).read_text(encoding="utf-8")
    except OSError as err:
        print(f"check-voice: cannot read {args.file}: {err}", file=sys.stderr)
        return 2

    rules = CHARS + load_tells() + REGISTER[args.register]
    findings = []
    for n, line in enumerate(text.splitlines(), 1):
        for name, rx in rules:
            for m in rx.finditer(line):
                start = max(0, m.start() - 30)
                findings.append(f"line {n}: {name}: ...{line[start:m.end() + 30].strip()}...")

    print("\n".join(findings) if findings else "check-voice: no findings")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
