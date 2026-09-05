# DLA Website — Multi-Page Architecture

**Site type:** Civic legal-aid platform (Digital Legal Aid, Bangladesh) — services, AI tools,
government directory, memorial/awareness content, contact channels.

**Core principle:** one page = one job. The old single-page monolith (7,300+ lines, ~20 sections)
became 9 focused pages. Each page answers one question; everything else lives elsewhere or in the footer.

---

## 1. Page Structure (9 pages, each with a distinct purpose)

| # | Page | Question it answers | Primary CTA |
|---|------|--------------------|-------------|
| 1 | `index.html` — **Home** | What is DLA and where do I start? | "Get Legal Help" |
| 2 | `ai.html` — **A ai Platform** | What AI tools do I get? | Launch platform / personas |
| 3 | `justice.html` — **Justice Map** | Where is legal help near me? | Open the map |
| 4 | `sheguard.html` — **SheGuard X** | How do women get emergency protection? | SOS / interactive suite |
| 5 | `government.html` — **Government** | Which office/service do I need? | Directory lookup |
| 6 | `contact.html` — **Contact** | How do I reach a human? | Complaint desk form |
| 7 | `about.html` — **About & Mission** | Who is behind this and why? | Read the mission |
| 8 | `july.html` — **July 2024** | What happened in July, and who are the martyrs? | Explore memorial |
| 9 | `blueprints.html` — **Visionary Blueprints** | What is the long-term vision? | Browse blueprints |

Supporting (not in nav, linked from pages):
- `female-safety.html` — self-contained interactive engine, embedded by `sheguard.html` via iframe.
- `_archive/` — superseded prototypes (`government-homepage`, `hadi`) kept for reference, never linked.

**Rule:** a page earns a nav slot only if a first-time visitor needs it within one session.

---

## 2. Content Distribution (what goes where — and what stays out)

### Home (`index.html`) — the lobby, not the warehouse
- Hero: one headline, one subline, primary + secondary CTA
- 3–4 capability cards → each links to its real page (never duplicate the feature page on Home)
- Compact stats strip (tabular numerals, one row)
- Emergency ticker (hotlines: 999, 109, 16430 …) — site-wide chrome
- **Not on Home:** full feature tours, memorials, blueprints, district grids

### `ai.html` — the product page
- Platform intro + personas, feature grid, quick access
- One demo surface; deep docs stay out

### `justice.html` — the map
- Map front and center; legend and filters adjacent; no marketing copy

### `sheguard.html` — the shield
- Overview + the interactive SheGuard suite (SOS, vault, FIR) via the iframe engine
- Safety-first copy; links out to `july.html` only for context

### `government.html` — the directory
- Service/office lookup; plain labels; hotlines table

### `contact.html` — the desk
- Complaint form (bilingual labels), direct channels, expectations ("we reply in X")
- No unrelated promos

### `about.html` — the story
- Mission, vision, roadmap; national-identity content (Kazi Nazrul Islam tribute lives here)
- Team/institutional info; links to July 2024 for memorial context

### `july.html` — the memorial
- Timeline of July 2024; martyr cards (Abu Sayed, Mir Mugdho …) each with portrait + bio;
  Hadi tribute; Abrar Fahad memorial; victims section; gallery
- Emotional pacing: quiet background, generous whitespace

### `blueprints.html` — the horizon
- Visionary chapters (incl. the futuristic chapter); progressive disclosure
  (`<details>`-style expanders) so the page stays scannable

---

## 3. Navigation System

### Top strip (site-wide): emergency ticker
Rotating hotlines with `tel:` links — actionable from any page, no navigation cost.

### Header: 6 flat items + 1 dropdown (7 ± 2 rule)
```
[Logo: A ai]   Home  A ai Platform  Justice Map  SheGuard X  Government  Contact  [Discover ▾]   [Login] [Get Legal Help]
                                                            ├ About & Mission → about.html
                                                            ├ July 2024      → july.html
                                                            └ Visionary Blueprints → blueprints.html
```
- Glass bar on scroll; active page gets a gradient underline (never a different color system)
- **One** persistent primary CTA ("Get Legal Help") — same place, every page
- Login secondary — outlined, visually quieter than the CTA
- Mobile: hamburger → full-screen drawer, same order, same CTAs

### Footer: 3 columns
1. **Explore** — all 9 pages (nav pages + About/July/Blueprints)
2. **Memory & Mission** — memorial links (`july.html#abrar-fahad`, `about.html#nazrul`, …)
3. **Identity** — logo, one-line mission, legal/social links
Mirror of the nav plus the "second ring" pages — no orphan pages.

---

## 4. UI/UX Rules (the noise-killers)

**Layout**
- One H1 per page; sections in a strict `Kicker → Headline → Text → Action` rhythm
- Max ~75 characters per line; 1.6+ line-height; section padding ≥ 96px
- One accent gradient (sky→indigo); amber reserved for memorials/tributes, red for emergencies

**Components**
- Glass cards with a glowing top hairline; hover lifts 4px — nothing else moves
- Buttons: one glowing primary style, one ghost secondary; a sheen sweep on hover
- Progressive disclosure for long content (blueprint chapters, FAQ): expanders, not walls

**Feedback & state**
- `:focus-visible` rings everywhere (keyboard parity)
- Tabular numerals + soft glow for stats; skeletons or 300ms thinking animation, never frozen UI
- `prefers-reduced-motion` kill-switch for every animation

**Consistency plumbing**
- Shared `assets/styles.css` + `assets/app.js` (cache-busted on every change: `?v=cssNN` / `?v=appNN`)
- Shared favicon; theme toggle applies `light` to **both** `html` and `body`; dark is default
- Chat FAB site-wide: one widget, one initialization (watch for double `app.js` includes)

**Anti-clutter checklist (apply before adding anything)**
1. Does this have its own page? If yes → link, don't embed.
2. Can it be a card that links out instead of a full section?
3. Does the page still say its one sentence after adding this?
4. Is it reachable within 2 clicks of Home via nav or footer?
5. Mobile check: does the section stack to a single column without horizontal scroll?
