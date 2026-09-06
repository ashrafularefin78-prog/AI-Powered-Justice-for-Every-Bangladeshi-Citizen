import re, hashlib, subprocess, os, sys

PATH='assets/app.js'
src=open(PATH, encoding='utf-8').read()

def lit_span(src, decl):
    m = re.search(decl, src)
    assert m, decl
    i = m.end()-1
    depth=0
    for j in range(i, len(src)):
        if src[j]=='{': depth+=1
        elif src[j]=='}':
            depth-=1
            if depth==0: break
    return i, j+1

# --- iterative comma repair inside the two object literals -------------------
for decl, name in ((r'var aliasMap=\{', 'aliasMap'), (r'var cR=\{', 'cR')):
    a,b = lit_span(src, decl)
    lit = src[a:b]
    prev = None
    while prev != lit:
        prev = lit
        lit = re.sub(r'\{\s*,', '{', lit)
        lit = re.sub(r',\s*,', ',', lit)
        lit = re.sub(r',\s*\}', ' }', lit)
    if lit != src[a:b]:
        src = src[:a] + lit + src[b:]
        print(name, 'literal repaired ->', len(lit), 'chars; starts:', lit[:70])

open(PATH,'w',encoding='utf-8',newline='').write(src)

# --- residual scan ------------------------------------------------------------
bad=[p for p in (r'\{\s*,', r',\s*,', r',\s*\}') if re.search(p, src)]
print('residual bad patterns:', bad if bad else 'none')

# --- REAL JS SYNTAX GATE via headless Edge ------------------------------------
harness = os.path.abspath('_synchk.html')
open(harness,'w',encoding='utf-8').write(
 '<script>fetch("assets/app.js").then(r=>r.text()).then(t=>{try{new Function(t);'
 'document.title="SYNTAX_OK"}catch(e){document.title="SYNTAX_FAIL: "+e.message}})'
 '.catch(e=>{document.title="FETCH_FAIL: "+e.message});</script>')

edge=r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
proj=os.path.abspath('.').replace('\\','/')
out=subprocess.run([edge,'--headless=new','--disable-gpu','--dump-dom',
                    'file:///'+proj+'/_synchk.html'],
                   capture_output=True, text=True, timeout=90).stdout
m=re.search(r'<title>(SYNTAX_OK|SYNTAX_FAIL[^<]*|FETCH_FAIL[^<]*)</title>', out)
print('SYNTAX GATE:', m.group(1) if m else 'INCONCLUSIVE')
os.remove(harness)
if not m or not m.group(1).startswith('SYNTAX_OK'):
    sys.exit('ABORT: app.js still does not parse')

# --- SHA ----------------------------------------------------------------------
sha=hashlib.sha256(open(PATH,'rb').read()).hexdigest()
sec=open('assets/security.js',encoding='utf-8').read()
sec2=re.sub(r"(EXPECTED_APP_SHA\s*=\s*')[0-9a-f]{64}(')", lambda mm:mm.group(1)+sha+mm.group(2), sec)
open('assets/security.js','w',encoding='utf-8').write(sec2)
print('SHA ->', sha[:12])
print('ALL OK')
