#!/usr/bin/env python2

import sys, os, os.path, json
import subprocess
import string
import random

# for a directory of 224x224 jpgs, use classify to extract a feature
# vector, and then generate one or more images from it

COLORFILE = '/opt/X11/share/X11/rgb.txt'
origfile = './Input/lite.jpg'
indir = './Manga/Features'
jsondir = './Output/MangaFeatures/Octaves'
outdir = './Output/MangaFeatures'
frames = './Output/MangaFeatures/Frames'
#octaves = "feature_g3m_s4a.json"
#octaves = [ "feature_e{}.json".format(x) for x in [1, 2, 3, 4] ]
octaves = [
    'feature_exa.json',
    'features_exb.json',
    'o_pikachu_6.json',
    'o_pikachu_9.json',
    'o_purple_5.json',
    'o_purple_6.json',
    'o_purple_7.json',
    'o_purple_8.json'
    ]
repeats = 1; 
dream_script = './dream.py'
classify_script = '../neuralgae/src/classify.py'
remote = '../neuralgae/src/remote.json'
model = 'manga'

bg = [ './Scripts/background.sh', '224x224', 'color', '10', '50', 'gradient:white-gray90', '5%,95%', '0x4', origfile ]

def is_jpg(f):
    return os.path.isfile(f) and f[-4:] == '.jpg'


def random_octave(fn):
    o = {
        "layer": "encode1neuron",
        "iter_n": 200,
        "start_sigma": random.uniform(0.1, 1.0),
        "end_sigma": random.uniform(0.1, 1.0),
        "start_step_size": random.uniform(3, 10),
        "end_step_size":random.uniform(3, 10)
    }
    os = [ o ]
    with open(fn, "w") as jf:
        jf.write(json.dumps(os, indent=4))


ff = [ f for f in os.listdir(indir) if is_jpg(os.path.join(indir, f)) ]

print ff




# for f in ff:
#     fn = f.split('.')[0]
#     origjpg = os.path.join(indir, f)
#     c = [ classify_script, '-m', model, '-r', remote, origjpg ]
#     featurejs = os.path.join(indir, "%s.json" % ( fn ))
#     print "Extracting features from %s" % ( origjpg )
#     with open(featurejs, 'w') as j:
#         subprocess.call(c, stdout=j)

for f in ff:
    fn = f.split('.')[0]
    for o in octaves:
        oname = o.split('.')[0]
        subprocess.call(bg)
        origfile = bg[8]
        #oname = "o_%s_%d" % ( fn, on )
        ofile = os.path.join(jsondir, o)
        #random_octave(ofile)
        basefile = "e_%s_%s.jpg" % ( fn, oname )
        featurejs = os.path.join(indir, "%s.json" % ( fn ))
        a = [ dream_script, "--model", model, "--target", featurejs, "--basefile", basefile, "--deepdraw", ofile, "--nojson", origfile,  outdir ]
        print "Rendering features from %s" % ( featurejs )
        subprocess.call(a)
