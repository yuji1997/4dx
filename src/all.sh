#!/bin/sh

sudo hub-ctrl -h 0 -P 2 -p 1
/use/bin/python /home/pi/4dx/src/sensor.py $1 $2
