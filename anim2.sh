#!/usr/bin/env bash

convert -size 768x512 xc: +noise Random ./Animations/random.png

dir="./Animations/Googlenet"
model=googlenet
layer=$1

mkdir -p "${dir}/${layer}"

for i in `seq 0 5 359`; do
    convert ./Animations/random.png  -channel G  -function Sinusoid 1,${i} \
            -virtual-pixel tile -blur 0x24 -auto-level \
            -separate ${dir}/gray4_${i}.jpg
    #convert Animations/gray4_${i}.jpg -function Sinusoid 4,90 Animations/gray4b_${i}.jpg
    convert ${dir}/gray4_${i}.jpg -colorspace rgb -type truecolor ${dir}/base4_${i}.jpg
    ./dream.py --dir "${dir}/${layer}" --model $model --iters 40 --layer $layer --basefile frame_${i}.jpg ${dir}/base4_${i}.jpg

    
done

rm ${dir}/gray4_*.jpg
rm ${dir}/base4_*.jpg

