#!/usr/bin/env python2

import sys, os, os.path
import subprocess
import string

origfile = 'Input/grey.jpg'
outdir = 'Output'
script = './dream.py'
model = 'manga_tag'
recipe_file = './Layers/layers_manga_high.txt'
iters = '2'
octaves = '5'
frames = '20'
basefile = 'Dive6/manga'
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
    newfile = os.path.join(outdir, basefile + ('_f%d.jpg' % (i + f - 1)))
    a = [ script, "--model", model, "--layer", layer, "--basefile", basefile, "--iters", iters, "--octaves", octaves, "--frames", frames, "--zoom", zoom, "--initial", str(i), origfile, outdir ]
    print ' '.join(a)
    subprocess.call(a)
    if os.path.isfile(newfile):
        origfile = newfile
        i += f
    else:
        origfile = lastfile

