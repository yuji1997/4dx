#!/Users/yuji1997/.pyenv/shims/python3
# -*- coding: utf-8 -*-

import pyreaper
import sys
import numpy as np
import cv2
import matplotlib.pyplot as plt
from scipy.io import wavfile
from os import chdir


def voice_analysis():
    # Get command line
    FILENAME = sys.argv[1]
    WAV_FILE = "../wav/"+FILENAME+".wav"
    option = sys.argv[2:]

    # Anlysis
    fs, row_data = wavfile.read(WAV_FILE)
    pm_times, pm, f0_times, f0, corr = pyreaper.reaper(row_data, fs)
    _time = pm_times[-1]

    # Save time length
    SAVE_FILENAME_NPY = "../time_arr/"+FILENAME+"_time.npy"
    np.save(SAVE_FILENAME_NPY, np.array([_time]))

    SAVE_FILENAME_TXT = "../time_arr/"+FILENAME+"_time.txt"
    np.savetxt(SAVE_FILENAME_TXT, np.array([_time]), fmt='%d', delimiter=',')


    # -debug option
    if "-debug" in option:
        fig,axes = plt.subplots(nrows=2,ncols=2,figsize=(14,10))
        # row_data graph
        axes[0,0].plot(row_data, label="Row_data")
        axes[0,0].legend(fontsize=10)

        # freq graph
        axes[0,1].plot(pm_times, pm, linewidth=3, color="red", label="Pitch mark")
        axes[0,1].legend(fontsize=10)

        # pirch mark graph
        axes[1,0].plot(f0_times, f0, linewidth=3, color="green", label="F0 contour")
        axes[1,0].legend(fontsize=10)

        # corr graph
        axes[1,1].plot(f0_times, corr, linewidth=3, color="blue", label="Correlations")
        axes[1,1].legend(fontsize=10)

        plt.show();

    return row_data, f0, f0_times, _time


def picking_yell(f0, f0_times, threshold_freq=350):
    # Get command line
    FILENAME = sys.argv[1]
    option = sys.argv[2:]

    yell_time_arr = np.unique(f0_times[np.where(f0>threshold_freq)[0]].astype(np.int))

    # Save time array
    SAVE_FILENAME_NPY = "../time_arr/"+FILENAME+"_yell.npy"
    np.save(SAVE_FILENAME_NPY, yell_time_arr)

    SAVE_FILENAME_TXT = "../time_arr/"+FILENAME+"_yell.txt"
    np.savetxt(SAVE_FILENAME_TXT, yell_time_arr, fmt='%d', delimiter=',')

    # -debug option
    if "-debug" in option:
        print("\n", end="")
        print("**********")
        print("length of yell_time_arr:"+str(len(yell_time_arr)))
        print("\n", end="")
        print("yell_time_arr")
        print(yell_time_arr)
        print("**********")


def picking_impact(row_data, _time, threshold_amp=15000):
    # Get command line
    FILENAME = sys.argv[1]
    option = sys.argv[2:]

    amp = abs(row_data)
    impact_time_arr = np.where(amp>threshold_amp)[0]/len(amp)*_time
    impact_time_arr = np.unique(impact_time_arr.astype(np.int))

    # Save time array
    SAVE_FILENAME_NPY = "../time_arr/"+FILENAME+"_impact.npy"
    np.save(SAVE_FILENAME_NPY, impact_time_arr)

    SAVE_FILENAME_TXT = "../time_arr/"+FILENAME+"_impact.txt"
    np.savetxt(SAVE_FILENAME_TXT, impact_time_arr, fmt='%d', delimiter=',')

    # -debug option
    if "-debug" in option:
        print("\n", end="")
        print("**********")
        print("length of impact_time_arr:"+str(len(impact_time_arr)))
        print("\n", end="")
        print("impact_time_arr")
        print(impact_time_arr)
        print("**********")


def picking_silence(row_data, _time, threshold_amp=500, threshold_intensity=35):
    # Get command line
    FILENAME = sys.argv[1]
    option = sys.argv[2:]
    MOVIE_FILE = "../movie/"+FILENAME+".mp4"

    cap = cv2.VideoCapture(MOVIE_FILE)

    # Get properties & Define variables
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_num = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    loop_count = 0
    intensity_list = []

    # Print movie properties
    print("\n", end="")
    print("**********")
    print("width:" + str(width))
    print("height:" + str(height))
    print("frame num:" + str(frame_num))
    print("fps:" + str(fps))
    print("movie_time:" + str(_time))
    print("**********")
    print("\n", end="")

    # Processing for each frame
    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            loop_count += 1
            intensity = 0
            gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Calculate average intensity
            for x in range(height):
                for y in range(width):
                    intensity += gray_img[x][y]

            intensity /= (width*height)
            intensity_list.append(intensity)

            # -debug option
            if "-debug" in option:
                print("intensity:{0:.4f}   ".format(intensity), end="")

            # -show option
            if "-show" in option:
                cv2.imshow("Movie", gray_img)

            # KeyboardIntterrupt
            if cv2.waitKey(25) & 0xFF==ord('q'):
                break

            # print %
            print(str(int(100*loop_count/frame_num)) + "% is written.")

        else:
            break

    cap.release()
    cv2.destroyAllWindows()

    # Calculate average intensity
    avg_intensity_arr = np.array(intensity_list)
    length_avg_intensity_arr = len(avg_intensity_arr) 
    length_avg_intensity_arr -= length_avg_intensity_arr % fps
    avg_intensity_arr = avg_intensity_arr[:length_avg_intensity_arr]
    avg_intensity_arr = avg_intensity_arr.reshape(-1, fps).mean(axis=1)
    dark_time_arr = np.where(avg_intensity_arr<threshold_intensity)[0]
    dark_time_arr = np.unique(dark_time_arr.astype(np.int))

    quiet_time_arr = np.where(amp<threshold_amp)[0]/len(amp)*_time
    quiet_time_arr = np.unique(quiet_time_arr.astype(np.int))

    # pick silence, judging from darkness && quietness
    silence_time_arr = np.intersect1d(dark_time_arr, quiet_time_arr)

    # Save time array
    SAVE_FILENAME_NPY = "..time_arr/"+FILENAME+"_silence.npy"
    np.save(SAVE_FILENAME_NPY, silence_time_arr)

    SAVE_FILENAME_TXT = "../time_arr/"+FILENAME+"_silence.txt"
    np.savetxt(SAVE_FILENAME_TXT, silence_time_arr, fmt='%d', delimiter=',')

    # -debug option
    if "-debug" in option:
        print("\n", end="")
        print("**********")
        print("average_intensity_arr")
        print(avg_intensity_arr)
        print("\n", end="")
        print("length of avg_intensity_arr:"+str(len(avg_intensity_arr)))
        print("\n", end="")
        print("silence_time_arr")
        print(silence_time_arr)
        print("**********")


if __name__ == "__main__":
    chdir("/Users/YujiNarita")

    print("\n", end="")
    print("voice anlysis...")
    print("\n", end="")
    row_data, f0, f0_times, _time = voice_analysis()

    print("\n", end="")
    print("picking yell...")
    picking_yell(f0, f0_times)

    print("\n", end="")
    print("picking impact...")
    picking_impact(row_data, _time) 

    print("\n", end="")
    print("picking silence...")
    picking_silence(row_data, _time)
