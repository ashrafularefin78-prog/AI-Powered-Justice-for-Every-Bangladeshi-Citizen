import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(ROOT, 'dla-website'))

# ============ 1. app.js: Nazrul KB block ============
src = open('assets/app.js', encoding='utf-8', newline='').read()
if 'cR["nazrul_bio"]' in src:
    print('app.js: Nazrul KB already present - skip')
else:
    kb = '''/* 2026-09-05 Kazi Nazrul Islam - National Poet knowledge (bilingual) */
cR["nazrul_bio"]="Kazi Nazrul Islam (\\u0995\\u09be\\u099c\\u09c0 \\u09a8\\u099c\\u09b0\\u09c1\\u09b2 \\u0987\\u09b8\\u09b2\\u09be\\u09ae; 24 May 1899 - 29 August 1976) is the National Poet of Bangladesh, the 'Rebel Poet' (\\u09ac\\u09bf\\u09a6\\u09cd\\u09b0\\u09cb\\u09b9\\u09c0 \\u0995\\u09ac\\u09bf) and the 'Bulbul' of modern Bengali music. Born in Churulia village, Bardhaman, West Bengal (11 Joishtho 1306); childhood nickname Dukhu Mia. After his imam father Kazi Fakir Ahmad died in 1908, child Nazrul worked as a majar caretaker, mosque muazzin and maktab teacher, then joined a Leto folk-theatre troupe where he began writing songs and plays. He also served in the British Indian Army (49 Bengal Regiment, 1917-1920, Karachi), where he learned Persian and wrote his first prose and poetry. In a short active literary life (1920-1942) he produced a vast body of work before a nervous illness in 1942 silenced him for the last 34 years of his life. | \\u09ac\\u09be\\u0982\\u09b2\\u09be\\u09a6\\u09c7\\u09b6\\u09c7\\u09b0 \\u099c\\u09be\\u09a4\\u09c0\\u09df \\u0995\\u09ac\\u09bf \\u0995\\u09be\\u099c\\u09c0 \\u09a8\\u099c\\u09b0\\u09c1\\u09b2 \\u0987\\u09b8\\u09b2\\u09be\\u09ae (\\u09e8\\u09ea \\u09ae\\u09c7 \\u09e7\\u09ee\\u09ef\\u09ef - \\u09e8\\u09ef \\u0986\\u0997\\u09b8\\u09cd\\u099f \\u09e7\\u09ef\\u09ed\\u09ec)\\u0964 \\u09ac\\u09bf\\u09a6\\u09cd\\u09b0\\u09cb\\u09b9\\u09c0 \\u0995\\u09ac\\u09bf \\u0993 \\u0986\\u09a7\\u09c1\\u09a8\\u09bf\\u0995 \\u09ac\\u09be\\u0982\\u09b2\\u09be \\u0997\\u09be\\u09a8\\u09c7\\u09b0 \\u09ac\\u09c1\\u09b2\\u09ac\\u09c1\\u09b2\\u0964 \\u09aa\\u09b6\\u09cd\\u099a\\u09bf\\u09ae\\u09ac\\u0999\\u09cd\\u0997\\u09c7\\u09b0 \\u09ac\\u09b0\\u09cd\\u09a7\\u09ae\\u09be\\u09a8\\u09c7\\u09b0 \\u099a\\u09c1\\u09b0\\u09c1\\u09b2\\u09bf\\u09df\\u09be \\u0997\\u09cd\\u09b0\\u09be\\u09ae\\u09c7 \\u099c\\u09a8\\u09cd\\u09ae; \\u09a1\\u09be\\u0995 \\u09a8\\u09be\\u09ae \\u09a6\\u09c1\\u0996\\u09c1 \\u09ae\\u09bf\\u09df\\u09be\\u0964 \\u09ac\\u09be\\u09b2\\u09df\\u0995\\u09be\\u09b2\\u09c7 \\u09ae\\u09c1\\u09df\\u09be\\u099c\\u09cd\\u099c\\u09bf\\u09a8, \\u09ae\\u09c1\\u09df\\u09be\\u099c\\u09cd\\u099c\\u09bf\\u09a6 \\u0993 \\u09b2\\u09c7\\u099f\\u09cb \\u09a6\\u09b2\\u09c7\\u09b0 \\u0995\\u09be\\u099c \\u0995\\u09b0\\u09c7\\u09a8; \\u09aa\\u09b0\\u09c7 \\u09b8\\u09c7\\u09a8\\u09be\\u09ac\\u09be\\u09b9\\u09bf\\u09a8\\u09c0\\u09a4\\u09c7 \\u09df\\u09cb\\u0997 \\u09a6\\u09bf\\u09df\\u09c7 \\u09b8\\u09be\\u09b9\\u09bf\\u09a4\\u09cd\\u09df \\u099a\\u09b0\\u09cd\\u099a\\u09be \\u09b6\\u09c1\\u09b0\\u09c1 \\u0995\\u09b0\\u09c7\\u09a8\\u0964 \\u09e7\\u09ef\\u09ea\\u09e8 \\u09b8\\u09be\\u09b2\\u09c7 \\u09b8\\u09cd\\u09a8\\u09be\\u09df\\u09c1\\u09ac\\u09bf\\u0995 \\u0985\\u09b8\\u09c1\\u0996\\u09c7 \\u09b8\\u09c1\\u09a6\\u09c0\\u09b0\\u09cd\\u0998 \\u09e9\\u09ea \\u09ac\\u099b\\u09b0 \\u09aa\\u09a3 \\u09b8\\u09cd\\u09ac\\u09aa\\u09cd\\u09a8\\u09b6\\u09c0\\u09b2 \\u09b9\\u09df \\u09af\\u09be\\u09a8\\u0964";
cR["nazrul_works"]="Nazrul's works: in roughly 23 active years he wrote over 3,000 songs (he composed melody and music for about 4,000 by some counts), 3 novels, 19 short stories and 5 volumes of essays, plus poetry, plays and ghazals. Landmark poems and books: 'Bidrohi' (The Rebel, 1921), 'Pralayollas', 'Agnibina' (1922), 'Bisher Banshi', 'Bandon Hara', 'Nater Gan', 'Kamal Pasha', 'Samyabadi' and 'Sarbahara'. He founded and edited the radical biweekly 'Dhumketu' (Comet, 12 Aug 1922). His music set Bengali songs on the foundation of North Indian raga music while embracing ghazal, hamd, naat, Shyama Sangeet and folk forms - a uniquely secular synthesis. | \\u09ac\\u09bf\\u09a6\\u09cd\\u09b0\\u09cb\\u09b9\\u09c0, \\u09aa\\u09cd\\u09b0\\u09b2\\u09df\\u0989\\u09b2\\u09cd\\u09b2\\u09be\\u09b8, \\u0985\\u0997\\u09cd\\u09a8\\u09bf\\u09ac\\u09c0\\u09a3\\u09be, \\u09ac\\u09bf\\u09b7\\u09c7\\u09b0 \\u09ac\\u09be\\u0981\\u09b6\\u09bf, \\u09ac\\u09be\\u0981\\u09a7\\u09a8 \\u09b9\\u09be\\u09b0\\u09be, \\u0995\\u09be\\u09ae\\u09be\\u09b2 \\u09aa\\u09be\\u09b6\\u09be \\u09aa\\u09cd\\u09b0\\u09ad\\u09c3\\u09a4\\u09bf \\u0995\\u09be\\u09b2\\u09c7\\u09ad\\u09cd\\u09b0\\u0995\\u09be\\u09aa\\u09cd\\u09a4 \\u09b0\\u099a\\u09a8\\u09be\\u0964 \\u09aa\\u09cd\\u09b0\\u09be\\u09df \\u09e9 \\u09b9\\u09be\\u099c\\u09be\\u09b0 \\u0997\\u09be\\u09a8, \\u09e9 \\u09c9\\u09c1\\u09aa\\u09a8\\u09cd\\u09df\\u09be\\u09b8, \\u09e7\\u09ef \\u099b\\u09cb\\u099f\\u0997\\u09b2\\u09cd\\u09aa, \\u09aa\\u09be\\u0981\\u099a\\u099f\\u09bf \\u09aa\\u09cd\\u09b0\\u09ac\\u09a8\\u09cd\\u09a7\\u0997\\u09cd\\u09b0\\u09a8\\u09cd\\u09a5\\u0964 \\u09a7\\u09c2\\u09ae\\u0995\\u09c7\\u09a4\\u09c1 \\u09aa\\u09a4\\u09cd\\u09b0\\u09bf\\u0995\\u09be\\u09b0 \\u09b8\\u09ae\\u09cd\\u09aa\\u09be\\u09a6\\u0995 \\u099b\\u09bf\\u09b2\\u09c7\\u09a8\\u0964 \\u09b0\\u09be\\u0997, \\u0997\\u099c\\u09b2, \\u09b9\\u09ae\\u09cd\\u09a6, \\u09a8\\u09be\\u09a4, \\u09b6\\u09cd\\u09df\\u09be\\u09ae\\u09be\\u09b8\\u0999\\u09cd\\u0997\\u09c0\\u09a4 \\u0993 \\u09b2\\u09cb\\u0995\\u09b8\\u0999\\u09cd\\u0997\\u09c0\\u09a4\\u09c7\\u09b0 \\u09b8\\u09ae\\u09a8\\u09cd\\u09ac\\u09df \\u09b8\\u0982\\u09b6\\u09cd\\u09b2\\u09c7\\u09b7\\u09a3\\u0964";
cR["nazrul_rebel"]="Nazrul the rebel: his poem 'Bidrohi' (Dec 1921) changed the course of Bengali poetry with the thunderous 'Bol bir - bol unnoto mom shir!' In 1922 the British government charged him with sedition over 'Dhumketu' and jailed him. From the dock he delivered the historic 'Rajbandir Jabanbandi' (Deposition of a Political Prisoner) and later held a hunger strike of about 40 days against jail oppression. Rabindranath Tagore dedicated his book 'Basanta' to Nazrul in support - the two leading Bengali poets remained close from their 1921 Santiniketan meeting until Tagore's death in 1941. | \\u09e7\\u09ef\\u09e8\\u09e8 \\u09b8\\u09be\\u09b2\\u09c7 \\u09b0\\u09be\\u099c\\u09a6\\u09cd\\u09b0\\u09cb\\u09b9\\u09bf\\u09a4\\u09be\\u09b0 \\u09ae\\u09be\\u09ae\\u09b2\\u09be\\u09df \\u0995\\u09be\\u09b0\\u09be\\u09a6\\u09a6\\u09a3\\u09cd\\u09a1\\u0964 \\u0986\\u09a6\\u09be\\u09b2\\u09a4\\u09c7 \\u09aa\\u09be\\u09a0 \\u0995\\u09b0\\u09c7\\u09a8 \\u0990\\u09a4\\u09bf\\u09b9\\u09be\\u09b8\\u09bf\\u0995 \\u09b0\\u09be\\u099c\\u09ac\\u09a8\\u09cd\\u09a6\\u09c0\\u09b0 \\u099c\\u09ac\\u09be\\u09a8\\u09ac\\u09a8\\u09cd\\u09a6\\u09bf \\u0993 \\u09aa\\u09cd\\u09b0\\u09be\\u09df \\u09ea\\u09e6 \\u09a6\\u09bf\\u09a8\\u09c7\\u09b0 \\u0985\\u09a8\\u09b6\\u09a8\\u0964 \\u09b0\\u09ac\\u09c0\\u09a8\\u09cd\\u09a6\\u09cd\\u09b0\\u09a8\\u09be\\u09a5 \\u09a4\\u09be\\u0995\\u09c7 \\u0989\\u09ce\\u09b8\\u09b0\\u09cd\\u0997 \\u0995\\u09b0\\u09c7\\u09a8 \\u09ac\\u09b8\\u09a8\\u09cd\\u09a4 \\u0995\\u09be\\u09ac\\u09cd\\u09df\\u0964";
cR["nazrul_final"]="Nazrul's final chapter: in 1972 the Government of Bangladesh brought him and his family to Dhaka, where he lived his last years. Dhaka University conferred an honorary D.Litt (1975); he received Bangladeshi citizenship in 1976 and the Ekushe Padak in 1976. He died on 29 August 1976 and was buried with state honours beside the Dhaka University central mosque - today the Kazi Nazrul Islam Mausoleum. Earlier honours: Jagattarini Padak (1945), Padma Bhushan (1960); posthumously the Independence Award (1977). Bangladesh observes his birthday 24 May as Nazrul Jayanti. | \\u09e7\\u09ef\\u09ed\\u09e8 \\u09b8\\u09be\\u09b2\\u09c7 \\u09aa\\u09b0\\u09bf\\u09ac\\u09be\\u09b0\\u09c7\\u09b0 \\u09b8\\u09b9 \\u09a2\\u09be\\u0995\\u09be\\u09df \\u09ac\\u09b8\\u09a8\\u09cd\\u09a4\\u09b0\\u09a3\\u0964 \\u09e8\\u09ef \\u0986\\u0997\\u09b8\\u09cd\\u099f \\u09e7\\u09ef\\u09ed\\u09ec \\u09aa\\u09b0\\u09ae \\u09a8\\u09bf\\u09b0\\u09cd\\u09ac\\u09be\\u09b8\\u09a8; \\u09a2\\u09be\\u0995\\u09be \\u09ac\\u09bf\\u09b6\\u09cd\\u09ac\\u09ac\\u09bf\\u09a6\\u09cd\\u09af\\u09be\\u09b2\\u09df \\u0995\\u09c7\\u09a8\\u09cd\\u09a6\\u09cd\\u09b0\\u09c0\\u09df \\u09ae\\u09b8\\u099c\\u09bf\\u09a6\\u09c7\\u09b0 \\u09aa\\u09be\\u09b6\\u09c7 \\u09b8\\u09ae\\u09be\\u09a7\\u09bf\\u0964 \\u099c\\u0997\\u09a4\\u09cd\\u09a4\\u09be\\u09b0\\u09bf\\u09a3\\u09c0 \\u09aa\\u09a6\\u0995 (\\u09e7\\u09ef\\u09ea\\u09eb), \\u09aa\\u09a6\\u09cd\\u09ae\\u09ad\\u09c2\\u09b7\\u09a3 (\\u09e7\\u09ef\\u09ec\\u09e6), \\u098f\\u0995\\u09c1\\u09b6\\u09c7 \\u09aa\\u09a6\\u0995 (\\u09e7\\u09ef\\u09ed\\u09ec), \\u09b8\\u09cd\\u09ac\\u09be\\u09a7\\u09c0\\u09a8\\u09a4\\u09be \\u09aa\\u09c1\\u09b0\\u09b8\\u09cd\\u0995\\u09be\\u09b0 (\\u09e7\\u09ef\\u09ed\\u09ed)\\u0964";
cR["nazrul_quote"]="Nazrul on humanity: in his final speech he said - 'Some call my words yavana (foreign), some call me kafir. I say I am neither. I have only tried to bring Hindu and Muslim together in one embrace, to turn curses into embraces.' His Rebel poem opens: 'Bol bir - bol unnoto mom shir!' (Say, hero - say, my head is held high!). His poetry's core themes were protest against oppression of man by man, equality, religious tolerance and women's emancipation - values at the heart of access to justice. | \\u09b6\\u09c7\\u09b7 \\u09ad\\u09be\\u09b7\\u09a3\\u09c7 \\u09ac\\u09b2\\u09c7\\u099b\\u09bf\\u09b2\\u09c7\\u09a8 - \\u0995\\u09c7\\u09c9 \\u09ac\\u09b2\\u09c7\\u09a8 \\u0986\\u09ae\\u09be\\u09b0 \\u09ac\\u09be\\u09a8\\u09c0 \\u09df\\u09ac\\u09a8, \\u0995\\u09c7\\u09c9 \\u09ac\\u09b2\\u09c7\\u09a8 \\u0995\\u09be\\u09ab\\u09c7\\u09b0\\u0964 \\u0986\\u09ae\\u09bf \\u09ac\\u09b2\\u09bf \\u0993 \\u09a6\\u09c1\\u099f\\u09cb\\u09b0 \\u0995\\u09cb\\u09a8\\u099f\\u09be\\u0987 \\u09a8\\u09be\\u0964 \\u0986\\u09ae\\u09bf \\u09b6\\u09c1\\u09a7\\u09c1 \\u09b9\\u09bf\\u09a8\\u09cd\\u09a6\\u09c1 \\u09ae\\u09c1\\u09b8\\u09b2\\u09bf\\u09ae\\u0995\\u09c7 \\u098f\\u0995 \\u099c\\u09be\\u09df\\u0997\\u09be\\u09df \\u09a7\\u09b0\\u09c7 \\u09a8\\u09bf\\u09df\\u09c7 \\u09b9\\u09cd\\u09df\\u09be\\u09a8\\u09cd\\u09a1\\u09b6\\u09c7\\u0995 \\u0995\\u09b0\\u09be\\u09a8\\u09cb\\u09b0 \\u099a\\u09c7\\u09b7\\u09cd\\u099f\\u09be \\u0995\\u09b0\\u09c7\\u099b\\u09bf\\u0964";
aliasMap["kazi nazrul islam"]="nazrul_bio";
aliasMap["nazrul islam"]="nazrul_bio";
aliasMap["nazrul"]="nazrul_bio";
aliasMap["national poet"]="nazrul_bio";
aliasMap["national poet of bangladesh"]="nazrul_bio";
aliasMap["rebel poet"]="nazrul_rebel";
aliasMap["bidrohi kobi"]="nazrul_rebel";
aliasMap["bidrohi poem"]="nazrul_works";
aliasMap["dukhu mia"]="nazrul_bio";
aliasMap["nazrul jayanti"]="nazrul_final";
aliasMap["nazrul works"]="nazrul_works";
aliasMap["nazrul songs"]="nazrul_works";
aliasMap["nazrul sangeet"]="nazrul_works";
aliasMap["nazrul death"]="nazrul_final";
aliasMap["nazrul mausoleum"]="nazrul_final";
aliasMap["\\u0995\\u09be\\u099c\\u09c0 \\u09a8\\u099c\\u09b0\\u09c1\\u09b2 \\u0987\\u09b8\\u09b2\\u09be\\u09ae"]="nazrul_bio";
aliasMap["\\u09a8\\u099c\\u09b0\\u09c1\\u09b2"]="nazrul_bio";
aliasMap["\\u09a8\\u099c\\u09b0\\u09c1\\u09b2 \\u0987\\u09b8\\u09b2\\u09be\\u09ae"]="nazrul_bio";
aliasMap["\\u099c\\u09be\\u09a4\\u09c0\\u09df \\u0995\\u09ac\\u09bf"]="nazrul_bio";
aliasMap["\\u09ac\\u09bf\\u09a6\\u09cd\\u09b0\\u09cb\\u09b9\\u09c0 \\u0995\\u09ac\\u09bf"]="nazrul_rebel";
aliasMap["\\u09ac\\u09bf\\u09a6\\u09cd\\u09b0\\u09cb\\u09b9\\u09c0"]="nazrul_works";
aliasMap["\\u09a8\\u099c\\u09b0\\u09c1\\u09b2\\u0997\\u09c0\\u09a4\\u09bf"]="nazrul_works";
aliasMap["\\u09a8\\u099c\\u09b0\\u09c1\\u09b2\\u09c7\\u09b0 \\u0997\\u09be\\u09a8"]="nazrul_works";
'''
    anchor = '/* processMessage dispatcher: grounded frontier LLM first, local engine as fallback */'
    i = src.find(anchor)
    assert i > 0, 'dispatcher anchor missing'
    src = src[:i] + kb + src[i:]
    print('app.js: Nazrul KB block inserted (5 entries + 23 aliases)')

if 'var isNazrulCard' in src:
    print('app.js: Nazrul hero card already present - skip')
else:
    card = '''    var nazrulKeys=(k.indexOf('nazrul')===0);
    var nazrulMent=(m.indexOf('nazrul')>-1||m.indexOf('নজরুল')>-1);
    var isNazrulCard=(nazrulKeys||(nazrulMent&&(k.indexOf('july')!==0)));
    if(isNazrulCard){
      var h10='<div style="max-width:220px;margin:0 0 12px;">';
      h10+='<div style="border-radius:12px;overflow:hidden;border:2px solid rgba(245,158,11,.45);box-shadow:0 4px 18px rgba(0,0,0,.25);background:#fff"><img src="assets/img/kazi-nazrul-islam.jpg" alt="Kazi Nazrul Islam with sitar" style="width:100%;aspect-ratio:1/1;object-fit:cover;object-position:top center;display:block"></div>';
      h10+='<div style="font-size:9.5px;color:rgba(255,255,255,.5);line-height:1.5;margin-top:5px;">Kazi Nazrul Islam (1899-1976) - National Poet of Bangladesh, with his sitar</div>';
      h10+='<div style="font-size:9.5px;color:rgba(255,255,255,.42);line-height:1.5;"><a href="https://commons.wikimedia.org/wiki/File:Kazi_nazrul_islam_with_Setar.jpg" target="_blank" rel="noopener" style="color:rgba(255,255,255,.55);">Photo: Nazrul Academy - public domain</a></div>';
      h10+='</div>';
      return h10;
    }
'''
    anchor2 = '    if(showAbu&&!showStrip){'
    i2 = src.find(anchor2)
    assert i2 > 0, 'showAbu anchor missing'
    src = src[:i2] + card + src[i2:]
    print('app.js: Nazrul portrait card inserted')
open('assets/app.js', 'w', encoding='utf-8', newline='').write(src)

# ============ 2. about.html: Nazrul tribute section ============
src = open('about.html', encoding='utf-8', newline='').read()
if 'id="nazrul"' not in src:
    sec = '''<section id="nazrul" style="padding:100px 0;background:linear-gradient(135deg,#1a1405 0%,#2a1f0a 50%,#0a1a2a 100%);position:relative;overflow:hidden;border-top:1px solid rgba(245,158,11,.2);">
<div style="position:absolute;inset:0;pointer-events:none;opacity:.05;font-size:160px;font-weight:900;color:#f59e0b;display:flex;align-items:center;justify-content:center;white-space:nowrap;">বিদ্রোহী</div>
<div class="container" style="max-width:1000px;margin:0 auto;padding:0 24px;position:relative;z-index:1;">
<div style="text-align:center;margin-bottom:40px;">
<span style="display:inline-block;background:linear-gradient(135deg,#f59e0b,#f97316);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-weight:700;font-size:13px;letter-spacing:3px;text-transform:uppercase;">The Rebel Poet</span>
<h2 style="font-size:clamp(28px,4vw,42px);text-align:center;margin:10px 0 8px;">কাজী নজরুল ইসলাম <span style="color:#fbbf24;">- Our National Poet</span></h2>
<p style="text-align:center;color:rgba(255,255,255,.5);font-size:16px;margin:0 0 6px;">24 May 1899 (11 Joishtho 1306) - 29 August 1976</p>
<p style="text-align:center;color:rgba(255,255,255,.65);font-size:15px;font-style:italic;margin:0;">"বল বীর - বল উন্নত মম শির!" &mdash; Bidrohi, 1921</p>
</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:start;">
<div>
<div style="width:100%;aspect-ratio:1/1;border-radius:20px;background:linear-gradient(135deg,rgba(245,158,11,.2),rgba(249,115,22,.2));border:2px solid rgba(251,191,36,.3);overflow:hidden;">
<img src="assets/img/kazi-nazrul-islam.jpg" alt="Kazi Nazrul Islam with his sitar, before 1940" style="width:100%;height:100%;object-fit:cover;object-position:top center;display:block;" loading="lazy">
</div>
<div style="margin-top:10px;text-align:center;font-size:11.5px;line-height:1.7;">
<span style="color:rgba(255,255,255,.5);">Nazrul with his sitar (before 1940) &middot; Nazrul Academy &middot; Public Domain</span><br>
<a href="https://commons.wikimedia.org/wiki/File:Kazi_nazrul_islam_with_Setar.jpg" target="_blank" rel="noopener" style="color:rgba(255,255,255,.65);text-decoration:none;border-bottom:1px dotted rgba(255,255,255,.4);">Wikimedia Commons</a> &middot;
<a href="https://bn.wikipedia.org/wiki/%E0%A6%95%E0%A6%BE%E0%A6%9C%E0%A7%80_%E0%A6%A8%E0%A6%9C%E0%A6%B0%E0%A7%81%E0%A6%B2_%E0%A6%87%E0%A6%B8%E0%A6%B2%E0%A6%BE%E0%A6%AE" target="_blank" rel="noopener" style="color:rgba(255,255,255,.65);text-decoration:none;border-bottom:1px dotted rgba(255,255,255,.4);">বাংলা উইকিপিডিয়া</a> &middot;
<a href="https://bn.banglapedia.org/index.php?title=%E0%A6%87%E0%A6%B8%E0%A6%B2%E0%A6%BE%E0%A6%AE,_%E0%A6%95%E0%A6%BE%E0%A6%9C%E0%A7%80_%E0%A6%A8%E0%A6%9C%E0%A6%B0%E0%A7%81%E0%A6%B2" target="_blank" rel="noopener" style="color:rgba(255,255,255,.65);text-decoration:none;border-bottom:1px dotted rgba(255,255,255,.4);">বাংলাপিডিয়া</a>
</div>
</div>
<div>
<div style="margin-bottom:22px;"><h3 style="color:#fbbf24;font-size:16px;margin:0 0 8px;">THE TITLES</h3><p style="color:#fff;font-size:15px;margin:0;">জাতীয় কবি (National Poet of Bangladesh) &middot; বিদ্রোহী কবি (The Rebel Poet) &middot; বুলবুল (The Bulbul of Bengali music)<br>Childhood name: দুখু মিয়া (Dukhu Mia) &middot; Pseudonym: ধূমকেতু</p></div>
<div style="margin-bottom:22px;"><h3 style="color:#fbbf24;font-size:16px;margin:0 0 8px;">EARLY LIFE</h3><p style="color:#fff;font-size:15px;margin:0;">Born in Churulia, Bardhaman, West Bengal. Father Kazi Fakir Ahmad - a mosque imam - died in 1908, leaving 9-year-old Nazrul to work as a majar caretaker, mosque muazzin, maktab teacher, bakery boy - and then star of a Leto folk-theatre troupe, writing his first songs and plays.</p></div>
<div style="margin-bottom:22px;"><h3 style="color:#fbbf24;font-size:16px;margin:0 0 8px;">THE REBEL</h3><p style="color:#fff;font-size:15px;margin:0;">British Indian Army (49 Bengal Regiment, 1917-20). Then: 'Bidrohi' (Dec 1921) rewired Bengali poetry; the biweekly <b>ধূমকেতু</b> (Aug 1922) shook the empire. Charged with sedition, he answered from the dock with <b>রাজবন্দীর জবানবন্দী</b> and a 40-day hunger strike. Tagore dedicated his book 'Basanta' to the imprisoned poet.</p></div>
<div style="margin-bottom:22px;"><h3 style="color:#fbbf24;font-size:16px;margin:0 0 8px;">THE WORK</h3><p style="color:#fff;font-size:15px;margin:0;">~3,000-4,000 songs (melody &amp; music), 3 novels, 19 short stories, 5 essay volumes, landmark poems (প্রলয়োল্লাস, কামাল পাশা, সাম্যবাদী, সর্বহারা), books (অগ্নিবীণা, বিষের বাঁশি, বাঁধন হারা). His music spans raga, ghazal, hamd, naat, Shyama Sangeet and folk - a secular synthesis in sound.</p></div>
<div style="margin-bottom:22px;"><h3 style="color:#fbbf24;font-size:16px;margin:0 0 8px;">THE SILENCE &amp; THE HONOUR</h3><p style="color:#fff;font-size:15px;margin:0;">A 1942 nervous illness silenced him for 34 years. Bangladesh brought him home in 1972; D.Litt from Dhaka University (1975); citizenship and Ekushe Padak (1976). He died 29 August 1976 and rests beside the DU central mosque. Independence Award followed in 1977.</p></div>
<div style="margin-bottom:0;"><h3 style="color:#fbbf24;font-size:16px;margin:0 0 8px;">WHY HE MATTERS HERE</h3><p style="color:#fff;font-size:15px;margin:0;">His poetry's core was protest against the oppression of man by man - equality, religious tolerance, women's emancipation: the same justice A ai serves. In his final speech: <i>"কেউ বলেন আমার বাণী যবন, কেউ বলেন কাফের... আমি শুধু হিন্দু মুসলিমকে এক জায়গায় ধরে নিয়ে হ্যান্ডশেক করানোর চেষ্টা করেছি।"</i></p></div>
</div>
</div>
<div style="margin-top:26px;text-align:center;font-size:12px;color:rgba(255,255,255,.4);">
His Dhaka mausoleum is also the resting place of Shaheed Sharif Osman Bin Hadi &middot; <a href="july.html#memorial" style="color:rgba(255,255,255,.6);text-decoration:none;border-bottom:1px dotted rgba(255,255,255,.4);">see the memorial</a>
</div>
</div>
</section>
'''
    anchor3 = '<footer>'
    i3 = src.find(anchor3)
    assert i3 > 0, 'footer anchor missing in about.html'
    src = src[:i3] + sec + src[i3:]
    print('about.html: #nazrul tribute section inserted')

# About-column footer link on all pages
LINK_N = '<a href="about.html#nazrul">National Poet Nazrul</a>'
pages = [f for f in os.listdir('.') if f.endswith('.html')]
for f in pages:
    s = open(f, encoding='utf-8', newline='').read()
    fi = s.find('<h4>About</h4>')
    if fi < 0:
        print(f, ': no About column - skip')
        continue
    if 'about.html#nazrul' in s:
        print(f, ': nazrul link already present')
        continue
    ins = fi + len('<h4>About</h4>')
    s = s[:ins] + LINK_N + s[ins:]
    open(f, 'w', encoding='utf-8', newline='').write(s)
    print(f, ': footer Nazrul link added')

# ============ 3. Cache bump app38 -> app39 ============
for f in pages:
    s = open(f, encoding='utf-8', newline='').read()
    if 'app.js?v=app38' in s:
        s = s.replace('app.js?v=app38', 'app.js?v=app39')
        open(f, 'w', encoding='utf-8', newline='').write(s)
        print(f, ': cache buster -> app39')

print('DONE')
