#!/usr/bin/env python3
"""Flags the mechanical caption failures for one platform.

Usage: check-caption.py <caption-file> --platform instagram|tiktok|shorts|linkedin
                        [--script <script-file>]

Checks, one finding per line:
  - a URL where caption links are not clickable (Instagram, TikTok, Shorts);
  - more hashtags than the platform allows or shows (Instagram 5, YouTube 3
    shown above the title, TikTok and LinkedIn 5 as a ceiling for "few");
  - engagement bait the platform demotes: asking for a specific word, a tag,
    a share or a like ("comenta EU QUERO", "marca alguém", "compartilha se");
  - the first line over the length seen before "mais" (a guide figure, so a
    warning, not a rule);
  - with --script, every caption sentence that repeats a spoken line of the
    script almost word for word.

Exit 0: nothing found. 1: findings printed. 2: usage or file error.
Needs: Python 3.8+, standard library only.
"""

import argparse
import re
import sys
from pathlib import Path

# Links in captions are not clickable on these platforms (sources.md, Links).
NO_LINKS = {"instagram", "tiktok", "shorts"}
MAX_HASHTAGS = {"instagram": 5, "tiktok": 5, "shorts": 3, "linkedin": 5}
# Characters visible before "mais"/"ver mais", per third-party guides.
FIRST_LINE = {"instagram": 125, "tiktok": 100, "shorts": 100, "linkedin": 140}

URL = re.compile(r"https?://|www\.|\b[\w-]+\.(com|br|io|dev|net|org|ly)(/|\b)", re.I)
HASHTAG = re.compile(r"(?<![\w&])#[\wÀ-ÿ]+")
BAIT = re.compile(
    r"\b(comenta|comente|escreve|escreva|digita|digite)\b[^.?!\n]{0,40}"
    r"(\"[^\"]+\"|'[^']+'|\b[A-ZÁÉÍÓÚÂÊÔÃÕÇ]{2,}\b|emoji|aqui embaixo)"
    r"|\b(marca|marque|marquem)\b[^.?!\n]{0,20}\b(algu[eé]m|amigo|amiga|quem)\b"
    r"|\b(compartilha|compartilhe|curte|curta|salva|salve)\b\s+(se|isso se|esse post se)\b",
    re.I,
)
# How a fact was checked serves the author, not the reader (checklist.md).
CHECK_NOTE = re.compile(
    r"\b(se[cç][aã]o|p[aá]gina|p\.)\s*\d|\bconferid[oa]\b|\b(t[aá]|est[aá]) na (doc|documenta[cç][aã]o)\b",
    re.I,
)
WORD = re.compile(r"[\wÀ-ÿ@>-]+")


def words(text):
    return [w.lower() for w in WORD.findall(text)]


def sentences(text):
    parts = re.split(r"(?<=[.?!])\s+|\n+", text)
    return [p.strip() for p in parts if len(words(p)) >= 5]


def spoken_lines(script):
    """Spoken lines of a script: the teleprompter part when there is one."""
    m = re.search(r"^## Teleprompter\s*$(.*?)(^## |\Z)", script, re.M | re.S)
    body = m.group(1) if m else script
    body = re.sub(r"^Duração estimada:.*$", "", body, flags=re.M)
    return sentences(body)


def overlap(a, b):
    """Share of a's words, in order, found as a run of 4+ words in b.

    Four words in a row is a copied phrase, not a shared term; a sentence
    with 60% or more of its words in such runs reads as the same line.
    """
    wa, wb = words(a), words(b)
    if len(wa) < 5:
        return 0.0
    grams = {tuple(wb[i:i + 4]) for i in range(len(wb) - 3)}
    hit = [False] * len(wa)
    for i in range(len(wa) - 3):
        if tuple(wa[i:i + 4]) in grams:
            for j in range(i, i + 4):
                hit[j] = True
    return sum(hit) / len(wa)


def main():
    parser = argparse.ArgumentParser(description="Flag mechanical caption failures.")
    parser.add_argument("file")
    parser.add_argument("--platform", required=True, choices=sorted(MAX_HASHTAGS))
    parser.add_argument("--script")
    args = parser.parse_args()

    try:
        text = Path(args.file).read_text(encoding="utf-8")
        script = Path(args.script).read_text(encoding="utf-8") if args.script else ""
    except OSError as err:
        print(f"check-caption: cannot read: {err}", file=sys.stderr)
        return 2

    findings = []
    lines = text.splitlines()
    first = next((l.strip() for l in lines if l.strip()), "")

    if args.platform in NO_LINKS:
        for n, line in enumerate(lines, 1):
            if URL.search(line):
                findings.append(f"line {n}: URL not clickable on {args.platform}; point to the bio or the platform's link field: {line.strip()}")

    tags = HASHTAG.findall(text)
    if len(tags) > MAX_HASHTAGS[args.platform]:
        findings.append(f"{len(tags)} hashtags; {args.platform} takes at most {MAX_HASHTAGS[args.platform]}: {' '.join(tags)}")

    for n, line in enumerate(lines, 1):
        m = BAIT.search(line)
        if m:
            findings.append(f"line {n}: engagement bait ('{m.group(0).strip()}'); ask an open question or make a request with a reason")

    for n, line in enumerate(lines, 1):
        if line.lstrip().lower().startswith("fonte:"):
            continue
        m = CHECK_NOTE.search(line)
        if m:
            findings.append(f"line {n}: check note ('{m.group(0)}'); state the fact and leave where it was checked to the author's notes")

    if len(first) > FIRST_LINE[args.platform]:
        findings.append(f"warning: first line has {len(first)} characters; about {FIRST_LINE[args.platform]} show before 'mais' on {args.platform}")

    if script:
        spoken = spoken_lines(script)
        for s in sentences(text):
            best = max((overlap(s, sp) for sp in spoken), default=0.0)
            if best >= 0.6:
                findings.append(f"repeats the script ({best:.0%} of its words): {s}")

    print("\n".join(findings) if findings else "check-caption: no findings")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
