#!/bin/bash

# Description: This script converts all the mesh files .msh (from gmsh) in the current directory to .xml format for later Nektar use .

# Usage: Run from the directory where the .msh files are stored:
# $directory_of_scripts/nekmesh.sh  

# Directory to search (change '.' to the target directory if needed)
directory=$(pwd)

# Find files matching the patterns (*.chk or *.fld) and store them in an array
files=($(find "${directory}" -maxdepth 1 -type f -name "*.msh" | sort))

# If no files are found, exit with a message
if [ ${#files[@]} -eq 0 ]; then
    echo "No .msh files found in the directory."
    exit 1
fi

# Loop through the files and convert them
for file in "${files[@]}"; do
    # Extract the basename of the folder
    name=$(basename "${file}" .msh)

    # Convert the file to .vtu format using FieldConvert
    NekMesh "${file}" "${name}.xml"

    echo "File ${name}.xml created."
done

