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

## Single-file builds for browser testing (no server needed)

Two builders produce self-contained `index.html` variants so you can test by
double-clicking the file (file://) or in a sandboxed preview that only serves
one file. They form an idempotent chain over the archive copies; **never run
one after the other's output has replaced index.html without re-running the
chain from the top**:

```
# 1. standalone HOME (only the home page, all CSS/JS/favicon inlined)
python3 build_standalone.py
#    source : _archive/index.html.bak-slim   (slim multi-page home - never overwritten)
#    writes : index.html  (standalone home)
#    keeps  : _archive/index.html.bak-standalone = the standalone it just built

# 2. WHOLE SITE in one file (run after 1, or whenever assets/pages changed)
python3 build_allinone.py
#    source : _archive/index.html.bak-standalone  (skeleton chrome + inlined assets)
#             + ai/justice/sheguard/government/contact/about/july/memorial-abrar/blueprints
#    writes : index.html  (~1.6 MB, every page stacked, nav = #pg-* anchors)
```

What `build_allinone.py` does:

- Slices each real page's unique content (first `<section>` → `<footer>`, which
  includes that page's own inline `<style>`/`<script>` blocks) and stacks it in
  nav order inside `<div class="allinone-page" id="pg-<page>">` blocks.
- Rewrites every `page.html` / `page.html#anchor` link (nav, drawer, footer,
  CTAs, content) into in-page anchors (`#pg-justice`, `#pg-about-nazrul`, ...).
- Namespaces every content id with a `pg-<page>-` prefix to avoid collisions
  between pages, EXCEPT the ids `assets/app.js` queries by id (kept exact so
  widgets like the justice map search and government tabs keep working).
- SheGuard's `female-safety.html` app stays an `<iframe>` but becomes fully
  inline via the `srcdoc` attribute (that page is self-contained: own styles +
  scripts, no external refs), so no second file is needed.
- Injects a deliberately **relaxed CSP meta tag** **in this local test file
  only**. The strict per-page CSP is `'self'`-based and cannot work here: under
  `file://` `'self'` never matches sibling files, so it would block the
  relative image refs and the srcdoc iframe. The relaxed policy (see
  `RELAXED_CSP` in `build_allinone.py`) still keeps `object-src 'none'`,
  `base-uri 'self'`, `form-action` limited to `self`/http(s), and **no
  `'unsafe-eval'`** (nothing uses `eval`), while explicitly allowing inline
  scripts/styles, `data:` URIs, `file:` images, `about:` srcdoc frames, CDN
  fonts, and the local AI proxy (`http`/`ws` 127.0.0.1:8787). The real
  multi-page pages and the standalone home keep their original strict CSP.
- **Fully portable images**: every image the site can actually load (34 files)
  is base64-embedded exactly once in a `window.__AIIM` map. `<img>` tags keep
  their relative `assets/img/...` srcs; a tiny capture script (installed right
  after `<body>`, plus a parent-linked copy inside the srcdoc iframe) swaps any
  image whose fetch fails to its data URI. The file runs with no `assets/`
  folder at all - the preview sandbox (which serves only the one file) shows
  every memorial photo correctly. Trade-off: when the folder is absent, each
  image logs one benign 404 attempt before the swap.

Caveats for the all-in-one file: it is a test artifact (~9 MB - the images
account for most of it); do not deploy it in place of the real multi-page
site. The standalone home (`build_standalone.py`) intentionally keeps the CSP
and stays small (~1 MB) with the favicon inlined only - re-run it, then
`build_allinone.py`, after any page or asset edit to refresh index.html.

### What the relaxed CSP loses, per page (all-in-one vs production)

Production pages and the standalone home ship the strict policy
(`default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self'
'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com
https://cdnjs.cloudflare.com; img-src 'self' data: blob: https:; connect-src
'self' data: http://127.0.0.1:8787 http://localhost:8787; frame-src 'self';
object-src 'none'; base-uri 'self'; form-action 'self'`). The all-in-one file's
relaxed policy widens several sources; the residual risk is low because the
file has no user-controlled remote content and `security.js` still sanitizes
stored text, but be aware of exactly what changed:

| Directive | Strict (production) | Relaxed (all-in-one) | What each page loses |
|---|---|---|---|
| `script-src` | `'self'` + inline only | also `http: https: data: blob:` | **Every page**: an XSS payload would not need a same-origin script file - any http(s)/data/blob script would run. (No such payload exists; stored content is sanitized.) |
| `style-src` | `'self'`, inline, Google Fonts only | also `http: https: data: blob:` | **Every page**: external stylesheets from any host (e.g. a malicious font/css CDN) would be applied. |
| `img-src` | `'self'`, `data:`, `blob:`, `https:` | also `http:` and `file:` | **Every page**: http:// and file:// images load natively (needed for folder mode); no https-only restriction on remote images. |
| `font-src` | Google/gstatic + cdnjs only | any `http:`/`https:` | **Every page**: fonts may load from any host (same risk class as style-src). |
| `connect-src` | `'self'`, `data:`, the 8787 proxy only | any `http:/https:/ws:` host | **AI chat / Home / Contact / SheGuard**: the chatbot, complaint desk and SOS flows (if ever wired to a backend) could reach any endpoint; today everything stays in localStorage, so nothing actually phones home except the optional 8787 AI proxy. |
| `frame-src` | `'self'` only | also `about:` (srcdoc), `data:`, `blob:`, any http(s) | **SheGuard**: its iframe may now host third-party pages; currently it embeds only our own srcdoc female-safety app. |
| `form-action` | `'self'` only | `'self'` + any http(s) | **Contact / auth forms**: a form could in principle submit cross-origin; all current forms are JS-handled (`preventDefault`) and never POST. |
| `base-uri`, `object-src`, `unsafe-eval` | restrictive | **kept**: `base-uri 'self'`, `object-src 'none'`, no `'unsafe-eval'` | nothing - these guardrails still hold in the all-in-one file. |

### PRO design-system layer (added 2026-09)

`assets/styles.css` ends with an appended **PRO DESIGN-SYSTEM LAYER** (~130
lines). It is pure CSS - no JS/DOM edits anywhere, so the security.js shield
button (injected next to `#themeToggle`) and `EXPECTED_APP_SHA` are untouched.
What it adds:

- Design tokens: `--pri-2/--sec-2` tints, `--ink/-2/-3` text scale,
  `--line/--line-2` hairlines, `--sh-1/--sh-2` shadows, `--ring` focus ring,
  `--r-2/--r-3` radii, `--ease` curve. Tune these to re-theme the whole site.
- **Aurora home hero**: layered radial gradients with a slow
  `auroraDrift` animation + masked grid overlay; glassy badge; hero stats
  became glass cards with hover lift.
- **`.page-hero`** component (tag chip + gradient h1 + subtext + CTA) inserted
  at the top of all 8 interior pages (ai, justice, sheguard, government,
  contact, about, july, blueprints) by `page-hero-insert.py`-style one-off
  script; `build_allinone.py`'s `extract_content` now starts at the page-hero
  header so the merged file keeps them (8 present).
- Surfaces: cards get gradient surfaces, hairline borders, hover lift+glow;
  buttons get the signature gradient + press states; nav links get a sliding
  underline; the three header toggles are visually grouped into one utility
  cluster (CSS-only).
- A11y: `:focus-visible` rings, `.skip-link` styles,
  `prefers-reduced-motion` kills the aurora/reveals.

Cache token bumped `styles.css?v=css25` -> `css26` on all pages and in
`build_pages.py`. After editing the layer, just re-run `build_standalone.py`
then `build_allinone.py` (and bump the token again if you want to bust caches).

### Red-green theme (added 2026-09, token v=css27 / v=app46)

The brand palette is now **green (primary) x red (secondary)**. Applied by a
byte-safe global swap in `assets/styles.css` (works under its CRLF endings;
`assets/app.js` stays UTF-8/LF):

- `#0ea5e9`/`rgba(14,165,233,...)` (blue)   -> `#10b981`/`rgba(16,185,129,...)` emerald
- `#6366f1`/`rgba(99,102,241,...)` (indigo) -> `#ef4444`/`rgba(239,68,68,...)` red
- light-blue tints `#38bdf8`/`#7dd3fc`/`#818cf8` -> `#34d399`/`#6ee7b7`/`#f87171`
- light-mode overrides `#0284c7`/`#4f46e5` -> `#047857`/`#dc2626`
- chatbot avatar gradient `#00ff88->#00b4ff` became `#10b981->#ef4444`
- `app.js` `divColors`: Rangpur `#0ea5e9`->`#22c55e`, Rajshahi `#6366f1`->`#ef4444`
  (this changed `app.js`, so `EXPECTED_APP_SHA` in `security.js` was recomputed
  to `73c29057...` - verified MATCH)
- Inline styles inside the 8 pages + `bak-slim` + `build_site.py` swapped with
  the same pairs; a trailing **RED-GREEN THEME LAYER** in `styles.css` adds soft
  fixed red/green radial background washes on `body` and alternating per-section
  washes (plus `.light` variants).
- Un-rethemed on purpose: success greens already in the design (`#10b981` etc.
  simply converged with the new primary), SheGuard's rose, amber/orange
  division colors.

Rebuild note: this re-theme triggered the archive-chain gotcha above (the
first `build_allinone.py` run consumed a clobbered `bak-standalone` skeleton
and produced a 17 MB double-merge). Fixed by the documented repair dance;
final all-in-one is ~9.0 MB with clean structure (4 benign script-string id
dupes only, 34/34 images embedded).

Maintenance note: `build_standalone.py` backs up whatever `index.html`
currently is over `_archive/index.html.bak-standalone` before rebuilding. If
`index.html` is currently the big all-in-one, repair the archive after running
it (copy the fresh ~1 MB standalone over `bak-standalone`) BEFORE running
`build_allinone.py`, or the merge will double-merge. A size guard
(`< 2 MB`) documents this in the build commands.

### file:// (double-click) test results

Verified with headless Edge (Chromium) opening the real file:// URL, in both
modes (temporary copies were used so the real `index.html` was never touched):

| Scenario | Images | Structure | Console |
|---|---|---|---|
| File in the project folder (assets/ present) | 42/42 load **natively from disk** (`src="assets/img/..."`, no swap needed) | 10 page blocks, 9 bands, srcdoc iframe, `__AIIM` helper | no CSP refusals, no JS exceptions |
| File alone in an empty folder (no assets/) | 42/42 auto-swapped to **embedded `data:` URIs** (0 left relative) | same | no CSP refusals, no JS exceptions |

Notes from real-browser testing:

- The relaxed CSP is genuinely file://-safe: `'self'` never matches file: URLs,
  so inline code, `data:` images, `file:` images, and the `about:` srcdoc
  iframe are allowed explicitly (that is why the strict per-page CSP was
  replaced in this build only).
- One cosmetic console line is expected under file://: security.js's app.js
  SHA-256 integrity check uses `fetch('assets/app.js')`, which browsers refuse
  for file:// URLs (CORS). security.js catches it and records "integrity check
  unavailable" in its audit log - non-fatal, same as the http sandbox's 404.
  The page itself still runs; do not edit security.js to "fix" this.
- Icons/fonts come from Google Fonts / Font Awesome CDNs, so they need network
  (they degrade to fallback fonts offline); that is not file://-specific.
- Quick re-check command (git-bash + Edge headless), e.g. on a stripped copy:
  `".../msedge.exe" --headless=new --disable-gpu --no-sandbox --enable-logging=stderr
  --virtual-time-budget=25000 --dump-dom "file:///C:/path/index.html"` and grep the
  DOM for `src="data:image` (folderless) or `src="assets/img` (folder present).

### Semantic color audit (added 2026-09, token v=css28 / v=app47)

Audit after the red/green re-theme: brand green/red now deliberately
distinguished from state colors by a trailing **SEMANTIC-DISAMBIGUATION
LAYER** in `assets/styles.css`:

- **Error/danger = crimson `#dc2626`** (`--err`) - never the brand red
  `#ef4444` used in CTAs/ticker/memorial accents. Applies to invalid form
  fields (`.invalid` ring), `.form-error`-style text, validation toasts.
- **Success = deep green `#059669`** (`--ok`) - auth success ring/check, chips.
- **Warning = brown-amber `#b45309`** (`--warn`), light-mode variants included.
- AI reasoning confidence chips (high/medium/low) now use ok/warn/err tokens.
- `showToast(msg, kind)` in `app.js` is now typed: success call sites pass
  `'ok'` (green `.toast-ok`), validation failures stay crimson (`.toast-err`
  default). `EXPECTED_APP_SHA` recomputed accordingly.
- Deliberately NOT restyled (brand/identity, not state): hotline ticker red,
  SheGuard rose, memorial photo-card borders, hero/section washes,
  red/green division map colors.

### "Monsoon of July" ambient memorial FX (added 2026-09, v=app51)

Cinematic, **ambient-only** atmosphere for the July memorial context
(canvas rain + drifting smoke + flickering amber embers + vignette dim).
Deliberately no cursor/click effects, no gore mechanics - the site memorializes
real people killed by gunfire.

- **Where**: `july.html` (static canvas + dim markup in chrome) and the
  all-in-one build (engine self-creates canvas/dim when absent - the extractor
  drops chrome-level nodes from page splices).
- **Engine**: `initMonsoonFX()` in `assets/app.js`. Scoped to
  `#pg-july` in the merged file, `.page-hero` on the standalone page. Runs via
  IntersectionObserver with `threshold:0` + 12% rootMargin (a percentage
  threshold is unreachable on a 36k-px-tall band), pauses off-screen AND on
  `visibilitychange`. Capped ~30fps; particle counts scale with viewport
  width; DPR clamped to 2. Fully disabled under `prefers-reduced-motion`.
- **Tuning knobs** (in `initMonsoonFX`): drops `Math.min(90, width/12)`,
  speed `R(380,700)`, smoke 5 blobs `a:R(.02,.05)`, embers 10 `r:R(.8,2.1)`,
  vignette opacity `.55`.
- **Integrity**: every app.js edit here recomputed `EXPECTED_APP_SHA`
  (current build verifies MATCH). Token chain now `css28` + `app51`.

### Sayeedi chatbot integration (added 2026-09, v=app52)

Delwar Hossain Sayeedi added to the A ai knowledge base from the English and
Bangla Wikipedia articles (fetched in full during the session):

- **3 bilingual `cR[]` entries**: `sayeedi_bio` (birth 1940 Saiyadkhali,
  family, madrasa education, waz-mahfil fame, Jamaat career, MP 1996/2001,
  2003 unseating + SC stay, US No-Fly 2004, death 2023 + burial),
  `sayeedi_trial` (ICT-1: 20 charges, 28 Feb 2013 verdict, HRW/Amnesty
  criticism, Shikdar mistaken-identity defence, 17 Sep 2014 commutation),
  `sayeedi_books` (40+ titles incl. Tafsir-e-Sayeedi series).
- **28 aliases** (EN + BN): "delwar hossain sayeedi", "sayeedi/sayedee",
  "সাঈদী", "দেলাওয়ার", "সাঈদীর বিচার", "সাঈদীর বই", "তাফসীরে সাঈদী" etc.
- **Portrait**: `assets/img/sayeedi.png` (140 KB, en-wiki `File:Sayeedi.png`,
  fair-use/educational like the existing memorial photos) rendered by a new
  `martyrPhotoHTML` branch for sayeedi keys/name mentions. Auto-embedded in
  the all-in-one build (35 images now in `__AIIM`).
- Integrity: `EXPECTED_APP_SHA` recomputed (`657a06a1...`), token `v=app52`.
  Verified in preview: EN bio + portrait (data-URI), trial query, BN query
  all answer with the portrait card; console clean.

### Dynamic storm intensity (added 2026-09, v=app53)

`initMonsoonFX` now breathes with the content. Intensity is a continuous
value (0 gentle -> 1 full storm) eased per-frame toward a target set by
**martyr-zone overlap**: `.martyrs-strip`, `#martyrs-list`, `#memorial`,
`#victims-of-injustice` and the individual martyr sections. What changes:

- Rain: 35% -> 100% of the 220-drop pool; drops get longer, faster, heavier,
  more opaque; stroke width scales.
- Storm haze gradient + smoke opacity/speed scale up; vignette deepens
  (0.45 -> 0.85, overriding the CSS transition value).
- Embers fade out above intensity .6 (lamp-light gives way to storm).
- Lightning flicker above .92 intensity: white wash + steel-blue radial glow,
  every 3.5-9s, ~0.45s decay.

Tuning: zone list in `findZones()`, ease rate `dt*1.6`, drop pool `MAXD=220`,
flicker cadence `R(3.5,9)`. Verified: dim 0.46 gentle vs 0.84 in martyrs
section, flicker frames present in canvas samples, off-band pause intact.

### Language-gate intro removed from A ai chat (v=app54)

The "Select your language!" full-screen gate inside the chat window is no
longer shown by default: when no `aai_lang` is stored, the chat now calls
`setLang('en')` immediately, so users land straight on the greeting + input.
Nothing was deleted - the intro markup, EN/BN buttons and `setLang` remain,
so the gate can be re-enabled by removing that one `setLang('en');` call.
Language buttons, qs-unlock listener and stored-language behavior unchanged.
Verified: intro hidden on first open, greeting/input visible, Sayeedi query
answers with portrait, console clean. SHA recomputed for the app.js edit.

### FIGURES registry - data-only person additions (v=app55)

Adding a figure to the chatbot no longer requires code edits. Append one
object to the `FIGURES` array (in `assets/app.js`, next to the Sayeedi entry)
and `installFigures()` wires it up at load:

    FIGURES.push({
      id:'<slug>',
      match:['en substr','bn substr', ...],   // name mentions -> show portrait
      keys:['<slug>_bio', ...],               // cR keys that always show portrait
      photo:{ src, name, bn, dates, credit, link },
      entries:[ {key:'<slug>_bio', text:'EN | BN'}, ... ],
      aliases:[ ['alias phrase','<slug>_bio'], ... ]   // EN + BN
    });

- `entries` install into `cR`, `aliases` into `aliasMap` (longest-alias
  matcher handles the rest - answer formatting, confidence, followups).
- `martyrPhotoHTML` now calls the generic `figurePhotoHTML(k,m)`; the
  hand-written Sayeedi branch was removed. Sayeedi became the first registry
  entry (1 photo, 3 entries, 28 aliases) - output verified identical to the
  old hard-coded path.
- All-in-one builds: `installFigures()` runs before any user input, so
  registry entries work identically in the merged file; the portrait rides
  the existing `__AIIM` error-swap (confirmed: assets path -> data URI,
  282px rendered).

### Sayeedi Memorial Record page (memorial-sayeedi.html)

New printable bilingual memorial record for Delwar Hossain Sayeedi (1940-2023),
modeled on memorial-abrar.html, sourced from the English + Bangla Wikipedia
articles.

- **Standalone file** (`memorial-sayeedi.html`): self-contained A4 print page -
  @page rules, print hero with floating portrait (assets/img/sayeedi.png),
  facts table (9 rows), 7 bilingual sections (early life incl. the Jessore/
  Pirojpur competing accounts, political career, 1971 accusations + ICT-1
  trial with the mistaken-identity defence and intl. criticism, death,
  40+ books), both Wikipedia sources credited, Print/Save-as-PDF button.
  Green accent (#047857/#10b981) vs abrar's red - record, not tragedy.
- **In-section dark header** (`.rec-head`): abrar's merged block starts with a
  name header that lives inside the section (extractor-safe), so Sayeedi got
  the same - "Reference Archive / Delwar Hossain Sayeedi" + bilingual byline.
  Hidden in @media print so it never duplicates the print hero.
- **Build integration**: registered in build_allinone.py PAGES (between
  memorial-abrar and blueprints) -> merged block `#pg-memorial-sayeedi` with
  band; NOT added to build_pages.py (it's a standalone print page, no shared
  chrome - same treatment as memorial-abrar).
- **Entry points**:
  - Footer "About" column: "Sayeedi Memorial Record" link in all 8 production
    pages + bak-slim (-> auto-rewritten to #pg-memorial-sayeedi in the merge).
  - Chat: sayeedi_bio EN + BN entries end with a printable-record link
    (innerHTML-rendered, so it works; convert_page_links rewrites it in the
    all-in-one).
- **Plumbing**: app.js changed (chat link) -> EXPECTED_APP_SHA recomputed
  (edc4ea96...), cache token v=app55 -> v=app56 on all pages + builders.
  Rebuild: build_standalone.py -> repair bak-standalone -> build_allinone.py
  (9,229,231 bytes, 35/35 images embedded).
- **Verified live**: merged block renders (7 sections, 9-row table, 13 bn
  paragraphs), rec-head + band visible, footer + chat links resolve, portrait
  swaps to data URI, July-band image 404s are the expected lazy-load->swap
  pattern (41/41 swapped, zero broken).

### July monsoon rumble (opt-in storm audio)

A `#rumbleToggle` button (storm icon, injected by app.js next to #soundToggle
on July-capable pages only) starts a generated Web Audio storm bed:
looped brown noise -> 120 Hz lowpass -> gain. The gain continuously follows
the monsoon engine's storm intensity (setTargetAtTime, 0.4s smoothing):
0 in gentle rain, ~0.5 at full martyrs storm, curve = st^1.5 * 0.5.

- **Off by default, per-session**: no autoplay risk, no persistence - every
  load starts silent; the user must click (which also satisfies the autoplay
  gesture requirement). Nothing plays until clicked.
- **Sync**: the monsoon frame() loop publishes `window.__monsoonIntensity`
  and calls `RumbleFX.setIntensity(st)` every frame; exiting the July band
  (IO exit) or hiding the tab forces intensity 0 so the rumble always fades -
  no frozen-mid-storm audio on Back-to-top/Home jumps.
- **Lifecycle verified live** (all-in-one build, real clicks): off by default;
  enable -> ctx running; gentle hero -> gain 0; martyrs strip -> intensity
  0.99, gain 0.48; jump to pg-home -> intensity 0, gain -> 0.001; toggle off
  -> silent. Tab-hidden suspends the AudioContext.
- **Not a real storm recording**: synthesized noise (no audio files, no CDN,
  CSP-safe, works offline/file://). Toggle styling: .on state glows steel-blue.
- **Plumbing**: EXPECTED_APP_SHA recomputed (1c13131d...), tokens v=app58,
  both artifacts rebuilt (9,233,970 bytes all-in-one, 35/35 images).
- `RumbleFX.dbg()` console getter returns {on, ctx, gain} for quick checks.

### Cinematic scroll reveals ("emerge from the rain")

July-band timeline items, martyr-strip cards, and martyr cards (89 total)
now rise out of the rain as you scroll: fade + 34px rise + blur(7px)->sharp
(.9s signature easing), with a per-container sibling stagger.

- **Fail-safe by construction**: the new `.cin` / `.cin-done` classes are
  added at RUNTIME by initCinematicFX() (app.js) - the CSS only styles
  JS-added classes, so without JS (or if app.js ever fails to parse again)
  every element renders fully visible. Verified 0 `.cin` in page sources.
- **Scope**: only the July page (all-in-one `#pg-july` or standalone
  `july.html` filename match) - home's own timeline is untouched (no rain,
  no metaphor). Disabled under prefers-reduced-motion (CSS + early return).
- **Stagger**: cards animate in sibling batches - delay = (index % 8) * 80ms
  (0-560ms cycling window), so the 68-card grid reveals in waves instead of
  one 5s+ cascade. Timeline items: sequential 0-450ms cap.
- **One-shot**: each element reveals once (observer unobserves after
  .cin-done); rootMargin -8% bottom so cards complete their rise on screen.
- **Verified live**: all-in-one preview - before scroll opacity 0/blur 7px,
  after .cin-done opacity 1/sharp, stagger windows cycling (480->80->320ms);
  standalone july.html via headless Edge file:// - all 89 marked at runtime.
- **Plumbing**: EXPECTED_APP_SHA (ddba6c22...), tokens v=app59/v=css29,
  both artifacts rebuilt (9,236,745 bytes all-in-one).

### memorial-sayeedi.html screen/print header polish

The page showed the name/dates twice on screen (print hero + in-section
.rec-head). Fix: `@media screen { .mem-hero { display:none } }` - screen now
shows only .rec-head + floating portrait; print shows only the print hero
(.rec-head already print-hidden). The all-in-one merged block is unaffected
(extractor drops the page <head>, block unchanged - no rebuild needed).

### FIGURES refactor completed — all 15 figures data-driven (v=app60)

**Registry now owns every figure.** The earlier Sayeedi-only registry was extended
to the whole roster: 15 `FIGURES.push({...})` entries — Sayeedi, Hadi, Abu Sayed,
Abrar, Felani, Nafiz, Farhan, Wasim, Mugdho, Nazrul + the 5 student coordinators
(Nahid, Asif, Mahfuj, Sarjis, Hasnat). Migrated mechanically (verbatim literals):
30 `cR` knowledge lines, ~251 alias pairs, and all 11 bespoke `martyrPhotoHTML`
branches (incl. `coordMap`). The function is now a thin generic renderer
(`figurePhotoHTML`); schema additions carry what the old branches knew:
`keyPrefix` matching (e.g. any `hadi_*` key shows Hadi's portrait), per-figure
`accent` RGB, `extras` (protest/funeral grids, grave/memorial photos), and
`note` ("no free portrait exists").

**Live-verified behaviorally** (real chat UI, not string checks):
15 figures / 1760 aliases / 815 KB keys installed at runtime; tested
`osman hadi` (EN), `who is delwar hossain sayeedi` (EN), `সাঈদী কে` (BN),
`tell me about abu sayed`, `felani`, `nahid islam`, `সাঈদীর বিচার` (BN) —
all answered with the correct bilingual portrait card and embedded image.

**Build bug found & fixed: double `__AIIM` map (17.4 MB all-in-one).**
`build_standalone.py` backs up the *current* `index.html` to
`_archive/index.html.bak-standalone` BEFORE rebuilding it — so once a run
started from an all-in-one `index.html` (9.2 MB with the inlined image map),
it archived a merged file as the "standalone skeleton". The next
`build_allinone.py` then inlined the map a second time: 2 adjacent map
declarations, 15.1 MB of base64 (every blob duplicated), doubled file size.
The symptom that surfaced it: only `build_standalone` had been re-run after
app.js changes, so `index.html` was a 1.04 MB unmerged file whose images all
404'd (no `__AIIM` fallback). **Repair = run `build_standalone.py` TWICE
(first fixes index.html, second fixes the backup), then `build_allinone.py`.**
Verified: 9.23 MB, exactly 1 `window.__AIIM`, 35/35 images covered, 0 broken.

**Adding a figure remains one data object** — see the template above; no code
edits, no renderer branches. Housekeeping: `EXPECTED_APP_SHA` = `d9abd581…`
(matches disk), tokens `v=app60` on all 8 pages + builders, both artifacts
rebuilt, console clean apart from the 2 known integrity-probe 404s.

### Multi-page-first structure (user request: "less cluttered")

**The site is now genuinely multi-page.** `build_allinone.py` previously
overwrote `index.html` with the 15-page merged monolith (9.2 MB), so the
site's front door was the crowded single-file artifact even though the
dedicated pages existed. Retargeted: the merge now writes **`all-in-one.html`**
(a portability/QA artifact), and `index.html` is the clean 1.04 MB standalone
Home (8 focused sections: hero, quick-access, problem, solution, flow,
impact, partners, nationwide) linking to 8 separate pages + the Sayeedi
memorial record via nav/footer. Build chain: `build_standalone.py` ×2
(repairs index.html then the backup) → `build_allinone.py` → `all-in-one.html`.
Added a skeleton-poisoning guard in `build_allinone.py` (aborts if the backup
contains `__AIIM` or exceeds 4 MB, with the double-run repair instructions) —
closes the double-map bug class permanently. Verified via headless Edge on
real file:// URLs: index (840 KB DOM), about, july, ai, all-in-one all render
with title + chat + hero; home preview shows exactly 8 sections, nav to 8
pages, no monsoon on home (July-only effect, as designed), console clean
(1 known integrity-probe 404).

### "Monsoon of July" war layer: blood rain, gunfire flashes, crack audio (v=app61)

Extended the July monsoon engine with the requested blood/gunfire drama, kept
ambient + opt-in-audio so it stays memorial, not gore re-enactment:

**Visuals (canvas, storm-driven):**
- Blood-tinted rain: above intensity 0.55 the drop color blends
  slate `rgba(203,213,225)` → `rgba(225,70,80)`; the storm haze's bottom
  gradient shifts toward deep blood-red `rgba(76,10,18)`.
- Blood drips: at intensity ≥ 0.75 ten slow drips run down the viewport
  (38–85 px/s, `rgba(153,27,27)` trail + `rgba(127,29,29)` bead); dissolve
  below 0.5. Reads as rain-on-glass, not splatter.
- Distant gunfire: while intensity > 0.6, muzzle flashes spawn every
  1.2–4 s (scaled by storm) in the upper third — warm radial flash
  (`#fef3c7`→`#fbbf24`, 110 ms) + white core, 30% also fire a tracer streak.
  Each spawn calls `RumbleFX.crack(x)`.

**Audio (all behind the existing rumble toggle — off by default):**
- `RumbleFX.crack(pan)`: synthesized distant gunshot — 0.28 s noise burst
  (35 ms exponential decay) through a 900 Hz lowpass (gain 0.22–0.32),
  stereo-panned to the flash position, plus a 140→50 Hz sine thump. No audio
  files; CSP-safe, works offline/file://.
- Toggle labels updated to "July storm sound (rumble + distant gunfire)".

**Knobs:** blood ramp start (0.55) / drip gate (0.75) / flash gate (0.6) in
`initMonsoonFX`; flash cadence `R(1.2,4)/(0.5+0.5*st)`; crack loudness
`0.22+rand*0.1` and thump `0.28` in `RumbleFX.crack`. `window.__monsoonDbg()`
returns `{st, fl, dr}` for live probing.

**Verified:** merged build at martyrs zone → st 1.0, 10 drips alive, flashes
spawning (peak-1-alive sampling; 110 ms TTL), real spawn path invoked
`RumbleFX.crack` (proxy count 1), rumble gain 0.42 at storm with ctx running,
1800 red-dominant pixels in canvas samples, screenshot shows red rain over
the martyrs' gallery; standalone july.html file:// renders canvas + toggle at
v=app61. Console clean (known lazy-image 404s only).
**Plumbing:** `EXPECTED_APP_SHA` → `d7670668…` (64-hex, matches disk), tokens
`v=app61` on 8 pages + builders, chain rebuilt (standalone ×2 →
all-in-one.html 9.24 MB; index.html untouched as clean Home).

### Peak-battle crest at the Abu Sayed section (app64, SHA cd332fc4…)

**What it does**: scrolling the Abu Sayed martyr-strip card into the viewport fires one synced crest — storm intensity ramps to max in ~0.9s, HOLDS at full for ~3.2s, then eases back over ~2.6s to whatever the zone model says. Gunfire cadence multiplies ×4.5 during the crest (flNext divisor `(1+3.5*pLevel)`) and each flash bursts 1–2 extra spawns at high pLevel, so peak reads as a dense firefight: measured 4.0 cracks/s at peak vs 1.0/s baseline (3.8×) on the real audio path. Fires once per entry (re-arms only after leaving the card's viewport band); works in both the merged build and standalone july.html.

**Tuning knobs** (all in `initMonsoonFX`, ~line 1131 of assets/app.js): `PEAK_RAMP_S`, `PEAK_HOLD_S`, `PEAK_EASE_S`; density multiplier `3.5` in the cadence patch; burst thresholds `pLevel>0.5→2, >0.15→1`.

**Two real bugs found and fixed while integrating**:
1. **Standalone storm never reached the martyrs sections**: the engine's IntersectionObserver gated the rAF loop to the page hero only, so on july.html the storm *stopped* once you scrolled past the hero (merged build was unaffected — it observes the whole #pg-july band). Fixed by observing hero + all martyr zones on standalone.
2. **IO batch-cancellation**: first fix used a +/- counter, but IO's initial batch mixes intersecting and non-intersecting entries — the first `false` ate the hero's `+1` and the engine never started. Rewritten with per-target `liveMap` tracking. Verified via headless-Edge probes (`iz=1, pkOn=true` on standalone; engine diagnostics `__monsoonDbg()` now expose `pk`, `pkOn`, `pkT`, `zn`, `iz` permanently).

**Test-environment note**: headless `--dump-dom` runs throttle rAF so the eased curve freezes after a few frames — full curve verification was done in the live preview (maxPk=1.00, 9 samples pinned at peak, ease observed). Headless probes are valid for trigger/gating logic, not for timing.

**Plumbing**: `EXPECTED_APP_SHA` → `cd332fc4…` matching disk, tokens `v=app64` on 8 pages + builders, chain rebuilt (standalone ×2 → index.html 1.03 MB clean Home; all-in-one.html 9.23 MB, single image map, 35/35 images). Console clean apart from the known lazy-image 404→data-URI swaps.

### War effects intensified (app65, SHA 436d88ee…)

**What changed** (all in `initMonsoonFX` + `RumbleFX.crack`, assets/app.js):
- **Flash cadence**: R(1.2,4)s → R(0.7,2.2)s per flash — measured 0.90/s at storm (was ~0.4/s); with the crest multiplier unchanged, peak now measures **6.0 cracks/s (was 4.0)**, 32 cracks in a 9.5s crest window (was ~17).
- **Blood drips**: 10 → 22, faster (55–130 px/s vs 38–85), longer (34–80px), slightly thicker; engage earlier (st>0.7 vs 0.75) with alpha ramp widened to match.
- **Red saturation**: rain stroke at full storm now ~rgb(220,52,60) (was 225,70,80) and horizon haze ~rgb(76,6,16) (was 76,10,18) — deeper, less pink, more blood.
- **Crack audio**: gain 0.22–0.32 → 0.34–0.50, lowpass 900→1100 Hz (sharper snap), thump 0.28→0.42 at 120→45 Hz sweep (deeper). Thunder flicker cadence also up (R(2.6,6.5)s).
- **New limiter**: a DynamicsCompressor (threshold −12dB, ratio 8, 2ms attack) on the audio bus between rumble gain and destination, with cracks/thump routed through it — the louder cracks plus dense crest bursts can no longer clip.

**Verified live** (all-in-one preview, storm + crest): st=1.00 with 22 drips, 0.90 flashes/s baseline, 6.0 cracks/s at crest, audio context running at gain 0.5, red-dominant pixels on canvas probe, screenshot shows vivid red streaks + a drip crawling down the Abu Sayed portrait. Console clean apart from the known lazy-image 404→data-URI swaps; 0 broken images.

**Plumbing**: `EXPECTED_APP_SHA` → `436d88ee…` matching, tokens `v=app65` on 8 pages + builders, chain rebuilt (standalone ×2 → index.html 1.03 MB Home; all-in-one.html 9.23 MB, single map, 35/35 images).

**If it's now TOO much**, the reverse knobs are: cadence `R(0.7,2.2)`, drip count `<22` + speed range, rain red `190+30*bt / 200-148*bt / 212-152*bt`, crack gain `0.34+rand*0.16`, thump `0.42`.

### Rooftop battle line (app67, SHA 8e5a51a8…)

**What changed**: gunfire flashes no longer spawn randomly across the upper sky — they now pin to a **generated rooftop skyline** drawn on the canvas horizon, so the fight reads as one distant battle line.

- **Skyline model**: per-load, seeded by Math.random — 6+ building silhouettes (46–150px wide, 6–18.5% of viewport height) with random gaps, roofline at 78% of viewport height; rebuilt on resize. `__monsoonDbg().bld` exposes the count.
- **Flash placement**: main flashes spawn at rooflines (`skySpot()` picks a building, then a point along its roof edge, ±6px vertical jitter); **18% are street-level blooms** in the gaps between buildings (y = horizon +24–64px) so the line has depth, not one laser-straight row. Crest bursts walk the same line.
- **Tracers flatten**: vertical velocity ×0.4 so arcs skim the horizon instead of flying up into the sky.
- **Silhouettes drawn** just above the storm haze at `rgba(4,9,20, 0.55+0.25*st)` — dark masses that deepen with the storm; content above them (cards, photos) is untouched, they live inside the fixed canvas layer.

**Verified**: sampled 40 live flash Y-positions at storm — all within 404–578px on a 672px viewport, i.e. exactly the roofline band (horizon 524 minus building heights) plus street blooms; the old code would have put them at 81–202px (open sky). Screenshot confirms the horizon masses behind the content.

**Probe lessons (test artifacts, not bugs)**: canvas pixel probes must scale by devicePixelRatio, not raw width (first 0%-pinned readout sampled the wrong region); a ±80px band undercounts tall-building rooflines. The `fys` array in `__monsoonDbg()` (up to 8 live flash Ys) is now the canonical way to verify placement.

**Plumbing**: `EXPECTED_APP_SHA` → `8e5a51a8…` matching, tokens `v=app67` everywhere, chain rebuilt (standalone ×2 → index.html 1.03 MB; all-in-one.html 9.23 MB, single map, 35/35 images). Note: standalone pages carry app.js externally — grep for engine symbols in the .py/all-in-one, not in page HTML.

**Tuning knobs**: building height range `Rsd(0.06,0.185)`, roofline `ROOFY=innerHeight*0.78`, street-bloom probability `Math.random()<0.18`, silhouette alpha `0.55+0.25*st`.

### Skyline silhouettes removed + FIGURES text corruption repaired (app68, SHA 29013d39…)

**1. Gray/black blocks over "Victims of Injustice" removed (user report, screenshot).**
The rooftop-skyline *drawing* in `initMonsoonFX` (dark `rgba(4,9,20,...)` building
rectangles on the canvas horizon) read as ugly slabs over light page bands. The
draw block was deleted; the **invisible roofline placement math stays**
(`buildSky()`/`skySpot()`/`ROOFY`), so gunfire flashes still pin to a horizon
battle line — only the visible silhouettes are gone. Verified live: silhouette
code absent from the running page, sampled canvas horizon row is a smooth
gradient (2 dark transitions = vignette edges, not rectangles), screenshot clean.

**2. Chat replies rendered literal `\u0986` garbage + stray quotes (user report).**
The migrated FIGURES registry entries had been written through an extra escaping
pass: 2,861 double-escaped `\uXXXX` sequences (Abrar, Mir Mugdho, Nazrul entries
+ Bengali aliases; `\u2019` in Nafiz/Farhan/Wasim) and 29 entries wrapped in
stray quote pairs (`text:"..."` with literal quote chars — also Abu Sayed bio +
the 5 coordinator bios). Repair script decoded every sequence to real UTF-8 and
stripped the wrappers (scoped to the FIGURES block, legacy `cR` untouched).
Verified live: "Abrar Fahad" and the Bengali alias both answer with clean
bilingual text + portrait card; zero escape sequences; no stray quotes. JS
parses and the chat engine runs (live probes).

**Plumbing**: `EXPECTED_APP_SHA` -> `29013d39…` (matches disk), tokens
`v=app68` on 8 pages + `build_pages.py`, chain rebuilt (standalone x2 ->
index.html 1.03 MB Home; all-in-one.html 9.22 MB, single `__AIIM`, 35/35
images).

**Rule for future FIGURES additions**: write real UTF-8 characters (actual
Bengali), never JSON-escaped `\uXXXX` sequences, and never quote-wrap entry
text values.

### Corruption guard + full regression sweep (app69, SHA 4116de60…)

**check_figures.py (permanent guard).** Fails (exit 1) if the FIGURES block in
`assets/app.js` contains escaped `\uXXXX` sequences, stray quote-wrapped entry
texts, or any raw backslash (plain string ops only - no regex escaping
hazards). Wired into the top of BOTH `build_standalone.py` and
`build_allinone.py`, so a poisoned registry can no longer reach a build.
Negative-tested: poisoning the block flips the guard to exit 1 and both
builders would abort; restoring passes.

**Second repair pass.** The guard immediately caught 107 *single*-escaped
`\uXXXX` sequences the first repair had left (valid JS - the browser decodes
them - but the same corruption class in dormant form; all Bengali chars:
\u09be x18, \u09a6 x7, ...). Decoded to real UTF-8; the FIGURES block now has
ZERO backslashes and the guard passes clean (16 figures).

**20-query live regression sweep (all-in-one, real chat UI).** All 15 figures
queried in EN + 5 in BN (osman hadi, sayeedi, abu sayed, abrar, felani, nafiz,
farhan, wasim, mugdho, nazrul, nahid, asif, mahfuj, sarjis, hasnat / \u09b8\u09be\u0988\u09a6\u09c0 \u0995\u09c7,
\u0986\u09ac\u09b0\u09be\u09b0 \u09ab\u09be\u09b9\u09be\u09a6, \u09ae\u09bf\u09b0 \u09ae\u09c1\u0997\u09cd\u09a7, \u09a8\u09be\u09b9\u09bf\u09a6 \u0987\u09b8\u09b2\u09be\u09ae, \u0986\u09ac\u09c1 \u09b8\u09be\u0888\u09a6):
zero escape garbage, zero stray quotes, zero errors, every figure mentioned by
name. Portraits: 20/20 rendered, all swapped to embedded data URIs (note: the
swap is lazy - a portrait behind a closed chat window loads only when fetched;
forcing load confirmed 100% swap).

**Battle line verified without silhouettes.** 48 live flash Y-samples at full
storm (25ms collector - the 110ms flash TTL defeats 500ms polling), ALL inside
the roofline band [390,594]px on a 672px viewport; 12 crack() calls through a
proxied real audio path with plausible pans. Flashes still read as one distant
battle line; the ugly slabs stay gone.

**Plumbing**: `EXPECTED_APP_SHA` -> `4116de60\u2026`, tokens `v=app69` on 8 pages
+ builders, chain rebuilt (standalone x2 -> index.html 1.03 MB; all-in-one.html
9.22 MB, single map, 35/35 images).

### Git-merge repair for index.html (2026-09-06 22:02-22:20)

An external git merge/pull (not run by the agent) left index.html with 20
unresolved conflict-marker hunks (44 marker lines, mangled <title>, old
heading + EU badge resurrected, ancient tokens v=app45, hard 404s).
assets/app.js was also swapped to a merged variant (sha 5e78fd2a) -
inspected and confirmed it RETAINS all repairs (clean FIGURES registry with
zero backslashes, no skyline draw, full monsoon/RumbleFX engine) plus
merged-in additions; only the SHA bookkeeping was stale. All other pages,
both archive sources, and the builder guards survived intact.

Repair (no git state touched - merge left for the user to resolve):
1. security.js EXPECTED_APP_SHA recomputed -> 5e78fd2a (sync restored).
2. Cache tokens unified v=app45/v=app69 -> v=app70 on all 9 pages.
3. Full chain rebuild: build_standalone.py x2 -> build_allinone.py.
4. Live-verified: 8 unique sections, title fixed, 11/11 nav links, chat
   answers cleanly with portrait card, console clean (1 known probe 404).

NOTE: your git working tree is mid-merge (run.md still shows AA/conflicted
state). Finish the merge with git add + git commit when ready; the files on
disk are now consistent.
