#!/usr/bin/env bash


model=googlenet
dir="./Animations/Googlenet"
working="$dir/working"
layer=$1
lastframe=""
firstframe=""
iters="2"
glide="-5+7 -background grey"

mkdir -p "${dir}/${layer}"

convert -size 640x480 xc:grey ${working}/grey.png
convert ${working}/grey.png -colorspace rgb -type truecolor ${working}/base.jpg


#lasti="99"

for i in `seq 0 1 720`; do
    # blend the last frame, if it exists
    echo ${i} ${lastframe}
    if [ -n "$lastframe" ]; then
        convert ${lastframe} -page ${glide} -flatten ${working}/base.jpg
    fi
       
    ./dream.py --dir "${dir}/${layer}" --model $model --iters $iters --layer $layer --basefile frame_${i}.jpg ${working}/base.jpg
    lastframe="${dir}/${layer}/frame_${i}.jpg_f0.jpg"
    if [ -n "${firstframe}" ]; then
        firstframe="${lastframe}"
    fi
done

#rm ${dir}/gray4_*.jpg
#rm ${dir}/base4_*.jpg

