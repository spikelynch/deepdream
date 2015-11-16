#!/usr/bin/env bash


model=$1
dir="./Animations/$model"
target=$2
layer=$2
working="$dir/working"

lastframe=""
firstframe=""
iters="20"
blend="15"
lblend="10"
amp=".2"
mean=".7"

mkdir -p "${dir}/${target}"
mkdir -p "${dir}/working"

convert -size 227x227 xc: +noise Random ${working}/random.png

echo "Animation frames output to ${dir}/${target}"


lasti="345"

for i in `seq 0 15 359`; do
    convert ${working}/random.png  -channel R  -function Sinusoid 1,${i} \
            -virtual-pixel tile -blur 0x16 -auto-level \
            -separate ${working}/red.jpg
    convert ${working}/random.png  -channel G  -function Sinusoid 1,${i} \
            -virtual-pixel tile -blur 0x16 -auto-level \
            -separate ${working}/green.jpg
    convert ${working}/random.png  -channel B  -function Sinusoid 1,${i} \
            -virtual-pixel tile -blur 0x16 -auto-level \
            -separate ${working}/blue.jpg
    convert ${working}/red.jpg -function Sinusoid 1,0,${amp},${mean} ${working}/red2.jpg
    convert ${working}/blue.jpg -function Sinusoid 1,0,${amp},${mean} ${working}/blue2.jpg
    convert ${working}/green.jpg -function Sinusoid 1,0,${amp},${mean} ${working}/green2.jpg

    convert ${working}/red2.jpg ${working}/green2.jpg ${working}/blue2.jpg -combine ${working}/base_${i}.jpg
    # blend the last frame, if it exists
    if [ -n "$lastframe" ]; then
        composite -blend ${blend} ${lastframe} ${working}/base_${i}.jpg ${working}/blended_${i}.jpg
        if [ $i == $lasti ]; then
            composite -blend ${lblend} ${firstframe} ${working}/blended_${i}.jpg ${working}/blended_${i}.jpg
        fi
    else
        cp ${working}/base_${i}.jpg ${working}/blended_${i}.jpg
    fi
       
    ./dream.py --dir "${dir}/${target}" --model $model --iters $iters --layer $target --sigma .25 --basefile frame_${i} ${working}/blended_${i}.jpg
    lastframe="${dir}/${target}/frame_${i}.jpg"
    echo "lastframe = $lastframe"
    if [ -n "${firstframe}" ]; then
        firstframe="${lastframe}"
    fi
done

