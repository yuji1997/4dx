#!/bin/sh

/usr/bin/python3 /home/pi/4dx/src/gpio_control.py $1 yell 18 $2 &
/usr/bin/python3 /home/pi/4dx/src/gpio_control.py $1 silence 12 $2 &
/usr/bin/python3 /home/pi/4dx/src/gpio_control.py $1 impact $2 &
