#!/usr/bin/env bash

./classify.py Neuralgia/image6.jpg ./Neuralgia/conf7.json
./neuralgia.sh ./Neuralgia/conf7.json image7

./classify.py Neuralgia/image7.jpg ./Neuralgia/conf8.json
./neuralgia.sh ./Neuralgia/conf8.json image8

./classify.py Neuralgia/image8.jpg ./Neuralgia/conf9.json
./neuralgia.sh ./Neuralgia/conf9.json image9

./classify.py Neuralgia/image9.jpg ./Neuralgia/conf10.json
./neuralgia.sh ./Neuralgia/conf10.json image10

./classify.py Neuralgia/image10.jpg ./Neuralgia/conf11.json
./neuralgia.sh ./Neuralgia/conf11.json image11

./classify.py Neuralgia/image11.jpg ./Neuralgia/conf12.json
./neuralgia.sh ./Neuralgia/conf12.json image12

