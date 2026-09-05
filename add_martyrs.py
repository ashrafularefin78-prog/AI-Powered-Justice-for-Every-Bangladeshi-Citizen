# -*- coding: utf-8 -*-
# Adds Wasim Akram + Farhan Faiyaaz + Golam Nafiz: memorial sections (july.html)
# and bilingual AI knowledge (app.js). Idempotent, CRLF-aware.
import re, sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'C:\Users\user\Downloads\new\dla-website'
NL = '\r\n'

# =====================================================================
# PART 1 - july.html memorial sections
# =====================================================================
jp = ROOT + r'\july.html'
html = open(jp, encoding='utf-8', newline='').read()

SEC_STYLE = ('style="padding:100px 0;background:linear-gradient(135deg,#12100a 0%,#1c1408 55%,#1a0a0a 100%);'
             'position:relative;overflow:hidden;border-bottom:1px solid rgba(255,100,68,.12);"')

def build_section(secid, kicker, name_en, name_line, epigraph, img, alt, credit_txt, credit_url, credit_label, cards, story):
    L = []
    A = L.append
    A('<section id="' + secid + '" ' + SEC_STYLE + '>')
    A('<div class="container" style="max-width:1000px;margin:0 auto;padding:0 24px;position:relative;z-index:1;">')
    A('<div style="text-align:center;margin-bottom:40px;">')
    A('<span style="display:inline-block;background:linear-gradient(135deg,#ef4444,#f97316);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-weight:700;font-size:13px;letter-spacing:3px;text-transform:uppercase;">' + kicker + '</span>')
    A('<h2 style="font-size:clamp(28px,4vw,42px);text-align:center;margin:10px 0 8px;">Shaheed <span style="color:#ff6644;">' + name_en + '</span></h2>')
    A('<p style="text-align:center;color:rgba(255,255,255,.5);font-size:16px;margin:0 0 6px;">' + name_line + '</p>')
    A('<p style="text-align:center;color:rgba(255,255,255,.65);font-size:15px;font-style:italic;margin:0;">"' + epigraph + '"</p>')
    A('</div>')
    A('<div style="display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:start;">')
    A('<div>')
    A('<div style="width:100%;aspect-ratio:1/1;border-radius:20px;background:linear-gradient(135deg,rgba(239,68,68,.2),rgba(249,115,22,.2));border:2px solid rgba(255,102,68,.3);overflow:hidden;">')
    A('<img src="assets/img/' + img + '" alt="' + alt + '" style="width:100%;height:100%;object-fit:cover;object-position:center top;display:block;" loading="lazy">')
    A('</div>')
    A('<div style="margin-top:10px;text-align:center;font-size:11.5px;line-height:1.7;">')
    A('<span style="color:rgba(255,255,255,.5);">' + credit_txt + '</span><br>')
    A('<a href="' + credit_url + '" target="_blank" rel="noopener" style="color:rgba(255,255,255,.65);text-decoration:none;border-bottom:1px dotted rgba(255,255,255,.4);">' + credit_label + '</a>')
    A('</div></div>')
    A('<div>')
    for label, body in cards:
        A('<div style="margin-bottom:22px;"><h3 style="color:#ff6644;font-size:16px;margin:0 0 8px;">' + label + '</h3><p style="color:#fff;font-size:15px;margin:0;">' + body + '</p></div>')
    A('</div></div>')
    L.extend(story)
    L.append('</div>')
    L.append('</section>')
    return NL.join(L)

def story_block(title, paras):
    L = ['<div style="margin-top:44px;background:rgba(255,255,255,.03);border:1px solid rgba(255,102,68,.25);border-radius:18px;padding:28px 30px;">']
    L.append('<h3 style="color:#ff6644;font-size:18px;margin:0 0 12px;">' + title + '</h3>')
    for p in paras:
        L.append('<p style="color:rgba(255,255,255,.75);font-size:14.5px;line-height:1.8;margin:0 0 12px;">' + p + '</p>')
    L[-1] = L[-1].replace('margin:0 0 12px;', 'margin:0;')
    L.append('</div>')
    return NL.join(L)

def sources_block(pairs):
    parts = ['<div style="margin-top:26px;text-align:center;font-size:12px;color:rgba(255,255,255,.4);line-height:1.8;">Sources: ']
    links = []
    for label, url in pairs:
        links.append('<a href="' + url + '" target="_blank" rel="noopener" style="color:rgba(255,255,255,.6);">' + label + '</a>')
    parts.append(' &middot; '.join(links))
    parts.append('</div>')
    return NL.join(parts)

# ------------------------- WASIM AKRAM -------------------------
wasim_cards = [
    ('FULL NAME', 'Mohammad Wasim Akram (মোঃ ওয়াসিম আকরাম) - Chattogram division of the July Revolution'),
    ('BORN', '1998, Mehernama village, Pekua Upazila, Cox\u2019s Bazar - second of five siblings'),
    ('FAMILY', 'Father: Shafiul Alam &middot; Mother: Jyosna Begum'),
    ('EDUCATION', 'Mehernama High School (SSC 2017) &rarr; Bakalia Govt. College (HSC 2019) &rarr; <b>Chattogram College, BA (Hons) English, 4th year</b>'),
    ('SHAHADAT', '16 July 2024, ~4 PM, Bahaddarhat, Chattogram - shot in head and chest during Chhatra League/Jubo League attacks on students; pronounced dead at Chattogram Medical College Hospital'),
]
wasim_story = [
    story_block('His last Facebook status', [
        'On 16 July 2024 he posted: <b style="color:#fff;">\u099a\u09b2\u09c7 \u0986\u09b8\u09c1\u09a8 \u09b7\u09cb\u09b2\u09cb\u09b6\u09b9\u09b0</b> - "Come to Sholoshohor" - calling people to the streets of Chattogram. That afternoon he was shot.',
        'His honours result was published 2.5 months after his death: <b style="color:#fff;">First Class, 11th among all English department students</b> - he never saw it.',
    ]),
    story_block('Legacy', [
        'Thousands attended his janaza on 17 July at Pekua; buried in the family graveyard. Chattogram College students hold tree-planting and prayer events in his memory.',
        'A <b style="color:#fff;">Shaheed Wasim Akram Smritistambha</b> (memorial monument) stands in his honor, and his words are painted as graffiti on the city\u2019s expressway pillars. He is honored among the <b style="color:#fff;">first-rank martyrs of the July Revolution</b>, and his portrait appears in the e-passport watermark alongside Abu Sayed and Mir Mugdho.',
    ]),
    sources_block([
        ('বাংলা উইকিপিডিয়া', 'https://bn.wikipedia.org/wiki/%E0%A6%AE%E0%A7%8B:_%E0%A6%93%E0%A6%AF%E0%A6%BC%E0%A6%BE%E0%A6%B8%E0%A6%BF%E0%A6%AE_%E0%A6%86%E0%A6%95%E0%A6%B0%E0%A6%BE%E0%A6%AE'),
        ('shibir.org.bd', 'https://shibir.org.bd/en/martyrs/shaheed-wasim-akram'),
        ('Prothom Alo', 'https://www.prothomalo.com/bangladesh/district/xrd350ffzm'),
    ]),
]

# ------------------------- FARHAN FAIYAAZ -------------------------
farhan_cards = [
    ('FULL NAME', 'Mohammad Farhanul Islam Bhuiyan (মোহাম্মদ ফারহানুল ইসলাম ভূঁইয়া) - "Farhan Faiyaaz"'),
    ('BORN', '12 September 2007, Dhaka'),
    ('FAMILY', 'Father: Shahidul Islam (businessman) &middot; mother and a younger sister, Sayima'),
    ('EDUCATION', 'Dhaka Residential Model College (DRMC) from class 3; resident student; <b>Class XI Science, HSC batch of 2025</b> - aged 17'),
    ('SHAHADAT', '18 July 2024, Dhanmondi 27 - shot in the chest at the frontline; carried on a rickshaw, then an ambulance to City Hospital, Mohammadpur; died in treatment'),
]
farhan_story = [
    story_block('The bio he wrote himself', [
        '<span style="color:#fff;font-size:15px;font-style:italic;">\u201c\u098f\u0995\u09a6\u09bf\u09a8 \u09aa\u09c3\u09a5\u09bf\u09ac\u09c0 \u099b\u09c7\u09a1\u09bc\u09c7 \u099a\u09b2\u09c7 \u09af\u09c7\u09a4\u09c7 \u09b9\u09ac\u09c7\u0964 \u098f\u09ae\u09a8 \u099c\u09c0\u09ac\u09a8 \u0997\u09a1\u09bc\u09cb, \u09af\u09be\u09a4\u09c7 \u09ae\u09c3\u09a4\u09cd\u09af\u09c1\u09b0 \u09aa\u09b0 \u09ae\u09be\u09a8\u09c1\u09b7 \u09a4\u09cb\u09ae\u09be\u0995\u09c7 \u09ae\u09a8\u09c7 \u09b0\u09be\u0996\u09c7\u0964\u201d</span><br>"One day we must leave this world. Build a life such that people remember you after death." - from his own Facebook bio. He kept his word.',
        'He dreamed of research, higher study abroad, and returning to build his country. His father testified as the first prosecution witness at the International Crimes Tribunal (June 2026); classmate Wasif Munim, who carried him, testified in July 2026. Formal charges were accepted against 28 accused in January 2026.',
    ]),
    story_block('What his name became', [
        '<b style="color:#fff;">Shaheed Farhan Faiyaaz Playground</b> west of the National Parliament (Nov 2024) &middot; <b style="color:#fff;">Shaheed Farhan Faiyaz Road</b> - Dhanmondi Road 27, renamed May 2025, the street where he fell. His college commemorates him every July.',
    ]),
    sources_block([
        ('বাংলা উইকিপিডিয়া', 'https://bn.wikipedia.org/wiki/%E0%A6%AB%E0%A6%BE%E0%A6%B0%E0%A6%B9%E0%A6%BE%E0%A6%A8_%E0%A6%AB%E0%A6%BE%E0%A6%87%E0%A6%AF%E0%A6%BC%E0%A6%BE%E0%A6%9C'),
        ('julyshohid.com', 'https://julyshohid.com/details.php?id=664&lang=english'),
        ('The Daily Star', 'https://www.thedailystar.net/news/bangladesh/rights/news/dhanmondi-road-renamed-after-july-martyr-farhan-faiyaz-3897646'),
    ]),
]

# ------------------------- GOLAM NAFIZ -------------------------
nafiz_cards = [
    ('FULL NAME', 'Md. Golam Nafiz (মোঃ গোলাম নাফিজ)'),
    ('BORN', '22 May 2008, Mahakhali, Dhaka - younger of two brothers'),
    ('FAMILY', 'Father: Golam Ahmed &middot; Mother: Nasima Akter'),
    ('EDUCATION', 'Banani Bidyaniketan School &amp; College (SSC 2024); admitted to Navy College, Dhaka - <b>he never got to attend a single class</b>'),
    ('SHAHADAT', '4 August 2024, ~4:30 PM, Farmgate - shot by police; on the rickshaw he was still alive, but Chhatra League men blocked the way; pronounced dead at hospital. Aged 17.'),
]
nafiz_story = [
    story_block('The photograph that crossed the country', [
        'On the rickshaw, unconscious, with the flag of Bangladesh tied around his head, hanging from the footrest - photographer Jibon Ahmed (Daily Manab Zamin) captured the image that ran on the paper\u2019s front page and became one of the uprising\u2019s defining pictures.',
        'Rickshaw puller Noor Mohammad peddled through the blockade trying to save him; the rickshaw itself is now preserved at the <b style="color:#fff;">July Revolution Memorial Museum</b>. Banani Bidyaniketan named a building after him. His father spent the whole night searching hospital to hospital, finding him only the next morning at the Suhrawardy morgue.',
    ]),
    sources_block([
        ('বাংলা উইকিপিডিয়া', 'https://bn.wikipedia.org/wiki/%E0%A6%97%E0%A7%8B%E0%A6%B2%E0%A6%BE%E0%A6%AE_%E0%A6%A8%E0%A6%BE%E0%A6%AB%E0%A6%BF%E0%A6%9C'),
        ('Prothom Alo', 'https://www.prothomalo.com/bangladesh/district/'),
        ('The Daily Star', 'https://www.thedailystar.com.bd/'),
    ]),
]

sections = {
    'wasim-akram': build_section('wasim-akram', 'Chattogram\u2019s First Shaheed',
        'Wasim Akram', 'ওয়াসিম আকরাম &middot; 1998 - 16 July 2024',
        'His result came after him: First Class - a topper\u2019s ending, written by a martyr\u2019s hand.',
        'wasim-akram.jpg', 'Shaheed Wasim Akram (1998-2024)',
        'Photo: The Business Standard, via Bengali Wikipedia (fair use - memorial/educational)',
        'https://bn.wikipedia.org/wiki/%E0%A6%AE%E0%A7%8B:_%E0%A6%93%E0%A6%AF%E0%A6%BC%E0%A6%BE%E0%A6%B8%E0%A6%BF%E0%A6%AE_%E0%A6%86%E0%A6%95%E0%A6%B0%E0%A6%BE%E0%A6%AE',
        'বাংলা উইকিপিডিয়া - ওয়াসিম আকরাম',
        wasim_cards, wasim_story),
    'farhan-faiyaaz': build_section('farhan-faiyaaz', 'The boy who kept his word',
        'Farhan Faiyaaz', 'ফারহান ফাইয়াজ &middot; 12 September 2007 - 18 July 2024',
        'Build a life such that people remember you after death.',
        'farhan-faiyaaz.jpg', 'Shaheed Farhan Faiyaaz (2007-2024)',
        'Photo: The Business Standard, via Bengali Wikipedia (fair use - memorial/educational)',
        'https://bn.wikipedia.org/wiki/%E0%A6%AB%E0%A6%BE%E0%A6%B0%E0%A6%B9%E0%A6%BE%E0%A6%A8_%E0%A6%AB%E0%A6%BE%E0%A6%87%E0%A6%AF%E0%A6%BC%E0%A6%BE%E0%A6%9C',
        'বাংলা উইকিপিডিয়া - ফারহান ফাইয়াজ',
        farhan_cards, farhan_story),
    'golam-nafiz': build_section('golam-nafiz', 'The boy with the flag',
        'Golam Nafiz', 'গোলাম নাফিজ &middot; 22 May 2008 - 4 August 2024',
        'He held the flag in death the way he held it in life.',
        'nafiz-banner.jpg', 'Shaheed Golam Nafiz (2008-2024)',
        'Photo: Wikimedia Commons, CC BY 4.0 (commemoration banner - no free portrait exists)',
        'https://commons.wikimedia.org/wiki/File:Shaheed_Nafiz_in_NCD_youth_carnival.jpg',
        'Wikimedia Commons - Shaheed Nafiz banner',
        nafiz_cards, nafiz_story),
}

changed_html = False
for sid, block in sections.items():
    if ('<section id="' + sid + '"') not in html:
        # insert before martyrs-list section
        anchor = html.find('<section id="martyrs-list"')
        assert anchor > 0, 'martyrs-list anchor missing'
        html = html[:anchor] + block + NL + NL + html[anchor:]
        changed_html = True
        print('july.html: inserted section #' + sid)
    else:
        print('july.html: section #' + sid + ' already present, skipped')

if changed_html:
    open(jp, 'w', encoding='utf-8', newline='').write(html)

# =====================================================================
# PART 2 - app.js knowledge base
# =====================================================================
ap = ROOT + r'\assets\app.js'
js = open(ap, encoding='utf-8', newline='').read()
js_before = len(js)

entries = {
    'wasim_akram_bio': 'Shaheed Wasim Akram (ওয়াসিম আকরাম, 1998 - 16 July 2024): from Mehernama village, Pekua, Cox\\u2019s Bazar; second of five siblings. SSC 2017 (Mehernama High School), HSC 2019 (Bakalia Govt. College), then BA (Hons) English, 4th year at Chattogram College. On 16 July 2024, around 4 PM at Bahaddarhat, Chattogram, he was shot in the head and chest during Chhatra League and Jubo League attacks on quota-reform students, and pronounced dead at Chattogram Medical College Hospital. He is called the first martyr of Chattogram in the July uprising.',
    'wasim_akram_legacy': 'Wasim Akram\\u2019s legacy: his honours result was published 2.5 months after his death - First Class, 11th among all English department students, a result he never saw. Thousands joined his janaza at Pekua on 17 July 2024. Chattogram College students hold tree-plantings and prayers in his memory, a Shaheed Wasim Akram memorial monument (Smritistambha) stands in his honor, his words from his last Facebook status - Come to Sholoshohor - are painted as graffiti on expressway pillars, and his portrait appears in the new e-passport watermark alongside Abu Sayed and Mir Mugdho.',
    'farhan_faiyaaz_bio': 'Shaheed Farhan Faiyaaz (Mohammad Farhanul Islam Bhuiyan; 12 September 2007 - 18 July 2024): Class XI science student (HSC batch 2025) at Dhaka Residential Model College, aged 17. His Facebook bio read: One day we must leave this world; build a life such that people remember you after death. On 18 July 2024 at Dhanmondi 27 he was shot in the chest at the frontline of the quota movement, was carried by rickshaw and ambulance to City Hospital in Mohammadpur, and died in treatment - one of about forty martyrs of that day.',
    'farhan_faiyaaz_legacy': 'Farhan Faiyaaz\\u2019s legacy: Shaheed Farhan Faiyaaz Playground was named west of the National Parliament (November 2024), and Dhanmondi Road 27 - the street where he fell - was renamed Shaheed Farhan Faiyaz Road (May 2025). His father testified as the first prosecution witness at the International Crimes Tribunal (June 2026); classmate Wasif Munim, who carried him to the ambulance, testified in July 2026; formal charges were accepted against 28 accused in January 2026. His college commemorates him every July.',
    'golam_nafiz_bio': 'Shaheed Golam Nafiz (মোঃ গোলাম নাফিজ; 22 May 2008 - 4 August 2024): from Mahakhali, Dhaka, younger of two brothers; SSC 2024 from Banani Bidyaniketan School and College, admitted to Navy College Dhaka - a class he never got to attend. On 4 August 2024, around 4:30 PM at Farmgate, he was shot by police during the non-cooperation movement. His companions put him on a rickshaw; rickshaw puller Noor Mohammad peddled to save him, but Chhatra League men blocked the way and delayed him. He was pronounced dead at hospital, aged 17.',
    'golam_nafiz_legacy': 'Golam Nafiz\\u2019s legacy: photographer Jibon Ahmed captured him unconscious on the rickshaw with the flag of Bangladesh tied around his head - the image ran on the front page of Daily Manab Zamin and became one of the defining pictures of the uprising. The rickshaw is preserved at the July Revolution Memorial Museum, its puller Noor Mohammad honored by the interim government; Banani Bidyaniketan named a building after him, and advisers Nahid Islam and Asif Mahmud visited his family on 19 August 2024.',
}
new_entries = [k for k in entries if ('cR["' + k + '"]') not in js]
if new_entries:
    add = NL.join(['cR["' + k + '"]="' + entries[k] + '";' for k in new_entries])
    anchor = 'cR["abrar_fahad_bio"]'
    assert anchor in js, 'abrar anchor missing'
    js = js.replace(anchor, add + NL + anchor, 1)
    print('app.js: added cR entries:', new_entries)

aliases = [
    ('wasim akram', 'wasim_akram_bio'), ('wasim', 'wasim_akram_bio'),
    ('who was wasim akram', 'wasim_akram_bio'), ('wasim akram chattogram', 'wasim_akram_bio'),
    ('wasim sholoshohor', 'wasim_akram_legacy'), ('wasim first class', 'wasim_akram_legacy'),
    ('farhan faiyaaz', 'farhan_faiyaaz_bio'), ('farhan', 'farhan_faiyaaz_bio'),
    ('farhanul islam', 'farhan_faiyaaz_bio'), ('drmc martyr', 'farhan_faiyaaz_bio'),
    ('farhan dhanmondi', 'farhan_faiyaaz_bio'), ('farhan faiyaaz road', 'farhan_faiyaaz_legacy'),
    ('farhan playground', 'farhan_faiyaaz_legacy'), ('farhan tribunal', 'farhan_faiyaaz_legacy'),
    ('golam nafiz', 'golam_nafiz_bio'), ('nafiz', 'golam_nafiz_bio'),
    ('farmgate martyr', 'golam_nafiz_bio'), ('nafiz rickshaw', 'golam_nafiz_legacy'),
    ('nafiz flag photo', 'golam_nafiz_legacy'), ('nafiz museum rickshaw', 'golam_nafiz_legacy'),
]
new_aliases = [(k, v) for k, v in aliases if ('aliasMap["' + k + '"]') not in js]
if new_aliases:
    add = NL.join(['aliasMap["' + k + '"]="' + v + '";' for k, v in new_aliases])
    anchor = 'aliasMap["abrar fahad"]'
    assert anchor in js, 'alias anchor missing'
    js = js.replace(anchor, add + NL + anchor, 1)
    print('app.js: added aliases:', [k for k, v in new_aliases])

# Bangla routing: append inside the bn map that contains the abrar entries
bn_new = [
    ('ওয়াসিম আকরাম', 'wasim akram'), ('ওয়াসিম', 'wasim akram'),
    ('ফারহান ফাইয়াজ', 'farhan faiyaaz'), ('ফারহান', 'farhan faiyaaz'),
    ('গোলাম নাফিজ', 'golam nafiz'), ('নাফিজ', 'golam nafiz'),
    ('ষোলোশহর', 'wasim sholoshohor'), ('ফারমগেট শহীদ', 'golam nafiz'),
]
bn_anchor = "  'আবরার':'abrar fahad',"
assert bn_anchor in js, 'bn anchor missing'
add_bn = NL.join(["  '" + k + "':'" + v + "'," for k, v in bn_new if ("'" + k + "'") not in js])
if add_bn:
    js = js.replace(bn_anchor, bn_anchor + NL + add_bn, 1)
    print('app.js: added bn routing keys')

open(ap, 'w', encoding='utf-8', newline='').write(js)
print('app.js size:', js_before, '->', len(js))
print('DONE')
