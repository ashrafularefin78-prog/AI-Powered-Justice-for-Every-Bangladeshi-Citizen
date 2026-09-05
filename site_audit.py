import re, sys, os
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dla-website'))

def strip_js(src):
    # remove strings (incl. template literals) and comments via scan
    out = []
    i, n = 0, len(src)
    while i < n:
        c = src[i]
        if c == '`':
            i += 1
            while i < n:
                if src[i] == '\\': i += 2; continue
                if src[i] == '`': i += 1; break
                i += 1
            out.append("''")
        elif c == chr(34) or c == chr(39):
            q = c; i += 1
            while i < n:
                if src[i] == '\\': i += 2; continue
                if src[i] == q: i += 1; break
                i += 1
            out.append("''")
        elif c == '/' and i+1 < n and src[i+1] == '/':
            while i < n and src[i] != '\n': i += 1
        elif c == '/' and i+1 < n and src[i+1] == '*':
            j = src.find('*/', i+2)
            i = n if j < 0 else j+2
            out.append(' ')
        else:
            out.append(c); i += 1
    return ''.join(out)

print('== JS balance check ==')
for f in ('assets/app.js', 'assets/security.js'):
    if not os.path.exists(f): print(f, 'MISSING'); continue
    src = open(f, encoding='utf-8', errors='replace').read()
    s = strip_js(src)
    report = []
    for name, o, c in (('braces','{','}'), ('parens','(',')'), ('brackets','[',']')):
        co, cc = s.count(o), s.count(c)
        if co != cc: report.append(f'{name} {co}/{cc} (diff {co-cc})')
    print(f, 'OK' if not report else 'IMBALANCE: ' + '; '.join(report))
    # last 200 chars of stripped source can reveal truncation
    tail = s[-120:].replace('\n', ' ')
    print('   tail:', tail[-100:])

print()
print('== HTML checks ==')
for f in sorted(x for x in os.listdir('.') if x.endswith('.html')):
    src = open(f, encoding='utf-8', errors='replace').read()
    # remove inline script bodies so JS template strings don't pollute tag counts
    html_only_parts, last = [], 0
    for m in re.finditer(r'<script\b[^>]*>(.*?)</script>', src, flags=re.S | re.I):
        html_only_parts.append(src[last:m.start()])
        html_only_parts.append(m.group(0)[:m.group(0).find('>') + 1] + '</script>')
        last = m.end()
    html_only_parts.append(src[last:])
    html_only = ''.join(html_only_parts)
    src_for_tags = html_only
    issues = []
    # tag balance for common containers (outside script bodies)
    for tag in ('section', 'div', 'ul', 'footer', 'nav', 'style', 'script'):
        o = len(re.findall(rf'<{tag}[\s>]', src_for_tags))
        c = len(re.findall(rf'</{tag}>', src_for_tags))
        # void-safe: none of these are void
        if o != c: issues.append(f'<{tag}> {o} open / {c} close')
    # asset refs exist (check full src incl. scripts is fine for href/src)
    for m in re.finditer(r'(?:href|src)="([^"]+)"', src_for_tags):
        p = m.group(1)
        if p.startswith(('http', '//', '#', 'mailto:', 'tel:', 'data:')): continue
        p = p.split('?')[0].split('#')[0]
        if p and not os.path.exists(p): issues.append(f'MISSING FILE {p}')
    # css link present?
    if 'styles.css' not in src and f != 'index.html':
        issues.append('no styles.css link')
    if 'app.js' not in src and f not in ('index.html',):
        issues.append('no app.js script')
    print(f, '-> OK' if not issues else ' -> ' + ' | '.join(issues))
