#!/usr/bin/env bash


working="./Neuralgia/working"
scale=1
blend=60
size=224
config=$1
output=$2

convert -size ${size}x${size} xc: +noise Random ${working}/random.png

convert ${working}/random.png  -channel R \
        -function Sinusoid 1,0 \
        -virtual-pixel tile -blur 0x${scale} -auto-level \
        -separate ${working}/red.jpg
convert ${working}/random.png  -channel G \
        -function Sinusoid 1,0 \
        -virtual-pixel tile -blur 0x${scale} -auto-level \
        -separate ${working}/green.jpg
convert ${working}/random.png  -channel B \
        -function Sinusoid 1,0 \
        -virtual-pixel tile -blur 0x${scale} -auto-level \
        -separate ${working}/blue.jpg

# convert -size ${size}x${size} xc: +noise Random ${working}/noise.png
# convert ${working}/noise.png -virtual-pixel tile -blur 0x12 -colorspace Gray -auto-level ${working}/noise.jpg

convert ${working}/red.jpg ${working}/green.jpg ${working}/blue.jpg -combine ${working}/base1.jpg


convert -size ${size}x${size} gradient:black-white ${working}/fade.jpg
composite -blend ${blend} ${working}/fade.jpg ${working}/base1.jpg ${working}/base.jpg

#convert ${working}/graybase.jpg -colorspace rgb -type truecolor ${working}/base.jpg

./dream.py --config $config --basefile ${output} ${working}/base.jpg ./Neuralgia/
