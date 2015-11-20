#!/usr/bin/env bash


model=googlenet
dir="./Animations/Googlenet"
working="$dir/working"
layer=$1
lastframe=""
firstframe=""
iters="20"
blend="25"
lblend="10"
amp=".15"
mean=".6"

mkdir -p "${dir}/${layer}"

convert -size 320x320 xc:grey ${working}/grey.png
convert ${working}/grey.png -colorspace rgb -type truecolor ${working}/grey.jpg


lasti="99"

for i in `seq 0 1 100`; do
    # blend the last frame, if it exists
    echo ${i} ${lastframe}
    if [ -n "$lastframe" ]; then
        composite -blend ${blend} ${lastframe} ${working}/grey.jpg ${working}/blended_${i}.jpg
        if [ $i == $lasti ]; then
            composite -blend ${lblend} ${firstframe} ${working}/blended_${i}.jpg ${working}/blended_${i}.jpg
        fi
    else
        cp ${working}/grey.jpg ${working}/blended_${i}.jpg
    fi
       
    ./dream.py --dir "${dir}/${layer}" --model $model --iters $iters --layer $layer --basefile frame_${i}.jpg ${working}/blended_${i}.jpg
    lastframe="${dir}/${layer}/frame_${i}.jpg_f0.jpg"
    if [ -n "${firstframe}" ]; then
        firstframe="${lastframe}"
    fi
done

#rm ${dir}/gray4_*.jpg
#rm ${dir}/base4_*.jpg

