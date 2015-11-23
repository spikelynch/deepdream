#!/usr/bin/env python

import nltk, random, re

TEXT = 'definitions.txt'
LOG = 'log.txt'
LINELENGTH = 6

def makePairs(arr):
    pairs = []
    for i in range(len(arr)):
        if i < len(arr)-1: 
            temp = (arr[i], arr[i+1])
            pairs.append(temp)
    return pairs

def generate(cfd, word = 'the', num = 50):
    words = []
    for i in range(num):
        arr = []
        for j in cfd[word]:
            for k in range(cfd[word][j]):
                arr.append(j)
        words.append(word)
        word = arr[int((len(arr))*random.random())]     
    return words
        
with open(TEXT, 'r') as f:
    corpus = f.read()
    corpus = corpus.split()
    pairs = makePairs(corpus)
    cfd = nltk.ConditionalFreqDist(pairs)

    line_re = re.compile('^(.*): (.*)$')


    with open(LOG, 'r') as lf:
        for l in lf:
            m = line_re.match(l)
            if m:
                image = m.group(1)
                bits = m.group(2)
                words = bits.split(', ')
                print image
                for w in words:
                    start = w.replace(' ', '_')
                    try:
                        line = ' '.join(generate(cfd, start, LINELENGTH))
                    except IndexError as e:
                        print "ERROR: %s %s" % ( start, e )
                    print line.replace('_', ' ')
                print "\n"



        
