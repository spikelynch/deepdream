dream.py usage notes
==================

    dream.py [options] input_image.jpg


### Options

    -m --model MODELNAME

The neural net (model) to use. The default is googlenet (the original).  You'll need to download additional models, and add values to the MODELS and DEFAULT_LAYERS dicts in dream.py, for them to work.

    -l --layer LAYERNAME

Which layer to use for pattern-matching.  The default is inception_4c/output.

    -b --basefile FILENAME

Used to construct the output filename. The default is to use the input filename without the .jpg.

    -g --guide IMAGE.JPG

Use a guide image to control patterns in the output. This seems to need files with a width of
512 (or a multiple) and an even number of rows.

    -e --guidelayer LAYERNAME

Select which layer of the guide image to use. The default is inception_4c/output.

    -t --target A[,B,C,..]

If this flag is used, the script runs in deepdraw mode and tries to optimise one or
more image classes using the loss3 layer.  Classes are integers and are separated by
commas.

    -i --iters N

Number of iterations to run for each octave.

    -o --octaves N

Number of octaves. (Note that octaves do not work with the --target option yet)

    -s --sigma F

A floating-point value specifying the amount of blur to apply between iterations
when using --target.  Best results seem to be from .3 to .4.  Has no effect if
not using --target.

    -v --verbose

If this is selected, a file will be written out for each iteration.  Useful if
you want to see how the visualisations build up.  Doesn't work with --target.

    -f --frames N

If a value is passed in, this will run the process N times, feeding the previous
result back in to the input of the next frame.  Good for building dive animations.
The output files look like $BASEFILE_f$I.jpg where $I is the frame number.

    -z --zoom F

A floating-point value which zooms in to the image between frames. .5 = 150%. Default
is no zoom.

    -r --rotate F

Amount to rotate the image between frames, in degrees. Default is zero.

    -j --initial N

The initial frame number: useful if you're restarting a zoom which was interrupted.

    -d --dir OUTPUT_DIR

Override the default output path, which is ./Output

    -k --keys

Dumps out a list of all available layers for the model.

