#!/usr/bin/env python3
"""Ensure abbrv displays a source link for every record that provides one."""
import argparse
import re
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "references.bib"


def close_brace(text, opening):
    level = 1
    for pos in range(opening + 1, len(text)):
        if text[pos] == "{":
            level += 1
        elif text[pos] == "}":
            level -= 1
            if level == 0:
                return pos
    raise ValueError("Unbalanced bibliography field")


def field(entry, name):
    match = re.search(r"\b" + name + r"\s*=\s*\{", entry)
    if not match:
        return None
    begin = match.end() - 1
    end = close_brace(entry, begin)
    return begin, end, entry[begin + 1:end]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    text = PATH.read_text()
    updates = []
    for match in re.finditer(r"@\w+\{([^,]+),", text):
        start = match.start()
        end = close_brace(text, text.index("{", start)) + 1
        entry = text[start:end]
        if r"\url{" in entry:
            continue
        url = field(entry, "url")
        doi = field(entry, "doi")
        if not url and not doi:
            continue
        link = url[2] if url else "https://doi.org/" + doi[2]
        note = field(entry, "note")
        if note:
            new = entry[:note[1]] + r" \url{" + link + "}" + entry[note[1]:]
        else:
            body = entry[:-1].rstrip()
            if not body.endswith(","):
                body += ","
            new = body + "\n note={\\url{" + link + "}}\n}"
        updates.append((start, end, new, match.group(1)))
    if updates and not args.write:
        raise SystemExit("Missing displayed links: " + ", ".join(v[3] for v in updates))
    for start, end, new, _ in reversed(updates):
        text = text[:start] + new + text[end:]
    if args.write:
        PATH.write_text(text)
    print(f"Bibliography link audit passed; {len(updates)} records updated.")


if __name__ == "__main__":
    main()
