#!/bin/bash

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'  # No Color

function determineJobType() {
    if command -v qstat &> /dev/null; then
        echo 'p'  # PBS Pro detected
    elif command -v scontrol &> /dev/null; then
        echo 's'  # Slurm detected
    else
        echo 'n'  # Neither detected
    fi
}


# Function to read user input
function inputRead() {
    # Prompt the user to select the execution mode: local or cluster
    # echo -e "${CYAN}Select execution mode: Local (n), PBS (p), or Slurm (s):${NC}"
    # read -n 1 -p "Run in nodes (n) or submit to cluster (p for pbspro or s for slurm)? [n/p/s]: " mode
    # echo -e " " # New line
    
    mode=$(determineJobType)

    echo -e "${CYAN}Execution mode: $mode${NC}"

    # Validate user input
    if [[ "$mode" != "n" && "$mode" != "p" && "$mode" != "s" ]]; then
        echo -e "${RED}Invalid option. Please choose 'n' for nodes, 'p' for PBS, or 's' for Slurm.${NC}"
        exit 1
    fi

    # If running on nodes, prompt for the number of cores and check arguments
    if [[ "$mode" == "n" ]]; then
        read -p "Enter the number of cores to use: " num_cores

        if [[ "$#" -lt 2 ]]; then
            echo -e "${YELLOW}Usage: $0 <mesh_file> <session_file> <folder1> <folder2> ...${NC}"
            echo -e "${YELLOW}Example: $0 mesh.xml gap_IncNS.xml NumSteps500 NumSteps1000 NumSteps2000${NC}"
            exit 1
        fi

        mesh_file=$1
        session_file=$2
        echo -e "${CYAN}Mesh file: $mesh_file${NC}"
        echo -e "${CYAN}Session file: $session_file${NC}"
        shift 2  # Remove first two arguments
    else
        # Cluster mode (PBS/Slurm) should not expect mesh/session files, just folders
        if [[ "$#" -lt 1 ]]; then
            echo -e "${YELLOW}Usage: $0 <folder1> <folder2> ...${NC}"
            echo -e "${YELLOW}Example: $0 NumSteps500 NumSteps1000 NumSteps2000${NC}"
            exit 1
        fi
    fi
}

function getFolders() {
    for arg in "$@"; do
        if [[ "$arg" == *"*"* ]]; then
            folders+=( $(find . -maxdepth 1 -type d \( -name "$arg" \) | sort) )
        else
            folders+=("$arg")
        fi
    done
}

function runJobs() {
    # Iterate through folders
    for folder in "${folders[@]}"; do
        if [ -d "$folder" ]; then
            if [[ "$mode" == "n" ]]; then
                echo -e "${GREEN}Executing run.sh locally in $folder${NC}"
                cd "$folder"
                runLocally.sh "$num_cores" "$mesh_file" "$session_file" & disown
                cd ..
            elif [[ "$mode" == "p" ]]; then
                if [[ -f "$folder/pbspro.job" ]]; then
                    echo -e "${GREEN}Submitting PBS job in $folder${NC}"
                    cd "$folder"
                    qsub $PBSJOB
                    cd ..
                else
                    echo -e "${RED}No file pbspro.job found in $folder${NC}"
                fi
            else  # Slurm mode
                if [[ -f "$folder/slurm.job" ]]; then
                    echo -e "${GREEN}Submitting Slurm job in $folder${NC}"
                    cd "$folder"
                    sbatch $SLURMJOB
                    cd ..
                else
                    echo -e "${RED}No file slurm.job found in $folder${NC}"
                fi
            fi
        else
            echo -e "${RED}$folder is not a directory${NC}"
        fi
    done
}

SLURMJOB="slurm.job"
PBSJOB="pbspro.job"

inputRead "$@"

getFolders "$@"

runJobs
