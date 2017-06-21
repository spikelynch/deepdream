#!/usr/bin/env bash

outfile=$1
working="./"

convert -size 224x224 xc: +noise Random ${working}/random.png

convert ${working}/random.png  -channel G  \
        -virtual-pixel tile -blur 0x10  \
        -separate ${working}/gray.jpg

convert ${working}/gray.jpg -function Sinusoid 2,90 ${working}/gray2.jpg

convert ${working}/gray2.jpg -colorspace rgb -type truecolor ${working}/$outfile
