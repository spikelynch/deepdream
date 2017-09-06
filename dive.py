#!/usr/bin/env python2


import sys, os, os.path
import subprocess
import string



origfile = 'Input/start.jpg'
origsize = '512x384'

bgparams = [ 'Scripts/background.sh', origsize, "gray", "8", "70", "gradient:gray90-gray10", "10%,90%", "0x8" ]

outdir = 'Manga/Dive3'
script = './dream.py'
model = 'manga_tag'
# model = 'googlenet'
recipe = range(512, 1023) 
iters = '2'
octaves = '5'
dd_octaves = 'Manga/manga_dive_3.json'
frames = '12'
basefile = 'manga'
startframe = 1 
zoom = '0.001' 
glide = None

nsteps = 8 
nbetween = 4

def do_start():
    a = bgparams
    a.append(origfile)
    subprocess.call(a)

def do_sequence(origfile, startf, nframes, targets):
    a = [ script, "--gpu", "--model", model, "--target", targets, "--basefile", basefile, "--deepdraw", dd_octaves, "--frames", str(nframes), "--zoom", zoom, "--initial", str(startf), origfile, outdir ]
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

do_start()

steps = [ (n + 1) * 1.0 / nsteps for n in range(nsteps) ]

print steps

if startframe == 0:
    origfile, i = do_sequence(origfile, i, f * nbetween, '{{ "{}": 1 }}'.format(recipe[0]))

lasttarget = recipe[0]

for target in recipe[1:]:
    for step in steps:
        t = '{{ "{}":{}, "{}":{} }}'.format(target, step, lasttarget, 1 - step)
        print t
        origfile, i = do_sequence(origfile, i, f, t)
    lasttarget = target
    origfile, i = do_sequence(origfile, i, f * nbetween, '{{ "{}": 1 }}'.format(target))

