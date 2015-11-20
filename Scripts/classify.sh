#!/usr/bin/env bash

# All MIT Places on random colours

amp=".5"
mean=".5"
iters="200"
sigma="0.33"
blur="0x18"

for class in {11..204}
do
    convert -size 224x224 xc: +noise Random Input/noise.png
    convert Input/noise.png  -channel R  -function Sinusoid 1,0,${amp},${mean} \
            -virtual-pixel tile -blur $blur -auto-level  \
            -separate Input/red.jpg
    convert Input/noise.png  -channel G  -function Sinusoid 1,0,${amp},${mean} \
            -virtual-pixel tile -blur $blur -auto-level \
            -separate Input/green.jpg
    convert Input/noise.png  -channel B  -function Sinusoid 1,0,${amp},${mean} \
            -virtual-pixel tile -blur $blur -auto-level \
            -separate Input/blue.jpg
    #convert Input/red.jpg -function Sinusoid .5,0,${amp},${mean} Input/red2.jpg
    #convert Input/blue.jpg -function Sinusoid .5,0,${amp},${mean} Input/blue2.jpg
    #convert Input/green.jpg -function Sinusoid .5,0,${amp},${mean} Input/green2.jpg

    convert Input/red.jpg Input/green.jpg Input/blue.jpg -combine Input/base_${class}.jpg

    ./dream.py --model places --target $class --iters $iters --sigma $sigma --basefile places2_${class} Input/base_${class}.jpg Places2
   
done

