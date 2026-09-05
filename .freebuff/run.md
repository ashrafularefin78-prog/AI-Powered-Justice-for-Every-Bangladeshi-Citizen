# A ai — Digital Legal Aid Bangladesh (static multi-page site)

The site is fully static HTML/CSS/JS — no build step, no dependencies, no env files.

## How to run the server

Serve the `dla-website/` directory with any static file server, e.g. Python:

```
python -m http.server 8099 --bind 127.0.0.1 --directory dla-website
```

Then open `http://127.0.0.1:8099/index.html`.

## Pages

| Page | Path | Content |
|---|---|---|
| Home | `index.html` | Hero, problem/solution/features, impact, nationwide reach |
| A ai | `ai.html` | Multi-agent AI system, reasoning engine, features, roadmap |
| Justice Map | `justice.html` | 64-district map, Constitution, emergency helplines |
| Government | `government.html` | Government structure, e-services portals |
| SheGuard X | `sheguard.html` | Women's safety (embeds `female-safety.html`) |
| July 2024 | `july.html` | Uprising timeline, Osman Hadi memorial (links to the full tribute page) |
| Hadi Tribute | `hadi.html` | Dedicated \"In Memory of Sharif Osman Bin Hadi\" tribute: hero, life journey, portrait & bio, photo gallery, quotes, tributes |
| Blueprints | `blueprints.html` | Visionary archive (Futuristic → Beyond) |
| Contact | `contact.html` | Complaints desk, IT report, contact |

## Shared assets (do not edit by hand)

- `dla-website/assets/styles.css` — all styles, extracted from the old single page
- `dla-website/assets/app.js` — global chrome + A ai chatbot engine + knowledge base + auth + persistence
- `dla-website/assets/security.js` — **Quantum Shield**: AES-256-GCM at-rest encryption for all `aai_*`
  localStorage data (chat, memory, identity, complaints), PBKDF2 key derivation, SHA-256 asset
  integrity check, XSS sanitizer, honeypot, rate limit, audit log, and the Security Center UI
  (shield button in the nav, injected by the script). Loaded in `<head>` on every page **before**
  app.js. If you edit `assets/app.js`, recompute and update the `EXPECTED_APP_SHA` constant in
  security.js (one-liner is documented at the file's tail) or the integrity audit will flag it.

## Regenerating the pages

The 8 pages are generated from the original monolithic page by
`dla-website/build_pages.py` (reads `index.html.bak-pre`, writes all pages +
assets). Re-run after any manual edit to `index.html.bak-pre`:

```
cd dla-website && python3 build_pages.py
```

Editing `index.html` directly is fine for content tweaks, but note the
chatbot knowledge base lives in `assets/app.js` (shared by all pages), and the
SheGuard interactive app lives in `female-safety.html`.
## Cache busting

Pages include assets with version queries: `assets/styles.css?v=css2`,
`assets/security.js?v=sec2`, `assets/app.js?v=app2` (kept in sync in
`build_pages.py`). After editing an asset, bump its `?v=` token in all 8 pages
AND in `build_pages.py` (or just re-run the builder), or preview browsers may
serve a stale cached copy.
