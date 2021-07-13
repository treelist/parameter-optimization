#!/bin/bash

# Set maximum generation: in this case 10.
for ((i=0;i<10;i++))
do
  ./block.sh
  mkdir result$i    # Make directory for logging.
  cp *.txt result$i # Copy all result to the directory.
done
