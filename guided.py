#!/usr/bin/env python

import sys, os, os.path
import subprocess
import string

origfile = 'noise.jpg'
guide = 'Beatrice_Dante_512.jpg'
recipe = 'Layers/db_layers_100.txt'
model = 'googlenet'
script = './dream.py'
path = 'Guided450'
iters = '100'
octaves = '4'

content = None

with open(recipe) as f:
    content = [ x.strip('\n') for x in f.readlines() ]

if not content:
    exit()

tt = string.maketrans('/', '_')

for line in content:
    #fields = line.split()
    #model = fields[0]
    layer = line
    safelayer = os.path.join(path, layer.translate(tt))
    a = [ script, "--guide", guide, "--guidelayer", layer, "--model", model, "--layer", "inception_4c/output", "--basefile", safelayer, "--iters", iters, "--octaves", octaves, origfile]
    print ' '.join(a)
    subprocess.call(a)

