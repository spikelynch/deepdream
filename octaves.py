#!/usr/bin/env python2

import sys, os, os.path, json, copy
import subprocess
import string, random

DEFAULT_OCTAVE = {
    "layer": "prob",
    "iter_n": 1024,
    "start_sigma": 0.34,
    "end_sigma": 0.34,
    "start_step_size": 2.0,
    "end_step_size": 2.5
    }
 

origfile = './Input/vgg_bg.jpg'
model = 'vgg'
# bg = [ 'Scripts/background.sh', "224x224", "gray", "8", "70", "gradient:gray90-gray10", "10%,90%", "0x8", origfile ]
bg = [ "convert", "-size", "224x224", "-colorspace", "RGB", "-type", "truecolor", "canvas:gray60", origfile ]
script = './dream.py'
path = './Output/VGGScale2/'

def rand_octaves(fn):
    o = {
        "layer": "prob",
        "iter_n": 960,
        "start_sigma": random.uniform(0.02, 2.0),
        "end_sigma": random.uniform(0.02, 2.0),
        "start_step_size": random.uniform(0.5, 7.0),
        "end_step_size":random.uniform(0.5, 7.0)
    }
    os = [ o ]
    with open(fn, "w") as jf:
        jf.write(json.dumps(os, indent=4))

def make_octaves(fn, values):
    o = copy.copy(DEFAULT_OCTAVE)
    for k, v in values.iteritems():
        o[k] = v
    os = [ o ]
    with open(fn, "w") as jf:
        jf.write(json.dumps(os, indent=4))


def rand_targets(fn):
    ts = random.sample(range(1, 1000), random.randrange(2,6))
    targetjs = {}
    for t in ts:
        targetjs[str(t)] = 1.0
    with open(fn, "w") as jf:
        jf.write(json.dumps(targetjs, indent=4))
 
tfile = os.path.join(path, 'targets.json')
rand_targets(tfile)

subprocess.call(bg)

NRANGE = 20 
SIGMA = 0.4
STEP = 2.5 
SCALE = 4.0
 
for x in range(0, NRANGE + 1):
    ofile = os.path.join(path, 'octaves.{:02d}.json'.format(x))
    bfile = 'output.{:02d}'.format(x)
    scale = 0.75 + x * (SCALE - 0.75) / (NRANGE + 1.0)
    make_octaves(ofile, { "scale": scale })
    a = [ script, "--gpu", "--deepdraw", ofile, "--target", tfile, "--model", model, "--basefile", bfile, origfile, path ]
    print ' '.join(a)
    subprocess.call(a)
