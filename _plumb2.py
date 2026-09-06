import subprocess, sys, os, glob, hashlib, re

# --- 1. syntax gate ----------------------------------------------------------
def find_edge():
    cands = glob.glob('C:/Program Files*/Microsoft/Edge/Application/msedge.exe')
    return cands[0] if cands else None

edge = find_edge()
code = open('assets/app.js', encoding='utf-8').read()
doc = ("<!DOCTYPE html><html><head><meta charset='utf-8'></head><body>"
       "<script>var __syn=false;window.onerror=function(){__syn=true;};</script>"
       "<script>\n" + code + "\n</script>"
       "<script>document.title=__syn?'SYN_BAD':'SYN_OK';</script></body></html>")
open('_gate.html', 'w', encoding='utf-8').write(doc)
res = subprocess.run([edge, '--headless=new', '--disable-gpu', '--dump-dom',
                      'file:///' + os.path.abspath('_gate.html').replace('\\', '/')],
                     capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=60)
os.remove('_gate.html')
if 'SYN_OK' not in (res.stdout or ''):
    print('GATE_FAIL: app.js does not parse'); sys.exit(1)
print('GATE_OK')

# --- 2. SHA + tokens ----------------------------------------------------------
h = hashlib.sha256(open('assets/app.js', 'rb').read()).hexdigest()
sec = open('assets/security.js', encoding='utf-8').read()
sec, n = re.subn(r"var EXPECTED_APP_SHA = '[0-9a-f]{64}';",
                 "var EXPECTED_APP_SHA = '%s';" % h, sec)
assert n == 1
open('assets/security.js', 'w', encoding='utf-8', newline='').write(sec)
print('security.js SHA ->', h[:12])

files = [p for p in glob.glob('*.html') + glob.glob('*.py') + ['assets/security.js']
         if not p.startswith('_') and 'all-in-one' not in p.lower()]
cnt = 0
for p in files:
    try: s = open(p, encoding='utf-8').read()
    except Exception: continue
    if 'app62' in s:
        open(p, 'w', encoding='utf-8', newline='').write(s.replace('app62', 'app63'))
        cnt += 1
print('tokens app62->app63 in %d files' % cnt)

# --- 3. builds -----------------------------------------------------------------
for f in ('_plumb2.py',):
    pass
os.remove('_plumb2.py') if False else None
r1 = subprocess.run([sys.executable, 'build_standalone.py'], capture_output=True, text=True)
print(r1.stdout.strip().splitlines()[-1] if r1.stdout else r1.stderr[-200:])
r2 = subprocess.run([sys.executable, 'build_standalone.py'], capture_output=True, text=True)
print(r2.stdout.strip().splitlines()[-1] if r2.stdout else r2.stderr[-200:])
env = dict(os.environ, PYTHONIOENCODING='utf-8')
r3 = subprocess.run([sys.executable, 'build_allinone.py'], capture_output=True, text=True, env=env)
tail = [l for l in (r3.stdout or '').strip().splitlines() if l][-3:]
print('\n'.join(tail))
