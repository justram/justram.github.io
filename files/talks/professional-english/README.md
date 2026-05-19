# Professional English Mini-Presenter Deck

Run locally:

```bash
cd /Users/mattyang/Documents/Codex/2026-05-17/use-your-video-analysis-tools-and/mini-presenter-pro-english
npm run start
```

Slides: <http://localhost:8090/>
Presenter view: <http://localhost:8090/_/presenter>
Audience Q&A: <http://localhost:8090/_/questions>
Q&A QR page: <http://localhost:8090/_/questions/qr>

Keep one slide-display tab open at <http://localhost:8090/> while using the
presenter view. Opening `index.html` through `file://` can show the slides, but
it will not connect presenter view, notes, recording, or audience Q&A.

For audience phones or remote viewers, run with a public tunnel:

```bash
node vendor/mini-presenter/bin/mini-presenter.js . --port 8090 --watch --funnel
```

Then share the generated public `/_/questions` URL or QR page. Q&A submissions
are stored in `questions.json`.

Newsletter signup slide:

- Current Kit signup URL: <https://stencilzeit.kit.com/177c376f5f>
- QR asset: `assets/genai-newsletter-qr.svg`

If the Kit landing-page URL changes, update the slide-11 `data-signup-url`,
the visible signup link, and regenerate the QR asset:

```bash
npx --yes qrcode --type svg --error H --width 720 --qzone 3 --darkcolor 241b16ff --lightcolor fffaf0ff --output assets/genai-newsletter-qr.svg "https://YOUR-KIT-URL"
```

## Credits

Built with [mini-presenter](https://github.com/mitsuhiko/mini-presenter) by Armin Ronacher, licensed Apache-2.0.

Visual direction inspired by Armin Ronacher's AI Engineer talk deck:
https://mitsuhiko.github.io/talks/ai-engineer-talk/

This deck's cozy shadow theme, generated assets, and implementation are original adaptations, not a copy of the talk deck's source or visual assets.

## License

© 2026 Jheng-Hong (Matt) YANG. Licensed under CC BY 4.0
