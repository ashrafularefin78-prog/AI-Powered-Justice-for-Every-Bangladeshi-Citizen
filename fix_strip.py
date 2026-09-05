# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

p = 'july.html'
src = open(p, encoding='utf-8', newline='').read()

CARD_OPEN = '<div class="martyr-strip-card" style="width:200px;">'
LINKED_OPEN = ('<div class="martyr-strip-card" style="width:200px;cursor:pointer;" '
               'onclick="document.getElementById(\'%s\').scrollIntoView({behavior:\'smooth\'})" '
               'title="Read %s\'s full memorial">')

def link_card(name_bn, sec_id, label):
    """Positionally: find name, walk back to nearest card open, make it clickable."""
    global src
    name_idx = src.find(name_bn + '</div>')
    if name_idx < 0:
        print('MISS name', name_bn); return
    open_idx = src.rfind(CARD_OPEN, 0, name_idx)
    if open_idx < 0:
        print('MISS card open for', name_bn); return
    # is this card already linked? (next chars after open)
    after = src[open_idx:open_idx + len(CARD_OPEN) + 40]
    if 'cursor:pointer' in after:
        print('ALREADY', name_bn); return
    new_open = LINKED_OPEN % (sec_id, label)
    src = src[:open_idx] + new_open + src[open_idx + len(CARD_OPEN):]
    print('LINKED', name_bn, '->', sec_id)

link_card('গোলাম নাফিজ', 'golam-nafiz', 'Golam Nafiz')
link_card('ফারহান ফাইয়াজ', 'farhan-faiyaaz', 'Farhan Faiyaaz')
link_card('ওয়াসিম আকরাম', 'wasim-akram', 'Wasim Akram')

open(p, 'w', encoding='utf-8', newline='').write(src)
print('done')
