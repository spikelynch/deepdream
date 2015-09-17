#!/usr/bin/env python

import os

for i in range(0, 72):
    a = i * 15
    old = "frame_%d.jpg_f0.jpg" % a
    new = "frame_%d.jpg" % i
    os.rename(old, new)
    
