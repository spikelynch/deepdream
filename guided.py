#!/usr/bin/env python

import sys, os, os.path
import subprocess
import string

origfile = 'Input/Greyfriars_small.jpg'
guides = [ 'instructions', 'leaves', 'teddy' ]
layers = 'Layers/vgg.txt'
script = './dream.py'
output = 'Output/GuideMatrix'

iters = '10'
octaves = '8' 

content = None

with open(layers) as f:
    content = [ x.strip('\n') for x in f.readlines() ]

if not content:
    exit()

tt = string.maketrans('/', '_')

for layer in content:
    for guidelayer in content:
        for g in guides:
            gfile = "Input/Guides/{}_sm.jpg".format(g)
            bfile = "{}.{}.{}".format(g, layer, guidelayer)
            a = [ script, "--gpu", "--guide", gfile, "--guidelayer", guidelayer, "--model", "vgg", "--layer", layer, "--basefile", bfile, "--iters", iters, "--octaves", octaves, origfile, output ]
            print ' '.join(a)
            subprocess.call(a)

