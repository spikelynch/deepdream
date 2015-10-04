#!/usr/bin/env bash


model=googlenet
dir="./Animations/Googlenet"
working="$dir/working"
layer=$1
lastframe=""
firstframe=""
iters="35"
blend="15"
lblend="10"

mkdir -p "${dir}/${layer}"

convert -size 640x480 xc: +noise Random ${working}/random.png

lasti="345"

for i in `seq 0 15 359`; do
    convert ${working}/random.png  -channel G  -function Sinusoid 1,${i} \
            -virtual-pixel tile -blur 0x16 -auto-level \
            -separate ${working}/gray_${i}.jpg
    convert ${working}/gray_${i}.jpg -colorspace rgb -type truecolor ${working}/base_${i}.jpg
    # blend the last frame, if it exists
    if [ -n "$lastframe" ]; then
        composite -blend ${blend} ${lastframe} ${working}/base_${i}.jpg ${working}/blended_${i}.jpg
        if [ $i == $lasti ]; then
            composite -blend ${lblend} ${firstframe} ${working}/blended_${i}.jpg ${working}/blended_${i}.jpg
        fi
    else
        cp ${working}/base_${i}.jpg ${working}/blended_${i}.jpg
    fi
       
    ./dream.py --dir "${dir}/${layer}" --model $model --iters $iters --layer $layer --basefile frame_${i}.jpg ${working}/blended_${i}.jpg
    lastframe="${dir}/${layer}/frame_${i}.jpg_f0.jpg"
    if [ -n "${firstframe}" ]; then
        firstframe="${lastframe}"
    fi
done

#rm ${dir}/gray4_*.jpg
#rm ${dir}/base4_*.jpg
