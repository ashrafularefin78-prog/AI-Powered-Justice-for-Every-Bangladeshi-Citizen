# -*- coding: utf-8 -*-
"""Build _verify_july.html: self-contained copy of july.html (inline CSS+JS) for sandbox preview."""
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

html = open('july.html', encoding='utf-8', newline='').read()
css = open('assets/styles.css', encoding='utf-8', newline='').read()
app = open('assets/app.js', encoding='utf-8', newline='').read()
sec = open('assets/security.js', encoding='utf-8', newline='').read()

# inline styles.css in place of the link tag
html = re.sub(r'<link rel="stylesheet"[^>]*assets/styles\.css[^>]*>',
              lambda m: '<style>\n' + css + '\n</style>', html, count=1)

# neutralize remaining local subresource refs (sandbox 404s on them anyway)
html = html.replace('assets/img/favicon.svg', 'data:image/svg+xml,')

# inline app.js
html = re.sub(r'<script src="assets/app\.js[^"]*"></script>',
              lambda m: '<script>\n' + app + '\n</script>', html, count=1)
# inline security.js
html = re.sub(r'<script src="assets/security\.js[^"]*"></script>',
              lambda m: '<script>\n' + sec + '\n</script>', html, count=1)

open('_verify_july.html', 'w', encoding='utf-8', newline='').write(html)
print('_verify_july.html written:', len(html))
