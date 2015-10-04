#!/usr/bin/env bash

# All Oxford flowers on random colours

amp=".25"
mean=".5"

for class in {12..999}
do
    # convert -size 227x227 xc: +noise Random Input/noise.png
    # convert Input/noise.png  -channel R  -function Sinusoid 1,0 \
    #         -virtual-pixel tile -blur 0x16 -auto-level \
    #         -separate Input/red.jpg
    # convert Input/noise.png  -channel G  -function Sinusoid 1,0 \
    #         -virtual-pixel tile -blur 0x16 -auto-level \
    #         -separate Input/green.jpg
    # convert Input/noise.png  -channel B  -function Sinusoid 1,0 \
    #         -virtual-pixel tile -blur 0x16 -auto-level \
    #         -separate Input/blue.jpg
    # convert Input/red.jpg -function Sinusoid 1,0,${amp},${mean} Input/red2.jpg
    # convert Input/blue.jpg -function Sinusoid 1,0,${amp},${mean} Input/blue2.jpg
    # convert Input/green.jpg -function Sinusoid 1,0,${amp},${mean} Input/green2.jpg

    # convert Input/red2.jpg Input/green2.jpg Input/blue2.jpg -combine Input/base_${class}.jpg

    ./dream.py --model googlenet --iters 100 --target $class --sigma 0.35 --basefile Deepdraw/GoogleNet/class_$class  ./Input/me224.jpg
   
done
b
