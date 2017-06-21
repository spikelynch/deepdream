#!/usr/bin/env bash

geom=$1
mode=$2
att=$3
working="./working"
blend=$4
gradient=$5
level=$6
blur=$7
file=$8

echo "geom ${geom}"
echo "perlin mode ${mode}"
echo "attenuation ${att}"
echo "blend ${blend}"
echo "gradient ${gradient}"
echo "levels ${level}"
echo "blur ${blur}"

$HOME/deepdream/Scripts/perlin.sh ${geom} -m ${mode} -a ${att} ${working}/perlin.jpg

convert -size ${geom} ${gradient} ${working}/fade.jpg 
composite -blend ${blend} ${working}/perlin.jpg ${working}/fade.jpg ${working}/comp.jpg
convert -level ${level} -blur ${blur} ${working}/comp.jpg ${file}
convert ${file} -colorspace rgb -type truecolor ${file}

echo ${file}

