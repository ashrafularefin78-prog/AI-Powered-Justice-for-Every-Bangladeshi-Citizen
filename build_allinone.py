# -*- coding: utf-8 -*-
"""
Whole-site single-file builder (all-in-one).

Merges every page of the multi-page site into ONE self-contained test artifact,
all-in-one.html, so the entire site can be opened in a browser (file://
double-click or over http) with no server and no cross-page links — the
previous "not found" problem. The real site stays multi-page: index.html is
rebuilt as the clean standalone Home by build_standalone.py; all-in-one.html
is a portability/QA artifact, not the site's front page.

Approach
--------
* Skeleton: the current standalone index.html (built by build_standalone.py),
  which already carries the inlined <style> (assets/styles.css), inlined
  security.js + app.js, data-URI favicon, CDN fonts, and the shared chrome
  (ticker / nav / drawer / auth modal / chat widget / footer).
* Each real page contributes only its unique middle — everything between its
  first <section> and its <footer> (includes the page's own inline <style>
  and <script> blocks).
* Page blocks are stacked in nav order, each wrapped in <div id="pg-<page>">,
  with a small label band. Nav / drawer / footer / CTA links that pointed at
  "page.html" or "page.html#anchor" are rewritten to "#pg-<page>" /
  "#pg-<page>-<anchor>" anchors.
* To avoid duplicate ids between pages, every content id is namespaced with a
  "pg-<page>-" prefix — EXCEPT ids the shared app.js queries by id (EXEMPT),
  which must keep their exact names to keep page widgets working.
* SheGuard's female-safety app stays an <iframe> but becomes fully inline via
  the srcdoc attribute (female-safety.html is self-contained: own <style>,
  own scripts, no external refs), so no second file is needed.
* A deliberately RELAXED CSP meta is injected (the strict per-page CSP would
  block sibling images and the srcdoc iframe under file:// because 'self' cannot
  match file: URLs). The relaxed policy still keeps the meaningful guardrails -
  object-src 'none', base-uri, form-action limited to http(s), and NO
  'unsafe-eval' - while permitting inline scripts/styles, data: URIs, file:
  images, about: srcdoc frames, fonts, and the local AI proxy. The real
  multi-page pages keep their original strict CSP untouched.

Build chain (idempotent):
  edit pages/assets -> python build_standalone.py  (writes standalone home +
      _archive/index.html.bak-standalone)
                     -> python build_allinone.py    (this script; skeleton =
      _archive/index.html.bak-standalone so re-running never double-merges;
      output is all-in-one.html — index.html is never overwritten)

Run:  python build_allinone.py   (run build_standalone.py first if assets changed)
"""
import base64
import html as html_mod
import os
import re
import sys

IMGDIR = 'assets/img'
MIME = {'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'png': 'image/png',
        'gif': 'image/gif', 'webp': 'image/webp', 'svg': 'image/svg+xml'}

# Relaxed CSP for the all-in-one LOCAL TEST file only. The strict per-page CSP
# ('self'-based) cannot work here: under file:// 'self' never matches sibling
# files, so it would block the relative image refs and the srcdoc iframe.
# Kept guardrails: object-src 'none', base-uri 'self', form-action limited to
# http(s)/self, no 'unsafe-eval' (nothing uses eval). Everything this single
# file actually needs is explicitly allowed: inline scripts/styles, data:
# images, file: images (folder present), about: srcdoc frames, CDN fonts, and
# the local AI proxy (http/ws 127.0.0.1:8787 / localhost:8787).
RELAXED_CSP = (
    "default-src 'self' data: blob: http: https: ws: wss:; "
    "script-src 'unsafe-inline' 'self' data: blob: http: https:; "
    "style-src 'unsafe-inline' 'self' http: https: data: blob:; "
    "img-src 'self' data: blob: file: http: https:; "
    "font-src 'self' data: http: https:; "
    "connect-src 'self' data: blob: http: https: ws: wss: "
    "http://127.0.0.1:8787 ws://127.0.0.1:8787 http://localhost:8787 ws://localhost:8787; "
    "media-src 'self' data: blob: http: https:; "
    "frame-src 'self' about: data: blob: http: https:; "
    "object-src 'none'; base-uri 'self'; form-action 'self' http: https:"
)

sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)))

TITLE = 'A ai - Digital Legal Aid Bangladesh'

# ids the shared app.js reads by id — never rename these (widgets depend on the
# exact names). Copied from the getElementById/querySelector scan of app.js.
APP_JS_IDS = (
    'asLocTxt', 'asRoleIcon', 'asRoleTxt', 'asSub', 'asTitle', 'authOverlay',
    'authSub', 'authSuccess', 'authTitle', 'authToast', 'backToTop', 'cbIntro',
    'cbMem', 'cbMemTxt', 'cbMenu', 'cbPop', 'chatFab', 'chatIn', 'chatMsgs',
    'chatWin', 'drawerClose', 'drawerOverlay', 'futuristic-tech', 'hamburger',
    'loginBtn', 'loginForm', 'loginNid', 'loginPhone', 'mapResultCount',
    'mapSearchInput', 'mapTooltip', 'mobileDrawer', 'nav', 'officerFields',
    'roleGeneral', 'roleOfficer', 'scrollProgress', 'signupDesignation',
    'signupDistrict', 'signupDivision', 'signupForm', 'signupName', 'signupNid',
    'signupOffice', 'signupPhone', 'signupUnion', 'signupUpazila', 'soundToggle',
    'tabLogin', 'tabSignup', 'themeToggle', 'ttArea', 'ttPop', 'ttTh', 'ttUpa',
    'upAvatar', 'upName', 'userDropdown', 'userProfileBar', 'vaBody',
    'vaExpandBtn', 'visionary-archive', 'wsBar', 'wsSteps',
)
EXEMPT = frozenset(APP_JS_IDS)

# Merged "pages" in document order: (file, page key, band label)
PAGES = [
    ('ai.html',            'ai',            'A ai Platform'),
    ('justice.html',       'justice',       'Justice Map - 64 Districts'),
    ('sheguard.html',      'sheguard',      'SheGuard X - Women Safety'),
    ('government.html',    'government',    'Government e-Services'),
    ('contact.html',       'contact',       'Contact & Help Desk'),
    ('about.html',         'about',         'About & Mission'),
    ('july.html',          'july',          'July 2024 Memorial'),
    ('memorial-abrar.html','memorial-abrar','Abrar Fahad Memorial'),
    ('memorial-sayeedi.html','memorial-sayeedi','Delwar Hossain Sayeedi Record'),
    ('blueprints.html',    'blueprints',    'Visionary Blueprints'),
]


def read(p):
    with open(p, encoding='utf-8') as f:
        return f.read()


def write(p, s):
    with open(p, 'w', encoding='utf-8') as f:
        f.write(s)


def extract_content(path):
    """Unique middle of a standard page: the page-hero header (if present)
    through the first <footer>."""
    s = read(path)
    ph = s.find('<header class="page-hero">')
    start = ph if ph != -1 else s.index('<section')
    try:
        end = s.index('<footer>', start)
    except ValueError:
        end = s.index('</body>', start)
    return s[start:end]


def make_srcdoc_female_safety():
    """Self-contained document for the SheGuard iframe (srcdoc)."""
    fs = read('female-safety.html')
    style_start = fs.index('<style')
    style_end = fs.rindex('</style>') + len('</style>')
    own_styles = fs[style_start:style_end]
    body_open = fs.index('<body')
    inner_start = fs.index('>', body_open) + 1
    inner_end = fs.index('</body>')
    inner = fs[inner_start:inner_end]
    # helper inside the iframe doc: resolve failed images through the PARENT's
    # window.__AIIM map (srcdoc iframes are same-origin, no map duplication)
    helper = ('<script>(function(){document.addEventListener("error",function(e){'
              'var t=e.target;if(t&&t.tagName==="IMG"){var m=parent&&parent.__AIIM;'
              'var raw=(t.getAttribute("src")||"");'
              'var v=m&&m[raw];if(!v&&m){var b=raw.split("/").pop();if(m[b])v=m[m[b]];}'
              'if(v)t.setAttribute("src",v);}},true);})();</script>')
    return ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            '<title>SheGuard X - Female Safety Command Center</title>\n'
            + own_styles + '\n' + helper + '\n</head>\n<body>\n' + inner + '\n</body>\n</html>\n')


def namespace_ids(slice_html, p):
    """Rename every non-EXEMPT content id to pg-<p>-<id>, fixing the places that
    reference them: id="", #anchor/#selector/css references, getElementById."""
    ids = set(re.findall(r'\bid="([A-Za-z][\w-]*)"', slice_html))
    rename = {i for i in ids if i not in EXEMPT}
    for i in sorted(rename):
        ni = 'pg-%s-%s' % (p, i)
        # 1. element definitions
        slice_html = re.sub(r'id="%s"' % re.escape(i), 'id="%s"' % ni, slice_html)
        # 2. "#i" references: href, css selectors, querySelector, onclick strings
        #    (skip if preceded by alnum/'-' so ids inside longer tokens stay put)
        slice_html = re.sub(r'(?<![A-Za-z0-9_-])#%s(?=[\s"\':{}>,.+\[\]=/]|$)' % re.escape(i),
                            '#%s' % ni, slice_html)
        # 3. getElementById('i') / getElementById("i")
        slice_html = re.sub(r"getElementById\(\s*'%s'\s*\)" % re.escape(i),
                            "getElementById('%s')" % ni, slice_html)
        slice_html = re.sub(r'getElementById\(\s*"%s"\s*\)' % re.escape(i),
                            'getElementById("%s")' % ni, slice_html)
    return slice_html, rename


def band(label):
    return ('<div class="aiopg-band" style="background:linear-gradient(90deg,rgba(14,165,233,.16),'
            'rgba(99,102,241,.16));border-top:1px solid rgba(14,165,233,.3);border-bottom:1px solid '
            'rgba(255,255,255,.07);padding:.6rem 2rem;display:flex;align-items:center;'
            'justify-content:center;gap:1.1rem;font-size:.72rem;font-weight:700;letter-spacing:.16em;'
            'text-transform:uppercase;color:#7dd3fc"><span>&#9632; %s</span>'
            '<a href="#pg-home" style="color:#94a3b8;text-decoration:none;letter-spacing:.05em">'
            '&#9650; Back to top</a></div>' % label)


def convert_page_links(text):
    """Rewrite every remaining href="page.html[#anchor]" into an in-page anchor."""
    merged = {'index.html': 'pg-home'}
    for fname, key, _ in PAGES:
        merged[fname] = 'pg-' + key

    def repl(m):
        page, frag = m.group(1), m.group(2)
        target = merged.get(page)
        if target is None:
            return m.group(0)  # unknown page: leave as-is
        if target == 'pg-home':
            anchor = ('#' + frag.lstrip('#')) if frag else '#pg-home'
        else:
            anchor = ('#%s-%s' % (target, frag.lstrip('#'))) if frag else ('#%s' % target)
        return 'href="%s"' % anchor

    return re.sub(r'href="([A-Za-z0-9_-]+\.html)(#[^"]*)?"', repl, text)


def process_sheguard(content):
    """Inline the female-safety iframe via srcdoc and retarget its links."""
    srcdoc = make_srcdoc_female_safety()
    # find the iframe + its id so female-safety links can point at it later
    m = re.search(r'<iframe\b[^>]*>', content)
    if m:
        tag = m.group(0)
        im = re.search(r'\bid="([A-Za-z][\w-]*)"', tag)
        fid = im.group(1) if im else 'sheguardFrame'
        # drop original src (female-safety.html), add srcdoc
        tag2 = re.sub(r'\bsrc="[^"]*"', '', tag)
        tag2 = tag2.rstrip('/') if tag2.rstrip().endswith('/') else tag2
        tag2 = re.sub(r'/?>$', '>', tag2)
        content = content.replace(tag, tag2.replace('>',
                              ' srcdoc="%s">' % html_mod.escape(srcdoc, quote=True)))
        # retarget "open female-safety.html" links to the in-page iframe anchor
        content = re.sub(r'href="female-safety\.html"', 'href="#pg-sheguard-%s"' % fid, content)
        print('   female-safety iframe (%s) -> srcdoc (%d chars)' % (fid, len(srcdoc)))
    return content


def all_image_files():
    imgs = []
    for root, _dirs, fs in os.walk(IMGDIR):
        for f in fs:
            imgs.append(os.path.join(root, f).replace(os.sep, '/'))
    return imgs


def data_uri(p):
    ext = p.rsplit('.', 1)[-1].lower()
    mime = MIME.get(ext, 'application/octet-stream')
    with open(p, 'rb') as fh:
        b64 = base64.b64encode(fh.read()).decode('ascii')
    return 'data:%s;base64,%s' % (mime, b64)


def inline_images(text):
    """Make every image the document can load portable without the assets/
    folder, embedding each referenced image exactly ONCE.

    Instead of textually pasting data URIs into every <img> tag (which repeats
    big URIs and bloats the file), every referenced image is embedded once in a
    window.__AIIM lookup and a tiny capture script rewrites any <img> whose
    relative "assets/img/..." src fails to load into its data URI. This works
    for static tags, CSS-referenced files, runtime concatenations, and (via
    parent access) the srcdoc iframe.
    """
    import json
    allimgs = all_image_files()
    # referenced = its full assets/img path OR its basename appears in the doc
    by_name = {}
    for p in allimgs:
        by_name.setdefault(p.rsplit('/', 1)[-1], []).append(p)
    referenced = []
    for p in allimgs:
        if p in text:
            referenced.append(p)
    bare_used = set(re.findall(r'["\'\s=]\(?([A-Za-z0-9_-]+\.(?:jpg|jpeg|png|gif|webp|svg))["\'\s)]', text))
    for base, cands in by_name.items():
        if base in bare_used and len(cands) == 1 and cands[0] not in referenced:
            referenced.append(cands[0])
    referenced = sorted(set(referenced))

    # ---- one data URI per referenced file -----------------------------------
    uri = {p: data_uri(p) for p in referenced}
    # ---- lookup map, URIs stored ONCE ---------------------------------------
    #   full relative path -> data URI
    #   unambiguous basename -> that full path (tiny value, no URI duplication)
    lookup = dict(uri)
    for p in referenced:
        b = p.rsplit('/', 1)[-1]
        if len(by_name[b]) == 1:
            lookup[b] = p
    map_json = json.dumps(lookup)

    # ---- capture helper for the main document (installed before any image) ----
    helper = (
        '<script>(function(){window.__AIIM=%s;'
        'function fix(t){var raw=t.getAttribute("src")||"";'
        'if(!raw||raw.indexOf("data:")===0)return;'
        'var M=window.__AIIM;var v=M[raw];'
        'if(!v){var b=raw.split("/").pop();if(M[b])v=M[M[b]];}'
        'if(v)t.setAttribute("src",v);}'
        'document.addEventListener("error",function(e){var t=e.target;'
        'if(t&&t.tagName==="IMG")fix(t);},true);})();</script>' % map_json)
    text = re.sub(r'(<body[^>]*>)', lambda m: m.group(1) + helper, text, count=1)

    print('   images embedded once: %d referenced (%.0f KB of data URIs)'
          % (len(referenced), sum(len(v) for v in uri.values()) / 1024))
    return text


def main():
    # corruption guard: the skeleton carries app.js inline - keep it clean too
    import subprocess
    g = subprocess.run([sys.executable, 'check_figures.py'])
    if g.returncode != 0:
        sys.exit('ABORT: check_figures.py failed - fix assets/app.js first.')

    SKELETON = '_archive/index.html.bak-standalone'  # built by build_standalone.py
    if not os.path.exists(SKELETON):
        sys.exit('ABORT: %s missing - run build_standalone.py first' % SKELETON)
    skeleton = read(SKELETON)  # standalone home: inlined assets + shared chrome
    if '__AIIM' in skeleton or len(skeleton.encode('utf-8')) > 4_000_000:
        sys.exit(
            'ABORT: %s is an all-in-one file (contains the inlined image map '
            'or is > 4 MB). Re-run build_standalone.py TWICE: the first run '
            'repairs index.html, the second repairs this backup. Then merge.'
            % SKELETON)

    # --- home content = skeleton sections (kept unprefixed) -----------------
    home_start = skeleton.index('<section')
    home_end = skeleton.index('<button class="back-to-top"')
    prefix, home_content, tail = skeleton[:home_start], skeleton[home_start:home_end], skeleton[home_end:]

    blocks = ['<div class="allinone-page" id="pg-home">\n' + home_content + '\n</div>\n']
    for fname, key, label in PAGES:
        print('processing %-18s (%s)' % (fname, key))
        content = extract_content(fname)
        # every page ships its own trailing back-to-top button; the merged
        # chrome tail already has one, so drop the per-page duplicates
        content = re.sub(r'\s*<button class="back-to-top"[^>]*>.*?</button>', '', content, flags=re.S)
        if key == 'sheguard':
            content = process_sheguard(content)
        content, renamed = namespace_ids(content, key)
        print('   content %d chars, ids renamed: %d' % (len(content), len(renamed)))
        blocks.append('\n<!-- ==================== PAGE: %s ==================== -->\n'
                      '<div class="allinone-page" id="pg-%s">\n%s\n%s\n</div>\n'
                      % (label, key, band(label), content))

    out = prefix + '\n'.join(blocks) + tail

    # --- global: page.html[#a] links become in-page anchors -----------------
    out = convert_page_links(out)

    # --- replace the strict CSP with the relaxed one for this local file ------
    out = re.sub(
        r'<meta http-equiv="Content-Security-Policy"[^>]*>',
        lambda m: ('<!-- RELAXED CSP for the all-in-one local test file (see RELAXED_CSP): '
                   'the strict \'self\'-based policy cannot work under file:// where \'self\' '
                   'never matches sibling files. Inline code, data: URIs, file: images, the '
                   'srcdoc iframe (about:) and the local AI proxy stay allowed; object-src \'none\', '
                   'base-uri, form-action and no-unsafe-eval still hold. The production pages and '
                   'the standalone home keep their original strict CSP. -->\n'
                   '<meta http-equiv="Content-Security-Policy" content="%s">' % RELAXED_CSP),
        out, count=1, flags=re.I)

    # --- inline every image the document can load (full portability) ---------
    out = inline_images(out)

    # --- validation ----------------------------------------------------------
    leftover = re.findall(r'href="[A-Za-z0-9_-]+\.html', out)
    dup = {}
    for i in re.findall(r'\bid="([A-Za-z][\w-]*)"', out):
        dup[i] = dup.get(i, 0) + 1
    dup_ids = {k: v for k, v in dup.items() if v > 1 and not k.startswith('pg-band')}
    # images keep their relative refs by design (resolved at runtime via the
    # embedded __AIIM map) - just report coverage
    img_refs = set(re.findall(r'assets/img/[A-Za-z0-9_./-]+\.(?:jpg|jpeg|png|gif|webp|svg)', out))
    map_keys = set(re.findall(r'"(assets/img/[A-Za-z0-9_./-]+\.(?:jpg|jpeg|png|gif|webp|svg))":\s*"data:', out))
    missing = img_refs - map_keys
    print('leftover page links:', len(leftover), leftover[:5])
    print('duplicate ids:', len(dup_ids), dict(list(dup_ids.items())[:12]))
    print('image refs: %d, embedded in __AIIM map: %d, NOT covered: %s'
          % (len(img_refs), len(map_keys), sorted(missing)[:6] or 'none'))
    if leftover or dup_ids or missing:
        print('WARN: see above')

    write('all-in-one.html', out)
    print('wrote all-in-one.html (%d bytes) - index.html keeps the clean standalone Home'
          % len(out.encode('utf-8')))


if __name__ == '__main__':
    main()
