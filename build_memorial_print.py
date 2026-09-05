# -*- coding: utf-8 -*-
"""Build memorial-abrar.html (print-friendly) from july.html's #abrar-fahad section,
and add a print-version button into the memorial section."""
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

july_path = 'july.html'
july = open(july_path, encoding='utf-8', newline='').read()

# ---- extract <section id="abrar-fahad"> ... </section> with depth counting ----
start = july.find('<section id="abrar-fahad"')
if start < 0:
    print('FATAL: abrar section not found')
    sys.exit(1)
i = july.find('>', start)
depth, j = 1, i + 1
sec_re = re.compile(r'<(/?)section\b', re.I)
for m in sec_re.finditer(july, j):
    depth += -1 if m.group(1) else 1
    if depth == 0:
        end = july.find('>', m.end()) + 1
        break
section = july[start:end]
print('extracted section:', len(section), 'chars')

# ---- strip inline styles (print CSS handles layout) ----
section = re.sub(r'\sstyle="[^"]*"', '', section)

# ---- derive hero title: first h2 heading text ----
m2 = re.search(r'<h2[^>]*>(.*?)</h2>', section, re.S)
title_txt = 'শহীদ আবরার ফাহাদ'
if m2:
    t = re.sub(r'<[^>]+>', ' ', m2.group(1))
    t = re.sub(r'\s+', ' ', t).strip()
    if t:
        title_txt = t

PORTRAIT = 'assets/img/abrar-fahad.jpg'
PRINT_CSS = """@page { size: A4; margin: 18mm 16mm; }
* { box-sizing: border-box; }
body { font-family: 'Noto Serif Bengali','Noto Sans Bengali','Segoe UI',serif; color: #1a1a1a; background: #fff; margin: 0; line-height: 1.55; font-size: 11.5pt; }
.mem-hero { border-bottom: 3px solid #b91c1c; padding-bottom: 14px; margin-bottom: 18px; }
.mem-kicker { font-size: 9pt; letter-spacing: 2.5px; color: #b91c1c; font-weight: 700; margin: 0 0 6px; }
.mem-title { font-size: 22pt; font-weight: 800; margin: 0 0 10px; color: #111; }
.mem-hero-img { float: right; width: 130px; height: auto; border: 1px solid #ccc; margin: 0 0 10px 14px; }
.mem-hero-img figcaption { font-size: 8pt; color: #555; margin-top: 4px; }
section { break-inside: auto; }
h2, h3 { break-after: avoid; }
h3 { font-size: 13pt; color: #b91c1c; border-bottom: 1.5px solid #e5e5e5; padding-bottom: 4px; margin: 18px 0 8px; }
blockquote { border-left: 3px solid #b91c1c; margin: 10px 0; padding: 6px 14px; color: #333; font-style: italic; background: #faf5f5; }
img { max-width: 100%; height: auto; }
a { color: #1d4ed8; text-decoration: none; }
.mem-src { font-size: 9pt; color: #444; border-top: 1px solid #ddd; margin-top: 20px; padding-top: 10px; }
.mem-src ul { margin: 6px 0 0 16px; padding: 0; }
.no-print { position: fixed; top: 12px; right: 12px; z-index: 10; }
.no-print button { background: #b91c1c; color: #fff; border: 0; padding: 10px 18px; border-radius: 8px; font-size: 12pt; cursor: pointer; box-shadow: 0 2px 8px rgba(0,0,0,.25); }
@media print { .no-print { display: none; } }
"""

html = """<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Print Memorial &mdash; Shaheed Abrar Fahad | DLA</title>
<meta name="description" content="Print-friendly memorial record for Shaheed Abrar Fahad (1998-2019).">
<link rel="icon" type="image/svg+xml" href="assets/img/favicon.svg">
<style>""" + PRINT_CSS + """</style>
</head>
<body>
<div class="no-print"><button onclick="window.print()">&#128424; Print / Save as PDF</button></div>
<figure class="mem-hero-img"><img src="%(portrait)s" alt="Shaheed Abrar Fahad (1998-2019)"><figcaption>Shaheed Abrar Fahad (1998&ndash;2019)</figcaption></figure>
<div class="mem-hero">
  <p class="mem-kicker">PRINT MEMORIAL &middot; DLA &middot; JULY 2024 ARCHIVE</p>
  <h1 class="mem-title">%(title)s</h1>
</div>
%(section)s
<div class="mem-src">
  <strong>Sources:</strong>
  <ul>
    <li><a href="https://bn.wikipedia.org/wiki/%%E0%%A6%%86%%E0%%A6%%AC%%E0%%A6%%B0%%E0%%A6%%BE%%E0%%A6%%B0_%%E0%%A6%%AB%%E0%%A6%%BE%%E0%%A6%%B9%%E0%%A6%%BE%%E0%%A6%%A6">Bangla Wikipedia &mdash; Abrar Fahad</a></li>
    <li><a href="https://bn.wikipedia.org/wiki/%%E0%%A6%%86%%E0%%A6%%AC%%E0%%A6%%B0%%E0%%A6%%BE%%E0%%A6%%B0_%%E0%%A6%%AB%%E0%%A6%%BE%%E0%%A6%%B9%%E0%%A6%%BE%%E0%%A6%%A6_%%E0%%A6%%B9%%E0%%A6%%A4%%E0%%A7%%8D%%E0%%A6%%AF%%E0%%A6%%BE%%E0%%A6%%95%%E0%%A6%%BE%%E0%%A6%%A3%%E0%%A7%%8D%%E0%%A6%%A1">Bangla Wikipedia &mdash; Abrar Fahad Killing</a></li>
    <li><a href="https://abrarfahadarchive.org/">AbrarFahadArchive.org (batchmates' dedication)</a></li>
  </ul>
  <p>Generated from dla-website/july.html#abrar-fahad &middot; print format A4.</p>
</div>
</body>
</html>
""" % {'portrait': PORTRAIT, 'title': title_txt, 'section': section}

open('memorial-abrar.html', 'w', encoding='utf-8', newline='').write(html)
print('memorial-abrar.html written:', len(html), 'chars')

# ---- add print-version button into the live memorial (once) ----
july = open(july_path, encoding='utf-8', newline='').read()
BTN = '<a href="memorial-abrar.html" target="_blank" rel="noopener" style="display:inline-block;margin-top:18px;padding:10px 22px;border-radius:12px;border:1px solid rgba(255,120,100,.5);color:#ffb0a0;background:rgba(255,80,60,.08);text-decoration:none;font-size:14px;font-weight:600;">\U0001F5A8 Print / PDF version</a>'
if 'memorial-abrar.html' in july:
    print('button already present')
else:
    anchor = july.find('</section>', july.find('<section id="abrar-fahad"'))
    if anchor < 0:
        print('FATAL: closer not found')
        sys.exit(1)
    july = july[:anchor] + BTN + '\n    ' + july[anchor:]
    open(july_path, 'w', encoding='utf-8', newline='').write(july)
    print('print button added to july.html#abrar-fahad')
