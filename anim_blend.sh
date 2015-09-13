#!/usr/bin/env bash


model=googlenet
dir="./Animations/Googlenet"
working="$dir/working"
layer=$1
lastframe=""
firstframe=""
blend="20"
mkdir -p "${dir}/${layer}"

convert -size 1024x768 xc: +noise Random ${working}/random.png

lasti="340"

for i in `seq 0 5 359`; do
    convert ${working}/random.png  -channel G  -function Sinusoid 1,${i} \
            -virtual-pixel tile -blur 0x12 -auto-level \
            -separate ${working}/gray_${i}.jpg
    convert ${working}/gray_${i}.jpg -colorspace rgb -type truecolor ${working}/base_${i}.jpg
    # blend the last frame, if it exists
    if [ -n "$lastframe" ]; then
        composite -blend ${blend} ${lastframe} ${working}/base_${i}.jpg ${working}/blended_${i}.jpg
    else
        cp ${working}/base_${i}.jpg ${working}/blended_${i}.jpg
    fi
       
    ./dream.py --dir "${dir}/${layer}" --model $model --iters 40 --layer $layer --basefile frame_${i}.jpg ${working}/blended_${i}.jpg
    lastframe="${dir}/${layer}/frame_${i}.jpg_f0.jpg"
    if [ -n "${firstframe}" ]; then
        firstframe="${lastframe}"
    fi
done

#rm ${dir}/gray4_*.jpg
#rm ${dir}/base4_*.jpg

