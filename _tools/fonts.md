# Taiwan preview fonts

The preview uses the existing static Newsreader roman Latin and **one** page-sized GenRyuMin TW Regular (400) WOFF2. Fonts are self-hosted; nothing is fetched during a Pages build.

## Updating the Chinese copy

From the site root, after all Liquid includes, collection titles and translated UI have been reviewed:

```sh
bundle exec jekyll build
curl -fLsS -o /tmp/GenRyuMin2TW-R.otf https://raw.githubusercontent.com/ButTaiwan/genryu-font/030cd4fa3dd6b0607c5e7f35f13977a2e0a10522/otf/TW/GenRyuMin2TW-R.otf
uv run --python 3.12 _tools/cut-tw-font.py _site/zh-tw/index.html /tmp/GenRyuMin2TW-R.otf
bundle exec jekyll build
cmp assets/fonts/genryumin-tw-preview.woff2 _site/assets/fonts/genryumin-tw-preview.woff2
```

Use the first build's actual destination in place of `_site` if different. Commit only the resulting `assets/fonts/genryumin-tw-preview.woff2` with the copy changes, not the full OTF or build directory. The helper pins its dependencies, checks both input font hashes, preserves the input timestamp, and reopens the WOFF2 to verify **exact cmap equality** and weight. It reads the English homepage’s zh-TW switch label, zh-TW body text (including inactive tabs) and translated `alt`, `aria-label`, `title` and `placeholder` attributes, not URLs, scripts, comments or English subtrees. It keeps fullwidth and CJK punctuation present in this text, excludes characters covered by Newsreader and leaves other Latin letters to Latin fallback. CSS-generated or JS-injected Chinese text would require updating the collector.

## Provenance and redistribution

- **GenRyuMin TW:** [ButTaiwan/genryu-font, pinned OTF](https://github.com/ButTaiwan/genryu-font/blob/030cd4fa3dd6b0607c5e7f35f13977a2e0a10522/otf/TW/GenRyuMin2TW-R.otf), 16,449,288 bytes, SHA-256 `d244c6115431b2a18b5dfb0066e08381f56e6a33532915a0f517dd3f7063b646`. Shipped license `assets/fonts/genryumin-OFL.txt` is the [upstream license](https://github.com/ButTaiwan/genryu-font/blob/030cd4fa3dd6b0607c5e7f35f13977a2e0a10522/SIL_Open_Font_License_1.1.txt), SHA-256 `d84b652ca46586043946969a33c1dbf5a43028440825ae744a325965bec4c8fb`. The subset remains under OFL 1.1; its name does not use the reserved name “Source”.
- **Stencilzeit reference:** revision `885ca29f2bff31be7a6fe7e06fce4de7209f898b`. `src/_plugins/fonts-tc/index.ts` analyzes rendered pages, calls `src/assets/fonts/_tc-glyphs.ts` and `_cut-tc.ts`, emits artifacts and checks the staged result. `fonts-src/sources.json` ties its full compressed regular input (`6d0d4dd84ab1e6ac3d849be8d56824611706f2ae1360f6368935740a0d7fafcd`) to the OTF above. Here we use that OTF directly and keep the same horizontal features (`ccmp`, `liga`, `kern`, `halt`, `locl`), without importing its site-wide core, semibold or late-loading subsets.
- **Newsreader:** `src/assets/fonts/_refresh-latin.ts` in that revision requests static Google Fonts faces independently. The existing `assets/fonts/newsreader-latin.woff2` matches both its regular Latin asset and [the Google Fonts v26 file](https://fonts.gstatic.com/s/newsreader/v26/cY9qfjOCX1hbuyalUrK49dLac06G1ZGsZBtoBCzBDXXD9JVF438weI_wC-ZFHDWwgUii.woff2) byte for byte: 22,504 bytes, SHA-256 `283674309045e326b732488ff07dd9e7799cb1ffc3eeccbeb642c142a13c7131`. Keep the existing `assets/fonts/newsreader-OFL.txt` (SHA-256 `865f0949b59fab5925506f80102dff3d12e8666412daf52d212db969d40adc25`), identical to Stencilzeit's copy, equivalent except for whitespace to [the Newsreader Project Authors' OFL 1.1](https://github.com/productiontype/Newsreader/blob/1ece6a8bfe5db1a2b90c76cc1fe5d3b2eed5dcf3/OFL.txt).
