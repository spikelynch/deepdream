#!/usr/bin/env python2

import sys, os, os.path
import subprocess
import string

origfile = 'Input/desaturated.jpg'
origsize = '224x224'
outdir = 'Output'
script = './dream.py'
model = 'manga_tag'
recipe = range(512)
iters = '2'
octaves = '5'
dd_octaves = '../neuralgae/src/Control/Renderers/manga_quick_scale.json'
frames = '2'
basefile = 'Dive7/manga'
startframe = 0
zoom = '0.05'



i = startframe
f = int(frames)
lastfile = origfile

for target in recipe:
    newfile = os.path.join(outdir, basefile + ('_f%d.jpg' % (i + f - 1)))
    a = [ script, "--model", model, "--target", str(target), "--basefile", basefile, "--deepdraw", dd_octaves, "--frames", frames, "--zoom", zoom, "--initial", str(i), origfile, outdir ]
    print ' '.join(a)
    subprocess.call(a)
    if os.path.isfile(newfile):
        resizefile = newfile + ".resize.jpg"
        subprocess.call(['convert', '-resize', origsize, newfile, resizefile])
        origfile = resizefile
        i += f
    else:
        print "using lastfile {}".format(lastfile)
        origfile = lastfile

