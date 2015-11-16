#!/usr/bin/env python3

# get all jpgs in a directory and renames them to frame_0.jpg, frame_1.jpeg,
# etc

from os import listdir, rename
from os.path import isfile, join
import sys
import re

JPG_PATTERN = '(\d+).jpg$'

d = sys.argv[1]

files = [ f for f in listdir(d) if isfile(join(d, f)) ]

jpegs = []

jre = re.compile(JPG_PATTERN)

for f in files:
    m = jre.search(f)
    if m:
        i = int(m.group(1))
        jpegs.append((i, f))


jpegs.sort(key=lambda t: t[0])

j = 0
for i, f in jpegs:
    new = "frame_%d.jpg" % j
    print((f, new))
    rename(join(d, f), join(d, new))
    j += 1

    
