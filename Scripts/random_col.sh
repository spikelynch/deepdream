#!/usr/bin/env bash

# Randomised deepdraws

size="224"
model="googlenet"
working="Output/Random/working"

mkdir -p $working


for i in {1..50}; do
    ./scripts/cnoise_fade.sh ${working} ${size} 8 80

    ./dream.py --model $model --target randomise --iters 400 --sigma .1 --basefile case_8_80_${i} ${working}/base.jpg Output/DeepDraw/Randomfade/   
done
