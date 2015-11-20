#!/usr/bin/env bash

# Randomised deepdraws

size="224"
model="places"
working="Output/Random/working"

mkdir -p $working


lasti="350"

for i in {1..20}; do
    convert -size ${size}x${size} xc: +noise Random ${working}/random.png
    convert ${working}/random.png  -channel G  -function Sinusoid 1,0 \
            -virtual-pixel tile -blur 0x16 -auto-level \
            -separate ${working}/gray.jpg
    convert ${working}/gray.jpg -colorspace rgb -type truecolor ${working}/base.jpg
    ./dream.py --model $model --target randomise --iters 400 --sigma .33 --basefile case_${i} ${working}/base.jpg Output/Random/   
done
