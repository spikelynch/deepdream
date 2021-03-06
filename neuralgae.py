#!/usr/bin/env python

import subprocess
import os.path
from imagenet import ImageNet
import json
import random
import neuralgae

OUTDIR = './Neuralgae/Twitter1'

#"Good_sequence"
NSTART = 8

NTWEEN = 100
NSAMPLE = 8
SIZE = "224"
SCALE = "8"
BLEND = "75"

# NSTART = 12
# NTWEEN = 60
# NSAMPLE = 12
# SIZE = "224"
# SCALE = "8"
# BLEND = "90"

outfile = os.path.join(OUTDIR, "twitter1.txt")

start_targets = random.sample(range(0, 1000), NSTART)

conffile = os.path.join(OUTDIR, 'conf0.json')

neuralgia.write_config(start_targets, conffile)

subprocess.call(["./neuralgae_draw.sh", OUTDIR, 'image0', conffile, SIZE, SCALE, BLEND])

#lastimage = "./Neuralgia/Chapter5/image199.jpg"
lastimage = os.path.join(OUTDIR, 'image0.jpg')

imagen = ImageNet("./Classes/classes.txt")

classes = ', '.join([imagen.name(c) for c in start_targets])

with open(outfile, 'w') as f:
    f.write("%s: %s\n" % (lastimage, classes))




for i in range(0,20):
    jsonfile = os.path.join(OUTDIR, ("conf%d.json" % i))
    subprocess.call(["./classify.py", str(NTWEEN), str(NSAMPLE), lastimage, jsonfile])
    subprocess.call(["./neuralgae_draw.sh", OUTDIR, "image%d" % i, jsonfile, SIZE, SCALE, BLEND])
    lastimage = os.path.join(OUTDIR, ("image%d.jpg" % i))
    t = neuralgia.read_config(jsonfile)
    if t:
        print t
        classes = ', '.join([imagen.name(c) for c in t])
    else:
        classes = ""
    with open(outfile, 'a') as f:
        f.write("%s: %s\n" % (lastimage, classes))
