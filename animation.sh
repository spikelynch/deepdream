#!/usr/bin/env bash

convert -size 224x224 xc: +noise Random ./Animations/random.png

for i in `seq 0 15 359`; do
    convert ./Animations/random.png  -channel G  -function Sinusoid 1,${i} \
            -virtual-pixel tile -blur 0x8 -auto-level \
            -separate ./Animations/gray_${i}.jpg
    convert Animations/gray_${i}.jpg -colorspace rgb -type truecolor Animations/base_${i}.jpg
    ./dream.py --dir Animations --model places --iters 600 --target 0 --sigma 0.35 --basefile anim_${i}  ./Animations/base_${i}.jpg
    
done

