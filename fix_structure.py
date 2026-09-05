import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(ROOT, 'dla-website'))

# ---------- 1. Fix garbage nav closers on every page ----------
BAD = '</ul></li></ul>' + '</li></ul>' * 4
GOOD = '</ul></li></ul>'
for f in sorted(x for x in os.listdir('.') if x.endswith('.html')):
    src = open(f, encoding='utf-8', newline='').read()
    n = src.count(BAD)
    if n == 0:
        print(f, ': nav closers already clean')
        continue
    src = src.replace(BAD, GOOD)
    open(f, 'w', encoding='utf-8', newline='').write(src)
    print(f, ': removed', n, 'garbage nav closer run(s)')

# ---------- 2. Rebuild blueprints.html futuristic section + footer ----------
def balanced_section(src, start):
    """Return the balanced <section ...>...</section> block starting at start."""
    end = src.find('</section>', start)
    assert end > 0
    # sections in this codebase are not nested at top level of the monolith
    return src[start:end + len('</section>')]

bp = 'blueprints.html'
src = open(bp, encoding='utf-8', newline='').read()
mono = open(os.path.join('_archive', 'index.html.bak-pre'), encoding='utf-8', newline='').read()
mi = mono.find('<section id="futuristic"')
assert mi >= 0, 'futuristic section not found in archive monolith'
fresh = balanced_section(mono, mi)
print('extracted fresh #futuristic section:', len(fresh), 'chars')

i = src.find('<section id="futuristic"')
assert i >= 0, 'damaged futuristic marker not found in blueprints'
fb = src.find('<div class="fb">', i)
assert fb > i, 'footer fb marker not found'
damaged = src[i:fb]
fg = damaged.find('<div class="fgrid">')
assert fg > 0, 'footer fgrid not found inside damaged region'
fgrid_html = damaged[fg:]
print('footer fgrid preserved:', len(fgrid_html), 'chars, ends with:', repr(fgrid_html[-60:]))

repaired = src[:i] + fresh + '\n<footer>\n' + fgrid_html + src[fb:]
open(bp, 'w', encoding='utf-8', newline='').write(repaired)
print(bp, ': futuristic section restored + footer rebuilt')

# ---------- 3. Diagnose july.html missing </div> ----------
src = open('july.html', encoding='utf-8', errors='replace').read()
# strip script bodies so JS strings don't pollute
parts, last = [], 0
for m in re.finditer(r'<script\b[^>]*>(.*?)</script>', src, flags=re.S | re.I):
    parts.append(src[last:m.start()]); last = m.end()
parts.append(src[last:])
html = ''.join(parts)
depth = 0
first_neg = None
open_stack = []
for m in re.finditer(r'<div\b[^>]*>|</div>', html):
    if m.group(0).startswith('</'):
        depth -= 1
        if depth < 0 and first_neg is None:
            first_neg = (m.start(), html.count('\n', 0, m.start()) + 1)
            depth = 0
    else:
        depth += 1
        open_stack.append((m.start(), html.count('\n', 0, m.start()) + 1))
print('july.html div depth at EOF:', depth)
if first_neg:
    print('  extra </div> first seen at offset/line:', first_neg)
if depth > 0:
    # report opens that never got closed: the one whose line we can locate is the
    # open at stack position len(stack)-depth
    culprit = open_stack[len(open_stack) - depth] if len(open_stack) >= depth else None
    print('  unclosed <div> candidate (offset, line):', culprit)
    if culprit:
        print('  context:', repr(html[culprit[0]:culprit[0] + 300])[:340])

print('DONE')
