#!/usr/bin/env python

import random, subprocess, argparse

COLORFILE = '/opt/X11/share/X11/rgb.txt'
N = 7
CN = 4
XMAX = 1024
YMAX = 768

def randpt(c):
    x = random.randint(0, XMAX - 1)
    y = random.randint(0, YMAX - 1)
    return "{},{} {}".format(x, y, c)

colors = []
with open(COLORFILE, 'r') as cf:
    for line in cf:
        if line[0] == '#':
            next
        parts = line[:-1].split()
        if len(parts) == 4:
            colors.append(parts[3])

parser = argparse.ArgumentParser(description='Generate a voronoi map')
parser.add_argument('--algorithm', type=str, default='Voronoi', help='sparse algorithm')
parser.add_argument('--colours', type=int, default=N, help='number of colours')
parser.add_argument('--points', type=int, default=CN, help='sets of C points')
parser.add_argument('--blend', type=int, default=0, help='overlay a shadow gradiend')
parser.add_argument('--blur', type=str, help='blur')
parser.add_argument('output', type=str, help='output file')

args = parser.parse_args()

            
c4 = random.sample(colors, args.colours)

points = "'" + ' '.join([ randpt(c) for c in c4 * args.points ]) + "'"

im = [ 'convert', '-size', '{}x{}'.format(XMAX, YMAX), 'xc:', '-sparse-color', args.algorithm, points, args.output ]

cmd = ' '.join(im)
print(cmd)


rv = subprocess.run(cmd, shell=True)

if args.blend:
    fade = [ 'convert', '-size', '{}x{}'.format(XMAX, YMAX), 'gradient:white-black', './fade.jpg' ]
    rv = subprocess.run(' '.join(fade), shell=True)
    blend = [ 'composite', '-blend', str(args.blend), './fade.jpg', args.output, args.output ]
    rv = subprocess.run(' '.join(blend), shell=True)

if args.blur:
    blur = [ 'convert', '-blur', args.blur, args.output, args.output ]
    rv = subprocess.run(' '.join(blur), shell=True)
