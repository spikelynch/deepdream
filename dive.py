#!/usr/bin/env python2


import sys, os, os.path
import subprocess
import string

#origfile = 'Input/desaturated.jpg'
#origsize = '224x224'
origfile = 'Input/base.jpg'
origsize = '320x240'
outdir = 'Output'
script = './dream.py'
# model = 'manga_tag'
model = 'googlenet'
recipe = range(512)
iters = '2'
octaves = '5'
# dd_octaves = '../neuralgae/src/Control/Renderers/manga_quick_scale.json'
dd_octaves = '../neuralgae/src/Control/Renderers/googlenet_quick.json' 
frames = '12'
basefile = 'Dive8/google'
startframe = 0
zoom = '0.1'
rotate = '2' 



i = startframe
f = int(frames)
lastfile = origfile

for target in recipe:
    newfile = os.path.join(outdir, basefile + ('_f%d.jpg' % (i + f - 1)))
    a = [ script, "--model", model, "--target", str(target), "--basefile", basefile, "--deepdraw", dd_octaves, "--frames", frames, "--zoom", zoom, "--rotate", rotate, "--initial", str(i), origfile, outdir ]
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

