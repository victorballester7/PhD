#!/bin/bash

# Check if the correct number of arguments is passed
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <pattern_folders> <mesh_file> <session_file>"
    exit 1
fi

PATTERN=$1
mesh_file=$2
session_file=$3

# Prompt the user to select the execution mode: local or cluster
read -p "Run in nodes or submit to cluster (pbspro)? [n/c]: " mode

# Validate user input
if [[ "$mode" != "n" && "$mode" != "c" ]]; then
    echo "Invalid option. Please choose 'n' for nodes or 'c' for cluster."
    exit 1
fi

if [ "$mode" == "n" ]; then
    read -p "Enter the number of cores to use: " num_cores
fi


# Iterate through folders matching the pattern
for folder in ${PATTERN}*/; do
    if [ -d "$folder" ]; then  # Check if it is a directory
        if [ "$mode" == "n" ]; then
          echo "Executing run.sh locally in $folder"
          cd "$folder"
          run.sh $num_cores $mesh_file $session_file & disown
          cd ..
        else
            if [ -f "$folder/pbspro.job" ]; then  # Check if ./pbspro.job exists and is executable
              echo "Submitting run as a PBS job in $folder"
              cd "$folder"
              qsub "pbspro.job"
              cd ..
            else
              echo "No file pbspro.job found in $folder"
            fi
        fi
    else
        echo "$folder is not a directory"
    fi
done

