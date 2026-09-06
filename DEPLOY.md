# DLA Website — Deployment Checklist

Static multi-page site (HTML + CSS + JS). No build step required — deploy the
contents of `dla-website/` as-is to any static host.

## 1. Pre-flight (before every deploy)

- [ ] `python site_audit.py` — all pages print `OK` (asset refs, tag balance, script includes).
- [ ] No `_verify_*.html` or `_preview.html` or `_syntax_harness.html` or other scratch files in the site root (only the 10 pages + assets).
- [ ] No dead internal links: `python site_audit.py` reports `broken internal links: 0`.
- [ ] `sitemap.xml` domain matches the real domain (replace `dla.example.com`).
- [ ] `robots.txt` domain matches too.
- [ ] **If you edited `assets/app.js`:** recompute its SHA-256 and update `EXPECTED_APP_SHA`
      at the top of `assets/security.js`, or the Quantum Shield logs `TAMPER` on every load.
      Command: `python -c "import hashlib;print(hashlib.sha256(open('assets/app.js','rb').read()).hexdigest())"`
      (then bump `security.js?v=secNN` on all pages).
- [ ] Cache busters are bumped on scripts you changed:
  - `assets/app.js?v=appNN` and `assets/security.js?v=secNN` in **every** HTML file.
  - Grep: `grep -oh 'src="assets/[a-z]*\.js[^"]*"' *.html | sort | uniq -c`
    — counts must equal the number of pages including each script.

## 2. Browser smoke test (10 pages)

- [ ] Every nav item + dropdown item loads its page.
- [ ] Home: ticker, hero, cards, stats row render.
- [ ] Chat FAB opens on every page (exactly one widget).
- [ ] `july.html`: all 5 memorial sections (Abrar, Mugdho, Wasim, Farhan, Nafiz),
      martyrs strip cards scroll to their sections, gallery + lightbox work.
- [ ] `memorial-abrar.html`: opens, Print / Save-as-PDF produces clean A4 output.
- [ ] `contact.html`: form submits (mock/backend) and shows feedback.
- [ ] `about.html#nazrul`: tribute renders, portrait loads with attribution.
- [ ] `female-safety.html` loads inside SheGuard iframe (self-contained by design).
- [ ] Console: zero errors (missing favicon/robots is fine locally, they exist on server).

## 3. Chatbot QA (10 questions, both languages)

- [ ] "Who is Abu Sayed?" / "Who is Mir Mugdho?" / "পানি লাগবে পানি" — portrait card.
- [ ] "Who is Abrar Fahad?" / "আবরার হত্যাকাণ্ড" — portrait + justice detail.
- [ ] "Who was Wasim Akram?" — portrait card.
- [ ] "Who is Farhan Faiyaaz?" / "Who is Golam Nafiz?" / "গোলাম নাফিজ" — card.
- [ ] "Who is Kazi Nazrul Islam?" / "কাজী নজরুল ইসলাম কে" — sitar portrait card.
- [ ] A legal question (e.g. "how to file FIR") still routes to legal KB.
- [ ] Cell phone: same questions render (media queries, fonts load).

## 4. Deploy

- [ ] Upload the **contents** of `dla-website/` (keep `assets/` structure).
- [ ] Do **not** upload `_archive/`, `*.py`, `.log`, `.edge-http.log`, `_verify_*`.
- [ ] Serve with HTTPS; set `Cache-Control` for `assets/*` (fingerprinted via `?v=`).
- [ ] Push `sitemap.xml` to Search Console; confirm robots.txt resolves at `/robots.txt`.

## 5. Known intentional quirks (do not "fix")

- `female-safety.html` is a self-contained iframe engine — no styles.css/app.js
  by design; the audit flags it, that is expected.
- Audit JS brace/paren "imbalance" lines come from regex literals in inline
  scripts — verified false positives; the browser console is the source of truth.
- Preview sandbox logs 404s for local images (single-file preview serves only
  the HTML); on a real server all assets resolve.