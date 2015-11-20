#!/usr/bin/env bash

for skew in 20 40 60 80 100
do
    ./dream.py --iters 120 --guide Input/Cells/$skew.jpg  --model googlenet --basefile soh_$skew  ./Input/SOH.jpg 
done
