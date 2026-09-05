# -*- coding: utf-8 -*-
"""
Multi-page restructure builder for A ai - Digital Legal Aid Bangladesh.
Splits the monolithic single-page index.html into 8 static pages sharing
assets/styles.css and assets/app.js. Idempotent: safe to re-run.
"""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'index.html')
ASSETS = os.path.join(ROOT, 'assets')

src = open(SRC, encoding='utf-8').read()
print('source chars:', len(src))

# ---------------------------------------------------------------- slices
# (start, end) measured on the ORIGINAL source, in document order.
HEAD          = (0, 50617)                    # doctype..</head> (contains master <style>)
BODY_TOP      = (src.find('<div class="scroll-progress"'), 58123)   # ticker + nav + drawer
FOOTER_BLOCK  = (src.find('<button class="back-to-top"'), src.find('</footer>') + len('</footer>'))  # backToTop + footer
AUTH_CHAT     = (src.find('<div class="auth-overlay"'), 370990)  # auth overlay + chat fab + chat window

SECTIONS = {
    # Home
    'hero':               (58123, 59417),
    'problem':            (59417, 61723),
    'solution':           (61723, 64047),
    'features':           (64047, 66576),
    'personas':           (66576, 68779),
    'impact':             (68779, 69609),
    'flow':               (69609, 71382),
    'roadmap':            (71382, 72797),
    'partners':           (72797, 73676),
    'nationwide':         (73676, 99204),
    'vision':             (99204, 100456),
    # A ai platform
    'agent-swarm':        (196655, 202625),
    'reasoning-engine':   (202625, 206621),
    'agent-comm':         (206621, 209697),
    'collective-intel':   (209697, 211865),
    'agent-evolution':    (211865, 215011),
    'constitutional-ai':  (215011, 219325),
    'ai-features':        (100456, 103682),
    'tech-stack':         (106778, 108896),
    'roadmap-phases':     (108896, 110676),
    'challenges':         (110676, 112587),
    'additional-features':(112587, 116383),
    'programming':        (293754, 301852),
    # Justice map
    'constitution-full':  (219325, 233778),
    'interactive-map':    (233778, 268278),
    'emergency-helplines':(283014, 289717),
    # Government
    'govt-structure':     (272995, 283014),
    'govt-services':      (301852, 314456),
    # SheGuard
    'women-safety':       (314456, 317106),
    'sheguard-live':      (317106, 325908),
    # July 2024
    'july-timeline':      (268278, 272995),
    'memorial':           (289717, 293754),
    # Blueprints
    'futuristic':         (103682, 106778),
    'visionary-archive':  (116383, 196655),
    # Contact
    'complaints':         (325908, 350672),
    'contact':            (350672, 351483),
}

# sanity: every slice must start with <section
for name, (a, b) in SECTIONS.items():
    assert src[a:a+8] == '<section', (name, a, src[a:a+20])
    assert a < b

# ---------------------------------------------------------------- scripts
def script_body(open_pos):
    s = src.find('>', open_pos) + 1
    e = src.find('</script>', s)
    return src[s:e]

MAIN_SCRIPT   = script_body(370990)      # chatbot engine + KB + auth + map wiring
VASHOW_SCRIPT = script_body(692867)      # visionary archive expander
CHIME_SCRIPT  = script_body(714569)      # success chime + mute toggle

# script5 @352444: split into home-only (particles/typing/parallax) + global chrome
s5 = script_body(352444)
p_end = s5.find('pc.appendChild(p)}') + len('pc.appendChild(p)}')
t_start = s5.find('// Typing animation for hero headline')
assert 0 < p_end < t_start
HOME_SCRIPT   = s5[:p_end] + '\n' + s5[t_start:]
CHROME_SCRIPT = s5[p_end:t_start]

# ---------------------------------------------------------------- styles
# NOTE: assets/styles.css + assets/app.js are now CANONICAL runtime files
# (they carry the Quantum Shield integration). Regenerate them only if missing.
os.makedirs(ASSETS, exist_ok=True)
if not os.path.exists(os.path.join(ASSETS, 'styles.css')):
    style_parts = []
    for m in re.finditer(r'<style>.*?</style>', src, re.S):
        style_parts.append(m.group(0)[7:-8])
    css = '\n'.join(style_parts) + '\n'
    css += '/* Multi-page nav active state */\n.nav-links a.active{color:#34d399!important;border-bottom:2px solid #34d399!important}.drawer-links a.active{color:#34d399!important;border-left:3px solid #34d399!important;padding-left:.4rem}\n'
    open(os.path.join(ASSETS, 'styles.css'), 'w', encoding='utf-8').write(css)
    print('styles.css regenerated (chars:', len(css), ')')
else:
    print('styles.css kept (canonical, has Quantum Shield CSS)')

def strip_styles(html):
    return re.sub(r'<style>.*?</style>', '', html, flags=re.S)

def slice_of(a, b):
    return strip_styles(src[a:b])

# ---------------------------------------------------------------- assets/app.js
if not os.path.exists(os.path.join(ASSETS, 'app.js')):
    app_js = CHROME_SCRIPT + '\n\n' + MAIN_SCRIPT + '\n\n' + VASHOW_SCRIPT + '\n\n' + CHIME_SCRIPT + '\n'
    open(os.path.join(ASSETS, 'app.js'), 'w', encoding='utf-8').write(app_js)
    print('app.js regenerated (chars:', len(app_js), ')')
else:
    print('app.js kept (canonical, has Quantum Shield wiring)')

# ---------------------------------------------------------------- shared chrome
head = slice_of(*HEAD)
# replace master inline style with link, swap title
head = re.sub(r'<style>.*?</style>', '', head, flags=re.S)
head = re.sub(r'<title>[^<]*</title>', '<title>%TITLE%</title>', head)
CSP = ('<meta http-equiv="Content-Security-Policy" content="'
       "default-src 'self'; "
       "script-src 'self' 'unsafe-inline'; "
       "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
       "font-src https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
       "img-src 'self' data: blob: https:; "
       "connect-src 'self' data:; "
       "frame-src 'self'; "
       "object-src 'none'; "
       "base-uri 'self'; "
       "form-action 'self'"
       '">')
head = head + '\n<link rel="stylesheet" href="assets/styles.css?v=css6">\n' + CSP + '\n' + \
       '<script src="assets/security.js?v=sec33"></script>\n</head>'

body_top = slice_of(*BODY_TOP)
footer_block = slice_of(*FOOTER_BLOCK)
auth_chat = slice_of(*AUTH_CHAT)

# ---- nav links
NAV_ITEMS = [
    ('index.html',     'Home',       ''),
    ('ai.html',        'A ai',       ''),
    ('justice.html',   'Justice Map',''),
    ('government.html','Government', ''),
    ('sheguard.html',  'SheGuard X', 'style="color:#fb7185;font-weight:700"'),
    ('july.html',      'July 2024',  ''),
    ('blueprints.html','Blueprints', ''),
    ('contact.html',   'Contact',    ''),
]
def nav_ul(active_page):
    lis = []
    for href, label, extra in NAV_ITEMS:
        act = ' class="active"' if href == active_page else ''
        lis.append('<li><a href="%s"%s %s>%s</a></li>' % (href, act, extra, label))
    return '<ul class="nav-links">' + ''.join(lis) + '</ul>'

def drawer_ul(active_page):
    lis = []
    for href, label, extra in NAV_ITEMS:
        act = ' class="active"' if href == active_page else ''
        lis.append('<li><a href="%s"%s %s>%s</a></li>' % (href, act, extra, label))
    return '<ul class="drawer-links">' + ''.join(lis) + '</ul>'

def rebuild_chrome(active_page):
    bt = body_top
    bt = re.sub(r'<ul class="nav-links">.*?</ul>', nav_ul(active_page), bt, flags=re.S)
    bt = re.sub(r'<ul class="drawer-links">.*?</ul>', drawer_ul(active_page), bt, flags=re.S)
    bt = bt.replace('<a href="#" class="nav-logo"><span>A ai</span></a>', '')
    bt = bt.replace('<a href="#contact" class="nav-cta">Get Involved</a>',
                    '<a href="contact.html" class="nav-cta">Get Involved</a>')
    bt = bt.replace('<a href="#contact" class="btn-p" style="width:100%;justify-content:center">Get Involved</a>',
                    '<a href="contact.html" class="btn-p" style="width:100%;justify-content:center">Get Involved</a>')
    return bt

def rebuild_footer():
    fb = footer_block
    new_cols = (
        '<div><a href="index.html" class="nav-logo" style="margin-bottom:1rem;display:inline-flex"><span>A ai</span></a>'
        '<p>Next-Gen Digital Legal Aid - Access to justice for 682,500+ citizens across all 64 districts.</p></div>'
        '<div class="fcol"><h4>Platform</h4>'
        '<a href="ai.html">A ai AI Platform</a>'
        '<a href="justice.html">Justice Map</a>'
        '<a href="sheguard.html">SheGuard X</a>'
        '<a href="july.html">July 2024</a></div>'
        '<div class="fcol"><h4>Government</h4>'
        '<a href="government.html">Structure &amp; e-Services</a>'
        '<a href="blueprints.html">Visionary Blueprints</a>'
        '<a href="contact.html">Complaints</a>'
        '<a href="contact.html">Contact</a></div>'
        '<div class="fcol"><h4>Resources</h4>'
        '<a href="justice.html#emergency-helplines">Emergency Helplines</a>'
        '<a href="justice.html#constitution-full">Constitution</a>'
        '<a href="government.html#govt-services">e-Services Portals</a>'
        '<a href="justice.html#interactive-map">Districts Map</a></div>'
    )
    fb = re.sub(r'<div class="fgrid">.*?</div>\s*<div class="fb">', '<div class="fgrid">' + new_cols + '</div><div class="fb">', fb, flags=re.S)
    return fb

# ---------------------------------------------------------------- pages
PAGES = [
    ('index.html', 'A ai - Digital Legal Aid Bangladesh',
     ['hero','problem','solution','features','personas','impact','flow','roadmap','partners','nationwide','vision'],
     'index.html', True),
    ('ai.html', 'A ai AI Platform - Multi-Agent Legal Intelligence',
     ['agent-swarm','reasoning-engine','agent-comm','collective-intel','agent-evolution','constitutional-ai',
      'ai-features','tech-stack','roadmap-phases','challenges','additional-features','programming'],
     'ai.html', False),
    ('justice.html', 'Justice Map - Districts, Courts & Legal Aid',
     ['constitution-full','interactive-map','emergency-helplines'],
     'justice.html', False),
    ('government.html', 'Government of Bangladesh - Structure & e-Services',
     ['govt-structure','govt-services'],
     'government.html', False),
    ('sheguard.html', 'SheGuard X - Women Safety Guardian',
     ['women-safety','sheguard-live'],
     'sheguard.html', False),
    ('july.html', 'July 2024 Uprising - History & Memorial',
     ['july-timeline','memorial'],
     'july.html', False),
    ('blueprints.html', 'Visionary Blueprints - The Future of Justice',
     ['futuristic','visionary-archive'],
     'blueprints.html', False),
    ('contact.html', 'Contact & Complaints - A ai',
     ['complaints','contact'],
     'contact.html', False),
]

for fname, title, secs, active, is_home in PAGES:
    body = []
    body.append(head.replace('%TITLE%', title))
    body.append('<body>')
    body.append(rebuild_chrome(active))
    for s in secs:
        body.append(slice_of(*SECTIONS[s]))
    body.append(rebuild_footer())
    body.append(auth_chat)
    if is_home:
        body.append('<script>' + HOME_SCRIPT + '</script>')
    body.append('<script src="assets/app.js?v=app33"></script>')
    body.append('</body>\n</html>\n')
    out = '\n'.join(body)
    # drop the artificial blank line between body parts
    out = re.sub(r'\n{3,}', '\n\n', out)
    open(os.path.join(ROOT, fname), 'w', encoding='utf-8').write(out)
    print('wrote', fname, len(out.encode('utf-8')), 'bytes')

# ---------------------------------------------------------------- security hardening
# Re-apply the Quantum Shield wiring to contact.html (idempotent) so a rebuild
# reproduces the honeypot, throttle and qs-unlock re-render.
def harden_contact():
    p = os.path.join(ROOT, 'contact.html')
    s = open(p, encoding='utf-8').read()
    hp = ('<input type="text" id="cbxHp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true" '
          'style="position:absolute;left:-9999px;top:-9999px;width:1px;height:1px;opacity:0">')
    if 'cbxHp' not in s:
        s = s.replace('<form id="cbxCitForm" class="cbx-form" autocomplete="off">',
                      '<form id="cbxCitForm" class="cbx-form" autocomplete="off">' + hp, 1)
    if "document.addEventListener('qs-unlock',function(){render();});" not in s:
        s = s.replace("var cf=document.getElementById('cbxCitForm');if(cf)cf.addEventListener('submit',handleCit);",
                      "var cf=document.getElementById('cbxCitForm');if(cf)cf.addEventListener('submit',handleCit);\n"
                      "  document.addEventListener('qs-unlock',function(){render();});", 1)
    throttle = ('var _now=Date.now();\n'
                '        var _hits=window.__cbxThrottle||[];\n'
                '        _hits=_hits.filter(function(t){return _now-t<60000;});\n'
                '        if(_hits.length>=3){if(window.QS)QS.audit(\'rate limit hit\');return;}\n'
                '        _hits.push(_now);window.__cbxThrottle=_hits;')
    if 'window.__cbxThrottle' not in s:
        s = s.replace('function handleCit(e){\n    e.preventDefault();',
                      'function handleCit(e){\n    e.preventDefault();\n' + throttle, 1)
        s = s.replace('function handleIt(e){\n    e.preventDefault();',
                      'function handleIt(e){\n    e.preventDefault();\n' + throttle, 1)
    open(p, 'w', encoding='utf-8').write(s)
    print('contact.html hardened (honeypot + throttle + qs-unlock)')

harden_contact()
print('DONE')