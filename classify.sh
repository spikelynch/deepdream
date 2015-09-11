#!/usr/bin/env bash

# All places on random colours

# todo - use the looping noise described http://www.imagemagick.org/Usage/canvas/#random_flux

for class in {0..205}
do
    convert -size 224x224 xc: +noise Random Input/noise.png
    convert Input/noise.png -virtual-pixel tile -blur 0x12 -colorspace Gray -auto-level Input/graynoise.jpg
    convert Input/graynoise.jpg -colorspace rgb -type truecolor Input/noise.jpg
    ./dream.py --model places --iters 600 --target $class --sigma 0.35 --basefile Deepdraw/Plasma/class600_$class  ./Input/noise.jpg
done
b
