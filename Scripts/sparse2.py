#!/usr/bin/env python2

import random, subprocess, argparse, itertools

COLORFILE = '/shared/homes/960700/neuralgae/src/rgb.txt'
NC = 4
NP = 20
XMAX = 1024
YMAX = 768
GEOMETRY = '{}x{}'.format(XMAX, YMAX)

def randpt():
    x = random.randint(0, XMAX - 1)
    y = random.randint(0, YMAX - 1)
    return (x, y)

def pt(x, y, c):
    return "{},{} {}".format(x, y, c)


def makepts(cs, n, v, h):
    pts = []
    for c in itertools.cycle(cs):
        x, y = randpt()
        pts.append(pt(x, y, c)) 
        if v:
            pts.append(pt(XMAX - x, y, c))
            if h:
                pts.append(pt(XMAX - x, YMAX - y, c))
        if h:
            pts.append(pt(x, YMAX - y, c))
        if len(pts) >= n:
            break
    return "'" + ' '.join(pts) + "'"


def sparse(algorithm, points, filename):
    im = [ 'convert', '-size', '{}x{}'.format(XMAX, YMAX), 'xc:', '-sparse-color', algorithm, points, filename ]
    cmd = ' '.join(im)
    print(cmd)
    rv = subprocess.call(cmd, shell=True)
    return (not rv)




parser = argparse.ArgumentParser(description='Generate a voronoi map')
parser.add_argument('-x', '--width', type=int, default=XMAX, help="canvas width")
parser.add_argument('-y', '--height', type=int, default=YMAX, help="canvas height")
parser.add_argument('-a', '--algorithm', type=str, default='Voronoi', help='sparse algorithm 1')
parser.add_argument('-b', '--blgorithm', type=str, default=None, help='sparse algorithm 2')
parser.add_argument('-c', '--colours', type=int, default=NC, help='number of colours')
parser.add_argument('-e', '--monochrome', action='store_true', help='grayscale only')
parser.add_argument('-n', '--points', type=int, default=NP, help='number of points')
parser.add_argument('-f', '--blend', type=int, default=50, help='blend')
parser.add_argument('-u', '--blur', type=str, help='blur')
parser.add_argument('-v', '--vertical', action='store_true', help="vertical symmetry")
parser.add_argument('-m', '--horizontal', action='store_true', help="horizontal symmetry")
parser.add_argument('-g', '--gradient', type=str, default=None, help='overlay gradient')
parser.add_argument('-l', '--list', type=str, default=None, help="comma-separated list of colours")
parser.add_argument('output', type=str, help='output file')

args = parser.parse_args()

XMAX = args.width
YMAX = args.height

colors = []

if args.list:
    colors = args.list.split(',')
else:
    with open(COLORFILE, 'r') as cf:
        for line in cf:
            if line[0] == '#':
                next
            parts = line[:-1].split()
            if len(parts) == 4:
                if args.monochrome:
                    if parts[0] == parts[1] and parts[1] == parts[2]:
                        colors.append(parts[3])
                else:
                    colors.append(parts[3])


geometry = "{}x{}".format(XMAX, YMAX)
cs = random.sample(colors, args.colours)

points = makepts(cs, args.points, args.vertical, args.horizontal)


if args.blgorithm:
    sparse(args.algorithm, points, 'a1.jpg')
    sparse(args.blgorithm, points, 'b1.jpg')
    merge = [ 'composite', '-blend', str(args.blend), 'a1.jpg', 'b1.jpg', args.output]
    rv = subprocess.call(' '.join(merge), shell=True)
else:
    sparse(args.algorithm, points, args.output)

if args.gradient:
    grad = [ 'convert', '-size', geometry, args.gradient, 'fade.jpg' ]
    print(grad)
    subprocess.call(' '.join(grad), shell=True)
    merge = [ 'composite', '-blend', '50', 'fade.jpg', args.output, args.output ]
    subprocess.call(' '.join(merge), shell=True)


    
if args.blur:
    blur = [ 'convert', '-blur', args.blur, args.output, args.output ]
    rv = subprocess.call(' '.join(blur), shell=True)

ensure_col = [ 'convert', args.output, '-colorspace', 'rgb', '-type', 'truecolor', args.output ]
rv = subprocess.call(' '.join(ensure_col), shell=True)


    
