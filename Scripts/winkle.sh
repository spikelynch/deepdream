#!/usr/bin/env bash

./dream.py --iters 40 --guide Input/Cells/20.jpg --guidelayer inception_4a/3x3_reduce --basefile WC020  Input/Winkle.jpg
./dream.py --iters 40 --guide Input/Cells/40.jpg --guidelayer inception_4a/3x3_reduce --basefile WC040  Input/Winkle.jpg
./dream.py --iters 40 --guide Input/Cells/60.jpg --guidelayer inception_4a/3x3_reduce --basefile WC060  Input/Winkle.jpg
./dream.py --iters 40 --guide Input/Cells/80.jpg --guidelayer inception_4a/3x3_reduce --basefile WC080  Input/Winkle.jpg
./dream.py --iters 40 --guide Input/Cells/100.jpg --guidelayer inception_4a/3x3_reduce --basefile WC100  Input/Winkle.jpg
