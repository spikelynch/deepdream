#!/usr/bin/env bash

# Class and anticlass

model="caffenet"
amp=".3"
mean=".5"
iters="200"
sigma="0.33"
blur="0x12"
size="227"

for class in {0..999}; do
    convert -size ${size}x${size} xc: +noise Random Input/noise.png
    convert Input/noise.png  -channel G  -function Sinusoid 1,${i} \
            -virtual-pixel tile -blur $blur -auto-level \
            -separate Input/gray.jpg
    convert Input/gray.jpg -colorspace rgb -type truecolor Input/base_anti.jpg

#    ./dream.py --model $model --target $class --iters $iters --sigma $sigma --basefile ${class}_pos Input/base_anti.jpg Output/Deepdraw/Anti/Caffenet
    ./dream.py --model $model --target $class --weight -1 --iters $iters --sigma $sigma --basefile ${class}_neg_a Input/base_anti.jpg Output/Deepdraw/Anti/Caffenet
   
done

