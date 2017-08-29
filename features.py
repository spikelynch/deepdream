#!/usr/bin/env python2

import sys, os, os.path, json
import subprocess
import string
import random

# for a directory of 224x224 jpgs, use classify to extract a feature
# vector, and then generate one or more images from it

origfile = './Input/lite.jpg'
indir = './Input/Features'
octavedir = './Features'
jsondir = './Output/Features4/Octaves'
outdir = './Output/Features4'
#frames = './Output/MangaFeatures/Frames'
#octaves = "feature_g3m_s4a.json"
#octaves = [ "feature_e{}.json".format(x) for x in [1, 2, 3, 4] ]
octaves = [
    'beach_0.json',
    'bird_10.json',
    'einstein_7.json',
    'fall_2.json',
    'hyperion_7.json',
    'fountain_1.json',
    'latham_5.json',
    'moonhoax_4.json',
    'pasquino_10.json'
   ]
repeats = 12; 
dream_script = './dream.py'
classify_script = '../neuralgae/src/classify.py'
model = 'manga'

bg = [ './Scripts/background.sh', '512x384', 'gray', '10', '50', 'gradient:white-gray50', '5%,95%', '0x12', origfile ]

def is_jpg(f):
    return os.path.isfile(f) and f[-4:] == '.jpg'


def random_octave(fn):
    o = {
        "layer": "encode1neuron",
        "iter_n": 4000,
        "start_sigma": random.uniform(0.3, 1.0),
        "end_sigma": random.uniform(0.3, 1.0),
        "start_step_size": random.uniform(1.0, 7.0),
        "end_step_size":random.uniform(1.0, 7.0)
    }
    os = [ o ]
    with open(fn, "w") as jf:
        jf.write(json.dumps(os, indent=4))


ff = [ f for f in os.listdir(indir) if is_jpg(os.path.join(indir, f)) ]

print ff




for f in ff:
    fn = f.split('.')[0]
    origjpg = os.path.join(indir, f)
    c = [ classify_script, '-m', model, '-g', origjpg ]
    featurejs = os.path.join(indir, "%s.json" % ( fn ))
    if os.path.isfile(featurejs):
        print "Feature file %s exists" % ( featurejs )
    else:
        print "Extracting features from %s" % ( origjpg )
        with open(featurejs, 'w') as j:
            subprocess.call(c, stdout=j)

for f in ff:
    fn = f.split('.')[0]
    for ofile in octaves:
        #subprocess.call(bg)
        #origfile = bg[8]
        #oname = "o_%s_%d" % ( fn, on )
        #ofile = os.path.join(jsondir, oname + ".json")
        #random_octave(ofile)
        opath = os.path.join(octavedir, ofile)
        origfile = os.path.join(indir, "%s.jpg" % ( fn ))
        basefile = "fn_%s_%s.jpg" % ( fn, ofile )
        featurejs = os.path.join(indir, "%s.json" % ( fn ))
        a = [ dream_script, "--gpu", "--model", model, "--target", featurejs, "--basefile", basefile, "--deepdraw", opath, "--nojson", origfile,  outdir ]
        print "Rendering features from %s" % ( featurejs )
        print a
        subprocess.call(a)
