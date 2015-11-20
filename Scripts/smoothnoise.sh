#!/usr/bin/env bash

outfile=$1
working="./"

convert -size 224x224 xc: +noise Random ${working}/random.png

convert ${working}/random.png  -channel G  -function Sinusoid 1,0 \
        -virtual-pixel tile -blur 0x16 -auto-level \
        -separate ${working}/gray.jpg
convert ${working}/gray.jpg -colorspace rgb -type truecolor ${working}/$outfile
