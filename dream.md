dream.py usage notes
====================

    dream.py -m MODEL -l LAYER -g GUIDE -e GUIDE_LAYER -i ITERS -n OCTAVES INPUT.JPG

## -m --model

The neural net (model) to use. The default is bvlc_googlenet (the original).  You'll need to download additional models for them to work.

## -l --layer

Which layer to use for pattern-matching. 
