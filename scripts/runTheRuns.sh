#!/bin/bash

if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <pattern_folders> <num_cores> <mesh_file> <session_file>"
    exit 1
fi

PATTERN=$1
num_cores=$2
mesh_file=$3
session_file=$4

# Iterate through folders matching the pattern
for folder in ${PATTERN}*/; do
    if [ -d "$folder" ]; then  # Check if it is a directory
        if [ -x "$folder/run.sh" ]; then  # Check if ./run.sh exists and is executable
            echo "Executing ./run.sh in $folder"
            cd "$folder"
            ./run.sh $num_cores $mesh_file $session_file & disown
            cd .. 
        else
            echo "No executable ./run.sh found in $folder"
        fi
    else
        echo "$folder is not a directory"
    fi
done

