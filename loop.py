#!/usr/bin/env python

import sys, os, os.path
import subprocess
import string

origfile = 'Output/Dive3/goog_f780.jpg'
script = './dream.py'
recipe = './Layers/gnet_all_layers_restart.txt'
iters = '5'
octaves = '3'
frames = '20'
basefile = 'Dive3/goog'
startframe = 781
zoom = '0.02'
rotate = 5

with open(recipe) as f:
    content = [ x.strip('\n') for x in f.readlines() ]

if not content:
    sys.exit()

recipe = []

for line in content:
    fields = line.split()
    if len(fields) == 2:
        recipe.append((fields[0], fields[1]))


tt = string.maketrans('/', '_')

i = startframe
f = int(frames)
lastfile = origfile

for model, layer in recipe:
    a = [ script, "--model", model, "--layer", layer, "--basefile", basefile, "--iters", iters, "--octaves", octaves, "--frames", frames, "--zoom", zoom, "--initial", str(i), origfile ]
    print ' '.join(a)
    subprocess.call(a)
    newfile = 'Output/' + basefile + ('_f%d.jpg' % (i + f - 1))
    if os.path.isfile(newfile):
        origfile = newfile
        i += f
    else:
        origfile = lastfile

