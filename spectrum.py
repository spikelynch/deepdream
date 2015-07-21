#!/usr/bin/env python

import sys, os
import subprocess
import string

origfile = 'greyfriars.jpg'
file = 'recipe.txt'
script = './dream.py'

content = None

with open(file) as f:
    content = [ x.strip('\n') for x in f.readlines() ]

if not content:
    exit()

tt = string.maketrans('/', '_')
    
for layer in content:
    safelayer = layer.translate(tt)
    a = [ script, "--layer", layer, "--basefile", safelayer, origfile]
    print ' '.join(a)
    subprocess.call(a)
    
