#!/usr/bin/env python

import sys, os, os.path
import subprocess
import string

origfile = 'Input/blank_places.jpg'
script = './dream.py'
model = 'places'
recipe_file = './Layers/places_layers.txt'
iters = '5'
octaves = '3'
frames = '20'
basefile = 'Dive5/goog'
startframe = 0
zoom = '0.05'

recipe = None

with open(recipe_file) as f:
    recipe = [ x.strip('\n') for x in f.readlines() ]

if not recipe:
    sys.exit()

print recipe



i = startframe
f = int(frames)
lastfile = origfile

for layer in recipe:
    a = [ script, "--model", model, "--layer", layer, "--basefile", basefile, "--iters", iters, "--octaves", octaves, "--frames", frames, "--zoom", zoom, "--initial", str(i), origfile ]
    print ' '.join(a)
    subprocess.call(a)
    newfile = 'Output/' + basefile + ('_f%d.jpg' % (i + f - 1))
    if os.path.isfile(newfile):
        origfile = newfile
        i += f
    else:
        origfile = lastfile

