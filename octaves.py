#!/usr/bin/env python2

import sys, os, os.path, json, copy
import subprocess
import string, random

DEFAULT_OCTAVE = {
    "layer": "prob",
    "iter_n": 1000,
    "start_sigma": 1.0,
    "end_sigma": 1.0,
    "start_step_size": 2.5,
    "end_step_size": 2.5
    }
 

origfile = './Input/vgg_bg.jpg'
model = 'vgg16'
# bg = [ 'Scripts/background.sh', "224x224", "gray", "8", "70", "gradient:gray90-gray10", "10%,90%", "0x8", origfile ]
bg = [ "convert", "-size", "320x320", "-colorspace", "RGB", "-type", "truecolor", "canvas:gray", origfile ]
script = './dream.py'
path = './Output/VGG16Matrix'

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
    ts = random.sample(range(1000), 3)
    targetjs = {}
    for t in ts:
        targetjs[str(t)] = 1.0
    write_targets(targetjs, fn)

def write_targets(targets, fn):
    with open(fn, "w") as jf:
        jf.write(json.dumps(targets, indent=4))
 
tfile = os.path.join(path, 'targets.json')
# write_targets({ "496": 1.0 }, tfile)

rand_targets(tfile)

subprocess.call(bg)

NRANGE = 10 
SIGMA_MIN = 0.1
SIGMA_MAX = 0.4
SIGMA_START = 1.2
STEP_MIN = 1
STEP_MAX = 8
STEP_START = 1.2
SCALE = 4.0

def xyoctaves(x, y):
    x0 = x / (0.0 + NRANGE)
    y0 = y / (0.0 + NRANGE)
#    step = STEP_MIN + x0 * ( STEP_MIN - STEP_MAX )
#    sigma = SIGMA_MIN + y0 * ( SIGMA_MIN - SIGMA_MAX )
    step = STEP_MIN + x0 * ( STEP_MAX - STEP_MIN )
    sigma = SIGMA_MIN + y0 * ( SIGMA_MAX - SIGMA_MIN )


    return {
        "start_step_size": step * STEP_START,
        "end_step_size": step,
        "start_sigma": sigma * SIGMA_START,
        "end_sigma": sigma
    }
 
for x in range(0, NRANGE + 1):
    for y in range(0, NRANGE + 1):
        ofile = os.path.join(path, 'octaves.{:02d}.{:02d}.json'.format(x, y))
        bfile = 'output.{:02d}.{:02d}'.format(x, y)
        make_octaves(ofile, xyoctaves(x, y))
        a = [ script, "--gpu", "--deepdraw", ofile, "--target", tfile, "--model", model, "--basefile", bfile, origfile, path ]
        print ' '.join(a)
        subprocess.call(a)
