#!/usr/bin/env python3
"""Generate Academic Pages publication Markdown files from BibTeX.

The BibTeX file is the source of truth. Run from the repository root:

    uv run python scripts/generate_publications.py
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

GENERATED_MARKERS = {"generated_from_bib: true", "generated_from_bib: \"true\""}
MONTHS = {
    "jan": 1,
    "january": 1,
    "feb": 2,
    "february": 2,
    "mar": 3,
    "march": 3,
    "apr": 4,
    "april": 4,
    "may": 5,
    "jun": 6,
    "june": 6,
    "jul": 7,
    "july": 7,
    "aug": 8,
    "august": 8,
    "sep": 9,
    "sept": 9,
    "september": 9,
    "oct": 10,
    "october": 10,
    "nov": 11,
    "november": 11,
    "dec": 12,
    "december": 12,
}


@dataclass(frozen=True)
class BibEntry:
    entry_type: str
    key: str
    fields: dict[str, str]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bib", default="bibliography/papers.bib", help="Input BibTeX file")
    parser.add_argument("--out", default="_publications", help="Output collection directory")
    args = parser.parse_args()

    bib_path = Path(args.bib)
    out_dir = Path(args.out)
    entries = parse_bibtex(bib_path.read_text(encoding="utf-8"))

    out_dir.mkdir(parents=True, exist_ok=True)
    generated_paths = []
    for entry in entries:
        path = output_path(out_dir, entry)
        path.write_text(render_publication(entry), encoding="utf-8")
        generated_paths.append(path)

    remove_stale_generated_files(out_dir, set(generated_paths))
    print(f"Generated {len(generated_paths)} publication file(s) from {bib_path}")


def parse_bibtex(text: str) -> list[BibEntry]:
    entries: list[BibEntry] = []
    index = 0

    while True:
        at = text.find("@", index)
        if at == -1:
            return entries

        match = re.match(r"@\s*([A-Za-z]+)\s*\{", text[at:])
        if not match:
            index = at + 1
            continue

        entry_type = match.group(1).lower()
        body_start = at + match.end()
        body_end = find_matching_brace(text, body_start - 1)
        body = text[body_start:body_end]
        index = body_end + 1

        if entry_type in {"comment", "preamble", "string"}:
            continue

        key, fields_text = split_key_and_fields(body)
        entries.append(BibEntry(entry_type=entry_type, key=key, fields=parse_fields(fields_text)))


def find_matching_brace(text: str, open_brace: int) -> int:
    depth = 0
    quote_open = False
    escaped = False

    for pos in range(open_brace, len(text)):
        char = text[pos]
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == '"':
            quote_open = not quote_open
            continue
        if quote_open:
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return pos

    raise ValueError("Unclosed BibTeX entry")


def split_key_and_fields(body: str) -> tuple[str, str]:
    depth = 0
    quote_open = False
    for index, char in enumerate(body):
        if char == '"':
            quote_open = not quote_open
        elif not quote_open and char == "{":
            depth += 1
        elif not quote_open and char == "}":
            depth -= 1
        elif not quote_open and depth == 0 and char == ",":
            return body[:index].strip(), body[index + 1 :]
    raise ValueError(f"BibTeX entry is missing fields: {body[:80]}")


def parse_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    index = 0

    while index < len(text):
        match = re.search(r"([A-Za-z][A-Za-z0-9_-]*)\s*=\s*", text[index:])
        if not match:
            break

        name = match.group(1).lower()
        value_start = index + match.end()
        value, value_end = parse_value(text, value_start)
        fields[name] = normalize_text(value)
        index = value_end

    return fields


def parse_value(text: str, start: int) -> tuple[str, int]:
    while start < len(text) and text[start].isspace():
        start += 1

    if start >= len(text):
        return "", start

    if text[start] == "{":
        end = find_matching_brace(text, start)
        return text[start + 1 : end], skip_separator(text, end + 1)

    if text[start] == '"':
        escaped = False
        chars = []
        for index in range(start + 1, len(text)):
            char = text[index]
            if escaped:
                chars.append(char)
                escaped = False
                continue
            if char == "\\":
                escaped = True
                chars.append(char)
                continue
            if char == '"':
                return "".join(chars), skip_separator(text, index + 1)
            chars.append(char)
        raise ValueError("Unclosed quoted BibTeX value")

    match = re.match(r"([^,\n}]+)", text[start:])
    if not match:
        return "", start + 1
    return match.group(1).strip(), skip_separator(text, start + match.end())


def skip_separator(text: str, index: int) -> int:
    while index < len(text) and text[index] in {" ", "\t", "\r", "\n", ","}:
        index += 1
    return index


def normalize_text(value: str) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    replacements = {
        r"\&": "&",
        r"\_": "_",
        r"\%": "%",
        "{": "",
        "}": "",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    return value


def output_path(out_dir: Path, entry: BibEntry) -> Path:
    year, month, day = publication_date(entry)
    slug = slugify(entry.key or entry.fields.get("title", "publication"))
    return out_dir / f"{year:04d}-{month:02d}-{day:02d}-{slug}.md"


def render_publication(entry: BibEntry) -> str:
    fields = entry.fields
    title = require_field(entry, "title")
    year, month, day = publication_date(entry)
    date = f"{year:04d}-{month:02d}-{day:02d}"
    venue = venue_for(entry)
    category = fields.get("category") or category_for(entry.entry_type)
    permalink = f"/publication/{date}-{slugify(entry.key)}"
    paper_url = fields.get("paperurl") or fields.get("pdf") or fields.get("url") or doi_url(fields.get("doi"))
    slides_url = fields.get("slidesurl") or fields.get("slides")
    excerpt = fields.get("abstract") or fields.get("note") or ""
    citation = fields.get("citation") or build_citation(entry, title, venue, year)

    front_matter = {
        "title": title,
        "collection": "publications",
        "category": category,
        "permalink": permalink,
        "excerpt": excerpt,
        "date": date,
        "venue": venue,
        "paperurl": paper_url,
        "slidesurl": slides_url,
        "citation": citation,
        "bibtex_key": entry.key,
        "generated_from_bib": "true",
    }

    lines = ["---"]
    for key, value in front_matter.items():
        if value:
            if key == "generated_from_bib":
                lines.append(f"{key}: true")
            else:
                lines.append(f"{key}: {yaml_quote(value)}")
    lines.extend(
        [
            "---",
            "",
            "This publication page is generated from `bibliography/papers.bib`.",
            "Edit the BibTeX entry and run `uv run python scripts/generate_publications.py` to update it.",
            "",
        ]
    )
    return "\n".join(lines)


def require_field(entry: BibEntry, field: str) -> str:
    value = entry.fields.get(field)
    if not value:
        raise ValueError(f"BibTeX entry '{entry.key}' is missing required field '{field}'")
    return value


def publication_date(entry: BibEntry) -> tuple[int, int, int]:
    year = int(require_field(entry, "year"))
    month = parse_month(entry.fields.get("month", "1"))
    day = int(entry.fields.get("day", "1"))
    return year, month, day


def parse_month(value: str) -> int:
    normalized = value.strip().lower().strip("{}\"")
    if normalized.isdigit():
        month = int(normalized)
    else:
        month = MONTHS.get(normalized)
    if not month or month < 1 or month > 12:
        raise ValueError(f"Invalid BibTeX month: {value}")
    return month


def venue_for(entry: BibEntry) -> str:
    fields = entry.fields
    return fields.get("venue") or fields.get("booktitle") or fields.get("journal") or fields.get("publisher") or ""


def category_for(entry_type: str) -> str:
    if entry_type in {"book", "inbook", "incollection"}:
        return "books"
    if entry_type in {"article", "misc", "unpublished"}:
        return "manuscripts"
    return "conferences"


def doi_url(doi: str | None) -> str:
    if not doi:
        return ""
    if doi.startswith("http://") or doi.startswith("https://"):
        return doi
    return f"https://doi.org/{doi}"


def build_citation(entry: BibEntry, title: str, venue: str, year: int) -> str:
    authors = entry.fields.get("author", "")
    author_text = format_authors(authors) if authors else ""
    venue_text = f" <i>{venue}</i>." if venue else ""
    prefix = f"{author_text} ({year})." if author_text else f"({year})."
    return f"{prefix} &quot;{title}.&quot;{venue_text}"


def format_authors(authors: str) -> str:
    return ", ".join(part.strip() for part in re.split(r"\s+and\s+", authors) if part.strip())


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "publication"


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def remove_stale_generated_files(out_dir: Path, current_paths: set[Path]) -> None:
    for path in out_dir.glob("*.md"):
        if path in current_paths:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if any(marker in text for marker in GENERATED_MARKERS):
            path.unlink()


if __name__ == "__main__":
    main()
