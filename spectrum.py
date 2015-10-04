#!/usr/bin/env python

import sys, os, os.path
import subprocess
import string

origfile = './Input/Flowers.jpg'
model = 'caffenet'
recipe = 'Layers/caffenet_layers.txt'
script = './dream.py'
path = './Layers/Caffenet/'

content = None

with open(recipe) as f:
    content = [ x.strip('\n') for x in f.readlines() ]

if not content:
    exit()

for line in content:
    fields = line.split()
    #model = fields[0]
    layer = fields[0]
    layerpath = os.path.join(path, layer)
    if not os.path.exists(layerpath):
        os.makedirs(layerpath)
    print layer
    bfile = os.path.join(layer, "frame")
    a = [ script, "--dir", path, "--model", model, "--layer", layer, "--iters", "40", "--basefile", bfile, origfile]
    print ' '.join(a)
    subprocess.call(a)
