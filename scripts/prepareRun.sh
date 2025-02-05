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

# Check argument count
if [ "$#" -ne 3 ]; then
    echo -e "${RED}Usage: $0 sessionFile.xml depth width${RESET}"
    echo -e "${YELLOW}Example: $0 sessionFile.xml 4 15${RESET}"
    exit 1
fi

# Get the script's directory
DIR_SCRIPT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"


# Execute the historyPoints.sh script
echo -e "${CYAN}Executing historyPoints.sh...${RESET}"
$DIR_SCRIPT/historyPoints.sh "$1" "$2" "$3"
if [ $? -ne 0 ]; then
    echo -e "${RED}Error executing historyPoints.sh${RESET}"
    exit 1
fi

# Directory to search (current directory)
directory=$(pwd)

# Convert .geo files to .msh
convert_geo2msh

# Convert .msh files to .xml
convert_msh2xml
