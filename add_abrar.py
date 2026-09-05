import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(ROOT, 'dla-website'))

# ============ 1. app.js: Abrar KB block ============
src = open('assets/app.js', encoding='utf-8', newline='').read()
if 'cR["abrar_fahad_bio"]' in src:
    print('app.js: Abrar KB already present - skip')
else:
    kb = '''/* 2026-09-05 Shaheed Abrar Fahad memorial knowledge (bilingual) */
cR["abrar_fahad_bio"]="Shaheed Abrar Fahad Rabbi (\\u0986\\u09ac\\u09b0\\u09be\\u09b0 \\u09ab\\u09be\\u09b9\\u09be\\u09a6 \\u09b0\\u09ac\\u09cd\\u09ac\\u09c0; 12 Feb 1998 - 7 Oct 2019) was a second-year EEE student at BUET, murdered in his dormitory by BUET-unit Chhatra League leaders. Born in Kushtia (home: Kumarkhali); father Barkatullah (BRAC inspection officer), mother Rokaya Khatun (kindergarten teacher); younger brother Abrar Fayaz, who later joined BUET (Mechanical, 2022). Educated at Kushtia Zilla School and Notre Dame College; joined BUET EEE in 2018. He was posthumously awarded the Independence Award 2025, Bangladesh's highest civilian honour, in the 'Rebellious Youth' category. | \\u09b6\\u09b9\\u09c0\\u09a6 \\u0986\\u09ac\\u09b0\\u09be\\u09b0 \\u09ab\\u09be\\u09b9\\u09be\\u09a6 (\\u09e7\\u09e8 \\u09ab\\u09c7\\u09ac\\u09cd\\u09b0\\u09c1\\u09df\\u09be\\u09b0\\u09bf \\u09e7\\u09ef\\u09ef\\u09ee - \\u09ed \\u0985\\u0995\\u09cd\\u099f\\u09cb\\u09ac\\u09b0 \\u09e8\\u09e6\\u09e7\\u09ef) \\u09ac\\u09c1\\u09df\\u09c7\\u099f\\u09c7\\u09b0 \\u09a4\\u09dc\\u09bf\\u0993 \\u0993 \\u0987\\u09b2\\u09c7\\u0995\\u099f\\u09cd\\u09b0\\u09a8\\u09bf\\u0995 \\u09aa\\u09cd\\u09b0\\u0995\\u09cc\\u09b6\\u09b2\\u09c7\\u09b0 \\u09a6\\u09cd\\u09ac\\u09bf\\u09a4\\u09c0\\u09df \\u09ac\\u09b0\\u09cd\\u09b7\\u09c7\\u09b0 \\u09b6\\u09bf\\u0995\\u09cd\\u09b7\\u09be\\u09b0\\u09cd\\u09a5\\u09c0 \\u099b\\u09bf\\u09b2\\u09c7\\u09a8\\u0964 \\u0995\\u09c1\\u09b7\\u09cd\\u099f\\u09bf\\u09df\\u09be\\u09df \\u099c\\u09a8\\u09cd\\u09ae; \\u09aa\\u09bf\\u09a4\\u09be \\u09ac\\u09b0\\u0995\\u09a4\\u09c1\\u09b2\\u09cd\\u09b2\\u09be\\u09b9, \\u09ae\\u09be \\u09b0\\u09cb\\u0995\\u09c7\\u09df\\u09be \\u0996\\u09be\\u09a4\\u09c1\\u09a8\\u0964 \\u09e8\\u09e6\\u09e8\\u09eb \\u09b8\\u09be\\u09b2\\u09c7 \\u09a4\\u09be\\u0995\\u09c7 \\u09ae\\u09b0\\u09a3\\u09cb\\u09a4\\u09cd\\u09a4\\u09b0 \\u09b8\\u09cd\\u09ac\\u09be\\u09a7\\u09c0\\u09a8\\u09a4\\u09be \\u09aa\\u09c1\\u09b0\\u09b8\\u09cd\\u0995\\u09be\\u09b0\\u09c7 \\u09ad\\u09c2\\u09b7\\u09bf\\u09a4 \\u0995\\u09b0\\u09be \\u09b9\\u09af\\u09bc\\u0964";
cR["abrar_fahad_death"]="How Abrar Fahad was killed: after Facebook posts criticizing Bangladesh-India agreements (Mongla port use, Feni river water withdrawal, LNG import terms), BCL leaders suspected him of being a Shibir activist. On 6 Oct 2019, exam period brought him back to Sher-e-Bangla Hall. That night he was taken to room 2011, his two phones and laptop checked, then beaten for hours with cricket stamps, a skipping rope and blunt weapons by at least 20 attackers. He vomited repeatedly, was moved to room 2005, and was pronounced dead around 3:00 AM on 7 Oct 2019 on the ground floor. The autopsy confirmed death by blunt-force beating. | \\u09ec \\u0985\\u0995\\u09cd\\u099f\\u09cb\\u09ac\\u09b0 \\u09e8\\u09e6\\u09e7\\u09ef \\u09b0\\u09be\\u09a4\\u09c7 \\u09b6\\u09c7\\u09b0\\u09c7 \\u09ac\\u09be\\u0982\\u09b2\\u09be \\u09b9\\u09b2\\u09c7\\u09b0 \\u09e8\\u09e6\\u09e7\\u09e7 \\u09a8\\u09ae\\u09cd\\u09ac\\u09b0 \\u0995\\u0995\\u09cd\\u09b7\\u09c7 \\u0985\\u09a8\\u09cd\\u09a4\\u09a4 20 \\u0986\\u0995\\u09cd\\u09b0\\u09ae\\u0995\\u09be\\u09b0\\u09c0 \\u0998\\u09a3\\u09cd\\u099f\\u09be\\u0998\\u09a3\\u09cd\\u099f\\u09bf \\u09aa\\u09bf\\u099f\\u09bf\\u09df\\u09c7 \\u09b9\\u09a4\\u09cd\\u09df\\u09be \\u0995\\u09b0\\u09c7\\u0964 \\u09ad\\u09cb\\u09b0 3 \\u099f\\u09be\\u09df \\u09ae\\u09c3\\u09a4 \\u0998\\u09cb\\u09b7\\u09a3\\u09be\\u0964 \\u09ae\\u09df\\u09a8\\u09be\\u09a4\\u09a6\\u09cd\\u09a8\\u09c7 \\u09ad\\u09cb\\u0982\\u099f \\u099c\\u09a8\\u09bf\\u09a4 \\u09ae\\u09be\\u09b0\\u09a7\\u09cd\\u09ac\\u09b0\\u09c7\\u09b0 \\u09aa\\u09cd\\u09b0\\u09ae\\u09be\\u09a3 \\u09ae\\u09bf\\u09b2\\u09c7\\u0964";
cR["abrar_fahad_post"]="Abrar Fahad's final Facebook post (5 Oct 2019) criticized three India-Bangladesh deals signed during the PM's visit: 1) Bangladesh letting India use Mongla and Chittagong ports - though history showed how the port was opened for famine relief in 1947-era Bengal; 2) giving India 1.85 cusecs of Feni river water while Indian states refuse river-water sharing among themselves; 3) importing LNG from a country that once blocked coal-and-stone exports, while gas shortages shut Bangladeshi factories. It ended with Tagore's couplet: 'parer karone swartho diya boli / e jibon mon sokoli dao...' - giving one's all for others' interests. | \\u09b6\\u09c7\\u09b7 \\u09ab\\u09c7\\u09b8\\u09ac\\u09c1\\u0995 \\u09aa\\u09cb\\u09b8\\u09cd\\u099f\\u09c7 \\u09a4\\u09bf\\u09a8\\u099f\\u09bf \\u099a\\u09c1\\u0995\\u09cd\\u09a4\\u09bf\\u09b0 \\u09b8\\u09ae\\u09be\\u09b2\\u09cb\\u099a\\u09a8\\u09be \\u0995\\u09b0\\u09c7\\u09a8 - \\u09ae\\u09c1\\u0982\\u09b2\\u09be \\u0993 \\u099a\\u099f\\u09cd\\u099f\\u0997\\u09cd\\u09b0\\u09be\\u09ae \\u09ac\\u09a8\\u09cd\\u09a6\\u09b0 \\u09ac\\u09cd\\u09af\\u09ac\\u09b9\\u09be\\u09b0, \\u09ab\\u09c7\\u09a8\\u09c0 \\u09a8\\u09a6\\u09c0\\u09b0 \\u09aa\\u09be\\u09a8\\u09bf \\u09aa\\u09cd\\u09b0\\u09a4\\u09cd\\u09df\\u09be\\u09b9\\u09be\\u09b0 \\u0993 \\u098f\\u09b2\\u09aa\\u09bf\\u0997 \\u0986\\u09ae\\u09a6\\u09be\\u09a8\\u09c0\\u0964 \\u09b6\\u09c7\\u09b7\\u09c7 \\u09b0\\u09ac\\u09c0\\u09a8\\u09cd\\u09a6\\u09cd\\u09b0\\u09a8\\u09be\\u09a5\\u09c7\\u09b0 \\u0995\\u09ac\\u09bf\\u09a4\\u09be\\u09b0 \\u099a\\u09df\\u0997\\u09c1\\u09b2\\u09cb \\u0989\\u09a6\\u09cd\\u09a7\\u09c3\\u09a4 \\u0995\\u09b0\\u09c7\\u09a8\\u0964";
cR["abrar_fahad_verdict"]="Justice for Abrar Fahad: his father filed a case against 19 accused at Chawkbazar police station. On 13 Nov 2019, DB police submitted a charge sheet against 25. On 7 Dec 2021, Dhaka Speedy Trial Tribunal-1 (Judge Abu Jafar Kamruzzaman) sentenced 20 accused to death and 5 to life imprisonment - 3 remain absconding. The tribunal said the accused 'in collusion brought false, fabricated accusations against Abrar Fahad as a Shibir suspect and killed him with premeditation.' On 16 Mar 2025 the High Court (Justices Syed Enayet Hossain & AKM Asaduzzaman) upheld 20 death sentences and 5 life terms; the full verdict was published 3 May 2025. | \\u09ec \\u09a1\\u09bf\\u09b8\\u09c7\\u09ae\\u09cd\\u09ac\\u09b0 \\u09e8\\u09e6\\u09e8\\u09e7 \\u098f \\u09e8\\u09e6 \\u099c\\u09a8\\u09c7\\u09b0 \\u09ae\\u09c3\\u09af\\u09bc\\u09c1\\u09a6\\u09a3\\u09cd\\u09a1 \\u0993 \\u09eb \\u099c\\u09a8\\u09c7\\u09b0 \\u09af\\u09be\\u09ac\\u099c\\u09cd\\u099c\\u09c0\\u09ac\\u09a8 \\u0995\\u09be\\u09b0\\u09be\\u09a6\\u09a6\\u09a3\\u09cd\\u09a1\\u0964 \\u09e9 \\u09ae\\u09be\\u09b0\\u09cd\\u099a \\u09e8\\u09e6\\u09e8\\u09eb \\u098f \\u09b9\\u09be\\u0987\\u0995\\u09cb\\u09b0\\u09cd\\u099f \\u09b0\\u09be\\u09af\\u09bc \\u09ac\\u09b9\\u09be\\u09b2 \\u0995\\u09b0\\u09c7\\u0964 \\u09aa\\u09c2\\u09b0\\u09cd\\u09a3 \\u09b0\\u09be\\u09af\\u09bc \\u09aa\\u09cd\\u09b0\\u0995\\u09be\\u09b6 3 \\u09ae\\u09c7 \\u09e8\\u09e6\\u09e8\\u09eb\\u0964";
cR["abrar_fahad_legacy"]="Abrar Fahad's legacy: Bangabandhu Avenue in Dhaka was renamed Shaheed Abrar Fahad Avenue (25 Mar 2025). Kushtia Stadium became Shaheed Abrar Fahad Stadium (2025). The 'Eight Pillars Against Aggression' memorial was founded at Palashi intersection (Oct 2025), and BUET installed a memorial plaque in Sher-e-Bangla Hall. His killing seeded the resistance that grew into the July 2024 uprising. Culture: short film 'Room Number 2011' (Oct 2024); books 'Chetonay Abrar Fahad' (Farjana Boby Chumki, 2025), 'Gaza Theke Bangladesh' (Shamshun Zahan Akhtari); novel 'Akor' (Mita Ali, 2025). Calls to declare 7 Oct a national day were accepted by the government in Oct 2025. | \\u09ac\\u0982\\u0997\\u09ac\\u09a8\\u09cd\\u09a7\\u09c1 \\u0985\\u09cd\\u09af\\u09be\\u09ad\\u09bf\\u09a8\\u09bf\\u09c9\\u09b0 \\u09a8\\u09be\\u09ae \\u09b9\\u09df \\u09b6\\u09b9\\u09c0\\u09a6 \\u0986\\u09ac\\u09b0\\u09be\\u09b0 \\u09ab\\u09be\\u09b9\\u09be\\u09a6 \\u0985\\u09cd\\u09af\\u09be\\u09ad\\u09bf\\u09a8\\u09bf\\u09c9\\u09b0 (\\u09e8\\u09eb \\u09ae\\u09be\\u09b0\\u09cd\\u099a \\u09e8\\u09e6\\u09e8\\u09eb)\\u0964 \\u0995\\u09c1\\u09b7\\u09cd\\u099f\\u09bf\\u09df\\u09be \\u09b8\\u09cd\\u099f\\u09c7\\u09a1\\u09bf\\u09df\\u09be\\u09ae \\u09b9\\u09df \\u09b6\\u09b9\\u09c0\\u09a6 \\u0986\\u09ac\\u09b0\\u09be\\u09b0 \\u09ab\\u09be\\u09b9\\u09be\\u09a6 \\u09b8\\u09cd\\u099f\\u09c7\\u09a1\\u09bf\\u09df\\u09be\\u09ae\\u0964 \\u09aa\\u09b2\\u09be\\u09b6\\u09c0\\u09df \\u0986\\u0997\\u09cd\\u09b0\\u09b8\\u09a8\\u09ac\\u09bf\\u09b0\\u09cb\\u09a7\\u09c0 \\u0986\\u099f\\u09b8\\u09cd\\u09a4\\u09ae\\u09cd\\u09ad\\u09c7\\u09b0 \\u09ad\\u09bf\\u09a4\\u09cd\\u09a4\\u09bf\\u09b8\\u09cd\\u09a5\\u09b2 \\u09b8\\u09cd\\u09a5\\u09be\\u09aa\\u09a8 \\u09b9\\u09af\\u09bc (\\u0985\\u0995\\u09cd\\u099f\\u09cb\\u09ac\\u09b0 \\u09e8\\u09e6\\u09e8\\u09eb)\\u0964";
cR["abrar_fahad_archive"]="AbrarFahadArchive.org was built by his BUET batchmates of the '17 batch as a war against forgetting. Its dedication reads: 'Someone so outspoken yet so gentle. Someone so bright yet so modest. Someone who said what needed to be said and paid the highest price for it. To his memory we cherish. To his name we look forward.' It hosts memories and stories about Abrar, photo and video galleries of the movement, news links about the murder, and a day-by-day timeline of 6-16 Oct and 2 Nov 2019. | \\u09a4\\u09be\\u09b0 \\u09ac\\u09c1\\u09df\\u09c7\\u099f \\u09e7\\u09ed \\u09ac\\u09cd\\u09af\\u09be\\u099a\\u09c7\\u09b0 \\u09ac\\u09a8\\u09cd\\u09a7\\u09c1\\u09b0\\u09be \\u09ac\\u09bf\\u09b8\\u09cd\\u09ae\\u09c3\\u09a4\\u09bf\\u09b0 \\u09ac\\u09bf\\u09b0\\u09c1\\u09a6\\u09cd\\u09a7\\u09c7 \\u09af\\u09c1\\u09a6\\u09cd\\u09a7 \\u0995\\u09b0\\u09a4\\u09c7 \\u0985\\u09ac\\u09b0\\u09be\\u09b0\\u09ab\\u09be\\u09b9\\u09be\\u09a6\\u0986\\u09b0\\u09cd\\u0995\\u09be\\u0987\\u09ad\\u0964\\u0985\\u09b0\\u09cd\\u0997 \\u09a4\\u09c8\\u09b0\\u09c0 \\u0995\\u09b0\\u09c7\\u099b\\u09c7 - \\u09b8\\u09cd\\u09ae\\u09c3\\u09a4\\u09bf, \\u099b\\u09ac\\u09bf, \\u09ad\\u09bf\\u09a1\\u09bf\\u0993 \\u0993 \\u09a6\\u09bf\\u09a8\\u0993\\u09df\\u09be\\u09b0 \\u099f\\u09be\\u0987\\u09ae\\u09b2\\u09be\\u0987\\u09a8 \\u09b8\\u0987\\u099f\\u09c7 \\u09b8\\u0982\\u09b0\\u0995\\u09cd\\u09b7\\u09bf\\u09a4\\u0964";
aliasMap["abrar fahad"]="abrar_fahad_bio";
aliasMap["abrar"]="abrar_fahad_bio";
aliasMap["who killed abrar"]="abrar_fahad_death";
aliasMap["abrar fahad murder"]="abrar_fahad_death";
aliasMap["abrar fahad killing"]="abrar_fahad_death";
aliasMap["abrar fahad verdict"]="abrar_fahad_verdict";
aliasMap["abrar fahad justice"]="abrar_fahad_verdict";
aliasMap["abrar fahad court"]="abrar_fahad_verdict";
aliasMap["abrar fahad award"]="abrar_fahad_bio";
aliasMap["abrar fahad independence award"]="abrar_fahad_legacy";
aliasMap["abrar fahad post"]="abrar_fahad_post";
aliasMap["abrar fahad facebook post"]="abrar_fahad_post";
aliasMap["abrar fahad legacy"]="abrar_fahad_legacy";
aliasMap["abrar fahad avenue"]="abrar_fahad_legacy";
aliasMap["room 2011"]="abrar_fahad_legacy";
aliasMap["buet student killed"]="abrar_fahad_death";
aliasMap["abrarfahadarchive"]="abrar_fahad_archive";
aliasMap["\\u0986\\u09ac\\u09b0\\u09be\\u09b0 \\u09ab\\u09be\\u09b9\\u09be\\u09a6"]="abrar_fahad_bio";
aliasMap["\\u0986\\u09ac\\u09b0\\u09be\\u09b0"]="abrar_fahad_bio";
aliasMap["\\u09b6\\u09b9\\u09c0\\u09a6 \\u0986\\u09ac\\u09b0\\u09be\\u09b0"]="abrar_fahad_bio";
aliasMap["\\u0986\\u09ac\\u09b0\\u09be\\u09b0 \\u09ab\\u09be\\u09b9\\u09be\\u09a6 \\u09b9\\u09a4\\u09cd\\u09df\\u09be\\u0995\\u09be\\u09a3\\u09cd\\u09a1"]="abrar_fahad_death";
aliasMap["\\u0986\\u09ac\\u09b0\\u09be\\u09b0 \\u09ac\\u09bf\\u099a\\u09be\\u09b0"]="abrar_fahad_verdict";
aliasMap["\\u0986\\u09ac\\u09b0\\u09be\\u09b0\\u09c7\\u09b0 \\u09aa\\u09cb\\u09b8\\u09cd\\u099f"]="abrar_fahad_post";
'''
    anchor = '/* processMessage dispatcher: grounded frontier LLM first, local engine as fallback */'
    i = src.find(anchor)
    assert i > 0, 'dispatcher anchor missing'
    src = src[:i] + kb + src[i:]
    print('app.js: Abrar KB block inserted (6 entries + 22 aliases)')

if 'var isAbrarCard' in src:
    print('app.js: Abrar portrait card already present - skip')
else:
    card = '''    var isAbrarCard=(k.indexOf('abrar_fahad')===0||(m.indexOf('abrar fahad')>-1||m.indexOf('আবরার ফাহাদ')>-1)&&!showStrip&&k.indexOf('july')!==0);
    if(isAbrarCard){
      var h9='<div style="max-width:220px;margin:0 0 12px;">';
      h9+='<div style="border-radius:12px;overflow:hidden;border:2px solid rgba(185,28,28,.45);box-shadow:0 4px 18px rgba(0,0,0,.25);background:#fff"><img src="assets/img/abrar-fahad.jpg" alt="Shaheed Abrar Fahad" style="width:100%;aspect-ratio:1/1;object-fit:cover;object-position:top center;display:block"></div>';
      h9+='<div style="font-size:9.5px;color:rgba(255,255,255,.5);line-height:1.5;margin-top:5px;">Shaheed Abrar Fahad (1998-2019) - BUET EEE student, killed 7 Oct 2019</div>';
      h9+='<div style="font-size:9.5px;color:rgba(255,255,255,.42);line-height:1.5;"><a href="https://bn.wikipedia.org/wiki/%E0%A6%86%E0%A6%AC%E0%A6%B0%E0%A6%BE%E0%A6%B0_%E0%A6%AB%E0%A6%BE%E0%A6%B9%E0%A6%BE%E0%A6%A6" target="_blank" rel="noopener" style="color:rgba(255,255,255,.55);">Photo: banglanews24 via Bengali Wikipedia</a></div>';
      h9+='</div>';
      return h9;
    }
'''
    anchor2 = '    if(showAbu&&!showStrip){'
    i2 = src.find(anchor2)
    assert i2 > 0, 'showAbu anchor missing'
    src = src[:i2] + card + src[i2:]
    print('app.js: Abrar portrait card inserted')
open('assets/app.js', 'w', encoding='utf-8', newline='').write(src)

# ============ 2. july.html: Abrar memorial section ============
src = open('july.html', encoding='utf-8', newline='').read()
if 'id="abrar-fahad"' not in src:
    sec = '''<section id="abrar-fahad" style="padding:100px 0;background:linear-gradient(135deg,#1a0a0a 0%,#2a1010 50%,#1a0a2a 100%);position:relative;overflow:hidden;border-bottom:1px solid rgba(255,100,68,.15);">
<div class="container" style="max-width:1000px;margin:0 auto;padding:0 24px;position:relative;z-index:1;">
<div style="text-align:center;margin-bottom:40px;">
<span style="display:inline-block;background:linear-gradient(135deg,#ef4444,#f97316);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-weight:700;font-size:13px;letter-spacing:3px;text-transform:uppercase;">The Spark of Resistance</span>
<h2 style="font-size:clamp(28px,4vw,42px);text-align:center;margin:10px 0 8px;">Shaheed <span style="color:#ff6644;">Abrar Fahad</span></h2>
<p style="text-align:center;color:rgba(255,255,255,.5);font-size:16px;margin:0 0 6px;">আবরার ফাহাদ রাব্বি &middot; 12 February 1998 - 7 October 2019</p>
<p style="text-align:center;color:rgba(255,255,255,.65);font-size:15px;font-style:italic;margin:0;">"His question still echoes: why must we give our own to light another's lamp?"</p>
</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:start;">
<div>
<div style="width:100%;aspect-ratio:1/1;border-radius:20px;background:linear-gradient(135deg,rgba(239,68,68,.2),rgba(249,115,22,.2));border:2px solid rgba(255,102,68,.3);overflow:hidden;">
<img src="assets/img/abrar-fahad.jpg" alt="Shaheed Abrar Fahad (1998-2019)" style="width:100%;height:100%;object-fit:cover;object-position:top center;display:block;" loading="lazy">
</div>
<div style="margin-top:10px;text-align:center;font-size:11.5px;line-height:1.7;">
<span style="color:rgba(255,255,255,.5);">Photo: banglanews24.com, via Bengali Wikipedia (fair use - memorial/educational)</span><br>
<a href="https://bn.wikipedia.org/wiki/%E0%A6%86%E0%A6%AC%E0%A6%B0%E0%A6%BE%E0%A6%B0_%E0%A6%AB%E0%A6%BE%E0%A6%B9%E0%A6%BE%E0%A6%A6" target="_blank" rel="noopener" style="color:rgba(255,255,255,.65);text-decoration:none;border-bottom:1px dotted rgba(255,255,255,.4);">বাংলা উইকিপিডিয়া - আবরার ফাহাদ</a>
</div>
</div>
<div>
<div style="margin-bottom:22px;"><h3 style="color:#ff6644;font-size:16px;margin:0 0 8px;">FULL NAME</h3><p style="color:#fff;font-size:15px;margin:0;">Abrar Fahad Rabbi (আবরার ফাহাদ রাব্বি) - known as Rabbi to family</p></div>
<div style="margin-bottom:22px;"><h3 style="color:#ff6644;font-size:16px;margin:0 0 8px;">BORN</h3><p style="color:#fff;font-size:15px;margin:0;">12 February 1998, Kushtia - village home Kumarkhali</p></div>
<div style="margin-bottom:22px;"><h3 style="color:#ff6644;font-size:16px;margin:0 0 8px;">FAMILY</h3><p style="color:#fff;font-size:15px;margin:0;">Father: Barkatullah (BRAC inspection officer)<br>Mother: Rokaya Khatun (kindergarten teacher)<br>Younger brother: Abrar Fayaz - admitted to BUET Mechanical, 2022</p></div>
<div style="margin-bottom:22px;"><h3 style="color:#ff6644;font-size:16px;margin:0 0 8px;">EDUCATION</h3><p style="color:#fff;font-size:15px;margin:0;">Kushtia Mission Primary &rarr; Kushtia Zilla School &rarr; Notre Dame College (Science)<br>BUET, Dept. of Electrical &amp; Electronic Engineering (2018, 2nd year)</p></div>
<div style="margin-bottom:22px;"><h3 style="color:#ff6644;font-size:16px;margin:0 0 8px;">6-7 OCTOBER 2019</h3><p style="color:#fff;font-size:15px;margin:0;">Returned to Sher-e-Bangla Hall for exams. That night, in room 2011, at least 20 Chhatra League leaders beat him for hours over his Facebook posts criticizing Bangladesh-India deals. Pronounced dead at 3:00 AM, 7 October. Autopsy: blunt-force beating.</p></div>
<div style="margin-bottom:0;"><h3 style="color:#ff6644;font-size:16px;margin:0 0 8px;">RESTING PLACE</h3><p style="color:#fff;font-size:15px;margin:0;">Kushtia</p></div>
</div>
</div>
<div style="margin-top:44px;background:rgba(255,255,255,.03);border:1px solid rgba(255,102,68,.25);border-radius:18px;padding:28px 30px;">
<h3 style="color:#ff6644;font-size:18px;margin:0 0 12px;">His final Facebook post</h3>
<p style="color:rgba(255,255,255,.75);font-size:14.5px;line-height:1.8;margin:0 0 12px;">Hours before his death, Abrar questioned three India-Bangladesh deals: giving India access to the <b style="color:#fff;">Mongla and Chittagong ports</b>; granting India <b style="color:#fff;">Feni river water</b> while Indian states refuse sharing among themselves; and importing <b style="color:#fff;">LNG</b> when gas shortages idle our own factories. He closed with Tagore's couplet:</p>
<p style="color:#fff;font-size:15px;font-style:italic;text-align:center;margin:0 0 12px;">"পরের কারণে স্বার্থ দিয়া বলি<br>এ জীবন মন সকলি দাও,<br>তার মত সুখ কোথাও কি আছে<br>আপনার কথা ভুলিয়া যাও।"</p>
<p style="color:rgba(255,255,255,.55);font-size:13.5px;line-height:1.8;margin:0;">That post - and that question - made him a symbol. Justice: on 7 Dec 2021, 20 of his killers were sentenced to death and 5 to life imprisonment; the High Court upheld it on 16 Mar 2025. Bangabandhu Avenue became <b style="color:#fff;">Shaheed Abrar Fahad Avenue</b> (25 Mar 2025); Kushtia Stadium bears his name; the Independence Award 2025 - posthumous, in the Rebellious Youth category. His killing seeded the resistance that grew into the July 2024 uprising.</p>
</div>
<div style="margin-top:26px;text-align:center;font-size:12px;color:rgba(255,255,255,.4);line-height:1.8;">
Sources: <a href="https://bn.wikipedia.org/wiki/%E0%A6%86%E0%A6%AC%E0%A6%B0%E0%A6%BE%E0%A6%B0_%E0%A6%AB%E0%A6%BE%E0%A6%B9%E0%A6%BE%E0%A6%A6" target="_blank" rel="noopener" style="color:rgba(255,255,255,.6);">বাংলা উইকিপিডিয়া</a> &middot;
<a href="https://bn.wikipedia.org/wiki/%E0%A6%86%E0%A6%AC%E0%A6%B0%E0%A6%BE%E0%A6%B0_%E0%A6%AB%E0%A6%BE%E0%A6%B9%E0%A6%BE%E0%A6%A6_%E0%A6%B9%E0%A6%A4%E0%A7%8D%E0%A6%AF%E0%A6%BE%E0%A6%95%E0%A6%BE%E0%A6%A3%E0%A7%8D%E0%A6%A1" target="_blank" rel="noopener" style="color:rgba(255,255,255,.6);">হত্যাকাণ্ড নিবন্ধ</a> &middot;
<a href="https://abrarfahadarchive.org/" target="_blank" rel="noopener" style="color:rgba(255,255,255,.6);">AbrarFahadArchive.org (BUET '17 batchmates)</a>
</div>
</div>
</section>
'''
    anchor3 = '<section id="mir-mugdho"'
    i3 = src.find(anchor3)
    assert i3 > 0, 'mir-mugdho anchor missing'
    src = src[:i3] + sec + src[i3:]
    print('july.html: #abrar-fahad memorial section inserted')

# Update strip card: real portrait + link
m = re.search(r'<div class="martyr-strip-card"[^>]*>(?:(?!</div>).)*?abrar-protest\.jpg', src, flags=re.S)
if m:
    block = m.group(0)
    opener = block[:block.find('>') + 1]
    new_opener = '<div class="martyr-strip-card" style="width:200px;cursor:pointer;" onclick="document.getElementById(\'abrar-fahad\').scrollIntoView({behavior:\'smooth\'})" title="Read Abrar Fahad\'s full memorial">'
    src = src[:m.start()] + new_opener + src[m.start() + len(opener):]
    src = src.replace('<img src="assets/img/abrar-protest.jpg" alt="Justice for Abrar Fahad protest"', '<img src="assets/img/abrar-fahad.jpg" alt="Shaheed Abrar Fahad (1998-2019)"', 1)
    print('july.html: Abrar strip card -> real portrait + memorial link')
# Martyr-list card link
mc = '<div class="martyr-card" data-name="আবরার ফাহাদ" data-district="ঢাকা"'
if mc in src:
    src = src.replace(mc, '<div class="martyr-card" data-name="আবরার ফাহাদ" data-district="ঢাকা" style="cursor:pointer;" onclick="document.getElementById(\'abrar-fahad\').scrollIntoView({behavior:\'smooth\'})" title="Read full memorial"', 1)
    print('july.html: Abrar martyr-list card links to memorial')
open('july.html', 'w', encoding='utf-8', newline='').write(src)

# ============ 3. Update in-chat old Abrar card (protest photo -> real portrait) ============
src = open('assets/app.js', encoding='utf-8', newline='').read()
src = src.replace('h4+=\'<div style="border-radius:12px;overflow:hidden;border:2px solid rgba(185,28,28,.45);box-shadow:0 4px 18px rgba(0,0,0,.25);background:#fff"><img src="assets/img/abrar-protest.jpg" alt="Prote', 'h9+=\'<div style="border-radius:12px;overflow:hidden;border:2px solid rgba(185,28,28,.45);box-shadow:0 4px 18px rgba(0,0,0,.25);background:#fff"><img src="assets/img/abrar-fahad.jpg" alt="Shaheed Abrar Fahad"')
open('assets/app.js', 'w', encoding='utf-8', newline='').write(src)
print('app.js: legacy Abrar chat card portrait swapped (where present)')

print('DONE')
