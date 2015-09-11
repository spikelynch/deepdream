#!/usr/bin/env bash

convert -size 320x320 xc: +noise Random ./Animations/random.png

convert ./Animations/random.png  -channel G  -function Sinusoid 1,0 \
        -virtual-pixel tile -blur 0x16 -auto-level \
        -separate ./Animations/gray4.jpg


