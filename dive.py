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
#dd_octaves = '../neuralgae/src/Control/Renderers/manga_dive_grad.json'
dd_octaves = '../neuralgae/src/Control/Renderers/googlenet_quick.json' 
frames = '2'
basefile = 'Dive9/google'
startframe = 0
zoom = '0.01'


def do_sequence(origfile, startf, targets):
    a = [ script,  "--model", model, "--target", targets, "--basefile", basefile, "--deepdraw", dd_octaves, "--frames", frames, "--zoom", zoom, "--initial", str(startf), origfile, outdir ]
    print ' '.join(a)
    subprocess.call(a)
    f = int(frames)
    newfile = os.path.join(outdir, basefile + ('_f%d.jpg' % (startf + f - 1)))
    if os.path.isfile(newfile):
        resizefile = newfile + ".resize.jpg"
        subprocess.call(['convert', '-resize', origsize, newfile, resizefile])
        endfile = resizefile
        startf += f
    else:
        print "using lastfile {}".format(lastfile)
        endfile = lastfile
    return endfile, startf



i = startframe
f = int(frames)
lastfile = origfile

lasttarget = recipe[0]


for target in recipe[1:]:
    for step in [ 0, .25, .5, .75 ]:
        t = '{{ "{}":{}, "{}":{} }}'.format(target, step, lasttarget, 1 - step)
        print t
        origfile, i = do_sequence(origfile, i, t)
        lasttarget = target

