#!/usr/bin/env python

import sys, os, os.path
import subprocess
import string

frames = 'Input/frame-%03d.jpg'
model = 'places'
layer = 'inception_4a/output'
script = './dream.py'
base = 'frames-%d'
iters = "15"
octaves = "4"

i = 1

file = frames % i

print file

while os.path.isfile(file):
    output = base % i
    a = [ script, "--model", model, "--layer", layer, "--basefile", output, "--iters", iters, "--octaves", octaves, file]
    print ' '.join(a)
    subprocess.call(a)
    i += 1
    file = frames % i
    
