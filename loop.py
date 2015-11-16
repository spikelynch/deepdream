#!/usr/bin/env python

import sys, os, os.path
from shutil import copy
import subprocess
import string

origfile = 'Output/Loop4/google_f9719.jpg'
tempfile = 'Output/tempfile.jpg'
glide="-5 -background grey"
script = './dream.py'
model = 'googlenet'
recipe_file = './Layers/places_layers.txt'
iters = '2'
octaves = '2'
frames = '960'
basefile = 'Loop4/google'
startframe = 9720
zoom = '0.00'
rotate = '4'
glide = '0,-2'
sigma = '.35'

# origfile = 'Input/noise640x480.jpg'
# tempfile = 'Output/tempfile.jpg'
# glide="-5 -background grey"
# script = './dream.py'
# model = 'googlenet'
# recipe_file = './Layers/places_layers.txt'
# iters = '2'
# octaves = '2'
# frames = '120'
# basefile = 'Loop4/google'
# startframe = 0
# zoom = '0.00'
# rotate = '4'
# glide = '0,-2'
# sigma = '.35'


# recipe = None

# with open(recipe_file) as f:
#     recipe = [ x.strip('\n') for x in f.readlines() ]

# if not recipe:
#     sys.exit()

# print recipe

recipe = [ 'inception_5b/output' ]


i = startframe
f = int(frames)
lastfile = origfile

for layer in recipe:
    a = [ script, "--model", model, "--layer", layer, "--basefile", basefile, "--iters", iters, "--octaves", octaves, "--frames", frames, "--zoom", zoom, "--glide", glide, "--sigma", sigma, "--initial", str(i), origfile ]
    print ' '.join(a)
    subprocess.call(a)
    newfile = 'Output/' + basefile + ('_f%d.jpg' % (i + f - 1))
    if os.path.isfile(newfile):
        origfile = newfile
        i += f
    else:
        origfile = lastfile

