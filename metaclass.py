#!/usr/bin/env python

import sys, os, os.path
import subprocess
import string

METACLASS = {
    'fish': "0-7,390-397",
    'birds': "8-24,80-100,127-146",
    'amphibians': "25-32",
    'reptiles': "33-68",
    'arachnids': "69-79",
    'mammals': "101-106,269-299",
    'invertebrates': "107-117,327-329",
    'crustacea': "118-126",
    'seamammals': "147-150",
    'dogs': "151-268",
    'insects': "300-326",
    'allmammal': "101-106,151-299,147-150",
    'objects': "398-921,999",
    'food': "922-969",
    'landscapes': "970-980",
    'people': "981-983",
    'plants': "984-990",
    'fungi': "991-998"
    }

base = [ './Scripts/cnoise_fade.sh', './Temp', '224', '16', '60' ]
origfile = './Temp/base.jpg'
outdir = 'Output/DeepDraw/Metaclass/Gradient'
script = './dream.py'
iters = '200'
sigma = '.3'
model = "googlenet"

for c, target in METACLASS.iteritems():
    subprocess.call(base)
    a = [ script, "--model", model, "--target", target, "--basefile", c, "--iters", iters, "--sigma", sigma, origfile, outdir ]
    print ' '.join(a)
    subprocess.call(a)

