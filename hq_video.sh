#!/usr/bin/env bash

# Adapted from http://rodrigopolo.com/ffmpeg/cheats.php#Other_FFmpeg_Options

ffmpeg -y -i $1 -r 24000/1001 -b 6144k -bt 8192k -vcodec libx264 -pass 1 -flags +loop -me_method dia -g 250 -qcomp 0.6 -qmin 10 -qmax 51 -qdiff 4 -bf 16 -b_strategy 1 -i_qfactor 0.71 -cmp +chroma -subq 1 -me_range 16 -coder 1 -sc_threshold 40 -flags2 -bpyramid-wpred-mixed_refs-dct8x8+fastpskip -keyint_min 25 -refs 1 -trellis 0 -directpred 1 -partitions -parti8x8-parti4x4-partp8x8-partp4x4-partb8x8-an $2.mp4

ffmpeg -y -i $1 -r 24000/1001 -b 6144k -bt 8192k -vcodec libx264 -pass 2 -flags +loop -me_method umh -g 250 -q 0.6 -qmin 10 -qmax 51 -qdiff 4 -bf 16 -b_strategy 1 -i_qfactor 0.71 -cmp +chroma -subq 8 -me_range 16 -coder 1 -sc_threshold 40 -flags2 +bpyramid+wpred+mixed_refs+dct8x8+fastpskip -keyint_min 25 -refs 4 -trellis 1 -directpred 3 -partitions +parti8x8+parti4x4+partp8x8+partb8x8-acodec libfaac -ac 2 -ar 44100 -ab 128k $2.mp4
