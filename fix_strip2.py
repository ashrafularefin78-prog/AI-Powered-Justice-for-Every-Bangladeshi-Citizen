# -*- coding: utf-8 -*-
"""Make Nafiz/Farhan strip cards clickable + insert Wasim Akram strip card."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

p = 'july.html'
src = open(p, encoding='utf-8', newline='').read()

PLAIN_OPEN = '<div class="martyr-strip-card" style="width:200px;">'
CLICK_TMPL = ("<div class=\"martyr-strip-card\" style=\"width:200px;cursor:pointer;\" "
              "onclick=\"document.getElementById('{sid}').scrollIntoView({{behavior:'smooth'}})\" "
              "title=\"Read {name}'s full memorial\">")


def make_clickable(img_file, sec_id, en_name):
    global src
    ipos = src.find('src="assets/img/' + img_file + '"')
    if ipos < 0:
        print('IMG NOT FOUND', img_file)
        return
    strip_end = src.find('class="martyr-card"')  # strip lives above the martyr grid
    if strip_end < 0:
        strip_end = len(src)
    if ipos > strip_end:
        print('SKIP (img outside strip)', img_file)
        return
    opos = src.rfind(PLAIN_OPEN, 0, ipos)
    if opos < 0:
        print('OPEN TAG NOT FOUND for', img_file)
        return
    new_open = CLICK_TMPL.format(sid=sec_id, name=en_name)
    src = src[:opos] + new_open + src[opos + len(PLAIN_OPEN):]
    print('CLICKABLE', img_file, '->', sec_id)


make_clickable('nafiz-banner.jpg', 'golam-nafiz', 'Golam Nafiz')
make_clickable('farhan-faiyaaz-chattar.jpg', 'farhan-faiyaaz', 'Farhan Faiyaaz')

# Insert Wasim Akram card right after Abu Sayed's (same day: 16 July 2024)
WASIM_CARD = """      <!-- Wasim Akram -->
      <div class="martyr-strip-card" style="width:200px;cursor:pointer;" onclick="document.getElementById('wasim-akram').scrollIntoView({behavior:'smooth'})" title="Read Wasim Akram's full memorial">
        <div style="border-radius:16px;overflow:hidden;border:2px solid rgba(244,63,94,.5);box-shadow:0 8px 30px rgba(0,0,0,.4);">
          <img src="assets/img/wasim-akram.jpg" alt="Shaheed Wasim Akram (1998-2024)"
               style="width:100%;aspect-ratio:3/4;object-fit:cover;display:block;" loading="lazy">
        </div>
        <div style="margin-top:12px;color:#fff;font-weight:700;font-size:16px;">ওয়াসিম আকরাম</div>
        <div style="color:rgba(255,255,255,.6);font-size:13px;">Wasim Akram (d. 2024)</div>
        <div style="color:rgba(255,255,255,.4);font-size:11px;margin-top:4px;">Shot by police · Chattogram</div>
      </div>
      """

if "wasim-akram').scrollIntoView" in src:
    print('wasim strip card already present')
else:
    anchor = src.find('<!-- Mir Mugdho -->')
    if anchor < 0:
        print('ANCHOR NOT FOUND')
        sys.exit(1)
    src = src[:anchor] + WASIM_CARD + src[anchor:]
    print('wasim strip card inserted before Mugdho card')

open(p, 'w', encoding='utf-8', newline='').write(src)
print('saved')
