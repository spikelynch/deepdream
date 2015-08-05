#!/usr/bin/env python

# imports and basic notebook setup
from cStringIO import StringIO
import numpy as np
import scipy.ndimage as nd
import PIL.Image
from IPython.display import clear_output, Image, display
from google.protobuf import text_format

import argparse
import re
import sys
import os
import caffe


MODELS = {
    'googlenet': 'bvlc_googlenet',
    'places': 'googlenet_places205',
    'oxford': 'oxford102',
    'cnn_age': 'cnn_age',
    'cnn_gender': 'cnn_gender',
    'caffenet': 'bvlc_reference_caffenet',
    'ilsvrc13': 'bvlc_reference_rcnn_ilsvrc13',
    'flickr_style': 'finetune_flickr_style'
}

DEFAULT_LAYERS = {
    'googlenet': 'inception_4c/output',
    'places': 'inception_4c/output',
    'cnn_age': 'pool5',
    'cnn_gender': 'pool5',
    'oxford': 'pool5',
    'cars': 'pool5',
    'caffenet': 'pool5',
    'ilsvrc13': 'pool5',
    'flickr_style': 'pool5'
}

MEAN_BINARIES = {
    'cnn_age': 'cnn_age_gender/mean.binaryproto',
}


# inception layers (for both of the above)
# 3a, 3b, 4a, 4b, 4c, 4d, 4e, 5a, 5b

models = MODELS.keys()

def showarray(a, fmt='jpeg'):
    a = np.uint8(np.clip(a, 0, 255))
    f = StringIO()
    PIL.Image.fromarray(a).save(f, fmt)
    display(Image(data=f.getvalue()))

def writearray(a, filename, fmt='jpeg'):
    a = np.uint8(np.clip(a, 0, 255))
    PIL.Image.fromarray(a).save(filename, fmt)

    
def loadmean(filename):
    proto_data = open(filename, "rb").read()
    a = caffe.io.caffe_pb2.BlobProto.FromString(proto_data)
    mean  = caffe.io.blobproto_to_array(a)[0]
    print "Loaded mean binary %s" % filename
    print mean.shape
    return mean
    
output_path = 'Output/'
default_layer = None

def load_net(model_name):
    model = MODELS[model_name]
    model_path = '../caffe/models/' + model + '/'
    net_fn   = model_path + 'deploy.prototxt'
    param_fn = model_path + model + '.caffemodel'
    default_layer = DEFAULT_LAYERS[model_name]

    # load mean binary if it's defined

    if model in MEAN_BINARIES:
        mean = loadmean('../caffe/models/' + MEAN_BINARIES[model])
    else:
        mean = np.float32([104.0, 116.0, 122.0])
        
    # Patching model to be able to compute gradients.
    # Note that you can also manually add "force_backward: true" line to "deploy.prototxt".
    model = caffe.io.caffe_pb2.NetParameter()
    text_format.Merge(open(net_fn).read(), model)
    model.force_backward = True
    open('tmp.prototxt', 'w').write(str(model))

    net = caffe.Classifier('tmp.prototxt', param_fn,
                           mean=mean, # ImageNet mean, training set dependent
                           channel_swap = (2,1,0)) # the reference model has channels in BGR order instead of RGB
    return net

# a couple of utility functions for converting to and from Caffe's input image layout

def preprocess(net, img):
    return np.float32(np.rollaxis(img, 2)[::-1]) - net.transformer.mean['data']

def deprocess(net, img):
    return np.dstack((img + net.transformer.mean['data'])[::-1])

def objective_L2(dst):
    dst.diff[:] = dst.data

def make_step(net, step_size=1.5, end=default_layer, jitter=32, clip=True, objective=objective_L2):
    '''Basic gradient ascent step.'''

    src = net.blobs['data'] # input image is stored in Net's 'data' blob
    dst = net.blobs[end]

    ox, oy = np.random.randint(-jitter, jitter+1, 2)
    src.data[0] = np.roll(np.roll(src.data[0], ox, -1), oy, -2) # apply jitter shift
            
    net.forward(end=end)
    objective(dst)           # new parametrised objective
    #dst.diff[:] = dst.data  # specify the optimization objective
    net.backward(start=end)
    g = src.diff[0]
    # apply normalized ascent step to the input image
    src.data[:] += step_size/np.abs(g).mean() * g

    src.data[0] = np.roll(np.roll(src.data[0], -ox, -1), -oy, -2) # unshift image
            
    if clip:
        bias = net.transformer.mean['data']
        src.data[:] = np.clip(src.data, -bias, 255-bias)


def deepdream(net, base_img, verbose_file=None, iter_n=10, octave_n=4, octave_scale=1.4, end=default_layer, clip=True, **step_params):
    # prepare base images for all octaves
    octaves = [preprocess(net, base_img)]
    for i in xrange(octave_n-1):
        octaves.append(nd.zoom(octaves[-1], (1, 1.0/octave_scale,1.0/octave_scale), order=1))
    
    src = net.blobs['data']
    detail = np.zeros_like(octaves[-1]) # allocate image for network-produced details
    for octave, octave_base in enumerate(octaves[::-1]):
        h, w = octave_base.shape[-2:]
        if octave > 0:
            # upscale details from the previous octave
            h1, w1 = detail.shape[-2:]
            detail = nd.zoom(detail, (1, 1.0*h/h1,1.0*w/w1), order=1)

        src.reshape(1,3,h,w) # resize the network's input image size
        src.data[0] = octave_base+detail
        for i in xrange(iter_n):
            make_step(net, end=end, clip=clip, **step_params)
            
            # visualization
            vis = deprocess(net, src.data[0])
            if not clip: # adjust image contrast if clipping is disabled
                vis = vis*(255.0/np.percentile(vis, 99.98))
            #showarray(vis)
            print octave, i, end #, vis.shape
            if verbose_file:
                filename = "%s_%d_%i.jpg" % ( verbose_file, octave, i ) 
                writearray(vis, filename)
                print "Wrote %s" % filename
            
        # extract details produced on the current octave
        detail = src.data[0]-octave_base
    # returning the resulting image
    return deprocess(net, src.data[0])


def make_objective_guide(net, guide, end):
    h, w = guide.shape[:2]
    src, dst = net.blobs['data'], net.blobs[end]
    src.reshape(1, 3, h, w)
    src.data[0] = preprocess(net, guide)
    net.forward(end=end)
    guide_features = dst.data[0].copy()
    return lambda dst: objective_guide(guide_features, dst)
    
def objective_guide(guide_features, dst):
    x = dst.data[0].copy()
    y = guide_features
    ch = x.shape[0]
    x = x.reshape(ch,-1)
    y = y.reshape(ch,-1)
    A = x.T.dot(y) # compute the matrix of dot-products with guide features
    dst.diff[0].reshape(ch,-1)[:] = y[:,A.argmax(1)] # select ones that match best


    


    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("s",        type=str, help="The source image")
    parser.add_argument("-m", "--model", type=str, help="The model", choices=models, default='googlenet')
    parser.add_argument("-l", "--layer", type=str, help="The layer")
    parser.add_argument("-b", "--basefile", type=str, help="Base filename", default=None)
    parser.add_argument("-g", "--guide", type=str, help="The guide image", default=None)
    parser.add_argument("-e", "--guidelayer", type=str, help="The guide layer", default='inception_3b/output')
    parser.add_argument("-i", "--iters",  type=int, help="Number of iterations per octave", default=10)
    parser.add_argument("-o", "--octaves", type=int, help="Number of octaves", default=4)
    parser.add_argument("-v", "--verbose", action='store_true', help="Dump out a file for every iteration", default=False)
    parser.add_argument("-z", "--zoom", type=float, help="Zoom factor", default=0)
    parser.add_argument("-f", "--frames", type=int, help="Number of frames", default=1)
    parser.add_argument("-j", "--initial", type=int, help="Initial frame #", default=0)
    parser.add_argument("-d", "--dir", type=str, help="Directory for output jpgs", default=output_path)
    parser.add_argument("-k", "--keys", action='store_true', help="Dump a list of available layers", default=False)
    args = parser.parse_args()

    origfile = args.s 

    if args.basefile:
        bfile = os.path.join(args.dir, args.basefile)
    else:
        p = re.compile('^(.*)\.jpg')
        m = p.match(origfile)
        if m:
            bfile = os.path.join(args.dir, m.group(1))
        else:
            bfile = os.path.join(args.dir, 'output')

    # format: "$BASEIMG_fZ.jpg" or "$BASEIMG_O_I.jpg" for verbose
    
    vfile = None
    if args.verbose:
        vfile = bfile
    
    print "Loading %s" % origfile

    img = np.float32(PIL.Image.open(origfile))


    print "Starting neural net..."

    net = load_net(args.model)

    if args.keys:
        print "Layers" 
        for k in net.blobs.keys():
            print k
        exit()

    if args.layer:
        layer = args.layer
    else:
        layer = DEFAULT_LAYERS[args.model]
    
    print "Dreaming..."
    
    if args.guide:
        guide = np.float32(PIL.Image.open(args.guide))
        guide_layer = args.guidelayer
        obj_guide = make_objective_guide(net, guide, guide_layer)
        dreamer = lambda x: deepdream(net, x, verbose_file=vfile, iter_n=args.iters, octave_n=args.octaves, end=layer, objective=obj_guide)
    else:
        dreamer = lambda x: deepdream(net, x, verbose_file=vfile, iter_n=args.iters, octave_n=args.octaves, end=layer)

    # default value of args.frames is 1

    h, w = img.shape[:2]
    s = args.zoom
    fi = args.initial
    for i in xrange(args.frames):
        img = dreamer(img)
        filename = "%s_f%d.jpg" % ( bfile, fi )
        writearray(img, filename)
        print "Wrote frame %s" % filename
        if s != 0:
            img = nd.affine_transform(img, [1-s,1-s,1], [h*s/2,w*s/2,0], order=1)
        fi += 1
        

    print "Done"
