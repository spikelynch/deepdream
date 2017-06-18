#!/usr/bin/env python3

import json

LIST = 'manga_tag_list.json'

with open(LIST, 'r') as f:
    names = json.load(f)
    i = 0
    for name in names:
        print("{} {}".format(i, name))
        i += 1
