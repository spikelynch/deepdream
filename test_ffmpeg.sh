#!/usr/bin/env bash

ffmpeg -i $1 -c:v libx264  -profile:v high -crf 18 -c:a copy $2
