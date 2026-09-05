import os, sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(ROOT, 'dla-website'))

SCRIPT_LINE = '<script src="assets/app.js?v=app35"></script>'
FAVICON = '  <link rel="icon" type="image/svg+xml" href="assets/img/favicon.svg">\n'

# 1. Fix duplicated tails: keep only content up to and including the first </html>
for fname in ('index.html', 'about.html', 'ai.html'):
    src = open(fname, encoding='utf-8', newline='').read()
    first = src.find('</html>')
    if first < 0:
        print(fname, ': no </html> found - SKIP')
        continue
    tail = src[first:]
    closed = tail.count('</html>')
    if closed == 1:
        print(fname, ': tail already clean')
    else:
        # Safety: verify the duplicate region holds no unique markup
        dup_region = src[first + len('</html>'):].replace(SCRIPT_LINE, '').replace('</body>', '').replace('</html>', '').strip()
        if dup_region:
            print(fname, ': WARNING duplicate region has unexpected content:', repr(dup_region[:200]))
        src = src[:first + len('</html>')] + '\n'
        open(fname, 'w', encoding='utf-8', newline='').write(src)
        print(fname, ': truncated duplicate tail (had', closed, '</html>)')

# 2. Add favicon link to every page that lacks one
pages = [f for f in os.listdir('.') if f.endswith('.html')]
for fname in pages:
    src = open(fname, encoding='utf-8', newline='').read()
    if 'rel="icon"' in src or 'rel="shortcut icon"' in src:
        print(fname, ': favicon already present')
        continue
    anchor = '<title>'
    i = src.find(anchor)
    if i < 0:
        print(fname, ': no <title> to anchor favicon - SKIP')
        continue
    j = src.find('>', i) + 1
    src = src[:j] + '\n' + FAVICON.rstrip('\n') + src[j:]
    open(fname, 'w', encoding='utf-8', newline='').write(src)
    print(fname, ': favicon link added')

# 3. Bump JS cache buster app35 -> app36 everywhere
for fname in pages:
    src = open(fname, encoding='utf-8', newline='').read()
    if 'app.js?v=app35' in src:
        src = src.replace('app.js?v=app35', 'app.js?v=app36')
        open(fname, 'w', encoding='utf-8', newline='').write(src)
        print(fname, ': cache buster -> app36')

print('DONE')
