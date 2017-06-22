#!/usr/bin/env python2

import sys, os, os.path
import subprocess
import string

origfile = 'Input/bg.jpg'
origsize = '224x224'
outdir = 'Output'
script = './dream.py'
model = 'manga_tag'
recipe = range(5)
iters = '2'
octaves = '5'
dd_octaves = '../neuralgae/src/Control/Renderers/manga_big_grad.json'
frames = '48'
basefile = 'Dive/manga'
startframe = 0
zoom = '0.05'



i = startframe
f = int(frames)
lastfile = origfile

for target in recipe:
    newfile = os.path.join(outdir, basefile + ('_f%d.jpg' % (i + f - 1)))
    a = [ script, "--gpu", "--model", model, "--target", str(target), "--basefile", basefile, "--deepdraw", dd_octaves, "--frames", frames, "--zoom", zoom, "--initial", str(i), origfile, outdir ]
    print ' '.join(a)
    subprocess.call(a)
    sys.exit()
    if os.path.isfile(newfile):
        rfile = newfile + '.resize.jpg'
        print "found newfile, resizing to {}".format(rfile)
        r = [ 'convert', '-resize', origsize, newfile, rfile  ]
        subprocess.call(r)
        origfile = rfile
        i += f
    else:
        print "using lastfile {}".format(lastfile)
        origfile = lastfile

