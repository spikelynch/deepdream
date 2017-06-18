#!/usr/bin/env python3

import re

CLASSFILE = 'divs.txt'

cat_re = re.compile('^# ([A-Za-z]+)')
class_re = re.compile('^([0-9]+) n')

cats = {}
cat = None

with open(CLASSFILE, 'r') as cf:
    for l in cf:
        m = cat_re.search(l)
        if m:
            cat = m.group(1)
        m = class_re.search(l)
        if m:
            if not cat:
                print("Fuck")
            else:
                if not cat in cats:
                    cats[cat] = 0
                cats[cat] += 1

dcats = sorted(cats, key=cats.get, reverse=True)

t = 0
for cat in dcats:
    print("%s: %d" % ( cat, cats[cat]))
    t += cats[cat]

print("Total: %d" % t)
        
