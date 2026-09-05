import os, sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(ROOT, 'dla-website'))

# ============ 1. app.js: KB block + hero card + aliases ============
src = open('assets/app.js', encoding='utf-8', newline='').read()

if 'mir_mugdho_bio' in src:
    print('app.js: Mugdho KB already present - skip')
else:
    kb = '''
/* 2026-09-05 Mir Mugdho memorial knowledge (bilingual) */
cR["mir_mugdho_bio"]="Shaheed Mir Mahfuzur Rahman Mugdho (\\u09ae\\u09c0\\u09b0 \\u09ae\\u09be\\u09b9\\u09ab\\u09c1\\u099c\\u09c1\\u09b0 \\u09b0\\u09b9\\u09ae\\u09be\\u09a8 \\u09ae\\u09c1\\u0997\\u09cd\\u09a7; 9 Oct 1998 - 18 July 2024) was a Bangladeshi student activist and freelancer, martyred in the July Uprising. Born in Uttara, Dhaka - one minute after his twin brother Mir Mahbubur Rahman Snigdho; family home Ramrail, Brahmanbaria. Father Mir Mustafizur Rahman was a health inspector. BSc in Mathematics from Khulna University (2023); was pursuing his MBA at Bangladesh University of Professionals (BUP). A talented Fiverr freelancer (1,000+ completed projects, SEO and social-media marketing, earning $2,000-3,000/month), a former Bangladesh Scout, footballer and travel lover. | \\u09b6\\u09b9\\u09c0\\u09a6 \\u09ae\\u09c0\\u09b0 \\u09ae\\u09be\\u09b9\\u09ab\\u09c1\\u099c\\u09c1\\u09b0 \\u09b0\\u09b9\\u09ae\\u09be\\u09a8 \\u09ae\\u09c1\\u0997\\u09cd\\u09a7 (\\u09ef\\u09af \\u0985\\u0995\\u09cd\\u099f\\u09cb\\u09ac\\u09b0 \\u09e7\\u09ef\\u09ef\\u09ee - \\u09e7\\u09ee \\u099c\\u09c1\\u09b2\\u09be\\u0987 \\u09e8\\u0668\\u09e8\\u09ea) \\u099b\\u09bf\\u09b2\\u09c7\\u09a8 \\u099c\\u09c1\\u09b2\\u09be\\u0987 \\u0997\\u09a3\\u0985\\u09cd\\u09af\\u09c1\\u09a4\\u09cd\\u09a5\\u09be\\u09a8\\u09c7\\u09b0 \\u09b6\\u09b9\\u09c0\\u09a6\\u0964 \\u0989\\u09a4\\u09cd\\u09a4\\u09b0\\u09be, \\u09a2\\u09be\\u0995\\u09be\\u09af\\u09bc \\u099c\\u09a8\\u09cd\\u09ae; \\u0997\\u09cd\\u09b0\\u09be\\u09ae\\u09c7\\u09b0 \\u09ac\\u09be\\u09dc\\u09bf \\u09ac\\u09cd\\u09b0\\u09be\\u09b9\\u09cd\\u09ae\\u09a3\\u09ac\\u09be\\u09dc\\u09bf\\u09af\\u09bc\\u09be\\u09b0 \\u09b0\\u09be\\u09ae\\u09b0\\u09be\\u0987\\u09b2\\u0964 \\u0996\\u09c1\\u09b2\\u09a8\\u09be \\u09ac\\u09bf\\u09b6\\u09cd\\u09ac\\u09ac\\u09bf\\u09a6\\u09cd\\u09af\\u09be\\u09b2\\u09af\\u09bc \\u09a5\\u09c7\\u0995\\u09c7 \\u0997\\u09a3\\u09bf\\u09a4\\u09c7 \\u09b8\\u09cd\\u09a8\\u09be\\u09a4\\u0995 (\\u09e8\\u0668\\u09e8\\u09e9), \\u09ac\\u09bf\\u0987\\u0989\\u09aa\\u09bf\\u09a4\\u09c7 \\u098f\\u09ae\\u09ac\\u09bf\\u098f \\u099a\\u09b2\\u099b\\u09bf\\u09b2\\u0964 \\u09ab\\u09be\\u0987\\u09ad\\u09be\\u09b0\\u09c7 \\u09e7,\\u0e68\\u0e68\\u0e68+ \\u09aa\\u09cd\\u09b0\\u099c\\u09c7\\u0995\\u09cd\\u099f \\u09b8\\u09ae\\u09cd\\u09aa\\u09a8\\u09cd\\u09a8 \\u0995\\u09b0\\u09be \\u09aa\\u09cd\\u09b0\\u09a4\\u09bf\\u09ad\\u09be\\u09ac\\u09be\\u09a8 \\u09ab\\u09cd\\u09b0\\u09bf\\u09b2\\u09cd\\u09af\\u09be\\u09a8\\u09cd\\u09b8\\u09be\\u09b0, \\u09ac\\u09be\\u0982\\u09b2\\u09be\\u09a6\\u09c7\\u09b6 \\u09b8\\u09cd\\u0995\\u09be\\u0989\\u099f\\u09b8\\u09c7\\u09b0 \\u09b8\\u09a6\\u09b8\\u09cd\\u09af, \\u09ab\\u09c1\\u099f\\u09ac\\u09b2\\u09be\\u09b0 \\u0993 \\u09ad\\u09cd\\u09b0\\u09ae\\u09a3\\u09aa\\u09bf\\u09aa\\u09be\\u09b8\\u09c1\\u0964";
cR["mir_mugdho_death"]="How Mir Mugdho died: on 18 July 2024, during the quota-reform protests, he went out to distribute food, water and biscuits to protesters, starting around 4 pm at Azampur intersection, Uttara, Dhaka. In a video recorded 15 minutes before his death he is seen carrying a water case, asking again and again: 'Does anyone need water? Water, water?' Around 5 pm he was shot in the head at Azampur crossing - the bullet entered his forehead and exited the right side of his head. His friend Zakirul Islam took him to Uttara Crescent Hospital, where the on-duty doctor pronounced him dead on arrival. He was 25. | \\u09e7\\u09ee \\u099c\\u09c1\\u09b2\\u09be\\u0987 \\u09e8\\u0e68\\u09e8\\u09ea \\u09b8\\u09be\\u099c\\u09c7 \\u09ae\\u09c1\\u0997\\u09cd\\u09a7 \\u0986\\u09a8\\u09cd\\u09a6\\u09cb\\u09b2\\u09a8\\u0995\\u09be\\u09b0\\u09c0\\u09a6\\u09c7\\u09b0 \\u09ae\\u09be\\u099d\\u09c7 \\u0996\\u09be\\u09ac\\u09be\\u09b0, \\u09aa\\u09be\\u09a8\\u09bf \\u0993 \\u09ac\\u09bf\\u09b8\\u09cd\\u0995\\u09c1\\u099f \\u09ac\\u09bf\\u09a4\\u09b0\\u09a3 \\u0995\\u09b0\\u099b\\u09bf\\u09b2\\u09c7\\u09a8\\u0964 \\u09ae\\u09c3\\u09a4\\u09cd\\u09af\\u09c1\\u09b0 \\u09e7\\u09eb \\u09ae\\u09bf\\u09a8\\u09bf\\u099f \\u0986\\u0997\\u09c7\\u09b0 \\u09ad\\u09bf\\u09a1\\u09bf\\u0993\\u09a4\\u09c7 \\u09a4\\u09be\\u0995\\u09c7 \\u09aa\\u09be\\u09a8\\u09bf\\u09b0 \\u0995\\u09c7\\u09b8 \\u09b9\\u09be\\u09a4\\u09c7 \\u09ac\\u09b2\\u09a4\\u09c7 \\u09b6\\u09cb\\u09a8\\u09be \\u09af\\u09be\\u09af\\u09bc - \\u09aa\\u09be\\u09a8\\u09bf \\u09b2\\u09be\\u0997\\u09ac\\u09c7 \\u0995\\u09be\\u09b0\\u09cb, \\u09aa\\u09be\\u09a8\\u09bf, \\u09aa\\u09be\\u09a8\\u09bf? \\u09ac\\u09bf\\u0995\\u09c7\\u09b2 \\u09b8\\u09be\\u095e\\u09c7 ৫\\u099f\\u09be\\u09b0 \\u09a6\\u09bf\\u0995\\u09c7 \\u0986\\u099c\\u09ae\\u09aa\\u09c1\\u09b0 \\u0995\\u09cd\\u09b0\\u09b8\\u09bf\\u0982\\u09c7 \\u0995\\u09aa\\u09be\\u09b2\\u09c7 \\u0997\\u09c1\\u09b2\\u09bf \\u09b2\\u09be\\u0997\\u09c7; \\u09ac\\u09a8\\u09cd\\u09a7\\u09c1 \\u099c\\u09be\\u0995\\u09bf\\u09b0\\u09c1\\u09b2 \\u0987\\u09b8\\u09b2\\u09be\\u09ae \\u09a4\\u09be\\u0995\\u09c7 \\u0995\\u09cd\\u09b0\\u09bf\\u09b8\\u09c7\\u09a8\\u09cd\\u099f \\u09b9\\u09be\\u09b8\\u09aa\\u09be\\u09a4\\u09be\\u09b2\\u09c7 \\u09a8\\u09bf\\u09b2\\u09c7 \\u099a\\u09bf\\u0995\\u09bf\\u09ce\\u09b8\\u0995 \\u09a4\\u09be\\u0995\\u09c7 \\u09ae\\u09c3\\u09a4 \\u0998\\u09cb\\u09b7\\u09a3\\u09be \\u0995\\u09b0\\u09c7\\u09a8\\u0964 \\u09ac\\u09af\\u09bc \\u09b9\\u09af\\u09bc\\u09c7\\u099b\\u09bf\\u09b2 \\u09e8\\u09eb\\u0964";
cR["mir_mugdho_pani"]="Pani lagbe pani (Water needed, water) became the symbolic slogan of the July Uprising after Mugdho's final moments. Minutes before he was shot, the viral video showed him distributing water while asking 'Does anyone need water? Water, water?' The phrase spread as graffiti on walls across Bangladesh, appeared as a giant water-bottle motif in the 14 April 2025 Ananda Shobhajatra (Bengali New Year), was shown in the largest drone show at Manik Mia Avenue, inspired 'Mugdho' named water bottles handed out at a post-revolution cartoon festival, and Shah Md Safinur's poetry book 'Pani Lagbo Pani?'. | \\u09aa\\u09be\\u09a8\\u09bf \\u09b2\\u09be\\u0997\\u09ac\\u09c7 \\u09aa\\u09be\\u09a8\\u09bf - \\u09ae\\u09c1\\u0997\\u09cd\\u09a7\\u09c7\\u09b0 \\u09b6\\u09c7\\u09b7 \\u09ae\\u09c1\\u09b9\\u09c2\\u09b0\\u09cd\\u09a4\\u09c7\\u09b0 \\u09ad\\u09be\\u0987\\u09b0\\u09be\\u09b2 \\u09ad\\u09bf\\u09a1\\u09bf\\u0993 \\u09a5\\u09c7\\u0995\\u09c7 \\u099c\\u09c1\\u09b2\\u09be\\u0987 \\u0985\\u09ad\\u09cd\\u09af\\u09c1\\u09a4\\u09cd\\u09a5\\u09be\\u09a8\\u09c7\\u09b0 \\u09aa\\u09cd\\u09b0\\u09a4\\u09c0\\u0995\\u09c0 \\u09b8\\u09cd\\u09b2\\u09cb\\u0997\\u09be\\u09a8\\u09c7 \\u09aa\\u09b0\\u09bf\\u09a3\\u09a4 \\u09b9\\u09af\\u09bc\\u0964 \\u09a6\\u09c7\\u09af\\u09bc\\u09be\\u09b2\\u09c7 \\u09a6\\u09c7\\u09af\\u09bc\\u09be\\u09b2\\u09c7 \\u0997\\u09cd\\u09b0\\u09be\\u09ab\\u09bf\\u09a4\\u09bf, \\u09b6\\u09cb\\u09ad\\u09be\\u09af\\u09be\\u09a4\\u09cd\\u09b0\\u09be\\u09b0 \\u09aa\\u09be\\u09a8\\u09bf\\u09b0 \\u09ac\\u09cb\\u09a4\\u09b2 \\u09ae\\u09cb\\u099f\\u09bf\\u09ab, \\u09a1\\u09cd\\u09b0\\u09cb\\u09a8 \\u09b6\\u09cb\\u09a4\\u09c7 \\u099a\\u09bf\\u09a4\\u09cd\\u09b0 - \\u09b8\\u09ac\\u0996\\u09be\\u09a8\\u09c7 \\u098f\\u0987 \\u09ac\\u09be\\u0995\\u09cd\\u09af\\u0987\\u0964";
cR["mir_mugdho_legacy"]="Mir Mugdho's legacy: Bangabandhu Mukta Mancha in Uttara was renamed Mugdho Mancha (Aug 2024). The Mugdho Safe Drinking Water Corner opened at Joydebpur Junction railway station, Gazipur (5 Aug 2025, about 975,000 BDT, free drinking water for passengers). Bangladesh's new e-passport design (Home Ministry notification, July 2026) will carry Mugdho's portrait in the watermark of pages 32-33 alongside fellow July martyrs Abu Sayed and Wasim Akram. Fiverr publicly mourned him; his twin brother Snigdho's tribute video went viral. His death is remembered as a pivotal moment that turned the quota movement into the mass July Uprising. | \\u09ae\\u09c1\\u0997\\u09cd\\u09a7\\u09c7\\u09b0 \\u09b8\\u09cd\\u09ae\\u09c3\\u09a4\\u09bf\\u09a4\\u09c7: \\u0989\\u09a4\\u09cd\\u09a4\\u09b0\\u09be\\u09b0 \\u09ac\\u0999\\u09cd\\u0997\\u09ac\\u09a8\\u09cd\\u09a7\\u09c1 \\u09ae\\u09c1\\u0995\\u09cd\\u09a4\\u09ae\\u099e\\u09cd\\u099a\\u09c7\\u09b0 \\u09a8\\u09be\\u09ae \\u09ae\\u09c1\\u0997\\u09cd\\u09a7 \\u09ae\\u099e\\u09cd\\u099a (\\u0986\\u0997\\u09b8\\u09cd\\u099f \\u09e8\\u0e68\\u09e8\\u09ea); \\u0997\\u09be\\u099c\\u09c0\\u09aa\\u09c1\\u09b0\\u09c7\\u09b0 \\u099c\\u09af\\u09bc\\u09a6\\u09c7\\u09ac\\u09aa\\u09c1\\u09b0 \\u09b8\\u09cd\\u099f\\u09c7\\u09b6\\u09a8\\u09c7 \\u09ae\\u09c1\\u0997\\u09cd\\u09a7 \\u09b8\\u09c1\\u09aa\\u09c7\\u09af\\u09bc \\u09aa\\u09be\\u09a8\\u09bf\\u09b0 \\u0995\\u09b0\\u09cd\\u09a8\\u09be\\u09b0 (\\u09eb \\u0986\\u0997\\u09b8\\u09cd\\u099f \\u09e8\\u0e68\\u09e8\\u09eb); \\u09e8\\u0e68\\u09e8\\u09ec\\u09c7\\u09b0 \\u09a8\\u09a4\\u09c1\\u09a8 \\u0987-\\u09aa\\u09be\\u09b8\\u09aa\\u09cb\\u09b0\\u09cd\\u099f\\u09c7\\u09b0 \\u09e9\\u09e8-\\u09e9\\u09e9 \\u09aa\\u09c3\\u09b7\\u09cd\\u09a0\\u09be\\u09b0 \\u099c\\u09b2\\u099b\\u09be\\u09aa\\u09c7 \\u0986\\u09ac\\u09c1 \\u09b8\\u09be\\u0988\\u09a6 \\u0993 \\u0993\\u09df\\u09be\\u09b8\\u09bf\\u09ae \\u0986\\u0995\\u09b0\\u09be\\u09ae\\u09c7\\u09b0 \\u09b8\\u09be\\u0999\\u09cd\\u0997\\u09c7 \\u09ae\\u09c1\\u0997\\u09cd\\u09a7\\u09c7\\u09b0 \\u09aa\\u09cd\\u09b0\\u09a4\\u09bf\\u0995\\u09c3\\u09a4\\u09bf\\u0964";
cR["mir_mugdho_family"]="Mir Mugdho's family: father Mir Mustafizur Rahman (health inspector), mother Shahana Chowdhury. Twin brother Mir Mahbubur Rahman Snigdho (born one minute earlier) - a filmmaker who first identified Mugdho's body and posted the viral tribute video; elder brother Mir Dipto. Family home: Ramrail, Brahmanbaria. He was buried at Kamarpara Bamnartek Graveyard, Sector 10, Uttara, Dhaka. | \\u09aa\\u09b0\\u09bf\\u09ac\\u09be\\u09b0: \\u09ac\\u09be\\u09ac\\u09be \\u09ae\\u09c0\\u09b0 \\u09ae\\u09cb\\u09b8\\u09cd\\u09a4\\u09be\\u09ab\\u09bf\\u099c\\u09c1\\u09b0 \\u09b0\\u09b9\\u09ae\\u09be\\u09a8, \\u09ae\\u09be \\u09b6\\u09be\\u09b9\\u09be\\u09a8\\u09be \\u099a\\u09cc\\u09a7\\u09c1\\u09b0\\u09c0, \\u09af\\u09ae\\u099c \\u09ad\\u09be\\u0987 \\u09ae\\u09c0\\u09b0 \\u09ae\\u09be\\u09b9\\u09ac\\u09c1\\u09ac\\u09c1\\u09b0 \\u09b0\\u09b9\\u09ae\\u09be\\u09a8 \\u09b8\\u09cd\\u09a8\\u09bf\\u0997\\u09cd\\u09a7 \\u0993 \\u09ac\\u09dc \\u09ad\\u09be\\u0987 \\u09ae\\u09c0\\u09b0 \\u09a6\\u09c0\\u09aa\\u09cd\\u09a4\\u0964 \\u0997\\u09cd\\u09b0\\u09be\\u09ae\\u09c7\\u09b0 \\u09ac\\u09be\\u09dc\\u09bf \\u09ac\\u09cd\\u09b0\\u09be\\u09b9\\u09cd\\u09ae\\u09a3\\u09ac\\u09be\\u09dc\\u09bf\\u09af\\u09bc\\u09be\\u09b0 \\u09b0\\u09be\\u09ae\\u09b0\\u09be\\u0987\\u09b2; \\u09b8\\u09ae\\u09be\\u09a7\\u09bf \\u0989\\u09a4\\u09cd\\u09a4\\u09b0\\u09be\\u09b0 \\u0995\\u09be\\u09ae\\u09be\\u09b0\\u09aa\\u09be\\u09dc\\u09be \\u09ac\\u09be\\u09ae\\u09a8\\u09b0\\u09cd\\u09a4\\u09c7\\u0995 \\u0995\\u09ac\\u09b0\\u09b8\\u09cd\\u09a5\\u09be\\u09a8\\u09c7\\u0964";
aliasMap["mir mugdho"]="mir_mugdho_bio";
aliasMap["mugdho"]="mir_mugdho_bio";
aliasMap["who is mugdho"]="mir_mugdho_bio";
aliasMap["who was mir mugdho"]="mir_mugdho_bio";
aliasMap["mir mahfuzur rahman mugdho"]="mir_mugdho_bio";
aliasMap["water boy of july"]="mir_mugdho_bio";
aliasMap["pani lagbe pani"]="mir_mugdho_pani";
aliasMap["pani dorkobe pani"]="mir_mugdho_pani";
aliasMap["water needed water"]="mir_mugdho_pani";
aliasMap["how did mugdho die"]="mir_mugdho_death";
aliasMap["mir mugdho death"]="mir_mugdho_death";
aliasMap["mugdho shot"]="mir_mugdho_death";
aliasMap["mugdho water video"]="mir_mugdho_pani";
aliasMap["mugdho legacy"]="mir_mugdho_legacy";
aliasMap["mugdho mancha"]="mir_mugdho_legacy";
aliasMap["mugdho water corner"]="mir_mugdho_legacy";
aliasMap["mugdho passport"]="mir_mugdho_legacy";
aliasMap["mugdho family"]="mir_mugdho_family";
aliasMap["mugdho brother"]="mir_mugdho_family";
aliasMap["mugdho snigdho"]="mir_mugdho_family";
aliasMap["mugdho education"]="mir_mugdho_bio";
aliasMap["mugdho fiverr"]="mir_mugdho_bio";
aliasMap["\\u099c\\u09c1\\u09b2\\u09be\\u0987 \\u09b6\\u09b9\\u09c0\\u09a6 \\u09ae\\u09c1\\u0997\\u09cd\\u09a7"]="mir_mugdho_bio";
aliasMap["\\u09b6\\u09b9\\u09c0\\u09a6 \\u09ae\\u09c0\\u09b0 \\u09ae\\u09c1\\u0997\\u09cd\\u09a7"]="mir_mugdho_bio";
aliasMap["\\u09ae\\u09c0\\u09b0 \\u09ae\\u09c1\\u0997\\u09cd\\u09a7"]="mir_mugdho_bio";
aliasMap["\\u09ae\\u09c1\\u0997\\u09cd\\u09a7"]="mir_mugdho_bio";
aliasMap["\\u09ae\\u09c0\\u09b0 \\u09ae\\u09be\\u09b9\\u09ab\\u09c1\\u099c\\u09c1\\u09b0 \\u09b0\\u09b9\\u09ae\\u09be\\u09a8 \\u09ae\\u09c1\\u0997\\u09cd\\u09a7"]="mir_mugdho_bio";
aliasMap["\\u09aa\\u09be\\u09a8\\u09bf \\u09b2\\u09be\\u0997\\u09ac\\u09c7 \\u09aa\\u09be\\u09a8\\u09bf"]="mir_mugdho_pani";
aliasMap["\\u09ae\\u09c1\\u0997\\u09cd\\u09a7 \\u09aa\\u09be\\u09a8\\u09bf\\u09b0 \\u0995\\u09b0\\u09cd\\u09a8\\u09be\\u09b0"]="mir_mugdho_legacy";
aliasMap["\\u09ae\\u09c1\\u0997\\u09cd\\u09a7 \\u09ae\\u099e\\u09cd\\u099a"]="mir_mugdho_legacy";
aliasMap["\\u09ae\\u09c1\\u0997\\u09cd\\u09a7\\u09c7\\u09b0 \\u09aa\\u09b0\\u09bf\\u09ac\\u09be\\u09b0"]="mir_mugdho_family";
aliasMap["\\u09ae\\u09c1\\u0997\\u09cd\\u09a7 \\u0995\\u09c7\\u09ae\\u09a8 \\u09ae\\u09b0\\u09c7\\u099b\\u09c7"]="mir_mugdho_death";
'''
    anchor = '/* processMessage dispatcher: grounded frontier LLM first, local engine as fallback */'
    i = src.find(anchor)
    assert i > 0, 'dispatcher anchor not found'
    src = src[:i] + kb.lstrip('\n') + '\n' + src[i:]
    print('app.js: KB block inserted (5 entries + 30 aliases)')

if "isMugdho" in src:
    print('app.js: Mugdho hero card already present - skip')
else:
    card = '''    var mugdhoKeys=(k.indexOf('mir_mugdho')===0);
    var mugdhoMent=(m.indexOf('mugdho')>-1||m.indexOf('\\u09ae\\u09c1\\u0997\\u09cd\\u09a7')>-1);
    var isMugdho=(mugdhoKeys||(mugdhoMent&&(k.indexOf('july')===0||k==='')));
    if(isMugdho&&!showStrip){
      var h8='<div style="max-width:220px;margin:0 0 12px;">';
      h8+='<div style="border-radius:12px;overflow:hidden;border:2px solid rgba(16,185,129,.45);box-shadow:0 4px 18px rgba(0,0,0,.25);background:#fff"><img src="assets/img/mir-mugdho.jpg" alt="Mir Mahfuzur Rahman Mugdho" style="width:100%;aspect-ratio:1/1;object-fit:cover;object-position:top center;display:block"></div>';
      h8+='<div style="font-size:9.5px;color:rgba(255,255,255,.5);line-height:1.5;margin-top:5px;">Shaheed Mir Mugdho (1998-2024) - shot while handing water to protesters, 18 July 2024</div>';
      h8+='<div style="font-size:9.5px;color:rgba(255,255,255,.42);line-height:1.5;"><a href="https://en.wikipedia.org/wiki/Mir_Mugdho" target="_blank" rel="noopener" style="color:rgba(255,255,255,.55);">Photo: Prothom Alo via Wikipedia</a></div>';
      h8+='</div>';
      return h8;
    }
'''
    anchor2 = '    if(showAbu&&!showStrip){'
    i2 = src.find(anchor2)
    assert i2 > 0, 'showAbu anchor not found'
    src = src[:i2] + card + src[i2:]
    print('app.js: hero portrait card inserted')

open('assets/app.js', 'w', encoding='utf-8', newline='').write(src)

# ============ 2. july.html: memorial section + card updates ============
src = open('july.html', encoding='utf-8', newline='').read()

if 'id="mir-mugdho"' not in src:
    section = '''<section id="mir-mugdho" style="padding:100px 0;background:linear-gradient(135deg,#0a1a14 0%,#0a2a1e 50%,#0a1a2a 100%);position:relative;overflow:hidden;">
<div style="position:absolute;inset:0;pointer-events:none;opacity:.05;font-size:170px;font-weight:900;color:#10b981;display:flex;align-items:center;justify-content:center;white-space:nowrap;">\\u09aa\\u09be\\u09a8\\u09bf</div>
<div class="container" style="max-width:1000px;margin:0 auto;padding:0 24px;position:relative;z-index:1;">
<div style="text-align:center;margin-bottom:40px;">
<span style="display:inline-block;background:linear-gradient(135deg,#10b981,#0ea5e9);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-weight:700;font-size:13px;letter-spacing:3px;text-transform:uppercase;">Shaheed of July 18</span>
<h2 style="font-size:clamp(28px,4vw,42px);text-align:center;margin:10px 0 8px;">Shaheed <span style="color:#34d399;">Mir Mugdho</span></h2>
<p style="text-align:center;color:rgba(255,255,255,.5);font-size:16px;margin:0 0 6px;">\\u09ae\\u09c0\\u09b0 \\u09ae\\u09be\\u09b9\\u09ab\\u09c1\\u099c\\u09c1\\u09b0 \\u09b0\\u09b9\\u09ae\\u09be\\u09a8 \\u09ae\\u09c1\\u0997\\u09cd\\u09a7 &middot; 9 October 1998 - 18 July 2024</p>
<p style="text-align:center;color:rgba(255,255,255,.65);font-size:15px;font-style:italic;margin:0;">&ldquo;Does anyone need water? Water, water?&rdquo; &mdash; \\u09aa\\u09be\\u09a8\\u09bf \\u09b2\\u09be\\u0997\\u09ac\\u09c7 \\u09aa\\u09be\\u09a8\\u09bf</p>
</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:start;">
<div>
<div style="width:100%;aspect-ratio:1/1;border-radius:20px;background:linear-gradient(135deg,rgba(16,185,129,.2),rgba(14,165,233,.2));border:2px solid rgba(52,211,153,.3);overflow:hidden;">
<img src="assets/img/mir-mugdho.jpg" alt="Mir Mahfuzur Rahman Mugdho (1998-2024)" style="width:100%;height:100%;object-fit:cover;object-position:top center;display:block;" loading="lazy">
</div>
<div style="margin-top:10px;text-align:center;font-size:11.5px;line-height:1.7;">
<span style="color:rgba(255,255,255,.5);">Photo: Prothom Alo, via English Wikipedia (fair use - memorial/educational)</span><br>
<a href="https://en.wikipedia.org/wiki/Mir_Mugdho" target="_blank" rel="noopener" style="color:rgba(255,255,255,.65);text-decoration:none;border-bottom:1px dotted rgba(255,255,255,.4);">English Wikipedia - Mir Mugdho</a> &middot;
<a href="https://bn.wikipedia.org/wiki/%E0%A6%AE%E0%A7%80%E0%A6%B0_%E0%A6%AE%E0%A7%81%E0%A6%97%E0%A7%8D%E0%A6%A7" target="_blank" rel="noopener" style="color:rgba(255,255,255,.65);text-decoration:none;border-bottom:1px dotted rgba(255,255,255,.4);">\\u09ac\\u09be\\u0982\\u09b2\\u09be \\u0989\\u0987\\u0995\\u09bf\\u09aa\\u09bf\\u09a1\\u09bf\\u09af\\u09bc\\u09be</a>
</div>
</div>
<div>
<div style="margin-bottom:22px;"><h3 style="color:#34d399;font-size:16px;margin:0 0 8px;">FULL NAME</h3><p style="color:#fff;font-size:15px;margin:0;">Mir Mahfuzur Rahman Mugdho (\\u09ae\\u09c0\\u09b0 \\u09ae\\u09be\\u09b9\\u09ab\\u09c1\\u099c\\u09c1\\u09b0 \\u09b0\\u09b9\\u09ae\\u09be\\u09a8 \\u09ae\\u09c1\\u0997\\u09cd\\u09a7) - known as Mugdho</p></div>
<div style="margin-bottom:22px;"><h3 style="color:#34d399;font-size:16px;margin:0 0 8px;">BORN</h3><p style="color:#fff;font-size:15px;margin:0;">9 October 1998, Uttara, Dhaka - twin brother Snigdho born one minute earlier; family from Ramrail, Brahmanbaria</p></div>
<div style="margin-bottom:22px;"><h3 style="color:#34d399;font-size:16px;margin:0 0 8px;">FAMILY</h3><p style="color:#fff;font-size:15px;margin:0;">Father: Mir Mustafizur Rahman (health inspector)<br>Mother: Shahana Chowdhury<br>Twin brother: Mir Mahbubur Rahman Snigdho (filmmaker) &middot; Elder brother: Mir Dipto</p></div>
<div style="margin-bottom:22px;"><h3 style="color:#34d399;font-size:16px;margin:0 0 8px;">EDUCATION</h3><p style="color:#fff;font-size:15px;margin:0;">Uttara High School &amp; College<br>BSc Mathematics, Khulna University (2023)<br>MBA (ongoing), Bangladesh University of Professionals</p></div>
<div style="margin-bottom:22px;"><h3 style="color:#34d399;font-size:16px;margin:0 0 8px;">WORK &amp; LIFE</h3><p style="color:#fff;font-size:15px;margin:0;">Fiverr freelancer - 1,000+ projects in SEO &amp; social media ($2,000-3,000/mo)<br>Bangladesh Scout, footballer, traveller</p></div>
<div style="margin-bottom:22px;"><h3 style="color:#34d399;font-size:16px;margin:0 0 8px;">18 JULY 2024</h3><p style="color:#fff;font-size:15px;margin:0;">Distributed food, water and biscuits to protesters at Azampur crossing from 4 pm. Shot in the head around 5 pm - 15 minutes after the viral "water" video. Pronounced dead at Uttara Crescent Hospital, age 25.</p></div>
<div style="margin-bottom:0;"><h3 style="color:#34d399;font-size:16px;margin:0 0 8px;">RESTING PLACE</h3><p style="color:#fff;font-size:15px;margin:0;">Kamarpara Bamnartek Graveyard, Sector 10, Uttara, Dhaka</p></div>
</div>
</div>
<div style="margin-top:44px;background:rgba(255,255,255,.03);border:1px solid rgba(52,211,153,.25);border-radius:18px;padding:28px 30px;">
<h3 style="color:#34d399;font-size:18px;margin:0 0 12px;">&ldquo;\\u09aa\\u09be\\u09a8\\u09bf \\u09b2\\u09be\\u0997\\u09ac\\u09c7 \\u09aa\\u09be\\u09a8\\u09bf&rdquo; - the slogan he left behind</h3>
<p style="color:rgba(255,255,255,.75);font-size:14.5px;line-height:1.8;margin:0;">His final video - a young man with a water case, asking over and over if anyone needs water - became the symbolic slogan of the July Uprising. "Pani lagbe pani" spread as graffiti on walls across Bangladesh, appeared as a giant water-bottle motif in the 14 April 2025 Ananda Shobhajatra, was projected in the largest drone show at Manik Mia Avenue, and "Mugdho" water bottles were handed out at a post-revolution cartoon festival. On 5 August 2025 the <b style="color:#fff;">Mugdho Safe Drinking Water Corner</b> opened at Joydebpur Junction railway station - free water for travellers, the very thing he died giving. Uttara's Bangabandhu Mukta Mancha was renamed <b style="color:#fff;">Mugdho Mancha</b> (Aug 2024), and from July 2026 his portrait appears in the watermark of Bangladesh's new e-passport (pages 32-33) alongside Abu Sayed and Wasim Akram.</p>
</div>
<div style="margin-top:26px;text-align:center;font-size:12px;color:rgba(255,255,255,.4);line-height:1.8;">
Sources: <a href="https://bn.wikipedia.org/wiki/%E0%A6%AE%E0%A7%80%E0%A6%B0_%E0%A6%AE%E0%A7%81%E0%A6%97%E0%A7%8D%E0%A6%A7" target="_blank" rel="noopener" style="color:rgba(255,255,255,.6);">\\u09ac\\u09be\\u0982\\u09b2\\u09be \\u0989\\u0987\\u0995\\u09bf\\u09aa\\u09bf\\u09a1\\u09bf\\u09af\\u09bc\\u09be</a> &middot;
<a href="https://en.wikipedia.org/wiki/Mir_Mugdho" target="_blank" rel="noopener" style="color:rgba(255,255,255,.6);">English Wikipedia</a> &middot;
<a href="https://shibir.org.bd/en/martyrs/shaheed-mir-mugdho" target="_blank" rel="noopener" style="color:rgba(255,255,255,.6);">Shibir Martyrs Archive</a>
</div>
</div>
</section>
'''
    anchor3 = '<section id="hadi-contribution"'
    i3 = src.find(anchor3)
    assert i3 > 0, 'hadi-contribution anchor not found'
    src = src[:i3] + section + src[i3:]
    print('july.html: #mir-mugdho memorial section inserted')

# strip card: real portrait + link into memorial
old_img = '<img src="assets/img/mir-mugdho-memorial.jpg" alt="Mir Mugdho memorial building"'
if old_img in src:
    src = src.replace(old_img, '<img src="assets/img/mir-mugdho.jpg" alt="Mir Mahfuzur Rahman Mugdho (1998-2024)"', 1)
    print('july.html: strip card now uses real portrait')
old_card_open = '<div class="martyr-strip-card" style="width:200px;">\n        <div style="border-radius:16px;overflow:hidden;border:2px solid rgba(16,185,129,.5);box-shadow:0 8px 30px rgba(0,0,0,.4);">\n          <img src="assets/img/mir-mugdho.jpg"'
if old_card_open in src and 'mir-mugdho\').scrollIntoView' not in src:
    src = src.replace(old_card_open, '<div class="martyr-strip-card" style="width:200px;cursor:pointer;" onclick="document.getElementById(\'mir-mugdho\').scrollIntoView({behavior:\'smooth\'})" title="Read Mir Mugdho\'s full memorial">\n        <div style="border-radius:16px;overflow:hidden;border:2px solid rgba(16,185,129,.5);box-shadow:0 8px 30px rgba(0,0,0,.4);">\n          <img src="assets/img/mir-mugdho.jpg"', 1)
    print('july.html: strip card links to memorial')
# martyr list card: clickable
mc = '<div class="martyr-card" data-name="\\u09ae\\u09c0\\u09b0 \\u09ae\\u09be\\u09b9\\u09ab\\u09c1\\u099c\\u09c1\\u09b0 \\u09b0\\u09b9\\u09ae\\u09be\\u09a8 \\u09ae\\u09c1\\u0997\\u09cd\\u09a7" data-district="\\u09a2\\u09be\\u0995\\u09be"'
mc_real = '<div class="martyr-card" data-name="\u09ae\u09c0\u09b0 \u09ae\u09be\u09b9\u09ab\u09c1\u099c\u09c1\u09b0 \u09b0\u09b9\u09ae\u09be\u09a8 \u09ae\u09c1\u0997\u09cd\u09a7" data-district="\u09a2\u09be\u0995\u09be"'
if mc_real in src:
    src = src.replace(mc_real, '<div class="martyr-card" data-name="\u09ae\u09c0\u09b0 \u09ae\u09be\u09b9\u09ab\u09c1\u099c\u09c1\u09b0 \u09b0\u09b9\u09ae\u09be\u09a8 \u09ae\u09c1\u0997\u09cd\u09a7" data-district="\u09a2\u09be\u0995\u09be" style="cursor:pointer;" onclick="document.getElementById(\'mir-mugdho\').scrollIntoView({behavior:\'smooth\'})" title="Read full memorial"', 1)
    print('july.html: martyr-list card links to memorial')
else:
    print('july.html: martyr-card pattern not matched (check manually)')

open('july.html', 'w', encoding='utf-8', newline='').write(src)

# ============ 3. Footer memorial links on all pages ============
LINK_A = '<a href="july.html#abrar-fahad">Abrar Fahad Memorial</a>'
LINK_M = '<a href="july.html#mir-mugdho">Mir Mugdho Memorial</a>'
for f in sorted(x for x in os.listdir('.') if x.endswith('.html')):
    s = open(f, encoding='utf-8', newline='').read()
    fi = s.find('<h4>About</h4>')
    if fi < 0:
        print(f, ': footer About column not found - skip')
        continue
    ins = fi + len('<h4>About</h4>')
    add = ''
    if 'july.html#abrar-fahad' not in s and 'abrar_fahad' not in s:
        add += LINK_A
    if 'july.html#mir-mugdho' not in s:
        add += LINK_M
    if add:
        s = s[:ins] + add + s[ins:]
        open(f, 'w', encoding='utf-8', newline='').write(s)
        print(f, ': footer memorial links added')

# ============ 4. Cache bump app36 -> app37 ============
for f in sorted(x for x in os.listdir('.') if x.endswith('.html')):
    s = open(f, encoding='utf-8', newline='').read()
    if 'app.js?v=app36' in s:
        s = s.replace('app.js?v=app36', 'app.js?v=app37')
        open(f, 'w', encoding='utf-8', newline='').write(s)
        print(f, ': cache buster -> app37')

print('DONE')
