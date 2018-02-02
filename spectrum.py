#!/usr/bin/env python2

import sys, os, os.path
import subprocess
import string
from classes import ImageCategories

origfile = './Input/vgg_bg.jpg'
model = 'vgg'
recipe = 'Layers/vgg.txt'
# bg = [ 'Scripts/background.sh', "224x224", "gray", "8", "70", "gradient:gray90-gray10", "10%,90%", "0x8", origfile ]
bg = [ "convert", "-size", "224x224", "-colorspace", "RGB", "-type", "truecolor", "canvas:gray60" ] 
script = './dream.py'
iters = '10'
path = './Output/VGGDD4/'
ddspec = '../neuralgae/src/Control/Renderers/VGG/octaves009.json'
classdir = './Classes/'

ic = ImageCategories(classdir, model)


for t in range(0, 1000):
    name = ic.name(t)
    name = name.replace(' ', '_')
    layerpath = "class_{}_{}".format(t, name)
    print layerpath
    subprocess.call(bg)
    target = '{"' + str(t) + '": 1}'
    a = [ script, "--gpu", "--deepdraw", ddspec, "--target", target, "--model", model, "--basefile", layerpath, origfile, path ]
    print ' '.join(a)
    subprocess.call(a)
