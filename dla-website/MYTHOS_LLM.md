# Grounded LLM integration (currently DISABLED - no-api mode)

The chat currently runs in **no-api mode**: every answer is generated
entirely from the site's stored knowledge base (the local legal engine).
No network requests are made for answers, and the browser module never
probes or contacts the proxy.

## What exists on disk (kept for optional future re-enable)

- `mythos_proxy.py` - a dependency-free Python stdlib proxy that would
  forward chat questions to the Anthropic Messages API (key stays server-side).
- A browser-side LLM module in `assets/app.js` (and the inline copy in
  `index.html`) that would probe the proxy, ground questions in the local
  knowledge base, and fall back to the local engine on any failure.

## Re-enabling the API path later

1. In `assets/app.js` and the inline copy in `index.html`, restore the
   activation line:
   `try{probe();}catch(e){AAI.probeDone=true;}`
   (it is currently replaced by a no-op that keeps `llmEnabled=false`).
2. Run the proxy: `python mythos_proxy.py` with `ANTHROPIC_API_KEY` set
   (see proxy header comments for env vars: `ANTHROPIC_BASE_URL`,
   `MYTHOS_MODEL`, port/host/timeout).
3. The 8 multi-page files allow the loopback origin in their CSP
   `connect-src`; the single-file `index.html` has no CSP.
4. Bump the `app.js?v=` token on the 8 pages after changing app.js.

If a real request then fails (e.g. wrong model id), the chat falls back to
the local engine and logs the upstream error.
