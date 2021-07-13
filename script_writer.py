"""
script_writer.py is to make change.txt. Only a and b are changable.
"""
import sys
import os
import errno
import datetime

a = sys.argv[1]
b = sys.argv[2]

# For logging
LOGPATH = "./log/"
try:
    os.makedirs(LOGPATH)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

# Insertion orders
insert = [
"94\n",
"    sz = (unsigned int)(a * (sz + b));\n",
"104\n",
"    sz = (unsigned int)(a * (sz + b));\n",
"121\n",
"    sz = (unsigned int)(a * (sz + b));\n",
"136\n",
"    sz = (unsigned int)(a * (sz + b));\n",
"148\n",
"    sz = (unsigned int)(a * (sz + b));\n"]

# Changing orders.
change = [
"29\n",
"#define NCACHE 7 /* number of cache entries per bucket */\n",
"#define NCACHE 7 + 4 /* number of cache entries per bucket */\n",
"86\n",
"\n",
"double a = " + str(a) + ";\n",
"87\n",
"\n",
"unsigned int b = " + str(b) + ";\n",
"205\n",
"\n",
"    size = (unsigned int)(a * (size + b));\n",
"227\n",
"\n",
"    size = (unsigned int)(a * (size + b));\n",
"268\n",
"\n",
"    size = (unsigned int)(a * (size + b));\n"]

# Write change.txt
with open("change.txt", "wt") as fout:
    fout.write("numpy_source/numpy/core/src/multiarray/alloc.c\n") # alloc.c is the target code. Always same place.
    fout.write("\n\n")
    fout.write("".join(insert))
    fout.write("\n\n")
    fout.write("".join(change))

# For logging
with open(LOGPATH + "[" + datetime.datetime.now().strftime("%m%d%H%M%S") + "]" + "change.txt", "wt") as fout:
    fout.write("numpy_source/numpy/core/src/multiarray/alloc.c\n")
    fout.write("\n\n")
    fout.write("".join(insert))
    fout.write("\n\n")
    fout.write("".join(change))