#!/usr/bin/env bash

dir="./Animations/Sinusoid"

convert -size 320x320 xc: +noise Random ${dir}/random.png

layer=$1

mkdir -p "${dir}/${layer}"

convert $dir/random.png  -channel G  -function Sinusoid 1,${i} \
        -virtual-pixel tile -blur 0x16 -auto-level \
        -separate $dir/gray.jpg

for i in 1.5 1.6 1.7 1.8 1.9 2.0 2.1 2.2 2.3 2.4 2.5 2.6 2.7 2.8 2.9 3.0; do
    convert ${dir}/gray.jpg -function Sinusoid ${i},90,0.25,0.65 ${dir}/gray_${i}.jpg
    convert ${dir}/gray_${i}.jpg -colorspace rgb -type truecolor ${dir}/base_${i}.jpg
    ./dream.py --dir ${dir}/${layer} --model places --iters 100 --layer $layer --basefile frame_${i}.jpg ${dir}/base_${i}.jpg
    
done

#rm Animations/gray4_*.jpg
#rm Animations/base4_*.jpg

