#!/usr/bin/env bash

dir="./Animations/Sinusoid/Long"

convert -size 1024x768 xc: +noise Random ${dir}/random.png

layer=$1

mkdir -p "${dir}/${layer}"


for i in `seq 0 20 359`; do
    convert $dir/random.png  -channel G  -function Sinusoid 1,${i} \
            -virtual-pixel tile -blur 0x24 -auto-level \
            -separate $dir/gray.jpg
    convert ${dir}/gray.jpg -function Sinusoid 3,90 ${dir}/gray_${i}.jpg
    convert ${dir}/gray_${i}.jpg -colorspace rgb -type truecolor ${dir}/base_${i}.jpg
    ./dream.py --dir ${dir}/${layer} --model googlenet --iters 40 --layer $layer --basefile frame_${i}.jpg ${dir}/base_${i}.jpg
    
done

#rm Animations/gray4_*.jpg
#rm Animations/base4_*.jpg

