#!/Users/yuji1997/.pyenv/shims/python3
# -*- coding: utf-8 -*-

import sys,os
import numpy as np
import time
import subprocess


# Define shell command
USB_ON = ["hub-ctrl", "-b", "1", "-d", "2", "-P" "2", "-p", "0"]
USB_OFF = ["hub-ctrl", "-b", "1", "-d", "2", "-P" "2", "-p", "1"]

class USB_CONTROL:
    """
    Class for controling usb

    Parameters
    _____
    debug : If you want to debug, set "debug=True". The defaults are set to false.

    Functions
    _____
    acton(time_arr, movie_time) : Start up usb control according to time_arr.
    terminate() : Finish usb control.
    """

    def __init__(self, debug=False):
        self.debug = debug

    def TurnOn(self):
        try:
            if self.debug:
                print("***************")
                print("\n", end="")
            res = subprocess.check_call(USB_ON)
        except:
            print("Fail to Turn On.")

    def TurnOff(self):
        try:
            if self.debug:
                print("\n", end="")
            res = subprocess.check_call(USB_OFF)
        except:
            print("Fail to Turn Off.")


    def acton(self, time_arr, movie_time):
        start = time.time()

        while elapsed_time_int <= movie_time:
            elapsed_time_int = int(time.time()-start)

            if elapsed_time_int in time_arr:
                self.TurnOn()

            if elapsed_time_int not in time_arr:
                self.TurnOff()

        self.TurnOff()


if __name__ == "__main__":
    LOAD_NAME_time_arr = "../time_arr/"+sys.argv[1]+"_"+sys.argv[2]+".npy"
    time_arr = np.load(LOAD_NAME_time_arr)

    LOAD_NAME_movie_time = "../time_arr/"+sys.argv[1]+"_time.npy"
    movie_time = np.load(LOAD_NAME_movie_time)

    if len(sys.argv)>=4:
        debug = (sys.argv[3]=="-debug")
        FAN = USB_CONTROL(debug=debug)
    else:
        FAN = USB_CONTROL()

    FAN.acton(time_arr, movie_time)
