#!/bin/bash

# Description: This script converts all the mesh files .msh (from gmsh) in the current directory to .xml format for later Nektar use.
# On top of that, it adds the history points to the session file (otherwise I forget to execute that script before submitting simulations).

# Usage: Run from the directory where the .msh files are stored:
# $directory_of_scripts/nekmesh.sh  

# Define colors
RED="\e[31m"
GREEN="\e[32m"
YELLOW="\e[33m"
CYAN="\e[36m"
RESET="\e[0m"

# execute historyPoints.sh
function hisPoints {
    # Execute the historyPoints.sh script
    echo -e "${CYAN}Executing historyPoints.sh...${RESET}"
    $DIR_SCRIPT/historyPoints.sh $1 $2 $3
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error executing historyPoints.sh${RESET}"
        exit 1
    fi
}


# Function to convert .geo files to .msh
function convert_geo2msh {
    # Find .msh files in the directory
    files=($(find "${directory}" -maxdepth 1 -type f -name "*.geo" | sort))

    # If no files are found, exit with a message
    if [ ${#files[@]} -eq 0 ]; then
        echo -e "${YELLOW}No .geo files found in the directory.${RESET}"
        exit 1
    fi

    # Loop through the files and convert them
    for file in "${files[@]}"; do
        # Extract the basename of the file
        name=$(basename "${file}" .msh)

        echo -e "${CYAN}Processing: ${file}${RESET}"

        # Convert the file to .msh format
        gmsh -2 "${file}"

        if [ $? -eq 0 ]; then
            echo -e "${GREEN}File ${name}.msh created successfully.${RESET}"
        else
            echo -e "${RED}Error converting ${file} to msh.${RESET}"
        fi
    done
}

# Function to convert .msh files to .xml
function convert_msh2xml {
    # Find .msh files in the directory
    files=($(find "${directory}" -maxdepth 1 -type f -name "*.msh" | sort))

    # If no files are found, exit with a message
    if [ ${#files[@]} -eq 0 ]; then
        echo -e "${YELLOW}No .msh files found in the directory.${RESET}"
        exit 1
    fi

    # Loop through the files and convert them
    for file in "${files[@]}"; do
        # Extract the basename of the file
        name=$(basename "${file}" .msh)

        echo -e "${CYAN}Processing: ${file}${RESET}"
        
        # Convert the file to .xml format
        NekMesh "${file}" "${name}.xml"

        if [ $? -eq 0 ]; then
            echo -e "${GREEN}File ${name}.xml created successfully.${RESET}"
        else
            echo -e "${RED}Error converting ${name}.msh to XML.${RESET}"
        fi
    done
}

function editJobs {
  codename="d${depth%.}_w${width%.}"

  # Check if there are any .job files in the current directory
  if ls *.job 1> /dev/null 2>&1; then
    for job_file in *.job; do
      # If the job_file contains the pattern 'pbspro'
      if [[ "$job_file" == *pbspro* ]]; then
        sed -i "s/^#PBS -N .*/#PBS -N ${codename}/" "${job_file}"
      # If the job_file contains the pattern 'slurm'
      else 
        sed -i "s/^#SBATCH --job-name=.*/#SBATCH --job-name=${codename}/" "${job_file}"
      fi
    done
  else
    echo -e "${YELLOW}No .job files found in the current directory.${RESET}"
  fi   
}

# Get the script's directory
DIR_SCRIPT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

source $DIR_SCRIPT/bashFunctions/getMeshSessionFiles.sh
source $DIR_SCRIPT/bashFunctions/getDepthANDWidth.sh

# Check argument count
if [ "$#" -ge 1 ]; then
    echo -e "${CYAN}A directory argument is provided. Moving to ${1}${RESET}"
    cd "$1" || { echo -e "${RED}Failed to change directory to $1${RESET}"; exit 1; }
fi

# Directory to search (current directory)
directory=$(pwd)

# Convert .geo files to .msh
convert_geo2msh

# Convert .msh files to .xml
convert_msh2xml

# Get the session file
getMeshSessionFiles > /dev/null

depthANDwidth=$(getDepthANDWidth $mesh_file)
depth=$(echo $depthANDwidth | awk '{print $1}')
width=$(echo $depthANDwidth | awk '{print $2}')

echo -e "${CYAN}Depth: $depth${RESET}"
echo -e "${CYAN}Width: $width${RESET}"

# execute historyPoints.sh
hisPoints $session_file $depth $width

# Edit the job files
editJobs
