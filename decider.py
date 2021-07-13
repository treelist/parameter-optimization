"""
decider.py is to set pairs of a and b based on the result of step before.
"""
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

# Get results of step before.
file_list = os.listdir("./")
aresult_list = [file for file in file_list if file.startswith("aresult") and file.endswith(".txt")]

# Changing ratio
RATIO = 0.95

# Open aresult.txt and get values. (# of step, memory consumption, execution time).
def get_val(result):
    num = int(result.split(".")[0].split("_")[1])
    
    with open(result, "rt") as fin:
        mem, time = fin.read().strip().split(" ")
    return num, float(mem), float(time)

if not aresult_list: # This is first start.
    # Initializing.
    a = 2.5
    b = 100
    ap = 0.5
    bp = 30
    ar = 1.0
    br = 1.0
    
    # For four points. a +- delta(a), b +- delta(b).
    p_a = max(1.0, a - (a * ap))
    a_p = a + (a * ap)
    
    p_b = max(0, b - bp)
    b_p = b + bp
    
    # For check.
    with open("record.txt", "wt") as fout:
        fout.write("{:f} {:d} {:f} {:d} {:f} {:f}\n".format(a, b, ap, bp, ar, br))
    
    # cache.txt for next step.
    # String point, and four points around it.
    with open("cache.txt", "wt") as fout:
        fout.write("{:f} {:d} {:f} {:d} {:f} {:f}\n".format(a, b, ap, bp, ar, br))
        fout.write("{:f} {:d}\n".format(a, b))
        fout.write("{:f} {:d}\n".format(p_a, p_b))
        fout.write("{:f} {:d}\n".format(p_a, b_p))
        fout.write("{:f} {:d}\n".format(a_p, p_b))
        fout.write("{:f} {:d}\n".format(a_p, b_p))
else: # There is preceding step.
    # Read cache.txt wrote before step. Old parameters.
    with open("cache.txt", "rt") as fin:
        record = fin.readlines()
    old_a, old_b, old_ap, old_bp, old_ar, old_br = record[0].strip().split(" ")
    
    # Old (a, b) of 5 points (1 start point, 4 around points).
    olds = []
    for line in record[1:]:
        temp_a, temp_b = line.strip().split(" ")
        olds.append((float(temp_a), int(temp_b)))
    
    old_point = olds[0] # Old start point.
    # Get difference of (a, b) between old starting and each four points.
    diff = []
    for old in olds[1:]:
        diff.append((old[0] - old_point[0], old[1] - old_point[1]))
    
    print("diff:")
    print(diff)
    
    # Read aresult.txt files. There must be 5 aresult.txt file.
    vals = []
    for aresult in aresult_list:
        num, _, time = get_val(aresult)
        if num == 0 or time == -1:
            continue
        vals.append((num, time))
    vals.sort(key=lambda x: x[1], reverse=True) # Sort the list by execution time.
    
    print("vals:")
    print(vals)
    
    sum_diff_a = 0.0 # For sum of a values.
    sum_diff_b = 0   # For sum of b values.
    s = 0
    
    # vals is sorted by execution time. i is used as weight.
    for i, (num, _) in enumerate(vals, 1):
        s += i
        sum_diff_a += i * diff[num - 1][0] # diff[0]: point1, diff[1]: point2, ..
        sum_diff_b += i * diff[num - 1][1]
    
    # Set new ar, br
    ar = float(old_ar) * RATIO
    br = float(old_br) * RATIO
    
    # Set new start point.
    a = float(old_a) + ar * (sum_diff_a / s)
    if sum_diff_b == 0:
        b = int(old_b)
    else:
        b = int(int(old_b) + int(old_bp) * br * (sum_diff_b /abs(sum_diff_b)))
    
    print("new a:", a, " new b:", b)
    # Set new ap, bp
    ap = float(old_ap) * RATIO
    bp = int(int(old_bp) * RATIO)
    
    # For four points. a +- delta(a), b +- delta(b).
    p_a = max(1.0, a - (a * ap))
    a_p = a + (a * ap)
    
    p_b = max(0, b - bp)
    b_p = b + bp
    
    # For check. This is "at".
    with open("record.txt", "at") as fout:
        fout.write("{:f} {:d} {:f} {:d} {:f} {:f}\n".format(a, b, ap, bp, ar, br))
    
    # cache.txt for next step.
    # String point, and four points around it.
    with open("cache.txt", "wt") as fout:
        fout.write("{:f} {:d} {:f} {:d} {:f} {:f}\n".format(a, b, ap, bp, ar, br))
        fout.write("{:f} {:d}\n".format(a, b))
        fout.write("{:f} {:d}\n".format(p_a, p_b))
        fout.write("{:f} {:d}\n".format(p_a, b_p))
        fout.write("{:f} {:d}\n".format(a_p, p_b))
        fout.write("{:f} {:d}\n".format(a_p, b_p))

# parameters.txt are used other codes.
# String point, and four points around it.
with open("parameters.txt", "wt") as fout:
    fout.write("{:f} {:d}\n".format(a, b))
    fout.write("{:f} {:d}\n".format(p_a, p_b))
    fout.write("{:f} {:d}\n".format(p_a, b_p))
    fout.write("{:f} {:d}\n".format(a_p, p_b))
    fout.write("{:f} {:d}\n".format(a_p, b_p))

# For logging
with open(LOGPATH + "[" + datetime.datetime.now().strftime("%m%d%H%M%S") + "]" + "parameters.txt", "wt") as fout:
    fout.write("{:f} {:d}\n".format(a, b))
    fout.write("{:f} {:d}\n".format(p_a, p_b))
    fout.write("{:f} {:d}\n".format(p_a, b_p))
    fout.write("{:f} {:d}\n".format(a_p, p_b))
    fout.write("{:f} {:d}\n".format(a_p, b_p))
