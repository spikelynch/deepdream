#!/usr/bin/env python

import sys, os, os.path
from shutil import copy
import subprocess
import string

origfile = 'Input/blank_places.jpg'
tempfile = 'Output/tempfile.jpg'
glide="-5 -background grey"
script = './dream.py'
model = 'googlenet'
recipe_file = './Layers/places_layers.txt'
iters = '2'
octaves = '3'
frames = '60'
basefile = 'Loop3/google'
startframe = 0
zoom = '0.00'
rotate = '2'

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
    g = [ 'convert', newfile, '-page', glide, '-flatten', tempfile ]
    subprocess.call(g)
    print "shift %s -> %d" % ( newfile, tempfile )
    copy(tempfile, newfile)
    if os.path.isfile(newfile):
        origfile = newfile
        i += f
    else:
        origfile = lastfile
    origfile = tempfile

