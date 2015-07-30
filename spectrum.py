#!/usr/bin/env python

import sys, os, os.path
import subprocess
import string

origfile = 'theGap.jpg'
model = 'places'
recipe = 'places_layers.txt'
script = './dream.py'
path = 'PlacesSpectrum'

content = None

with open(recipe) as f:
    content = [ x.strip('\n') for x in f.readlines() ]

if not content:
    exit()

tt = string.maketrans('/', '_')
    
for line in content:
    fields = line.split()
    model = fields[0]
    layer = fields[1]
    safelayer = os.path.join(path, layer.translate(tt))
    a = [ script, "--model", model, "--layer", layer, "--basefile", safelayer, origfile]
    print ' '.join(a)
    subprocess.call(a)
    
