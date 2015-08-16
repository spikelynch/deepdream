#!/usr/bin/env python

import sys, os, os.path
import subprocess
import string

origfile = 'Input/noise.jpg'
guide = 'Input/Cells1.jpg'
recipe = 'Layers/inception_output_layers.txt'
script = './dream.py'
path = 'CellNoise'
iters = '25'
octaves = '4'

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
    safelayer = os.path.join(path, model + '_' + layer.translate(tt))
    a = [ script, "--guide", guide, "--guidelayer", layer, "--model", model, "--layer", "inception_4c/output", "--basefile", safelayer, "--iters", iters, "--octaves", octaves, origfile]
    print ' '.join(a)
    subprocess.call(a)

