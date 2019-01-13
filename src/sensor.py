#!/Users/yuji1997/.pyenv/shims/python3
# -*- coding: utf-8 -*-

import cv2
import time
import subprocess
import sys


def isBright(cap):

    ret, img = cap.read()

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    avg_intensity = 0

    for x in range(48):
        for y in range(64):
            avg_intensity += gray_img[x][y]

    avg_intensity /= (64*48)
    print avg_intensity

    isBright = (avg_intensity>80)

    return isBright 


def DCmotor_control():
    cap = cv2.VideoCapture(1)
    cap.set(3, 64)
    cap.set(4, 48)

    while not isBright(cap):
        isBright(cap)

    cmd = ["./theater.sh"]+sys.argv[1:]

    try:
        res = subprocess.check_call(cmd)
    except:
        print "./theater.sh exec Error."


def test():
    cap = cv2.VideoCapture(0)
    cap.set(3, 64)
    cap.set(4, 48)

    while True: 
        isBright(cap)


if __name__ == "__main__":
    DCmotor_control()
    #test()
