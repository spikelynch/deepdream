DeepDreamer Howto v1.0
======================

This is a description of how I got the
[deepdream code](https://github.com/google/deepdream/blob/master/dream.ipynb)
up and running on my MacBook Pro. The code give uses an iPython
notebook to process images using the
[Caffe](http://caffe.berkeleyvision.org/) neural network framework,
based on a model provided on the Google github, making strange things happen:

![Transformation](https://raw.githubusercontent.com/spikelynch/deepdream/master/Fractal_rails.jpg)


This how-to covers the following:

* Setting up a virtual OS
* Installing Caffe and its dependencies
* Compiling Caffe and its Python interface
* Adapting the iPython notebook to run from the command line

You'll need basic Linux command-line skills to do this. If any of the
following is hard to follow it's probably because I'm not spelling out
my own tacit knowledge - please drop me a line and I can try to make
it simpler.

**NOTE:** if you want to get dreaming with a minimum of fuss, [Ryan Kennedy has built a much more user-friendly solution](http://ryankennedy.io/running-the-deep-dream/) which gives you a container with all of the dependencies included and ready to run.  In true Lazyweb fashion, I found out about it when I was two-thirds of the way through writing this document.

See [this gallery](https://photos.google.com/album/AF1QipNzyzWbHZcJvIsmuQhVlxlAXXPj58m0DPujmdms) for examples of images I've generated with this code.

## Ubuntu

The first decision I made was to spin up an Ubuntu VM for Caffe,
rather than try to install it directly on Mac OS. This was pragmatic:
although Caffe's websites have instructions for OS X, past experience
of installing Unix stuff on Mac OS indicates that I'd have fewer
hassles if I installed on the right version and flavour of Linux.

[Caffe's installation guide](http://caffe.berkeleyvision.org/installation.html)
suggested Ubuntu 14.04.

I already had [Oracle VirtualBox](https://www.virtualbox.org/)
installed. (It's free and open source, and straightforward to install
on Macs, so go download it if you don't already have it.) This
basically lets you run another operating system inside a container on
your Mac (or Windows) box.

I downloaded an Ubuntu image from
[OSBoxes](http://www.osboxes.org/ubuntu/).

To get the image up and running, start up VirtualBox, select 'New' to
go into the wizard for creating a new VM, and on the third page ('Hard
drive') select 'Use an existing virtual hard drive' and use the file
browser to select the Ubuntu .vdi file.

The wizard will ask you how much RAM to assign the VM.  I've set mine
to 4096M - on the default setting, the deepdream code will run quite
slowly and often run out of memory and crash.

The default account details for the Ubuntu VM are on the osboxes page.

## The Ubuntu command line

Ubuntu's UI is impenetrable, even for a Linux.  Once you log in,
you'll get the Ubuntu desktop.  To install Caffe and its dependencies,
you'll need to get a command line terminal running (this is basically
the same thing as a terminal in Mac OS). Click the red icon in the top
left corner of the Ubuntu desktop, and you'll get a search field -
type 'terminal' and hit return to bring up a terminal.

![Ubuntu icon](https://raw.githubusercontent.com/spikelynch/deepdream/master/Ubuntu.png)

(The right sidebard of the Ubuntu desktop works like the Mac OS dock.
If you right-click on the Terminal icon, you can select 'Lock to
Launcher', which will keep the icon there for all sessions.)

Installing Caffe's dependency will need you to use two commands:
*apt-get*, which downloads and installs Ubuntu packages (software
which has been bundled and compiled for the correct OS) and *pip*
(similar to apt-get, but for Python libraries).

You'll also need to use *sudo*, which is used to give a command admin
privileges.  The first time you use a command with sudo, you'll be
asked for your Ubuntu password: use the one with which you logged in.

    sudo apt-get install $NAME_OF_UBUNTU_PACKAGE
    sudo pip install $NAME_OF_PYTHON_PACKAGE

When you use 'sudo apt-get', you'll be prompted for your password (the first time).

Almost all of the following commands will need a connection to the
internet, as we'll be downloading packages. VirtualBox should
automatically give your Ubuntu environment a link to whatever network
your machine is connected to.

First of all, run *apt-get update* to update Ubuntu's package directories:

    sudo apt-get update

(This will send a whole bunch of details about various package indices scrolling up your terminal: you can ignore this.)

Then, download pip:

    sudo apt-get install python-pip

## Installing Caffe's dependencies

These are libraries (bundles of software) which Caffe and its Python
interface need to be able to run.

### apt-get packages

Here is a list of all the Ubuntu packages I needed.  Note that some of
these may be surplus to requirements, but it's better to include
everything:

    sudo apt-get install libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libboost-all-dev libhdf5-serial-dev
    sudo apt-get install python-dev
    sudo apt-get install libgflags-dev libgoogle-glog-dev liblmdb-dev protobuf-compiler
    sudo apt-get install git
    sudo apt-get install libatlas-base-dev
    sudo apt-get install python-pip
    sudo apt-get install python-numpy
    sudo apt-get install python-scipy
    sudo apt-get install ipython
    sudo apt-get install python-protobuf

*apt-get* will prompt you as to whether to install other packages which these ones require: answer yes to everything.

### Python packages

Here's the list of Python packages required for the Caffe interface.
Some of these may duplicate libraries which you've already
downloaded - if it warns you that something is already installed,
don't worry about it.

    sudo pip install Cython
    sudo pip install scikit-image
    sudo pip install matplotlib
    sudo pip install h5py
    sudo pip install leveldb
    sudo pip install networkx
    sudo pip install nose
    sudo pip install pandas
    sudo pip install python-dateutil
    sudo pip install python-gflags
    sudo pip install pyyaml
    sudo pip install Pillow

Please let me know if any of these things don't install successfully.

## Getting Caffe from GitHub

Unfortunately, Caffe isn't the sort of software which you can get with
the package manager - it needs to be compiled on the system it will
run on.  To do this, you need to grab the whole of Caffe's source code from
GitHub.

[Caffe on GitHub](https://github.com/BVLC/caffe)

At the command line in your Ubuntu system, type the following commands

    cd
    mkdir Dreamer
    cd Dreamer
    git clone https://github.com/BVLC/caffe.git

This will create a directory called 'Dreamer' in your home directory,
and download the Caffe source from GitHub as a directory under that
one called 'caffe' (If you know enough about GitHub to want to use ssh
rather than https, that's fine too.)

## Building Caffe

I followed [Caffe's installation guide](http://caffe.berkeleyvision.org/installation.html) as closely as possible.  I won't duplicate too much of that, just point out some gotchas.

### Prerequisites

All of the Caffe prerequisites have been covered by the apt-get and
pip commands listed above, with the exception of CUDA. CUDA is a set
of drivers which allow Caffe to run on the GPUs of Nvidia graphics
cards: you don't need it to run the deepdreams code.

The default Caffe config has GPU on by default, so we'll need to fix that:

    cd ~/Dreamer/caffe
    cp Makefile.config.example Makefile.config
    gedit Makefile.config

The above commands move you to the caffe directory, copy the default config
to Makefile.config, and open Gedit, a simple text editor, so that you can
edit the config to switch GPU mode off.

Near the top of the file should be a couple of lines like:

    # CPU-only switch (uncomment to build without GPU support).
    # CPU_ONLY := 1

You need to remove the '#' at the start of the second line, so that it looks like:

    # CPU-only switch (uncomment to build without GPU support).
    CPU_ONLY := 1

Once you've done that, save your changes.

### Compiling Caffe

To compile Caffe, type the following command:

    make all

This will take a while, and will produce another stream of messages
from the compiler.

### Compiling the Python interface

You need to compile the Python interface to Caffe separately:

    make pycaffe

You will also need to add a line to your profile in Ubuntu: this sets
an environment variable to tell Python where to find the Caffe libraries.

    gedit ~/.profile

Once you've opened the .profile file, add the following line at the bottom:

    export PYTHONPATH="$HOME/Dreamer/caffe/python:$PYTHONPATH"

After you've added this line, you should restart your Ubuntu environment

### Downloading the model

You need to download a copy of the GoogleNet neural net model: this is
available from [BVLC's GitHub](https://github.com/BVLC/caffe/tree/master/models/bvlc_googlenet).

The simplest way to get it installed in your Ubuntu container is to open Firefox in Ubuntu and go to the URL above.  You should save the file in this directory:

    ~/Dreamer/caffe/models/bvlc_googlenet/

## Downloading and running the dreams.py script

The original dreams script is an iPython notebook, which runs as a
kind of interactive presentation with embedded code and output images.

I was a bit too impatient to try to get iPython working, so I
extracted the code and modified it a bit to make it write out the
results to a series of image files.  Here it is:

**[dream.py](https://raw.githubusercontent.com/spikelynch/deepdream/master/dream.py)**

For this to work, you should download the script to the ~/Dreamer
directory on your Ubuntu environment, and create a directory called 'Output'.

The simplest way to get a source image is to find something on the web and download it to ~/Dreamer:

    cd ~/Dreamer
    mkdir Output
    ./dream.py your_image.jpg

If all goes well, the script will start dreaming.  You should get 40 output files written into Output: these are progressive stages of the iterations of the dreamer algorithm.


Drop me a line via [my GitHub profile](https://github.com/spikelynch/) if you have any comments or corrections to this.
