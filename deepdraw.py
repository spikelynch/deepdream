#!/usr/bin/env python

# coding: utf-8

from cStringIO import StringIO
import numpy as np
import os,re,random
import scipy.ndimage as nd
import PIL.Image
import sys
from scipy.misc import imresize

import caffe

import argparse


CAFFE_MODELS = '../caffe/models/'

OUTPUT_DIR = './Output/Deepdraw'

IMAGENET_CLASS = 1
ALL_FRAMES = False


# guacamole, consomme, ice cream, pretzel, bagel, cheeseburger, hot dog, pomegranate, pizza, chocolate sauce

# CLASSLIST = [ 924, 925, 928, 931, 932, 933, 934, 957, 963, 960 ]

BASEFILE = 'PLtest'
# [ lionfish, altar ] / [ ambulance, panda ] / [ red panda, banjo ] / [ wheelbarrow, can opener ]
CLASSLIST = [ [ x ] for x in range(0,205)]

BASE_IMAGES = [ 'noise224.jpg' ]


#model = "bvlc_googlenet"
model = "googlenet_places205"
model_path = os.path.join(CAFFE_MODELS, model)
net_fn   = os.path.join(model_path, 'deploy.prototxt')
param_fn = os.path.join(model_path, model + '.caffemodel')


#model_path = '/your/path/here/caffe_models/bvlc_googlenet/' # substitute your path here
#net_fn   = './deploy_googlenet_updated.prototxt'
#param_fn = model_path + 'bvlc_googlenet.caffemodel'

mean = np.float32([104.0, 117.0, 123.0])

net = caffe.Classifier(net_fn, param_fn,
                       mean = mean, # ImageNet mean, training set dependent
                       channel_swap = (2,1,0)) # the reference model has channels in BGR order instead of RGB

# a couple of utility functions for converting to and from Caffe's input image layout
def preprocess(net, img):
    return np.float32(np.rollaxis(img, 2)[::-1]) - net.transformer.mean['data']
def deprocess(net, img):
    return np.dstack((img + net.transformer.mean['data'])[::-1])



def blur(img, sigma):
    if sigma > 0:
        img[0] = nd.filters.gaussian_filter(img[0], sigma, order=0)
        img[1] = nd.filters.gaussian_filter(img[1], sigma, order=0)
        img[2] = nd.filters.gaussian_filter(img[2], sigma, order=0)
    return img

def showarray(a, f, fmt='jpeg'):
    a = np.uint8(np.clip(a, 0, 255))
    f = StringIO()
    PIL.Image.fromarray(a).save(f, fmt)
    display(Image(data=f.getvalue()))

def writearray(a, filename, fmt='jpeg'):
    a = np.uint8(np.clip(a, 0, 255))
    path = os.path.join(OUTPUT_DIR, filename)
    PIL.Image.fromarray(a).save(path, fmt)


# Definition of the main gradient ascent functions. Note that these are based on the [deepdream code](https://github.com/google/deepdream/blob/master/dream.ipynb) published by Google as well as [this code](https://github.com/kylemcdonald/deepdream/blob/master/dream.ipynb) by Kyle McDonald.

# In[20]:

def make_step(net, step_size=1.5, end='inception_4c/output', clip=True, foci=None, sigma=None):
    '''Basic gradient ascent step.'''

    # print "make_step focus = %d end = %s" % ( focus, end )
    src = net.blobs['data'] # input image is stored in Net's 'data' blob

    dst = net.blobs[end]

    net.forward(end=end)

    one_hot = np.zeros_like(dst.data)
    for focus in foci:
        one_hot.flat[focus] = 1.
    dst.diff[:] = one_hot

    net.backward(start=end)
    g = src.diff[0]

    src.data[:] += step_size/np.abs(g).mean() * g

    if clip:
        bias = net.transformer.mean['data']
        src.data[:] = np.clip(src.data, -bias, 255-bias)

    src.data[0] = blur(src.data[0], sigma)

    # reset objective for next step
    dst.diff.fill(0.)

def deepdraw(net, base_img, octaves, random_crop=True, visualize=False, foci=None,
    clip=True, **step_params):

    print "Target imageclasses"
    print foci
    # prepare base image
    image = preprocess(net, base_img) # (3,224,224)

    # get input dimensions from net
    w = net.blobs['data'].width
    h = net.blobs['data'].height

    print "starting drawing"
    src = net.blobs['data']
    print "Reshaping input image size %d, %d" % ( h, w )

    src.reshape(1,3,h,w) # resize the network's input image size
    for e,o in enumerate(octaves):
        if 'scale' in o:
            # resize by o['scale'] if it exists
            image = nd.zoom(image, (1,o['scale'],o['scale']))
        _,imw,imh = image.shape
        print "Image shape octave %d, %d" % ( imw, imh )
        # select layer
        layer = o['layer']

        for i in xrange(o['iter_n']):
            if imw > w:
                if random_crop:
                    # randomly select a crop
                    #ox = random.randint(0,imw-224)
                    #oy = random.randint(0,imh-224)
                    mid_x = (imw-w)/2.
                    width_x = imw-w
                    ox = np.random.normal(mid_x, width_x*0.3, 1)
                    ox = int(np.clip(ox,0,imw-w))
                    mid_y = (imh-h)/2.
                    width_y = imh-h
                    oy = np.random.normal(mid_y, width_y*0.3, 1)
                    oy = int(np.clip(oy,0,imh-h))
                    # insert the crop into src.data[0]
                    print "Cropping: %d, %d" % ( ox, oy )
                    src.data[0] = image[:,ox:ox+w,oy:oy+h]
                else:
                    ox = (imw-w)/2.
                    oy = (imh-h)/2.
                    src.data[0] = image[:,ox:ox+w,oy:oy+h]
            else:
                ox = 0
                oy = 0
                src.data[0] = image.copy()

            sigma = o['start_sigma'] + ((o['end_sigma'] - o['start_sigma']) * i) / o['iter_n']
            step_size = o['start_step_size'] + ((o['end_step_size'] - o['start_step_size']) * i) / o['iter_n']

            make_step(net, end=layer, clip=clip, foci=foci,
                      sigma=sigma, step_size=step_size)

            if visualize:
                vis = deprocess(net, src.data[0])
                if not clip: # adjust image contrast if clipping is disabled
                    vis = vis*(255.0/np.percentile(vis, 99.98))
                if i % 1 == 0:
                    writearray(vis, "./octave%d_f%d.jpg" % ( e, i ))

            if i % 10 == 0:
                print 'finished step %d in octave %d' % (i,e)

            # insert modified image back into original image (if necessary)
            image[:,ox:ox+w,oy:oy+h] = src.data[0]

        print "octave %d image:" % e
        writearray(deprocess(net, image),"./octave_"+str(e)+".jpg")

    # returning the resulting image
    return deprocess(net, image)


# #### Generating the class visualizations
#
# The ```octaves``` list determines in which order we optimize layers, as well as how many iterations and scaling on each octave. For each octave, parameters are:
# * ```layer``` : which layer to optimize
# * ```iter_n``` : how many iterations
# * ```scale``` : by what factor (if any) to scale up the base image before proceeding
# * ```start_sigma``` : the initial radius of the gaussian blur
# * ```end_sigma``` : the final radius of the gaussian blur
# * ```start_step_size``` : the initial step size of the gradient ascent
# * ```end_step_size``` : the final step size of the gradient ascent
#
# The choice of octave parameters below will give decent images, and
# is the one used for visualizations in the blogpost. However, the
# choice of parameters was a bit arbitrary, so feel free to experiment.
# Note that generating an image will take around 1 minute with GPU-enabled Caffe, or 10-15 minutes if you're running purely on CPU, depending on your computer performance.

# In[21]:

# these octaves determine gradient ascent steps
octaves = [
    {
        'layer':'loss3/classifier',
        'iter_n':190,
        'start_sigma':2.5,
        'end_sigma':0.78,
        'start_step_size':11.,
        'end_step_size':11.
    },
    {
        'layer':'loss3/classifier',
        'scale': 1.2,
        'iter_n':150,
        'start_sigma':0.78*1.2,
        'end_sigma':0.78,
        'start_step_size':6.,
        'end_step_size':6.
    },
    {
        'layer':'loss2/classifier',
        'scale':1.2,
        'iter_n':150,
        'start_sigma':0.78*1.2,
        'end_sigma':0.44,
        'start_step_size':6.,
        'end_step_size':3.
    },
    {
        'layer':'loss1/classifier',
        'iter_n':10,
        'start_sigma':0.44,
        'end_sigma':0.304,
        'start_step_size':3.,
        'end_step_size':3.
    }
]

octaves_s = [
    {
        'layer':'loss3/classifier',
        'scale': 0.7,
        'iter_n':80,
        'start_sigma': 0.2,
        'end_sigma':0.5,
        'start_step_size':11.,
        'end_step_size':11.
    },
    {
        'layer':'loss3/classifier',
        'scale': 0.8,
        'iter_n':60,
        'start_sigma':0.1,
        'end_sigma':0.1,
        'start_step_size':6.,
        'end_step_size':6.
    },
    {
        'layer':'loss2/classifier',
        'scale':1.2,
        'iter_n':60,
        'start_sigma':0.4,
        'end_sigma':0.44,
        'start_step_size':6.,
        'end_step_size':3.
    },
    {
        'layer':'loss1/classifier',
        'iter_n':30,
        'start_sigma':0.44,
        'end_sigma':0.304,
        'start_step_size':3.,
        'end_step_size':3.
    }
]

octaves2 = [
    {
        'layer':'loss3/classifier',
        'iter_n':190,
        'scale':1,
        'start_sigma':2.5,
        'end_sigma':0.78,
        'start_step_size':11.,
        'end_step_size':11.
    },
    {
        'layer':'loss3/classifier',
        'scale':1.0,
        'iter_n':450,
        'start_sigma':0.78*1.2,
        'end_sigma':0.40,
        'start_step_size':6.,
        'end_step_size':3.
    }
]

octaves3 = [
    {
        'layer':'loss3/classifier',
        'iter_n':190,
        'start_sigma':1,
        'end_sigma':1,
        'start_step_size':11.,
        'end_step_size':11.
    }
]



# get original input size of network
original_w = net.blobs['data'].width
original_h = net.blobs['data'].height
# the background color of the initial image
background_color = np.float32([200.0, 200.0, 200.0])

print "Original image size = %d, %d" % ( original_w, original_h )

for fn in BASE_IMAGES:
    origfile = "Input/" + fn
    img = np.float32(PIL.Image.open(origfile))

    for ic in CLASSLIST:

        img = np.random.normal(background_color, 8, (original_w, original_h, 3))
        # generate class visualization via octavewise gradient ascent
        gen_image = deepdraw(net, img, octaves2, foci=ic,
                             random_crop=True, visualize=ALL_FRAMES)
        # save image
        img_fn = '_'.join([BASEFILE, str(ic), fn]) + ".png"
        writearray(gen_image, img_fn)
    #PIL.Image.fromarray(np.uint8(gen_image)).save('./' + img_fn)

