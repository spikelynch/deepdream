#!/usr/bin/env python2

import sys, os, os.path
import subprocess
import string

origfile = './Input/manga.jpg'
model = 'manga_tag'
recipe = 'Layers/layers_manga_features.txt'
script = './dream.py'
iters = '40'
path = './Output/MFeatures/'

content = None

with open(recipe) as f:
    content = [ x.strip('\n') for x in f.readlines() ]

if not content:
    sys.exit()

layers = []
    
for line in content:
    fields = line.split()
    layers.append(fields[0])


for layer in layers:
    layerpath = layer.replace('/', '_')
    print layerpath
    a = [ script, "--model", model, "--layer", layer, "--iters", iters, "--basefile", layerpath + '.jpg', origfile, path ]
    print ' '.join(a)
    subprocess.call(a)
