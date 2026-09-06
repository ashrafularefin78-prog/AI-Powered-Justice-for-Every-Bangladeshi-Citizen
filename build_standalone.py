# -*- coding: utf-8 -*-
"""
Standalone single-file builder.

Inlines all shared assets into index.html so it can be opened directly in a
browser (file://) for testing, mirroring the old _preview.html approach:

  * assets/styles.css   -> <style> block
  * assets/security.js  -> <script> block
  * assets/app.js       -> <script> block
  * assets/img/favicon.svg -> inline data: URI (the CSP only allows data: images)

The Google Fonts / Font Awesome CDN <link>s and the CSP meta tag are kept as-is
(the CSP already permits 'unsafe-inline' scripts/styles and data: images).

Run:  python build_standalone.py

Source of truth: _archive/index.html.bak-slim (the slim multi-page home, kept
forever in _archive). Each run rebuilds index.html as the standalone home from
that source and moves any previous index.html to
_archive/index.html.bak-standalone (which build_allinone.py consumes as its
skeleton). bak-slim is never overwritten, so the chain is idempotent.
"""
import base64
import os
import re
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)))

TITLE = 'A ai - Digital Legal Aid Bangladesh'


def read(p, binary=False):
    mode = 'rb' if binary else 'r'
    with open(p, mode, encoding=None if binary else 'utf-8') as f:
        return f.read()


def write(p, s):
    with open(p, 'w', encoding='utf-8') as f:
        f.write(s)


def inline_js(code):
    # Defensive: keep the inline <script> block from terminating early even if
    # the JS ever grows a literal "</script>" or "<!--" (script parsing hazard).
    return code.replace('</script>', '<\\/script>').replace('<!--', '<\\!--')


def main():
    # ---- corruption guard: never build from a poisoned FIGURES registry ----
    import subprocess
    g = subprocess.run([sys.executable, 'check_figures.py'])
    if g.returncode != 0:
        sys.exit('ABORT: check_figures.py failed - fix assets/app.js first.')

    # ---- stable sources (idempotent chain, never clobber the slim source) ----
    os.makedirs('_archive', exist_ok=True)
    SLIM = '_archive/index.html.bak-slim'
    if not os.path.exists(SLIM):
        sys.exit('ABORT: %s missing - nothing to build from' % SLIM)
    shutil.copyfile('index.html', '_archive/index.html.bak-standalone')
    print('backed up index.html -> _archive/index.html.bak-standalone')

    html = read(SLIM)  # always the slim multi-page home
    css = read('assets/styles.css')
    security_js = read('assets/security.js')
    app_js = read('assets/app.js')

    # ---- favicon as inline data URI ----
    fav = read('assets/img/favicon.svg')
    fav_b64 = base64.b64encode(fav.encode('utf-8')).decode('ascii')
    fav_uri = 'data:image/svg+xml;base64,' + fav_b64

    # ---- 1. fix the broken <title> (it currently wraps a <link> element) ----
    # and add the favicon link properly (as a data URI so it works under file://)
    html = re.sub(
        r'<title>.*?</title>',
        '<title>%s</title>\n<link rel="icon" type="image/svg+xml" href="%s">' % (TITLE, fav_uri),
        html, flags=re.S, count=1,
    )

    # NOTE: replacements are functions, not strings, so backslashes inside the
    # JS/CSS (e.g. app.js's \uXXXX escapes) are inserted literally instead of
    # being parsed as regex group escapes.

    # ---- 2. inline the stylesheet ----
    new_html, n_css = re.subn(
        r'<link rel="stylesheet" href="assets/styles\.css[^"]*">',
        lambda m: '<style>\n' + css + '\n</style>',
        html, count=1,
    )
    html = new_html

    # ---- 3. inline security.js (head) ----
    new_html, n_sec = re.subn(
        r'<script src="assets/security\.js[^"]*"></script>',
        lambda m: '<script>\n' + inline_js(security_js) + '\n</script>',
        html, count=1,
    )
    html = new_html

    # ---- 4. inline app.js (tail) ----
    new_html, n_app = re.subn(
        r'<script src="assets/app\.js[^"]*"></script>',
        lambda m: '<script>\n' + inline_js(app_js) + '\n</script>',
        html, count=1,
    )
    html = new_html

    # ---- report ----
    print('styles  inlined: %s' % ('ok' if n_css == 1 else '!! MISSED (%d)' % n_css))
    print('security inlined: %s' % ('ok' if n_sec == 1 else '!! MISSED (%d)' % n_sec))
    print('app.js  inlined: %s' % ('ok' if n_app == 1 else '!! MISSED (%d)' % n_app))
    if not (n_css == n_sec == n_app == 1):
        sys.exit('ABORT: one or more assets were not inlined; index.html NOT rewritten')

    write('index.html', html)
    print('wrote index.html (%d bytes)' % len(html.encode('utf-8')))


if __name__ == '__main__':
    main()