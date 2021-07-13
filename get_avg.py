"""
get_avg.py collects all results of testing in current directory, and make file about average values.
"""

import sys
import os
import errno
import datetime

# For logging
LOGPATH = "./log/"
try:
    os.makedirs(LOGPATH)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

# Collect results
file_list = os.listdir("./")
mprof_list = [file for file in file_list if file.startswith("mprofile") and file.endswith(".dat")]
tresult_list = [file for file in file_list if file.startswith("tresult") and file.endswith(".txt")]

if len(mprof_list) != len(tresult_list):
    print("Something wrong")

case = tresult_list[0].split("_")[1]
print(case)

# Read mprof file and return maximum value.
def get_max(file_name):
    with open(file_name, "rt") as fin:
        lines = fin.readlines()
    mems = [float(line.split(" ")[1]) for line in lines[1:]]
    return max(mems)

# Read tresult file and return time value. If there is an error message in file, return -1.
def get_time(file_name):
    with open(file_name, "rt") as fin:
        time, info = fin.read().strip().split("\n")
    
    if "Error" in info:
        return -1
    else:
        return float(time)

# Calculate average
def get_avg(val_list):
    if -1 in val_list:
        return -1
    return sum(val_list) / len(val_list)

# From the file list, pick value.
mprof_list = list(map(get_max, mprof_list))
tresult_list = list(map(get_time, tresult_list))

# Write result file containg average value
with open("aresult_" + case + ".txt", "wt") as  fout:
    fout.write(str(get_avg(mprof_list)))
    fout.write(" ")
    fout.write(str(get_avg(tresult_list)))
    fout.write("\n")

# For logging
with open(LOGPATH + "[" + datetime.datetime.now().strftime("%m%d%H%M%S") + "]" + "aresult_" + case + ".txt", "wt") as  fout:
    fout.write(str(get_avg(mprof_list)))
    fout.write(" ")
    fout.write(str(get_avg(tresult_list)))
    fout.write("\n")