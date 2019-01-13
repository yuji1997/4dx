#!/bin/sh

ffmpeg -y -i /Users/YujiNarita/4dx/movie/$1.mp4 -ac 1 -ar 44100 /Users/YujiNarita/4dx/wav/$1.wav
/Users/yuji1997/.pyenv/shims/python3 /Users/yuji1997/4dx/src/flip.py $1
/Users/yuji1997/.pyenv/shims/python3 /Users/yuji1997/4dx/src/picking.py $1 $2 $3
