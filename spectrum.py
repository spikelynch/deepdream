#!/usr/bin/env python2

import sys, os, os.path
import subprocess
import string
from classes import ImageCategories

origfile = './Input/vgg_bg.jpg'
model = 'vgg'
recipe = 'Layers/vgg.txt'
# bg = [ 'Scripts/background.sh', "224x224", "gray", "8", "70", "gradient:gray90-gray10", "10%,90%", "0x8", origfile ]
bg = [ "convert", "-size", "224x224", "-colorspace", "RGB", "-type", "truecolor", "canvas:gray70", origfile ] 
script = './dream.py'
iters = '10'
path = './Output/VGGLayers/'
ddspec = '../neuralgae/src/Control/Renderers/feature_g3m_s4b.json'
#classdir = './Classes/'

#ic = ImageCategories(classdir, model)

with open(recipe, 'r') as rf:
    for line in rf.readlines():
        layers.append(line)

for t in range(2416, 4096):
    layerpath = "vector_{}".format(t)
    print layerpath
    subprocess.call(bg)
    target = '{"' + str(t) + '": 1}'
    a = [ script, "--gpu", "--deepdraw", ddspec, "--target", target, "--model", model, "--basefile", layerpath, origfile, path ]
    print ' '.join(a)
    subprocess.call(a)
