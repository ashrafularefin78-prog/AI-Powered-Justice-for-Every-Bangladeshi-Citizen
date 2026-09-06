#!/usr/bin/env python3
"""Corruption guard for the chatbot FIGURES registry in assets/app.js.

Fails (exit 1) if the FIGURES.push({...}) block contains:
  1. double-escaped unicode sequences (a literal backslash + 'u' + 4 hex digits
     in the source) - these render as visible "\\u0986" garbage in replies;
  2. stray quote wrapping on entry texts (text:"\\"...\\"") - visible quote
     marks at the start/end of answers;
  3. any raw backslash inside the block (nothing legitimate uses one).

Run manually:  python3 check_figures.py
Also runs automatically at the top of build_standalone.py and
build_allinone.py, so a corrupted registry can no longer reach a build.
"""
import sys

HEX = set('0123456789abcdefABCDEF')


def count_dbl_escapes(block):
    """Count literal backslash+'u'+4hex occurrences (plain string scan)."""
    n = 0
    i = block.find(chr(92) + 'u')
    while i != -1:
        tail = block[i + 2:i + 6]
        if len(tail) == 4 and all(c in HEX for c in tail):
            n += 1
        i = block.find(chr(92) + 'u', i + 1)
    return n


def main():
    try:
        s = open('assets/app.js', encoding='utf-8').read()
    except OSError as e:
        print('check_figures: cannot read assets/app.js: %s' % e)
        return 1

    if 'FIGURES.push' not in s:
        print('check_figures: no FIGURES registry found - nothing to check')
        return 0

    start = s.index('FIGURES.push')
    end = s.rindex('installFigures')
    block = s[start:end]

    errors = []
    BS = chr(92)

    dbl = count_dbl_escapes(block)
    if dbl:
        errors.append('%d escaped unicode sequences (render as literal '
                      'backslash-uXXXX text in replies)' % dbl)

    lead = 'text:"' + BS + '"'
    n_lead = block.count(lead)
    if n_lead:
        errors.append('%d entry texts start with a stray escaped quote' % n_lead)

    n_bs = block.count(BS)
    if n_bs:
        errors.append('%d raw backslash(es) inside the FIGURES block (entries '
                      'must be real UTF-8 text, no escape sequences)' % n_bs)

    figs = block.count('FIGURES.push')
    if errors:
        print('check_figures: FAIL - FIGURES registry is corrupted:')
        for e in errors:
            print('  - ' + e)
        print('Fix: decode the sequences to real UTF-8 characters and remove '
              'quote wrapping, then re-run. See .freebuff/run.md (app68) for '
              'the repair recipe.')
        return 1

    print('check_figures: OK - %d figures, no escape/quote-wrap corruption' % figs)
    return 0


if __name__ == '__main__':
    sys.exit(main())
