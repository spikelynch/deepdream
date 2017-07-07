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
model = 'manga_tag'
# model = 'googlenet'
recipe = range(512)
iters = '2'
octaves = '5'
dd_octaves = '../neuralgae/src/Control/Renderers/manga_stable.json'
#dd_octaves = '../neuralgae/src/Control/Renderers/googlenet_quick.json' 
frames = '2'
basefile = 'Dive9/manga'
startframe = 0
zoom = '0.01'

nsteps = 5
nbetween = 5


def do_sequence(origfile, startf, nframes, targets):
    a = [ script,  "--model", model, "--target", targets, "--basefile", basefile, "--deepdraw", dd_octaves, "--frames", str(nframes), "--zoom", zoom, "--initial", str(startf), origfile, outdir ]
    print ' '.join(a)
    subprocess.call(a)
    newfile = os.path.join(outdir, basefile + ('_f%d.jpg' % (startf + nframes - 1)))
    if os.path.isfile(newfile):
        resizefile = newfile + ".resize.jpg"
        subprocess.call(['convert', '-resize', origsize, newfile, resizefile])
        endfile = resizefile
        startf += nframes
    else:
        print "using lastfile {}".format(lastfile)
        endfile = lastfile
    return endfile, startf



i = startframe
f = int(frames)
lastfile = origfile


steps = [ (n + 1) * 1.0 / nsteps for n in range(nsteps) ]

print steps

origfile, i = do_sequence(origfile, i, f * nbetween, '{{ "{}": 1 }}'.format(recipe[0]))
lasttarget = recipe[0]

for target in recipe[1:]:
    for step in steps:
        t = '{{ "{}":{}, "{}":{} }}'.format(target, step, lasttarget, 1 - step)
        print t
        origfile, i = do_sequence(origfile, i, f, t)
    lasttarget = target
    origfile, i = do_sequence(origfile, i, f * nbetween, '{{ "{}": 1 }}'.format(target))

