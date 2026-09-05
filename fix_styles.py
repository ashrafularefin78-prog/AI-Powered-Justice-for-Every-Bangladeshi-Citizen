# -*- coding: utf-8 -*-
"""One-off repair: restore CSS families lost during the multi-page split.

Problem: assets/styles.css was generated once from an early snapshot and frozen.
Later component CSS (complaint box .cbx-*, auth wizard .as-*/.auth-wstep*, chat
memory .cb-mem, and the 2026 chat redesign blocks) never made it in, while
build_pages.py strips inline <style> blocks from section slices. Result: split
pages render complaint/chat/auth components unstyled.

Fix: collect every class token used in the 8 split pages, find tokens with no
definition in styles.css, and append the style blocks that define them —
backup blocks (index.html.bak-pre / .bak-pro) first, then the newest chat
redesign blocks from the live index.html so they win the cascade.
"""
import re, hashlib, sys, os
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)))

ROOT = 'dla-website'
SPLIT_PAGES = ['index.html', 'ai.html', 'justice.html', 'government.html',
               'sheguard.html', 'july.html', 'blueprints.html', 'contact.html']

def read(p):
    with open(p, encoding='utf-8') as f:
        return f.read()

def style_blocks(text):
    return re.findall(r'<style>.*?</style>', text, re.S)

css_path = ROOT + '/assets/styles.css'
css = read(css_path)

# ---- 1. class tokens actually used in split-page markup --------------------
tokens = set()
for page in SPLIT_PAGES:
    html = read(ROOT + '/' + page)
    for m in re.finditer(r'class="([^"]+)"', html):
        for tok in m.group(1).split():
            if re.fullmatch(r'[a-zA-Z][a-zA-Z0-9_-]*', tok):
                tokens.add(tok)
# also tokens created by JS (chat messages, dynamic rows)
app = read(ROOT + '/assets/app.js')
for m in re.finditer(r'class=\\?"([a-zA-Z][a-zA-Z0-9_ -]+)\\?"', app):
    for tok in m.group(1).split():
        if re.fullmatch(r'[a-zA-Z][a-zA-Z0-9_-]*', tok):
            tokens.add(tok)

def defined(tok, stylesheet):
    return re.search(r'\.' + re.escape(tok) + r'(?=[{ ,:.>\[~+])', stylesheet) is not None

# ignore utility/state/icon namespaces handled elsewhere
SKIP_PREFIX = ('fa', 'fas', 'far', 'fab', 'fa-')
missing = sorted(t for t in tokens
                 if not defined(t, css) and not t.startswith(SKIP_PREFIX))
print('used tokens:', len(tokens), '| missing from styles.css:', len(missing))

# ---- 2. provider blocks -----------------------------------------------------
pre_blocks = style_blocks(read(ROOT + '/index.html.bak-pre'))
pro_blocks = style_blocks(read(ROOT + '/index.html.bak-pro'))
idx = read(ROOT + '/index.html')
lines = idx.splitlines(keepends=True)
new_chat = []
for s, e in [(6615, 6728), (6889, 6906), (7019, 7194)]:
    chunk = ''.join(lines[s - 1:e])
    assert chunk.lstrip().startswith('<style>'), chunk[:60]
    new_chat.append(chunk)

def block_defines(block, tok):
    return re.search(r'\.' + re.escape(tok) + r'\s*[{ ,.:]', block) is not None

appended, seen, resolved = [], set(), set()
css_working = css

def try_append(blocks, source):
    global css_working
    for b in blocks:
        hits = [t for t in missing if t not in resolved and block_defines(b, t)]
        if not hits:
            continue
        h = hashlib.md5(b.encode()).hexdigest()
        if h in seen:
            resolved.update(hits)
            continue
        seen.add(h)
        appended.append((source, b, hits))
        css_working += '\n' + b[len('<style>'):-len('</style>')]
        resolved.update(hits)

try_append(pre_blocks, 'bak-pre')   # oldest first
try_append(pro_blocks, 'bak-pro')
try_append(new_chat, 'index-new')   # newest last -> wins cascade

# ---- 3. write repaired stylesheet ------------------------------------------
banner = ('\n\n/* ===== RESTORED: component CSS lost in the multi-page split =====\n'
          '   Sources: index.html.bak-pre / .bak-pro (complaint box, auth wizard,\n'
          '   chat memory) and the 2026 chat-redesign blocks from index.html.\n'
          '   Order preserved oldest -> newest so later overrides win. */\n')
with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css + banner + '\n'.join(b[1][len('<style>'):-len('</style>')] for b in appended) + '\n')

print('appended blocks:', len(appended))
for source, _, hits in appended:
    print('  +', source, '->', ', '.join(hits[:8]) + ('...' if len(hits) > 8 else ''))

# ---- 4. verify ---------------------------------------------------------------
final = read(css_path)
still = [t for t in missing if not defined(t, final)]
print('resolved:', len(missing) - len(still), '| still undefined:', len(still))
for t in still[:40]:
    print('  ?', t)
