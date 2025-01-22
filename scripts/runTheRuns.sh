#!/bin/bash

# Prompt the user to select the execution mode: local or cluster
read -p "Run in nodes (n) or submit to cluster (p for pbspro or s for slurm)? [n/p/s]: " mode

# Validate user input
if [[ "$mode" != "n" && "$mode" != "p" && "$mode" != "s" ]]; then
    echo "Invalid option. Please choose 'n' for nodes or 'c' for cluster."
    exit 1
fi

# If running on nodes, prompt for the number of cores
if [[ "$mode" == "n" ]]; then
    read -p "Enter the number of cores to use: " num_cores
fi

# Check if the correct number of arguments is passed
if [[ "$mode" == "n" && "$#" -ne 3 ]]; then
    echo "Usage: $0 <pattern_folders> <mesh_file> <session_file>"
    echo "Example: $0 NumSteps mesh.xml gap_IncNS.xml"
    exit 1
fi

if [[ ("$mode" == "p" || "$mode" == "s") && "$#" -ne 1 ]]; then
    echo "Usage: $0 <pattern_folders>"
    echo "Example: $0 NumSteps"
    exit 1
fi


PATTERN=$1
mesh_file=$2
session_file=$3

# Iterate through folders matching the pattern
for folder in ${PATTERN}*/; do
    if [ -d "$folder" ]; then  # Check if it is a directory
        if [ "$mode" == "n" ]; then
          echo "Executing run.sh locally in $folder"
          cd "$folder"
          run.sh $num_cores $mesh_file $session_file & disown
          cd ..
        elif [ "$mode" == "p" ]; then
            if [ -f "$folder/pbspro.job" ]; then  # Check if ./pbspro.job exists and is executable
              echo "Submitting run as a PBS job in $folder"
              cd "$folder"
              qsub "pbspro.job"
              cd ..
            else
              echo "No file pbspro.job found in $folder"
            fi
        else
            if [ -f "$folder/slurm.job" ]; then  # Check if ./slurm.job exists and is executable
              echo "Submitting run as a Slurm job in $folder"
              cd "$folder"
              sbatch "slurm.job"
              cd ..
            else
              echo "No file slurm.job found in $folder"
            fi
        fi
    else
        echo "$folder is not a directory"
    fi
done

