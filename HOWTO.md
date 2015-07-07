DeepDreamer Howto v1.0
======================

This is a quick description of how I got the
[deepdream code](https://github.com/google/deepdream/blob/master/dream.ipynb)
up and running on my MacBook Pro. The code give uses an iPython
notebook to process images using the
[Caffe](http://caffe.berkeleyvision.org/) neural network framework,
based on a model provided on the Google github.  This how-to covers
the following:

* Setting up a virtual OS
* Installing Caffe and its dependencies
* Compiling Caffe and its Python interface
* Adapting the iPython notebook to run from the command line

You'll need basic Linux command-line skills to do this. If any of the
following is hard to follow it's probably because I'm not spelling out
my own tacit knowledge - please drop me a line and I can try to make
it simpler.

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
on Macs, so go download it if you don't already have it.)

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

Ubuntu's UI can seem a bit impenetrable.  Once you log in, you'll get
the Ubuntu desktop.  To install Caffe and its dependencies, you'll
need to get a command line terminal running (this is basically the
same thing as a terminal in Mac OS). Click the red icon in the top
left corner of the Ubuntu desktop, and you'll get a search field -
type 'terminal' and hit return to bring up a terminal.

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


## Installing Caffe

I followed [Caffe's installation guide](http://caffe.berkeleyvision.org/installation.html) as closely as possible.  I won't duplicate too much of that, just point out some gotchas.

Unfortunately, Caffe isn't the sort of software which you can get with
the package manager - it needs to be compiled on the system it will
run on.

### Caffe dependencies



Caffe Dependencies - remember to switch off GPU unless you want to fight with nVidia drivers

Python dependencies

Caffe make python

Download the model

# The script

extracted and modified version of the iPython notebook
