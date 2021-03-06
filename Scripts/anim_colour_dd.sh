#!/usr/bin/env bash


model=caffenet
dir="./Animations/CaffenetDD"
working="$dir/working"
lastframe=""
firstframe=""
iters="60"
blend="10"
lblend="10"
amp=".15"
mean=".7"
target="139"

mkdir -p "${dir}/"

convert -size 224x224 xc: +noise Random ${working}/random.png

lasti="352"

for i in `seq 0 8 359`; do
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
       
    ./dream.py --dir "${dir}" --model $model --iters $iters --target $target --basefile frame_${i}.jpg ${working}/blended_${i}.jpg
    lastframe="${dir}/frame_${i}.jpg_f0.jpg"
    if [ -n "${firstframe}" ]; then
        firstframe="${lastframe}"
    fi
done

#rm ${dir}/gray4_*.jpg
#rm ${dir}/base4_*.jpg

