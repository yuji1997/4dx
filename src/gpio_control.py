#!/Users/yuji1997/.pyenv/shims/python3
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time 
import numpy as np
import sys


class GPIO_CONTROL:
    """
    Class for controling DC motor by TA7291 @ GPIO
        *** This is based on the BCM standards. *** 

    Parameters
    _____
    PIN : GPIO PIN number.
    duty : PWM duty from 0 to 100. The defaults are set to duty=100.
    Hz : PWM frequency: 50Hz has been set as default.
    debug : If you want to debug, set "debug=True". False has been set as default.

    Functions
    _____
    action(time_arr movie_time) : Start up DCmotor control according to time_arr.
    terminate() : Finish DCmotor control.
    """

    def __init__(self, PIN, duty=100, Hz=50, debug=False):
        # Initialize
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN, GPIO.OUT)

        # Save member variables
        self.duty = duty
        self.debug = debug
        self.DCmotor = GPIO.PWM(PIN, Hz)

        GPIO.setwarnings(False)

        self.DCmotor.start(0)

    def action(self, time_arr, movie_time):
        start = time.time()
        elapsed_time_int = int(time.time()-start)

        # Control DCmotor according to time_arr
        while elapsed_time_int <= movie_time:
            elapsed_time_int = int(time.time()-start)

            # Turn Off
            if elapsed_time_int not in time_arr:
                self.DCmotor.ChangeDutyCycle(0)
                if self.debug:
                    print("\n", end="")

            # Turn On
            elif elapsed_time_int in time_arr:
                self.DCmotor.ChangeDutyCycle(self.duty)
                if self.debug:
                    print("***************")
                    print("\n", end="")

    def terminate(self):
        if self.debug:
            print("Terminate DCmotor control.")
        self.DCmotor.ChangeDutyCycle(0)
        GPIO.cleanup()


if __name__ == "__main__":
    LOAD_NAME_time_arr = "../time_arr/"+sys.argv[1]+"_"+sys.argv[2]+".npy"
    time_arr = np.load(LOAD_NAME_time_arr)

    LOAD_NAME_movie_time = "../time_arr/"+sys.argv[1]+"_time.npy"
    movie_time = np.load(LOAD_NAME_movie_time)

    PIN_NUM = int(sys.argv[3])

    if len(sys.argv)>=5:
        debug = (sys.argv[4]=="-debug")
        DCmotor = GPIO_CONTROL(PIN=PIN_NUM, debug=debug)
    else:
        DCmotor = GPIO_CONTROL(PIN=PIN_NUM)

    DCmotor.action(time_arr, movie_time)
    DCmotor.terminate()
