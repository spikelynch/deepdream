#!/usr/bin/env bash

# All Oxford flowers on random colours

amp=".2"
mean=".6"

for class in {0..19}
do
    ./dream.py --model flickr_style --iters 100 --target $class --sigma 0.35 --basefile Deepdraw/Flickr/class_$class  ./Input/me227.jpg
done
b
