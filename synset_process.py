#!/usr/bin/env python

import os

RAW = 'synset_words.txt'

def process(x):
    fields = x.split(' ')
    n = fields[0]
    names = ' '.join(fields[1:])
    return n, names





lines = None

with open(RAW) as f:
    lines = [ x.strip('\n') for x in f.readlines() ]

if not lines:
    sys.exit(-1)

classes = [ process(x) for x in lines ]

i = 0

for i in range(0, len(classes)):
    n, name = classes[i]
    print ' '.join([str(i), n, name])

