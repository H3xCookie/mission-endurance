#!/bin/bash

# unzip all the files inside the .tar.gz

tar -xvf sat_archive.tar.gz

python3 ./src/main.py --computed_coastline monkedir/precomputed_keypoingts.pkl
