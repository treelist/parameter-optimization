"""
code_changer.py get change.txt as a argument. Following the instruction in change.txt, change target code.
"""

import sys

# Get change.txt.
order = sys.argv[-1]
print(order)

# Open change.txt.
with open(order, "rt") as fin:
    parts = fin.read().split("\n\n\n")

path = parts[0].strip()                     # The path of target code.
insert_lines = parts[1].strip().split("\n") # Insertion orders.
change_lines = parts[2].strip().split("\n") # Changing orders.

print(path)
# Read the target code.
with open(path, "rt") as fin:
    code_lines = fin.readlines()

"""
>> Example of insertion order(2 lines) <<
94
    sz = a * (sz + b);
>> Insert the line "    sz = a * (sz + b);" to the line number 94
"""
for i in range(0, len(insert_lines), 2):
    line_number = int(insert_lines[i])
    if line_number == -1: # To ignore inserting part.
        break
    inserting = insert_lines[i + 1] + "\n"
    code_lines.insert(line_number - 1, inserting)

"""
>> Example of insertion order(3 lines) <<
29
#define NCACHE 7 /* number of cache entries per bucket */
#define NCACHE 7 + 4 /* number of cache entries per bucket */
>> Change line number 29 
>> from "#define NCACHE 7 /* number of cache entries per bucket */"
>> to   "#define NCACHE 7 + 4 /* number of cache entries per bucket */"
"""
for i in range(0, len(change_lines), 3):
    line_number = int(change_lines[i])
    before = change_lines[i + 1] + "\n"
    after = change_lines[i + 2] + "\n"
    
    if (code_lines[line_number - 1] != before):
        print("something wrong")
    code_lines[line_number - 1] = after

# Overwrite target code.
with open(path, "wt") as fout:
    fout.write("".join(code_lines))