#!/usr/bin/env bash

working=$1
size=$2
scale=$3
blend=$4

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

convert ${working}/red.jpg ${working}/green.jpg ${working}/blue.jpg -combine ${working}/base.jpg
convert -size ${size}x${size} gradient:black-white ${working}/fade.jpg
composite -blend ${blend} ${working}/fade.jpg ${working}/base.jpg ${working}/base.jpg
