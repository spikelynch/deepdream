#!/usr/bin/env bash

./rename.py $1
./gifenc.sh ${1}/frame_%d.jpg ${1}/anim.gif
