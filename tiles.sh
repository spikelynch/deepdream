#!/usr/bin/env bash


for q in 0_0 1_0 0_1 1_1
do
    ./dream.py --iters 150 --target 1 --sigma 0.35 --basefile tile_$q  ./Input/Denison_$q.jpg
done
