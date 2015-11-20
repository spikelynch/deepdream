#!/usr/bin/env bash


model=caffenet
dir="./Animations/Randomise"
working="$dir/working"
target=$1
config=$2
size="224"
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

    ./dream.py --basefile frame_${i} --config $config ${working}/blended_${i}.jpg ${dir}/${target}
    lastframe="${dir}/${target}/frame_${i}.jpg"
    if [ -n "${firstframe}" ]; then
        firstframe="${lastframe}"
    fi
done

./rename.py ${dir}/${target}
./gifenc.sh ${dir}/${target}/frame_%d.jpg ${dir}/${target}/anim.gif
