#!/bin/bash

python decider.py >> shell_log.txt # Set a, b and write the information to "parameters.txt"

params="parameters.txt"

i=0 # For the argument of fft_test.py
while read -r line # read lines of "parameters.txt"
do
  python script_writer.py $line     # Read change.txt.

  cp -r ../numpy_source ./          # Bring numpy source code.

  python code_changer.py change.txt # Change target code.

  cd ./numpy_source                 # Build numpy
  python setup.py build_ext -i      #|
  cp -r ./numpy ../                 #|
  cd ../                            #|

  for ((j=0;j<3;j++))               # Run test code three times.
  do                                #|
    mprof run fft_test.py $i $j  #|
    sleep 1                         #|
  done                              #|

  python get_avg.py                 # From the results, summarize them.

  mv mprofile_*.dat ./log/          # For logging

  rm change.txt                     # Delete intermediate files 
  rm tresult_*.txt                  #|
  rm -r numpy_source                #|
  rm -r numpy                       #|

  i=`expr $i + 1`                   # i += 1
  sleep 1
done < $params

rm parameters.txt # Delete "parameters.txt"
