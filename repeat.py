#!/usr/bin/env python2

import sys, os, os.path, random
import subprocess
import string

COLORFILE = '/opt/X11/share/X11/rgb.txt'
LAYERFILE = './Layers/layers_manga_high.txt'

script = './dream.py'
origfile = './working/bg1.jpg'
model = 'manga_tag'
const_layer = 'inception_4d/pool_proj'
iters = 20
octaves = 4 
repeats = 10
width = 512
height = 512
path = './Output/MangaTag'

fsin = 'Sinusoid {},90'

oc = [ './Scripts/background.sh', str(width) + 'x' + str(height), 'gray', '10', '34', 'radial-gradient:maroon-DarkGreen', '10%,75%', '10x10' ]

# oc = [ './Scripts/bg_ripple_tint.sh', '1024x768',  '', '50', 'radial-gradient:maroon-DarkGreen', 'gradient:black-white', '1%,99%', '0x23', origfile ]

#oc = [ './Scripts/sparse2.py', '--width', str(width), '--height', str(height), '--colours', '4', '--points', '8', '--blend', '50', '--algorithm', 'voronoi', '--blgorithm', 'shepards', '--blur', '0x8' ]

layers = [ 'conv6_1', 'conv6_2', 'conv6_3', 'conv6_4' ]
# with open(LAYERFILE, 'r') as lf:
#     for x in lf:
#         x = x.strip('\n')
#         fields = x.split()
#         layers.append(fields[0])

        
colors = []
with open(COLORFILE, 'r') as cf:
    for line in cf:
        if line[0] == '#':
            next
        parts = line[:-1].split()
        if len(parts) == 4:
            colors.append(parts[3])

def init_perlin(oc, n):
    oc[3] = str(random.randint(1, 10))
    oc[4] = str(random.randint(20, 80))
    g = random.choice(['gradient', 'radial-gradient'])
    gc = random.sample(colors, 2)
    oc[5] = '{}:{}-{}'.format(g, gc[0], gc[1])
    thisoc = oc[:]
    origfile = '{}/base{}.jpg'.format(path, n)
    thisoc.append(origfile)
    print(thisoc)
    subprocess.call(thisoc)
    return origfile


def init_voronoi(oc):
    oc[2] = str(random.randint(4, 10))
    oc[4] = str(random.randint(80, 180))
    oc[6] = str(random.randint(40, 60))
    thisoc = oc[:]
    thisoc.append('--vertical')
    if random.choice([True, False]):
        thisoc.append('--horizontal')
    origfile = '{}/base{}.jpg'.format(path, i)
    thisoc.append(origfile)
    print(thisoc)
    subprocess.call(thisoc)
    return origfile


def init_voronoi_grad(oc):
    oc[6] = str(random.randint(4, 10))
    oc[8] = str(random.randint(80, 180))
    oc[10] = str(random.randint(40, 60))
    thisoc = oc[:]
    if random.choice([True, False]):
        thisoc.append('--vertical')
    if random.choice([True, False]):
        thisoc.append('--horizontal')
    g = random.choice(['gradient', 'radial-gradient'])
    gc = random.sample(colors, 2)
    thisoc.append('--gradient')
    thisoc.append('{}:{}-{}'.format(g, gc[0], gc[1]))
    origfile = '{}/base{}.jpg'.format(path, i)
    thisoc.append(origfile)
    print(thisoc)
    subprocess.call(thisoc)
    return origfile


def init_ripple(oc):
    oc[2] = fsin.format(random.choice(range(2, 6)))
    oc[3] = str(random.choice(range(20, 80)))
    cs1 = random.sample(colors, 2)
    cs2 = random.sample(colors, 2)
    gr2 = random.choice(['radial-gradient', 'gradient'])
    oc[4] = '{}:{}-{}'.format('gradient', cs1[0], cs1[1])
    oc[5] = '{}:{}-{}'.format(gr2, cs2[0], cs2[1])
    oc[7] = '0x' + str(random.choice(range(5, 80)))
    origfile = '{}/base{}.jpg'.format(path, i)
    oc[8] = origfile
    print(oc)
    subprocess.call(oc)
    return origfile

            



for i in range(0, repeats):

    #init_voronoi(oc)
    #start = init_ripple(oc)
    #start = init_voronoi_grad(oc)
    start = init_perlin(oc, i)
    layer = random.choice(layers)
    basefile = 'image{}.jpg'.format(i)
    #model = random.choice([ "googlenet" ])
    a = [ script, "--model", model, "--layer", layer, "--iters", str(iters), "--octaves", str(octaves), "--basefile", basefile, start, path ]
    print ' '.join(a)
    subprocess.call(a)
