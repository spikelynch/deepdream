#!/usr/bin/env bash

adir="./Animations/Googlenet/inception_4e/5x5_reduce"
wdir="./Animations/Googlenet/working"
odir="./Animations/Googlenet/output"

for i in `seq 0 1 359`; do
    convert ${wdir}/base_${i}.jpg ${adir}/frame_${i}.jpg_f0.jpg -compose Mathematics -define compose:args="0,1,-1,.5" -composite ${odir}/out_${i}.jpg
done
