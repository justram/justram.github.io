# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = ["fonttools==4.59.2", "brotli==1.1.0", "lxml==6.0.2"]
# ///
"""Cut one regular face from the rendered zh-TW homepage. See fonts.md."""
import argparse
import hashlib
import io
import unicodedata
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from lxml import html

FONTS = Path(__file__).resolve().parents[1] / "assets/fonts"
OTF = "d244c6115431b2a18b5dfb0066e08381f56e6a33532915a0f517dd3f7063b646"
LATIN = "283674309045e326b732488ff07dd9e7799cb1ffc3eeccbeb642c142a13c7131"


def checked_font(path, sha):
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != sha:
        raise SystemExit(f"Unexpected font SHA-256: {path}")
    return TTFont(io.BytesIO(data), recalcTimestamp=False)


def strings(node, lang):
    if not isinstance(node.tag, str) or node.tag in {'style', 'script', 'template', 'svg'}:
        return
    lang = node.get('lang', lang).lower()
    if lang == 'zh-tw':
        yield node.text or ''
        for attr in ('alt', 'aria-label', 'placeholder', 'title'):
            yield node.get(attr, '')
    for child in node:
        yield from strings(child, lang)
        if lang == 'zh-tw':
            yield child.tail or ''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('page', type=Path, help='built zh-tw/index.html')
    parser.add_argument('otf', type=Path, help='pinned GenRyuMin2TW-R.otf')
    parser.add_argument('--output', type=Path, default=FONTS / 'genryumin-tw-preview.woff2')
    args = parser.parse_args()
    doc = html.document_fromstring(args.page.read_text(encoding='utf-8'))
    if doc.get('lang', '').lower() != 'zh-tw' or doc.body is None:
        raise SystemExit('Expected a built zh-TW page with a body')
    latin = checked_font(FONTS / 'newsreader-latin.woff2', LATIN).getBestCmap()
    wanted = {ord(c) for s in strings(doc.body, 'zh-tw') for c in s
              if not c.isspace() and unicodedata.category(c) not in ('Cf', 'Cc')
              and not unicodedata.name(c, '').startswith(('LATIN ', 'VARIATION SELECTOR'))} - latin.keys()
    if not wanted:
        raise SystemExit('No TC characters found')
    font = checked_font(args.otf, OTF)
    missing = wanted - font.getBestCmap().keys()
    if missing:
        raise SystemExit('Source lacks: ' + ' '.join(f'U+{cp:04X}' for cp in sorted(missing)))
    options = subset.Options()
    options.layout_features = ['ccmp', 'liga', 'kern', 'halt', 'locl']
    cutter = subset.Subsetter(options)
    cutter.populate(unicodes=wanted)
    cutter.subset(font)
    font.flavor = 'woff2'
    out = io.BytesIO()
    font.save(out)
    out.seek(0)
    result = TTFont(out)
    if set(result.getBestCmap()) != wanted or result['OS/2'].usWeightClass != 400:
        raise SystemExit('Output cmap/weight mismatch')
    data = out.getvalue()
    args.output.write_bytes(data)
    print(f'{args.output}: {len(wanted)} code points, {len(data)} bytes, sha256={hashlib.sha256(data).hexdigest()}')


if __name__ == '__main__':
    main()
