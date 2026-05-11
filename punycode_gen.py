"""
Interactive homoglyph → Punycode (ACE) listing for ASCII letters a–z.

Uses Unicode UTS #39 confusables (confusables.txt) plus Latin letters that
fold to the same base letter when combining marks are stripped (NFD).

Data file: confusables.txt next to this script (Unicode Security Mechanisms,
see https://www.unicode.org/reports/tr39/ ).
"""

from __future__ import annotations
import argparse
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

_LINE_RE = re.compile(r"^([0-9A-Fa-f]+)\s*;\s*([0-9A-Fa-f]+)\s*;")


def _configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except Exception:
                pass


def _confusables_path() -> Path:
    return Path(__file__).resolve().with_name("confusables.txt")


def _load_adjacency(path: Path) -> dict[int, set[int]]:
    adj: dict[int, set[int]] = defaultdict(set)
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.startswith("#") or not line.strip():
                continue
            match = _LINE_RE.match(line)
            if not match:
                continue
            a = int(match.group(1), 16)
            b = int(match.group(2), 16)
            adj[a].add(b)
            adj[b].add(a)
    return adj


def _component(adj: dict[int, set[int]], seeds: list[int]) -> set[int]:
    seen: set[int] = set(seeds)
    stack = list(seeds)
    while stack:
        u = stack.pop()
        for v in adj.get(u, ()):
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return seen


def _strip_marks_casefold(ch: str) -> str:
    nfd = unicodedata.normalize("NFD", ch)
    base = "".join(c for c in nfd if unicodedata.category(c) != "Mn")
    return base.casefold()


def _latin_same_base(target: str) -> set[str]:
    t = target.casefold()
    out: set[str] = set()
    for cp in range(0x110000):
        ch = chr(cp)
        try:
            if _strip_marks_casefold(ch) == t:
                out.add(ch)
        except Exception:
            continue
    return out


def _ace_label(ch: str) -> str:
    try:
        return ch.encode("idna").decode("ascii")
    except UnicodeError:
        return "<not IDNA-encodable>"


def collect_variants(letter: str, adj: dict[int, set[int]]) -> list[str]:
    low = letter.lower()
    if len(low) != 1 or low not in "abcdefghijklmnopqrstuvwxyz":
        raise ValueError("expected a single English letter a–z")

    seeds = [ord(low), ord(low.upper())]
    codepoints = _component(adj, seeds)
    chars = {chr(cp) for cp in codepoints}
    chars |= _latin_same_base(low)

    filtered: list[str] = []
    for ch in chars:
        if len(ch) != 1:
            continue
        if not ch.isprintable():
            continue
        if unicodedata.category(ch) == "Cc":
            continue
        filtered.append(ch)

    filtered.sort(key=lambda c: (_ace_label(c), ord(c)))
    return filtered


def main() -> None:
    _configure_stdio()
    parser = argparse.ArgumentParser(
        description="List Unicode homoglyphs for a–z and their Punycode (ACE) labels."
    )
    parser.add_argument(
        "-l",
        "--letter",
        metavar="L",
        help="Letter a–z (non-interactive). If omitted, you are prompted when stdin is a TTY.",
    )
    args = parser.parse_args()

    if args.letter is not None:
        letter = args.letter.strip()
    elif sys.stdin.isatty():
        letter = input("Enter a letter (a-z): ").strip()
    else:
        letter = sys.stdin.read().strip()[:1]

    if not letter:
        parser.error("no letter provided")

    low = letter.strip().lower()
    if len(low) != 1 or low not in "abcdefghijklmnopqrstuvwxyz":
        parser.error("expected a single English letter a–z")

    path = _confusables_path()
    if not path.is_file():
        print(
            f"error: missing data file {path}\n"
            "Download confusables.txt from Unicode security data, e.g.\n"
            "https://www.unicode.org/Public/security/latest/confusables.txt",
            file=sys.stderr,
        )
        raise SystemExit(2)

    adj = _load_adjacency(path)
    variants = collect_variants(low, adj)

    shown = low
    print(f"\n🔎 Punycode variants for letter: {shown!r}\n")
    try:
        for ch in variants:
            print(f"{ch} -> {_ace_label(ch)}")
    except BrokenPipeError:
        try:
            sys.stdout.close()
        except Exception:
            pass
        raise SystemExit(0) from None


if __name__ == "__main__":
    main()
