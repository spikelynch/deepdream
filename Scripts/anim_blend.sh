#!/usr/bin/env bash


model="manga_tag"
size="224"
target="{\"34\":1}"
sigma=".3"
dir="./Animations/Test/"
working="./Animations/Test/working"
lastframe=""
firstframe=""
iters="500"
blend="5"
lblend="10"

#mkdir -p "${dir}/${layer}"

convert -size ${size}x${size} xc: +noise Random ${working}/random.png

lasti="350"

for i in `seq 0 10 359`; do
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
       
    ./dream.py --gpu --model $model --iters $iters --target $target --sigma $sigma --basefile frame_${i} ${working}/blended_${i}.jpg ${dir}
    lastframe="${dir}/frame_${i}.jpg"
    if [ -n "${firstframe}" ]; then
        firstframe="${lastframe}"
    fi
done

./rename.py $dir
#./gifenc.sh ${dir}/frame_%d.jpg ${dir}/anim.gif

#rm ${dir}/gray4_*.jpg
#rm ${dir}/base4_*.jpg

