#!/usr/bin/env python

import sys, os, os.path
import subprocess
import string

phases = [ 0, 120 ]
origfiles = './Layers/gray_%d.jpg'
model = 'googlenet'
recipe = 'Layers/places_layers.txt'
script = './dream.py'
path = './Layers/Googlenet/'

content = None

with open(recipe) as f:
    content = [ x.strip('\n') for x in f.readlines() ]

if not content:
    exit()

for line in content:
    fields = line.split()
    #model = fields[0]
    layer = fields[1]
    layerpath = os.path.join(path, layer)
    if not os.path.exists(layerpath):
        os.makedirs(layerpath)
    print layer
    for i in phases:
        ofile = origfiles % i
        bfile = os.path.join(layer, "frame%d") % i
        a = [ script, "--dir", path, "--model", model, "--layer", layer, "--iters", "40", "--basefile", bfile, ofile]
        print ' '.join(a)
        subprocess.call(a)
