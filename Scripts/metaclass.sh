#!/usr/bin/env bash

# All MIT Places on random colours

iters="200"
sigma="0.33"

fish="0-7,390-397"
birds="8-24,80-100,127-146"
amphibians="25-32"
reptiles="33-68"
arachnids="69-79"
mammals="101-106,269-299"
invertebrates="107-117,327-329"
crustacea="118-126"
seamammals="147-150"
dogs="151-268"
insects="300-326"



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

