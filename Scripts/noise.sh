#!/usr/bin/env bash


convert -size 224x224 xc: +noise Random noise.png
convert noise.png -virtual-pixel tile -blur 0x12 -colorspace Gray -auto-level graynoise.jpg
convert graynoise.jpg -colorspace rgb -type truecolor noise.jpg
