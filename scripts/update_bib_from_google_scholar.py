#!/usr/bin/env python3
"""Update bibliography/papers.bib from a public Google Scholar profile.

Google Scholar does not provide a stable official BibTeX API for full profiles.
This script uses the public profile table as a pragmatic maintenance tool. Run
it sparingly when you intentionally want to refresh your local BibTeX source.

Usage:

    uv run python scripts/update_bib_from_google_scholar.py --user n3xCLnMAAAAJ
"""

from __future__ import annotations

import argparse
import html
import re
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path

SCHOLAR_BASE = "https://scholar.google.com/citations"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 " "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"


@dataclass(frozen=True)
class ScholarArticle:
    citation_id: str
    title: str
    fields: dict[str, str]


class ScholarProfileParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.citation_ids: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        attr_map = dict(attrs)
        href = attr_map.get("href", "") or ""
        if "view_op=view_citation" not in href or "citation_for_view=" not in href:
            return
        query = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
        values = query.get("citation_for_view")
        if values and values[0] not in self.citation_ids:
            self.citation_ids.append(values[0])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--user", default="n3xCLnMAAAAJ", help="Google Scholar user id")
    parser.add_argument("--out", default="bibliography/papers.bib", help="Output BibTeX file")
    parser.add_argument("--pagesize", type=int, default=100, help="Scholar profile page size")
    parser.add_argument("--delay", type=float, default=0.4, help="Delay between article detail requests, in seconds")
    parser.add_argument("--details", action="store_true", help="Fetch each article detail page for abstracts/pages/publisher")
    parser.add_argument("--rows-json", help="Read profile rows from a JSON file extracted from the browser")
    parser.add_argument("--details-json", help="Read article detail data extracted from the browser")
    args = parser.parse_args()

    if args.details_json:
        articles = articles_from_details_json(Path(args.details_json))
    elif args.rows_json:
        articles = articles_from_rows_json(Path(args.rows_json))
    else:
        articles = fetch_profile_articles(args.user, args.pagesize)

    if not articles:
        raise SystemExit("No publications found. Google may have blocked the request, or the user id is wrong.")

    if args.details:
        detailed_articles: list[ScholarArticle] = []
        for index, article in enumerate(articles, start=1):
            detailed_article = fetch_article(args.user, article.citation_id)
            detailed_articles.append(detailed_article)
            print(f"[{index:02d}/{len(articles):02d}] {detailed_article.title}", flush=True)
            time.sleep(args.delay)
        articles = detailed_articles

    articles, missing_year_count = drop_articles_without_year(articles)
    articles, duplicate_count = dedupe_articles(articles)
    for index, article in enumerate(articles, start=1):
        print(f"[{index:02d}/{len(articles):02d}] {article.title}", flush=True)
    if missing_year_count:
        print(f"Skipped {missing_year_count} publication(s) without a year", flush=True)
    if duplicate_count:
        print(f"Removed {duplicate_count} duplicate publication(s) by normalized title", flush=True)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render_bibtex(articles), encoding="utf-8")
    print(f"Wrote {len(articles)} BibTeX entries to {out_path}", flush=True)


def fetch_profile_articles(user_id: str, pagesize: int) -> list[ScholarArticle]:
    url = f"{SCHOLAR_BASE}?{urllib.parse.urlencode({'user': user_id, 'hl': 'en', 'cstart': 0, 'pagesize': pagesize})}"
    return parse_profile_articles(fetch_url(url))


def parse_profile_articles(page: str) -> list[ScholarArticle]:
    articles: list[ScholarArticle] = []
    for row in re.findall(r'<tr class="gsc_a_tr">(.*?)</tr>', page, re.S):
        title_match = re.search(r'<a[^>]*class="gsc_a_at"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', row, re.S)
        if not title_match:
            continue
        href = html.unescape(title_match.group(1))
        query = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
        citation_id = query.get("citation_for_view", [slugify(clean_html(title_match.group(2)))])[0]
        gray_values = re.findall(r'<div class="gs_gray">(.*?)</div>', row, re.S)
        year_match = re.search(r'<span class="gsc_a_h gsc_a_hc gs_ibl">(.*?)</span>', row, re.S)
        authors = clean_html(gray_values[0]) if gray_values else ""
        venue = clean_venue(clean_html(gray_values[1])) if len(gray_values) > 1 else ""
        title = clean_title(clean_html(title_match.group(2)))
        year = recover_year(clean_html(year_match.group(1)) if year_match else "", title, venue)
        fields = {"authors": authors, "publication date": year, "book": venue}
        articles.append(ScholarArticle(citation_id=citation_id, title=title, fields=fields))
    return articles


def articles_from_rows_json(path: Path) -> list[ScholarArticle]:
    import json

    rows = json.loads(path.read_text(encoding="utf-8"))
    articles: list[ScholarArticle] = []
    for row in rows:
        href = row.get("href") or ""
        query = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
        citation_id = query.get("citation_for_view", [slugify(row.get("title", "publication"))])[0]
        title = clean_title(row.get("title") or "Untitled")
        venue = clean_venue(row.get("venue") or "")
        fields = {
            "authors": row.get("authors") or "",
            "publication date": recover_year(row.get("year") or "", row.get("title") or "", row.get("venue") or ""),
            "book": venue,
        }
        articles.append(ScholarArticle(citation_id=citation_id, title=title, fields=fields))
    return articles


def articles_from_details_json(path: Path) -> list[ScholarArticle]:
    import json

    items = json.loads(path.read_text(encoding="utf-8"))
    articles: list[ScholarArticle] = []
    for item in items:
        href = item.get("href") or ""
        query = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
        citation_id = query.get("citation_for_view", [slugify(item.get("title", "publication"))])[0]
        detail = item.get("detail") or {}
        detail_fields = detail.get("fields") or {}
        title = clean_title(detail.get("title") or item.get("title") or "Untitled")
        fields = {str(key).lower(): str(value) for key, value in detail_fields.items() if value}

        if not fields.get("authors"):
            fields["authors"] = item.get("authors") or ""
        if not fields.get("publication date"):
            fields["publication date"] = recover_year(item.get("year") or "", item.get("title") or "", item.get("venue") or "")
        if not any(fields.get(key) for key in ["journal", "book", "conference", "source"]):
            fields["book"] = clean_venue(item.get("venue") or "")

        if url := detail.get("titleUrl"):
            fields["url"] = url

        articles.append(ScholarArticle(citation_id=citation_id, title=title, fields=fields))
    return articles


def clean_title(value: str) -> str:
    return re.sub(r",\s*(19|20)\d{2}\s*$", "", value).strip()


def clean_venue(value: str) -> str:
    value = value.replace("\u00a0", " ").strip()
    value = re.sub(r",?\s*\d{4}\s*$", "", value).strip()
    return value


def recover_year(*values: str) -> str:
    for value in values:
        match = re.search(r"\b((?:19|20)\d{2})\b", value or "")
        if match:
            return match.group(1)
    return ""


def fetch_article(user_id: str, citation_id: str) -> ScholarArticle:
    url = f"{SCHOLAR_BASE}?{urllib.parse.urlencode({'view_op': 'view_citation', 'hl': 'en', 'user': user_id, 'citation_for_view': citation_id})}"
    page = fetch_url(url)
    title = extract_title(page)
    fields = extract_fields(page)
    return ScholarArticle(citation_id=citation_id, title=title, fields=fields)


def fetch_url(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", "ignore")


def extract_title(page: str) -> str:
    match = re.search(r'<a[^>]*class="gsc_oci_title_link"[^>]*>(.*?)</a>', page, re.S)
    if not match:
        match = re.search(r'<div[^>]*id="gsc_oci_title"[^>]*>(.*?)</div>', page, re.S)
    if not match:
        raise ValueError("Could not extract article title")
    return clean_html(match.group(1))


def extract_fields(page: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    pattern = re.compile(r'<div class="gsc_oci_field">(.*?)</div>\s*<div class="gsc_oci_value">(.*?)</div>', re.S)
    for label_html, value_html in pattern.findall(page):
        label = clean_html(label_html).lower()
        value = clean_html(value_html)
        if value:
            fields[label] = value
    return fields


def clean_html(value: str) -> str:
    value = re.sub(r"<br\s*/?>", " ", value, flags=re.I)
    value = re.sub(r"<[^>]+>", " ", value)
    return html.unescape(re.sub(r"\s+", " ", value)).strip()


def drop_articles_without_year(articles: list[ScholarArticle]) -> tuple[list[ScholarArticle], int]:
    filtered = [article for article in articles if article.fields.get("publication date")]
    return filtered, len(articles) - len(filtered)


def dedupe_articles(articles: list[ScholarArticle]) -> tuple[list[ScholarArticle], int]:
    deduped: list[ScholarArticle] = []
    seen_titles: set[str] = set()

    for article in articles:
        key = normalize_title_for_dedupe(article.title)
        if key in seen_titles:
            continue
        seen_titles.add(key)
        deduped.append(article)

    return deduped, len(articles) - len(deduped)


def normalize_title_for_dedupe(title: str) -> str:
    title = title.lower()
    title = title.replace("‐", "-").replace("‑", "-").replace("–", "-").replace("—", "-")
    title = re.sub(r"\s*[\.,]?\s*(corr|arxiv)\s+abs/\S+.*$", "", title, flags=re.I)
    title = re.sub(r"\s*[\.,]?\s*[a-z]+\s*\((19|20)\d{2}\)\s*$", "", title, flags=re.I)
    title = re.sub(r"\s*\((19|20)\d{2}\)\s*$", "", title)
    title = re.sub(r",\s*(19|20)\d{2}\s*$", "", title)
    title = re.sub(r"[^a-z0-9]+", " ", title)
    title = re.sub(r"\btop\s+k\s+masking\b", "top masking", title)
    return re.sub(r"\s+", " ", title).strip()


def render_bibtex(articles: list[ScholarArticle]) -> str:
    blocks = ["% Generated from Google Scholar by scripts/update_bib_from_google_scholar.py."]
    blocks.append("% Edit manually only for fields Scholar does not expose, such as pdf/slides links.\n")
    used_keys: set[str] = set()
    for article in articles:
        blocks.append(render_entry(article, used_keys))
    return "\n\n".join(blocks).rstrip() + "\n"


def render_entry(article: ScholarArticle, used_keys: set[str]) -> str:
    fields = article.fields
    entry_type = bibtex_type(fields)
    year, month, day = parse_publication_date(fields.get("publication date", ""))
    key = unique_key(article, year, used_keys)
    venue_label, venue = venue_field(fields)

    bib_fields: list[tuple[str, str]] = [
        ("title", article.title),
    ]
    if authors := fields.get("authors"):
        bib_fields.append(("author", format_authors(authors)))
    if venue:
        bib_fields.append((venue_label, venue))
    if year:
        bib_fields.append(("year", str(year)))
    if month:
        bib_fields.append(("month", str(month)))
    if day:
        bib_fields.append(("day", str(day)))
    if pages := fields.get("pages"):
        bib_fields.append(("pages", pages))
    if publisher := fields.get("publisher"):
        bib_fields.append(("publisher", publisher))
    if url := fields.get("url"):
        bib_fields.append(("url", url))
    if description := fields.get("description"):
        bib_fields.append(("abstract", description))

    lines = [f"@{entry_type}{{{key},"]
    for index, (name, value) in enumerate(bib_fields):
        comma = "," if index < len(bib_fields) - 1 else ""
        lines.append(f"  {name} = {{{escape_bibtex(value)}}}{comma}")
    lines.append("}")
    return "\n".join(lines)


def bibtex_type(fields: dict[str, str]) -> str:
    if "journal" in fields:
        return "article"
    if "book" in fields or "conference" in fields:
        return "inproceedings"
    return "misc"


def parse_publication_date(value: str) -> tuple[int | None, int | None, int | None]:
    if not value:
        return None, None, None
    parts = [int(part) for part in re.findall(r"\d+", value)]
    if not parts:
        return None, None, None
    year = parts[0]
    month = parts[1] if len(parts) > 1 else None
    day = parts[2] if len(parts) > 2 else None
    return year, month, day


def venue_field(fields: dict[str, str]) -> tuple[str, str]:
    if journal := fields.get("journal"):
        return "journal", journal
    if book := fields.get("book"):
        return "booktitle", book
    if conference := fields.get("conference"):
        return "booktitle", conference
    if source := fields.get("source"):
        return "booktitle", source
    return "venue", ""


def format_authors(authors: str) -> str:
    return " and ".join(part.strip() for part in authors.split(",") if part.strip())


def unique_key(article: ScholarArticle, year: int | None, used_keys: set[str]) -> str:
    first_author = "yang"
    if authors := article.fields.get("authors"):
        first_author = authors.split(",", 1)[0].strip().split()[-1]
    base = slugify("-".join(part for part in [first_author, str(year or "nd"), article.title] if part))[:80].strip("-")
    key = base or slugify(article.citation_id)
    suffix = 2
    while key in used_keys:
        key = f"{base}-{suffix}"
        suffix += 1
    used_keys.add(key)
    return key


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "publication"


def escape_bibtex(value: str) -> str:
    return value.replace("\\", r"\\").replace("}", r"\}").replace("{", r"\{")


if __name__ == "__main__":
    main()
