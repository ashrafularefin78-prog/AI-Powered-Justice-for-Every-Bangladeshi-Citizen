import hashlib, os, re, subprocess, sys

PATH='assets/app.js'
code=open(PATH, encoding='utf-8').read()
assert '</textarea' not in code and '</script' not in code

harness=os.path.abspath('_synchk.html')
dump=os.path.abspath('_synchk_dump.txt')
html = ('<!DOCTYPE html><meta charset="utf-8"><textarea id="src" style="display:none">'
        + code +
        '</textarea><script>'
        'try{new Function(document.getElementById("src").value);document.title="SYNTAX_OK"}'
        'catch(e){document.title="SYNTAX_FAIL: "+e.message}'
        '</script>')
open(harness,'w',encoding='utf-8').write(html)

edge=r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
proj=os.path.abspath('.').replace('\\','/')
with open(dump,'wb') as fh:
    subprocess.run([edge,'--headless=new','--disable-gpu','--dump-dom',
                    'file:///'+proj+'/_synchk.html'],
                   stdout=fh, stderr=subprocess.DEVNULL, timeout=120)
out=open(dump,encoding='utf-8',errors='replace').read()
os.remove(harness); os.remove(dump)
m=re.search(r'<title>(SYNTAX_OK|SYNTAX_FAIL[^<]*)</title>', out)
print('SYNTAX GATE:', m.group(1) if m else 'INCONCLUSIVE')
if not m or m.group(1)!='SYNTAX_OK':
    sys.exit('ABORT: app.js does not parse')

sha=hashlib.sha256(open(PATH,'rb').read()).hexdigest()
sec=open('assets/security.js',encoding='utf-8').read()
sec2=re.sub(r"(EXPECTED_APP_SHA\s*=\s*')[0-9a-f]{64}(')", lambda mm:mm.group(1)+sha+mm.group(2), sec)
open('assets/security.js','w',encoding='utf-8').write(sec2)
print('SHA ->', sha[:12])
print('ALL OK')
