# -*- coding: utf-8 -*-
"""
Multi-page restructure builder (v2) — marker-based, idempotent.
Reuses the working chrome from contact.html and the real section content
from the monolith index.html. Rebuilds index.html as a clean Home, creates
about.html, and updates the shared nav + footer on every page.

Run:  python build_site.py
"""
import re, sys, os
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)))

ROOT = 'dla-website'
def read(p):
    with open(os.path.join(ROOT, p), encoding='utf-8') as f:
        return f.read()
def write(p, s):
    with open(os.path.join(ROOT, p), 'w', encoding='utf-8') as f:
        f.write(s)

# ---------------------------------------------------------------- chrome donor
contact = read('contact.html')
# Section content source: the full monolith. Never read the file we write.
MONO_SRC = 'index.html.bak-pre'
monolith = read(MONO_SRC)
print('monolith source:', MONO_SRC, len(monolith), 'chars')

# head template: up to </head>
HEAD = contact.split('</head>')[0] + '</head>'
# ticker (the hotline strip)
TICKER = re.search(r'<div class="scroll-progress".*?</div>\s*<div class="hotline-ticker">.*?</div></div>', contact, re.S)
TICKER = TICKER.group(0) if TICKER else ''
# footer
FOOTER = re.search(r'<button class="back-to-top".*?</footer>', contact, re.S).group(0)
# auth overlay + chat fab + window (tail before the app.js script)
TAIL_START = contact.index('<div class="auth-overlay"')
AUTH_CHAT = contact[TAIL_START:]

# ---------------------------------------------------------------- section extractor
def extract_section(html, id_):
    m = re.search(r'<section\b[^>]*\bid="%s"[^>]*>' % re.escape(id_), html)
    if not m:
        return None
    start, i, depth = m.start(), m.end(), 1
    for mm in re.finditer(r'<section\b|</section>', html[i:]):
        if mm.group(0) == '</section>':
            depth -= 1
            if depth == 0:
                return html[start:i + mm.end()]
        else:
            depth += 1
    return None

def strip_inline_styles(html):
    return re.sub(r'<style>.*?</style>', '', html, flags=re.S)

def sec(id_):
    s = extract_section(monolith, id_)
    return strip_inline_styles(s) if s else ''

# ---------------------------------------------------------------- nav (new)
NAV_FLAT = [
    ('index.html',     'Home',        ''),
    ('ai.html',        'A ai Platform',''),
    ('justice.html',   'Justice Map', ''),
    ('sheguard.html',  'SheGuard X',  'style="color:#fb7185;font-weight:700"'),
    ('government.html','Government',  ''),
    ('contact.html',   'Contact',     ''),
]
NAV_DISCOVER = [
    ('about.html',     'About &amp; Mission'),
    ('july.html',      'July 2024'),
    ('blueprints.html','Visionary Blueprints'),
]

def nav_links(active):
    lis = []
    for href, label, extra in NAV_FLAT:
        act = ' class="active"' if href == active else ''
        lis.append('<li><a href="%s"%s %s>%s</a></li>' % (href, act, extra, label))
    drop = ''.join('<li><a href="%s">%s</a></li>' % (h, l) for h, l in NAV_DISCOVER)
    lis.append('<li class="nav-drop"><a href="#">Discover <i class="fas fa-chevron-down"></i></a><ul class="nav-dropdown">%s</ul></li>' % drop)
    return '<ul class="nav-links">' + ''.join(lis) + '</ul>'

def drawer_links(active):
    lis = []
    for href, label, extra in NAV_FLAT:
        act = ' class="active"' if href == active else ''
        lis.append('<li><a href="%s"%s %s>%s</a></li>' % (href, act, extra, label))
    for href, label in NAV_DISCOVER:
        act = ' class="active"' if href == active else ''
        lis.append('<li><a href="%s"%s>%s</a></li>' % (href, act, label))
    return '<ul class="drawer-links">' + ''.join(lis) + '</ul>'

def patch_nav(html, active):
    # replace the nav-links and drawer-links ULs, and the CTA link target
    html = re.sub(r'<ul class="nav-links">.*?</ul>', nav_links(active), html, flags=re.S)
    html = re.sub(r'<ul class="drawer-links">.*?</ul>', drawer_links(active), html, flags=re.S)
    html = html.replace('Get Involved', 'Get Legal Help')
    return html

def patch_footer(html):
    new_cols = (
        '<div class="fgrid">'
        '<div><a href="index.html" class="nav-logo" style="margin-bottom:1rem;display:inline-flex"><span>A ai</span></a>'
        '<p>Next-Gen Digital Legal Aid - Access to justice for 682,500+ citizens across all 64 districts.</p></div>'
        '<div class="fcol"><h4>Get Help</h4>'
        '<a href="contact.html">Complaint Desk</a>'
        '<a href="justice.html#emergency-helplines">Emergency Helplines</a>'
        '<a href="contact.html">Free Legal Aid: 16430</a></div>'
        '<div class="fcol"><h4>Explore</h4>'
        '<a href="ai.html">A ai Platform</a>'
        '<a href="justice.html">Justice Map</a>'
        '<a href="sheguard.html">SheGuard X</a>'
        '<a href="government.html">Government</a></div>'
        '<div class="fcol"><h4>About</h4>'
        '<a href="about.html">About &amp; Mission</a>'
        '<a href="july.html">July 2024 Memorial</a>'
        '<a href="blueprints.html">Visionary Blueprints</a></div>'
        '</div>'
    )
    # Scope the footer edit to the <footer> block only, so content sections that
    # also use .fgrid are never touched.
    m = re.search(r'<footer>.*?</footer>', html, re.S)
    if not m:
        return html
    footer_block = m.group(0)
    new_footer = re.sub(r'<div class="fgrid">.*?(<div class="fb">)', new_cols + '\n' + r'\1', footer_block, flags=re.S)
    return html[:m.start()] + new_footer + html[m.end():]

# ---------------------------------------------------------------- assemble a page
def assemble(title, active, body_sections, extra_js=''):
    head = HEAD
    head = re.sub(r'<title>[^<]*</title>', '<title>%s</title>' % title, head)
    body_top = re.search(r'<body>\n(.*?)<section', contact, re.S).group(1)
    body_top = patch_nav(body_top, active)
    footer = patch_footer(FOOTER)
    scripts = '<script src="assets/app.js?v=app35"></script>\n</body>\n</html>\n'
    return (head + '\n<body>\n' + body_top + '\n' + '\n'.join(body_sections) +
            '\n' + footer + '\n' + AUTH_CHAT + '\n' + extra_js + scripts)

# ---------------------------------------------------------------- quick-access tiles
QUICK_ACCESS = '''
<section id="quick-access" style="padding:4rem 0"><div class="container">
  <div class="section-header"><div class="section-tag">Start Here</div><h2>What do you need help with?</h2><p>Choose a path - every service is free, confidential, and available in Bangla and English.</p></div>
  <div class="pgrid">
    <a href="contact.html" class="pcard reveal"><div class="picon" style="background:rgba(16,185,129,.15);color:#10b981"><i class="fas fa-life-ring"></i></div><h3>Get Legal Help</h3><p>Apply for free legal aid or reach a case officer. Call <b>16430</b> or file online.</p><span class="shl" style="background:rgba(16,185,129,.12);color:#10b981">Start application</span></a>
    <a href="sheguard.html" class="pcard reveal rd1"><div class="picon" style="background:rgba(251,113,133,.15);color:#fb7185"><i class="fas fa-shield-alt"></i></div><h3>Women's Safety</h3><p>SheGuard X - discreet protection, emergency help and safe reporting for women.</p><span class="shl" style="background:rgba(251,113,133,.12);color:#fb7185">SheGuard X</span></a>
    <a href="justice.html" class="pcard reveal rd2"><div class="picon" style="background:rgba(239,68,68,.15);color:#ef4444"><i class="fas fa-map-marked-alt"></i></div><h3>Find My District</h3><p>Locate courts, legal aid offices and emergency helplines across all 64 districts.</p><span class="shl" style="background:rgba(239,68,68,.12);color:#ef4444">Justice Map</span></a>
    <a href="government.html" class="pcard reveal rd3"><div class="picon" style="background:rgba(16,185,129,.15);color:#10b981"><i class="fas fa-landmark"></i></div><h3>Government e-Services</h3><p>Access structure, e-service portals and the grievance redressal system.</p><span class="shl" style="background:rgba(16,185,129,.12);color:#10b981">Government</span></a>
  </div>
</div></section>
'''

# compact nationwide strip (replaces the 25KB district grid)
def compact_nationwide():
    d = sec('nationwide')
    names = re.findall(r'>([A-Z][a-zA-Z\'\-]+)</span>', d)
    chips = ''.join('<span class="dchip">%s</span>' % n for n in names)
    return ('<section id="nationwide" style="background:linear-gradient(135deg,rgba(16,185,129,.06),rgba(239,68,68,.06))">'
            '<div class="container"><div class="section-header"><div class="section-tag">Nationwide Reach</div>'
            '<h2>Covering All 64 Districts of Bangladesh</h2>'
            '<p>From coastal Cox\'s Bazar to hill-tracted Rangamati, from metropolitan Dhaka to remote haor regions - A ai reaches every corner.</p></div>'
            '<div class="dchips">' + chips + '</div></div></section>')

# ---------------------------------------------------------------- HOME
def build_home():
    # static hero (typing animation needs the monolith's inline script; keep clean)
    hero = ('<section class="hero" id="hero"><div class="hero-bg"></div><div class="particles" id="particles"></div><div class="hero-content">'
            ''
            '<h1><span>Smart</span><br><span class="gt">Justice for Every Bangladeshi Citizen</span></h1>'
            '<p>A ai is a next-generation, privacy-preserving legal aid platform bringing autonomous AI dispute resolution, '
            'voice-first Bengali intake, and zero-knowledge cryptography to 682,500+ vulnerable citizens across all 64 districts of Bangladesh.</p>'
            '<div class="hero-buttons"><a href="contact.html" class="btn-p"><i class="fas fa-life-ring"></i> Get Legal Help</a>'
            '<a href="ai.html" class="btn-s"><i class="fas fa-robot"></i> Explore A ai Platform</a></div>'
            '<div class="hero-stats"><div class="hero-stat"><div class="num">682,500+</div><div class="label">Target Beneficiaries</div></div>'
            '<div class="hero-stat"><div class="num">300</div><div class="label">Pilot Unions</div></div>'
            '<div class="hero-stat"><div class="num">$3.24M</div><div class="label">EU Funding</div></div>'
            '<div class="hero-stat"><div class="num">64</div><div class="label">Districts Nationwide</div></div></div>'
            '</div></section>')
    sections = [hero, QUICK_ACCESS, sec('problem'), sec('solution'),
                sec('flow'), sec('impact'), sec('partners'), compact_nationwide()]
    return assemble('A ai - Digital Legal Aid Bangladesh', 'index.html', sections)

# ---------------------------------------------------------------- ABOUT
def build_ai():
    # reordered per plan: personas -> capabilities -> agent architecture -> trust -> stack
    ids = ['personas','features','ai-features','agent-swarm','reasoning-engine','agent-comm',
           'collective-intel','agent-evolution','constitutional-ai','tech-stack','challenges','additional-features']
    sections = []
    for i in ids:
        s = sec(i)
        if not s:
            print('  !! sec(%s) returned EMPTY' % i)
        sections.append(s)
    return assemble('A ai AI Platform - Multi-Agent Legal Intelligence', 'ai.html', sections)

def build_about():
    institutional = (
        '<section id="about" style="padding:6rem 2rem"><div class="container">'
        '<div class="section-header"><div class="section-tag">About A ai</div>'
        '<h2>Who We Are</h2>'
        '<p>A ai is the next-generation digital legal aid ecosystem for Bangladesh, executed by the Directorate of Bangladesh Legal Aid (DBLA) '
        'under the Ministry of Law, Justice &amp; Parliamentary Affairs, with technical partnership from UNDP and funding from the European Union.</p></div>'
        '<div class="fgrid">'
        '<div class="fcard"><div class="fiwrap" style="background:rgba(16,185,129,.15);color:#10b981"><i class="fas fa-gavel"></i></div><h3>Our Mission</h3><p>Democratize access to justice by making legal information, assistance and dispute resolution affordable, transparent and accessible to every citizen - regardless of language, literacy or economic status.</p></div>'
        '<div class="fcard"><div class="fiwrap" style="background:rgba(239,68,68,.15);color:#ef4444"><i class="fas fa-eye"></i></div><h3>Our Vision</h3><p>A Bangladesh where no one is denied justice. By 2030, autonomous AI-assisted services divert 40% of disputes to Online Dispute Resolution and reach 682,500+ vulnerable citizens.</p></div>'
        '<div class="fcard"><div class="fiwrap" style="background:rgba(16,185,129,.15);color:#10b981"><i class="fas fa-users"></i></div><h3>Who Runs It</h3><p>Executed by DBLA / MoLJPA, with UNDP Bangladesh as technical partner and the European Union as funding partner - governed by an ethical AI oversight board.</p></div>'
        '</div></div></section>')
    sections = [institutional, sec('vision'), sec('roadmap')]
    return assemble('About &amp; Mission - A ai', 'about.html', sections)

# ---------------------------------------------------------------- run
home = build_home()
about = build_about()
ai = build_ai()
write('index.html', home)
write('about.html', about)
write('ai.html', ai)
print('wrote index.html (%d), about.html (%d), ai.html (%d)' % (len(home), len(about), len(ai)))

# patch nav/footer on the other split pages
for page in ['ai.html', 'justice.html', 'government.html', 'sheguard.html', 'july.html', 'blueprints.html', 'contact.html']:
    html = read(page)
    active = page.replace('.html', '')
    active = 'index.html' if active == 'index' else (active + '.html')
    html = patch_nav(html, active)
    html = patch_footer(html)
    write(page, html)
    print('patched nav/footer on', page)
