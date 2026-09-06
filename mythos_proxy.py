#!/usr/bin/env python3
"""
mythos_proxy.py - local proxy that lets the A ai chat call a frontier model
(Anthropic Messages API) with the API key kept server-side.

Run (one terminal):
    export ANTHROPIC_API_KEY=sk-ant-...
    python mythos_proxy.py            # listens on 127.0.0.1:8787

Optional env:
    ANTHROPIC_BASE_URL=https://api.anthropic.com   # override for gateways/mocks
    MYTHOS_MODEL=claude-sonnet-4-5                 # model id
    MYTHOS_HOST=127.0.0.1  MYTHOS_PORT=8787  MYTHOS_TIMEOUT=60

The site auto-detects the proxy on load (/health). If it is not running, or no
key is configured, the chat silently keeps using the built-in local engine.
"""
import json
import os
import sys
import threading
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST = os.environ.get("MYTHOS_HOST", "127.0.0.1")
PORT = int(os.environ.get("MYTHOS_PORT", "8787"))
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "").strip()
BASE = os.environ.get("ANTHROPIC_BASE_URL", "https://api.anthropic.com").rstrip("/")
MODEL = os.environ.get("MYTHOS_MODEL", "claude-sonnet-4-5").strip()
VERSION = os.environ.get("ANTHROPIC_VERSION", "2023-06-01")
TIMEOUT = int(os.environ.get("MYTHOS_TIMEOUT", "60"))

PROMPT_SYS = (
    "You are A ai, the authoritative AI legal assistant of this website, which "
    "covers the Constitution of Bangladesh, courts in all 64 districts, public "
    "administration and reforms, anti-corruption, women-safety law, and the "
    "July 2024 movement archive.\n\n"
    "Below is GROUND KNOWLEDGE produced by the site's own legal database. It is "
    "the only source you may cite. Do not invent statutes, citations, phone "
    "numbers, or case outcomes that are not in the ground knowledge. If the "
    "ground knowledge does not cover the question, say so plainly and point the "
    "user to the right official route (police 999, women helpline 109, legal aid "
    "16430, ACC 106/333) instead of guessing.\n\n"
    "<ground_knowledge>\n{context}\n</ground_knowledge>\n\n"
    "Reply in {language}. Keep the answer under ~180 words unless detail is "
    "needed. Answer strictly as JSON with exactly this shape and nothing else:\n"
    '{{"steps":[{{"tag":"...","text":"..."}}],"answer":"...","confidence":0}}'
    "\nsteps: 3-6 short reasoning steps (tags like Intent, Knowledge Lookup, "
    "Grounding Check, Reasoning, Synthesis). answer: the plain-text reply "
    "(no markdown). confidence: 0-100 number for how well the ground knowledge "
    "supports the answer."
)


def extract_json(text):
    """Pull the first balanced JSON object out of a model reply."""
    try:
        return json.loads(text)
    except Exception:
        pass
    start = text.find("{")
    if start < 0:
        raise ValueError("no JSON object in model reply")
    depth = 0
    in_str = False
    esc = False
    for i in range(start, len(text)):
        ch = text[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return json.loads(text[start : i + 1])
    raise ValueError("unbalanced JSON in model reply")


def call_model(question, language, context):
    system = PROMPT_SYS.format(context=(context or "(none provided)"), language=language)
    body = {
        "model": MODEL,
        "max_tokens": 1600,
        "temperature": 0.3,
        "system": system,
        "messages": [{"role": "user", "content": question}],
    }
    req = urllib.request.Request(
        BASE + "/v1/messages",
        data=json.dumps(body).encode("utf-8"),
        method="POST",
        headers={
            "content-type": "application/json",
            "x-api-key": API_KEY,
            "anthropic-version": VERSION,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            raw = resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:500]
        raise RuntimeError("upstream HTTP %s: %s" % (e.code, detail)) from e
    data = json.loads(raw)
    if data.get("type") == "error":
        raise RuntimeError("upstream error: %s" % (data.get("error"),))
    text = "".join(
        b.get("text", "") for b in (data.get("content") or []) if b.get("type") == "text"
    )
    parsed = extract_json(text)
    steps = parsed.get("steps")
    if not isinstance(steps, list):
        steps = [{"tag": "Synthesis", "text": "Answer assembled"}]
    clean = []
    for s in steps[:8]:
        if isinstance(s, dict):
            clean.append({"tag": str(s.get("tag") or "Step"), "text": str(s.get("text") or "")})
    answer = str(parsed.get("answer") or "").strip()
    if not answer:
        raise ValueError("model returned no answer")
    conf = parsed.get("confidence")
    try:
        conf = max(0, min(99, int(float(conf))))
    except Exception:
        conf = 90
    return {"steps": clean, "answer": answer, "confidence": conf, "model": MODEL}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        sys.stderr.write("[mythos] " + (fmt % args) + "\n")

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Max-Age", "600")

    def _json(self, code, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._cors()
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        if self.path.split("?")[0] == "/health":
            self._json(
                200,
                {"ok": True, "configured": bool(API_KEY), "model": MODEL, "name": "mythos-proxy"},
            )
        else:
            self._json(404, {"error": "not found"})

    def do_POST(self):
        if self.path.split("?")[0] != "/v1/mythos":
            self._json(404, {"error": "not found"})
            return
        if not API_KEY:
            self._json(503, {"error": "proxy not configured: set ANTHROPIC_API_KEY"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length).decode("utf-8", "replace"))
            question = str(payload.get("question") or "").strip()
            if not question:
                self._json(400, {"error": "missing question"})
                return
            language = "Bengali" if payload.get("language") == "Bengali" else "English"
            context = str(payload.get("context") or "")
            result = call_model(question, language, context)
            self._json(200, result)
        except Exception as e:  # noqa: BLE001 - surface everything to the page
            self._json(502, {"error": str(e)})


def main():
    if not API_KEY:
        print("[mythos] WARNING: ANTHROPIC_API_KEY not set - /health will report configured=false")
    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    print("[mythos] listening on http://%s:%d  model=%s  key=%s" % (HOST, PORT, MODEL, "set" if API_KEY else "MISSING"))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[mythos] stopping")


if __name__ == "__main__":
    main()
