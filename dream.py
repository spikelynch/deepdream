#!/usr/bin/env python2
# imports and basic notebook setup
from cStringIO import StringIO
import numpy as np
import scipy.ndimage as nd
import PIL.Image
from google.protobuf import text_format

import argparse
import json
import re
import sys
import os

import caffe

if 'CAFFE_PATH' in os.environ:
    CAFFE_MODELS = os.path.join(os.environ['CAFFE_PATH'], 'models')
else:
    print """
You need to set the environment variable CAFFE_PATH to the location of your
Caffe installation
"""
    sys.exit(-1)

#CAFFE_MODELS = '../caffe/models/'

MODELS = {
    'googlenet': 'bvlc_googlenet',
    'places': 'googlenet_places205',
    'oxford': 'oxford102',
    'cnn_age': 'cnn_age',
    'cnn_gender': 'cnn_gender',
    'caffenet': 'bvlc_reference_caffenet',
    'ilsvrc13': 'bvlc_reference_rcnn_ilsvrc13',
    'flickr_style': 'finetune_flickr_style',
    'manga' : 'illustration2vec',
    'manga_tag' : 'illustration2vec_tag'
#    'cars' : 'cars'
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
    'flickr_style': 'pool5',
    'manga': 'pool5',
    'manga_tag': 'pool6'
}

CLASS_TARGET_LAYER = {
    'googlenet': 'loss3/classifier',
    'places': 'loss3/classifier',
    'oxford': 'fc8_oxford_102',
    'flickr_style': 'fc8_flickr',
    'cars': 'fc8',
    'cnn_age': 'fc8',
    'cnn_gender': 'fc8',
    'ilsvrc13': 'fc-rcnn',
    'caffenet': 'fc8',
    'manga': 'encode1neuron',
    'manga_tag': 'conv6_4'
}

N_CLASSES = {
    'googlenet': 1000,
    'caffenet': 1000,
    'manga': 4096,
    'places': 205,
    'manga_tag': 1538
}


DD_OCTAVES = [
    {
        'layer':'encode1neuron',
        'iter_n':200,
        'start_sigma':1.2,
        'end_sigma':0.2,
        'start_step_size':5.0,
        'end_step_size':1.5
    },
]

    
MAGIC_TARGETS = [ 'randomise' ]
        
CLASS_BACKGROUND = 128.0

MD_FILE = 'dream.json'

MEAN_BINARIES = {
#    'cnn_age': 'cnn_age_gender/mean.binaryproto',
    'manga_tag': 'illustration2vec_tag/image_mean.npy',
    'manga': 'illustration2vec_tag/image_mean.npy'
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
    #proto_data = open(filename, "rb").read()
    #a = caffe.io.caffe_pb2.BlobProto.FromString(proto_data)
    #mean  = caffe.io.blobproto_to_array(a)[0]
    mean = np.load(filename)
    print "Loaded mean binary %s" % filename
    print mean.shape
    return mean

output_path = 'Output/'
default_layer = None

def load_net(model_name):
    model = MODELS[model_name]
    model_path = os.path.join(CAFFE_MODELS, model)
    net_fn   = os.path.join(model_path, 'deploy.prototxt')
    param_fn = os.path.join(model_path, model + '.caffemodel')
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


# Objective functions

# This is the default objective

def objective_L2(dst):
    dst.diff[:] = dst.data

# objective function based on a guide image

def make_objective_guide(net, guide, guide_layer):
    h, w = guide.shape[:2]
    src, dst = net.blobs['data'], net.blobs[guide_layer]
    src.reshape(1, 3, h, w)
    src.data[0] = preprocess(net, guide)
    net.forward(end=guide_layer)
    guide_features = dst.data[0].copy()
    return lambda d: objective_guide(guide_features, d)

def objective_guide(guide_features, dst):
    x = dst.data[0].copy()       # the data
    y = guide_features           # the guide image
    ch = x.shape[0]              # the shape
    #print "objective_guide"
    #print "before", x.shape, y.shape
    x = x.reshape(ch,-1)         # reshape these
    y = y.reshape(ch,-1)         # to match one another
    #print "after", x.shape, y.shape
    A = x.T.dot(y)               # compute the matrix of dot-products with guide features
    dst.diff[0].reshape(ch,-1)[:] = y[:,A.argmax(1)] # select ones that match best


# Next idea: look at the API for loss layers (like loss3/classifier) and see what
# can be used from them to feedback into dst.diff (ie filter them by one or more
# target categories)


def make_objective_target(net, foci):
    return lambda d: objective_targets(foci, d)



def objective_targets(foci, dst):
    one_hot = np.zeros_like(dst.data)
    for focus, weight in foci.iteritems():
        one_hot.flat[int(focus)] = 1.0 * weight
    dst.diff[:] = one_hot


def make_magic_targets(type, model):
    n = N_CLASSES[model]
    foci = {}
    for i in range(0, n):
        if np.random.randint(0, 2):
            foci[i] = 1.
        else:
            foci[i] = -1.
    return foci
        
    
def blur(img, sigma):
    if sigma > 0:
        img[0] = nd.filters.gaussian_filter(img[0], sigma, order=0)
        img[1] = nd.filters.gaussian_filter(img[1], sigma, order=0)
        img[2] = nd.filters.gaussian_filter(img[2], sigma, order=0)
    return img



def make_step(net, step_size=1.5, end=default_layer, jitter=32, clip=True, objective=objective_L2, sigma=0):
    '''Basic gradient ascent step.'''

    src = net.blobs['data'] # input image is stored in Net's 'data' blob
    dst = net.blobs[end]    # the layer targeted by default_layer

    ox, oy = np.random.randint(-jitter, jitter+1, 2)
    src.data[0] = np.roll(np.roll(src.data[0], ox, -1), oy, -2) # apply jitter shift

    net.forward(end=end)     # inference of features

    objective(dst)           # set an objective

    net.backward(start=end)  # retrain

    g = src.diff[0]
    asc = np.abs(g).mean()
#    print " ascent step {}".format(asc)
    if asc != 0:
        # apply normalized ascent step to the input image
        src.data[:] += step_size / np.abs(g).mean() * g

    src.data[0] = np.roll(np.roll(src.data[0], -ox, -1), -oy, -2) # unshift image

    if clip:
        bias = net.transformer.mean['data']
        src.data[:] = np.clip(src.data, -bias, 255-bias)

    if sigma:
        src.data[0] = blur(src.data[0], sigma)




def deepdream(net, base_img, verbose_file=None, iter_n=10, octave_n=4, octave_scale=1.4, tiling=False, end=default_layer, clip=True, **step_params):
    # prepare base images for all octaves

    octaves = [preprocess(net, base_img)]

    w0 = net.blobs['data'].width
    h0 = net.blobs['data'].height

    for i in xrange(octave_n-1):
        o_base = nd.zoom(octaves[-1], (1, 1.0/octave_scale,1.0/octave_scale), order=1)
        h, w = o_base.shape[-2:]
        if not tiling or (h > h0 and w > w0):
            octaves.append(o_base)

    src = net.blobs['data']
    for o in octaves:
        print o.shape
    detail = np.zeros_like(octaves[-1]) # allocate image for network-produced details
    if tiling:
        image = np.zeros_like(base_img)
    for octave, octave_base in enumerate(octaves[::-1]):
        h, w = octave_base.shape[-2:]
        if octave > 0:
            # upscale details from the previous octave
            h1, w1 = detail.shape[-2:]
            detail = nd.zoom(detail, (1, 1.0*h/h1,1.0*w/w1), order=1)


        if not tiling:
            src.reshape(1, 3, h, w) # resize the network's input image size
            src.data[0] = octave_base + detail
            for i in xrange(iter_n):
                make_step(net, end=end, clip=clip, **step_params)
                vis = deprocess(net, src.data[0])
                if not clip: # adjust image contrast if clipping is disabled
                    vis = vis*(255.0/np.percentile(vis, 99.98))
                print octave, i, end
                if verbose_file:
                    filename = "%s_%d_%i.jpg" % ( verbose_file, octave, i )
                    writearray(vis, filename)
                    print "Wrote %s" % filename

            # extract details produced on the current octave
            detail = src.data[0] - octave_base
            writearray(deprocess(net, detail), "detail_%d.jpg" % octave)
        else:
#            image.reshape(1, 3, h, w)
            image = octave_base + detail
            print "tiling, image = %d %d" % ( h, w )
            tiles = make_tile_pattern(image, w0, h0)
            for i in xrange(iter_n):
                 print "Iter %d" % i
                 for x, y in tiles:
                    tile = get_tile(image, x, y, w0, h0)
                    # print "tile = ", tile.shape
                    if len(tile):
                        src.data[0] = tile
                        make_step(net, end=end, clip=clip, **step_params)
                        print src.data[0].shape
                        put_tile(image, src.data[0], x, y, w0, h0)
            detail = image - octave_base
            writearray(deprocess(net, detail), "detail_%d.jpg" % octave)

    # returning the resulting image
    if not tiling:
        return deprocess(net, src.data[0])
    else:
        return deprocess(net, image)



# have reverted this to the original code allowing multiple octaves as the
# tiling stuff was bad and slow

def deepdraw(net, base_img, verbose_file=None, random_crop=True, octaves=DD_OCTAVES, end=default_layer, clip=True,  **step_params):

    # prepare base image

    image = preprocess(net, base_img)

    _, imw, imh = image.shape


    # get input dimensions from net
    w = net.blobs['data'].width
    h = net.blobs['data'].height

    src = net.blobs['data']
    print "Reshaping input image size %d, %d" % ( h, w )

    src.reshape(1,3,h,w) # resize the network's input image size

    if not octaves:
        octaves = DD_OCTAVES
        octaves['layer'] = CLASS_TARGET_LAYER[end]

    vi = 0
    for e,o in enumerate(octaves):
        if 'scale' in o:
            # resize by o['scale'] if it exists
            image = nd.zoom(image, (1,o['scale'],o['scale']))
        _,imw,imh = image.shape
        
        # select layer
        layer = o['layer']

        for i in xrange(o['iter_n']):
            if imw > w:
                if random_crop:
                    # randomly select a crop 
                    mid_x = (imw-w)/2.
                    width_x = imw-w
                    ox = np.random.normal(mid_x, width_x*0.3, 1)
                    ox = int(np.clip(ox,0,imw-w))
                    mid_y = (imh-h)/2.
                    width_y = imh-h
                    oy = np.random.normal(mid_y, width_y*0.3, 1)
                    oy = int(np.clip(oy,0,imh-h))
                    # insert the crop into src.data[0]
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
            
            make_step(net, end=layer, clip=clip, sigma=sigma, step_size=step_size, **step_params)

            if verbose_file:
                vis = deprocess(net, src.data[0])
                if not clip: # adjust image contrast if clipping is disabled
                    vis = vis*(255.0/np.percentile(vis, 99.98))
                if i % 1 == 0:
                    writearray(vis,os.path.join(verbose_file, "dd_frame"+str(vi)+".jpg"))
                    vi += 1
            
            if i % 10 == 0:
                print 'finished step %d in octave %d' % (i,e)
            
            # insert modified image back into original image (if necessary)
            image[:,ox:ox+w,oy:oy+h] = src.data[0]
        
        print "octave %d image:" % e
        writearray(deprocess(net, image),"./octave_"+str(e)+".jpg")
            
    # returning the resulting image
    return deprocess(net, image)    

def parse_classes(s, w):
    if s == 'nil':
        return {}
    numeric_re = re.compile('^[0-9,-]*$')
    if numeric_re.search(s):
        il = []
        for c1 in s.split(','):
            c2 = c1.split('-')
            print len(c2)
            if len(c2) == 1:
                il.append(int(c2[0]))
            else:
                il += (range(int(c2[0]), int(c2[1]) + 1))
#        il = map(int, s.split(','))
        print il
        weight = 1.
        if w:
            weight = w
        c = { f: weight for f in il }
        return c
    else:
        return load_classes(s)


def load_classes(jf):
    try:
        with open(jf) as f:
            js = json.load(f)
#            print "Loaded JSON classes: {}".format(js)
            return js
    except Exception():
        print "JSON load {} failed".format(jf)
        sys.exit(-1)


def write_json(bfile, args):
    jsonfile = bfile + '.json'
    with open(jsonfile, 'wb') as jf:
        jf.write(json.dumps(args, sort_keys=True, indent=4))


def read_json(args, jfile):
    a = argparse.Namespace()
    with open(jfile, 'rb') as jf:
        data = json.load(jf)
        for arg, value in data.iteritems():
            a.__setattr__(arg, value)
    confv = vars(a)
    print("{} {}".format(confv, type))
    for arg in vars(args):
        if not arg in confv:
            v = getattr(args, arg)
            a.__setattr__(arg, v)
            print("Default value of missing conf {}: {}".format(arg, v))
    return a


def convert_focus(strfoci):
    foci = {}
    for target, weight in strfoci.iteritems():
        ti = int(target)
        foci[ti] = weight
    return foci

        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input",        type=str, help="The source image")
    parser.add_argument("output",        type=str, help="The output directory")
    parser.add_argument("-c", "--config",  type=str, default=None, help="JSON config file")
    parser.add_argument("-m", "--model", type=str, help="The model", choices=models, default='googlenet')
    parser.add_argument("-l", "--layer", type=str, help="The layer")
    parser.add_argument("-b", "--basefile", type=str, help="Base filename", default=None)
    parser.add_argument("-g", "--guide", type=str, help="The guide image", default=None)
    parser.add_argument("-e", "--guidelayer", type=str, help="The guide layer", default='inception_3b/output')
    parser.add_argument("-t", "--target", type=str, help="ImageNet class(es) (comma separated)", default=None)
    parser.add_argument("-w", "--weight", type=float, help="Weight of ImageNet classes", default=None)
    parser.add_argument("-i", "--iters",  type=int, help="Number of iterations per octave", default=10)
    parser.add_argument("-o", "--octaves", type=int, help="Number of octaves", default=4)
    parser.add_argument("-d", "--deepdraw", type=str, default=None, help="Deepdraw octaves (JSON file)")
    parser.add_argument("-s", "--sigma", type=float, help="Blur (sigma)", default=0)
    parser.add_argument("-u", "--glide", type=str, help="Glide between frames x,y", default=None)
    parser.add_argument("-v", "--verbose", type=str, help="Dump out a file for every iteration", default=None)
    parser.add_argument("-z", "--zoom", type=float, help="Zoom factor", default=0)
    parser.add_argument("-r", "--rotate", type=int, help="Rotate in degrees", default=0)
    parser.add_argument("-f", "--frames", type=int, help="Number of frames", default=1)
    parser.add_argument("-j", "--initial", type=int, help="Initial frame #", default=0)
    parser.add_argument("-k", "--keys", action='store_true', help="Dump a list of available layers", default=False)
    parser.add_argument("-n", "--nojson", action='store_true', help="Don't write out a json config file", default=False)
    args = parser.parse_args()
     
    origfile = args.input
    output_path = args.output

    if os.path.exists(output_path):
        if os.path.isdir(output_path):
            print "Warning: %s already exists" % output_path
        else:
            print "Output path %s is a file: exiting" % output_path
            sys.exit(-1)
    else:
        os.makedirs(output_path)

    # basefile is never taken from config
    if args.basefile:
        bfile = os.path.join(output_path, args.basefile)
    else:
        f, e = os.path.splitext(os.path.basename(origfile))
        #if e != '.jpg':
        #    print "Input must be a jpg"
        #    print "Got %s/%s" % ( f, e )
        #    sys.exit(-1)
        bfile = os.path.join(output_path, f)

        
    if args.config:
        if not os.path.isfile(args.config):
            print "Config file %s not found" % args.config
            sys.exit(-1)
        args = read_json(args, args.config)

            

    if args.target:
        if args.target in MAGIC_TARGETS and not args.config:
            print "make magic targets"
            foci = make_magic_targets(args.target, args.model)
            args.target = foci
        
    # TODO: if bfile exists, add something to its name 
    if not ('nojson' in args and args.nojson ): 
        write_json(bfile, vars(args))

    vfile = None
    if args.verbose:
        vfile = args.verbose

    print "Loading %s" % origfile

    img = np.float32(PIL.Image.open(origfile))


    print "Starting neural net..."

    net = load_net(args.model)

    original_w = net.blobs['data'].width
    original_h = net.blobs['data'].height

    print "Data original size: %d %d" % ( original_w, original_h )


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
    elif args.target is not None:
        if args.model not in CLASS_TARGET_LAYER:
            print "Can't do deepdraw on this model"
            sys.exit(-1)
        if type(args.target) is dict:
            foci = convert_focus(args.target)
        else:
            foci = parse_classes(args.target, args.weight)
        if not foci:
            print "Empty targets"
            foci = []
        print foci
        layer = CLASS_TARGET_LAYER[args.model]
        dd_octaves = DD_OCTAVES
        dd_octaves[0]['layer'] = layer
        if args.deepdraw:
            with open(args.deepdraw) as ddj:
                dd_octaves = json.load(ddj)
        obj_class = make_objective_target(net, foci)
        dreamer = lambda x: deepdraw(net, x, verbose_file=args.verbose, octaves=dd_octaves, end=layer, objective=obj_class)
    else:
        dreamer = lambda x: deepdream(net, x, verbose_file=vfile, iter_n=args.iters, octave_n=args.octaves, sigma=args.sigma, end=layer)

    # default value of args.frames is 1

    h, w = img.shape[:2]

    gx, gy = 0, 0
    if args.glide:
        g0 = args.glide.split(',')
        if len(g0) == 2:
            gx = int(g0[0])
            gy = int(g0[1])

    print "Shape" , img.shape
    s = args.zoom
    theta = args.rotate
    fi = args.initial
    for i in xrange(args.frames):
        img = dreamer(img)
        if args.frames > 1:
            filename = "%s_f%d.jpg" % ( bfile, fi )
        else:
            if '.' in bfile:
                # hack - if basefile has an extension, use it
                filename = bfile
            else:
                filename = "%s.jpg" % bfile
        writearray(img, filename)
        print "Wrote frame %s" % filename
        if theta != 0:
            print "rotate %d" % theta
            img = nd.rotate(img, theta, reshape=False)
        if s != 0:
            print "zoom %f" % s
            img = nd.affine_transform(img, [1-s,1-s,1], [h*s/2,w*s/2,0], order=1)
        if gx != 0 or gy != 0:
            print "glide %d ,%d" % ( gx, gy )
            img = nd.shift(img, [ gy, gx, 0], mode='nearest')
        fi += 1


    print "Done"
