#!/usr/bin/env bash


model=caffenet
dir="./Animations/Randomise"
working="$dir/working"
target=$1
config=$2
size="224"
amp=".3"
mean=".5"
lastframe=""
firstframe=""
iters="80"
blend="5"
lblend="10"

echo "${dir}/${target}"
mkdir -p "${working}"
mkdir -p "${dir}/${target}"

convert -size ${size}x${size} xc: +noise Random ${working}/random.png

lasti="355"

for i in `seq 0 5 359`; do

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
#    convert ${working}/base_${i}.jpg -fill white -colorize 30 ${working}/base_${i}.jpg
    
    
    # blend the last frame, if it exists
    if [ -n "$lastframe" ]; then
        composite -blend ${blend} ${lastframe} ${working}/base_${i}.jpg ${working}/blended_${i}.jpg
        if [ $i == $lasti ]; then
            composite -blend ${lblend} ${firstframe} ${working}/blended_${i}.jpg ${working}/blended_${i}.jpg
        fi
    else
        cp ${working}/base_${i}.jpg ${working}/blended_${i}.jpg
    fi

    ./dream.py --basefile frame_${i} --config $config ${working}/blended_${i}.jpg ${dir}/${target}
    lastframe="${dir}/${target}/frame_${i}.jpg"
    if [ -n "${firstframe}" ]; then
        firstframe="${lastframe}"
    fi
done

./rename.py ${dir}/${target}
./gifenc.sh ${dir}/${target}/frame_%d.jpg ${dir}/${target}/anim.gif
