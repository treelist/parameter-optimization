"""
The funtion itself is not important. 
Just doing time consuming calculation and memory allocation repeatedly.
Check if the answer is right.
Write tresult_#_.txt file which the value of execution time is written in.
"""

import sys
import os
import os.path
import errno
import sys
import wave
import struct
import pickle
import time
import datetime

case = sys.argv[1]  # 0: start point, 1~4: four points around start point.
trial = sys.argv[2] # To measure average time, there are three times of running.

import numpy as np

# All wav, pickle files are predefined. Path for them.
if sys.platform == "linux":
    DIRPATH = os.path.abspath("../sample") + "/"
    ANSPATH = os.path.abspath("../answer") + "/"
    RANDPATH = os.path.abspath("../randn") + "/"
else:
    DIRPATH = os.path.abspath("sample") + ("\\" if sys.platform == "win32" else "/")
    ANSPATH = os.path.abspath("answer") + ("\\" if sys.platform == "win32" else "/")
    RANDPATH = os.path.abspath("randn") + ("\\" if sys.platform == "win32" else "/")

# For logging
LOGPATH = "./log/"
try:
    os.makedirs(LOGPATH)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

filename_list = ["canon_mono.wav", "Cloud 9.wav", "Epic.wav", "Holiday.wav", "jatan.wav", "Prelude.wav"] * 6
periods = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 
           9, 7, 9, 3, 2, 3, 8, 4, 6, 2, 6, 4,
           3, 3, 8, 3, 2, 7, 9, 5, 1, 2, 8, 8]
#314159 265358 979323 846264 338327 950288
def stacker_1d(data, value):
    rest = data.shape[0] % value
    
    if not rest == 0:
        data = data[:-rest]
    
    return_data = data.reshape(data.shape[0] // value, value)
    return return_data

wg = []
start_time = time.time()

try:
    for period, filename in zip(periods, filename_list):
        with wave.open(DIRPATH + filename, "rb") as wav:
            wav_params = wav.getparams()
            (nchannels, sampwidth, framerate, nframes, comptype, compname) = wav_params
            frames = wav.readframes(nframes * nchannels)
            out = struct.unpack_from("%dh" % nframes * nchannels, frames)
            
            sample_rate = framerate
            data = np.array(out, dtype=np.int32)

        stacked = stacker_1d(data, sample_rate * period)
        
        result = None
        for i, piece in enumerate(stacked):
            spect = np.fft.fft(piece)
            if (i == 0):
                result = np.abs(spect)
            else:
                result = np.vstack((result, np.abs(spect)))
        
        with open(RANDPATH + "r" + str(period) + ".pickle", "rb") as f:
            rand = pickle.load(f)
        
        result = np.matmul(stacked, rand)
        
        with open(ANSPATH + filename.split(".")[0] + "_" + str(period) + ".pickle", "rb") as f:
            answer = pickle.load(f)
        
        if not np.allclose(result, answer):
            print("wrong")
            wg.append("wrong")
        else:
            print("good")
            wg.append("good")
except MemoryError: # If there is an error, record it.
    wg.append("MemoryError")
except:
    wg.append("Error")

end_time = time.time() # Execution time.

# Write tresult_#_.txt
with open("tresult_" + case + "_" + trial + ".txt", "wt") as fout:
    fout.write(str(end_time - start_time))
    fout.write("\n")
    fout.write("|".join(wg))
    fout.write("\n")

# For logging
with open(LOGPATH + "[" + datetime.datetime.now().strftime("%m%d%H%M%S") + "]" + "tresult_" + case + "_" + trial + ".txt", "wt") as fout:
    fout.write(str(end_time - start_time))
    fout.write("\n")
    fout.write("|".join(wg))
    fout.write("\n")