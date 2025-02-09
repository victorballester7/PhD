#!/bin/bash

# Prompt the user to select the execution mode: local or cluster
read -p "Run in nodes (n) or submit to cluster (p for pbspro or s for slurm)? [n/p/s]: " mode

# Validate user input
if [[ "$mode" != "n" && "$mode" != "p" && "$mode" != "s" ]]; then
    echo "Invalid option. Please choose 'n' for nodes, 'p' for PBS, or 's' for Slurm."
    exit 1
fi

# If running on nodes, prompt for the number of cores and check arguments
if [[ "$mode" == "n" ]]; then
    read -p "Enter the number of cores to use: " num_cores

    if [[ "$#" -lt 2 ]]; then
        echo "Usage: $0 <mesh_file> <session_file> <folder1> <folder2> ..."
        echo "Example: $0 mesh.xml gap_IncNS.xml NumSteps500 NumSteps1000 NumSteps2000"
        exit 1
    fi

    mesh_file=$1
    session_file=$2
    shift 2  # Remove first two arguments
else
    # Cluster mode (PBS/Slurm) should not expect mesh/session files, just folders
    if [[ "$#" -lt 1 ]]; then
        echo "Usage: $0 <folder1> <folder2> ..."
        echo "Example: $0 NumSteps500 NumSteps1000 NumSteps2000"
        exit 1
    fi
fi

# Get all remaining arguments as folders
folders=("$@")

# Iterate through folders
for folder in "${folders[@]}"; do
    if [ -d "$folder" ]; then
        if [[ "$mode" == "n" ]]; then
            echo "Executing run.sh locally in $folder"
            cd "$folder"
            run.sh "$num_cores" "$mesh_file" "$session_file" & disown
            cd ..
        elif [[ "$mode" == "p" ]]; then
            if [[ -f "$folder/pbspro.job" ]]; then
                echo "Submitting PBS job in $folder"
                cd "$folder"
                qsub "pbspro.job"
                cd ..
            else
                echo "No file pbspro.job found in $folder"
            fi
        else  # Slurm mode
            if [[ -f "$folder/slurm.job" ]]; then
                echo "Submitting Slurm job in $folder"
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

