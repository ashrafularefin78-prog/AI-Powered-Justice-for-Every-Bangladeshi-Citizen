import sys, re
sys.stdout.reconfigure(encoding='utf-8')
import os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dla-website'))

# --- 1. july.html: decode literal backslash-u escapes in HTML text to real Bengali ---
raw = open('july.html', encoding='utf-8', newline='').read()
pat = re.compile(r'\\u([0-9a-fA-F]{4})')
n = len(pat.findall(raw))
decoded = pat.sub(lambda m: chr(int(m.group(1), 16)), raw)
open('july.html', 'w', encoding='utf-8', newline='').write(decoded)
print('july.html: decoded', n, 'unicode escapes to real Bengali characters')

# --- 2. app.js: fix wrong-script digit escapes (u0e68 -> u09e6, u0668 -> u09ee) ---
src = open('assets/app.js', encoding='utf-8', newline='').read()
ESC_THAI = chr(92) + 'u0e68'      # \u0e68 as literal text
ESC_AR8  = chr(92) + 'u0668'
ESC_BN0  = chr(92) + 'u09e6'
ESC_BN8  = chr(92) + 'u09ee'
c1 = src.count(ESC_THAI); c2 = src.count(ESC_AR8)
src = src.replace(ESC_THAI, ESC_BN0).replace(ESC_AR8, ESC_BN8)
open('assets/app.js', 'w', encoding='utf-8', newline='').write(src)
print('app.js: digit escapes fixed:', c1, '+', c2)

# --- 3. Verify final state ---
BS = chr(92)
raw2 = open('july.html', encoding='utf-8').read()
ok1 = 'পানি লাগবে পানি' in raw2
ok2 = 'মীর মাহফুজুর রহমান মুগ্ধ' in raw2
ok3 = (BS + 'u09') not in raw2 and (BS + 'u0e') not in raw2
print('july slogan ok:', ok1, '| name ok:', ok2, '| no leftover escapes:', ok3)
src2 = open('assets/app.js', encoding='utf-8').read()
print('app.js thai/arabic escapes left:', src2.count('u0e68'), src2.count('u0668'))
print('app.js mugdho key refs:', src2.count('mir_mugdho'))
