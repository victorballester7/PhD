#!/bin/bash

# Description: This script converts the output (checkpoint) files (*.chk or *.fld) to .vtu format 
# in order to visualize the results in Paraview or similar.

# Usage: Run from the directory where the .chk or .fld files are stored:
# $directory_of_scripts/fieldconvert.sh mesh.xml sessionFile.xml  

# Check for exactly 2 arguments (mesh.xml and sessionFile.xml)
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 mesh.xml sessionFile.xml"
    exit 1
fi

# Directory to search (change '.' to the target directory if needed)
directory=$(pwd)

# Find files matching the patterns (*.chk or *.fld) and store them in an array
files=($(find "${directory}" -maxdepth 1 -type d \( -name "*.chk" -o -name "*.fld" \) | sort))

# If no files are found, exit with a message
if [ ${#files[@]} -eq 0 ]; then
    echo "No .chk or .fld files found in the directory."
    exit 1
fi

# Loop through the files and convert them
for file in "${files[@]}"; do
    # Extract the basename of the folder
    name=$(basename $(basename "${file}" .chk) .fld)

    # Check if the corresponding .vtu file already exists, skip if it does
    if [ -f "${name}.vtu" ]; then
        echo "File ${name}.vtu already exists. Skipping..."
        continue
    fi

    # Convert the file to .vtu format using FieldConvert
    FieldConvert -f "$1" "$2" "${file}" "${name}.vtu"
done



# # Description: This script converts the output (checkpoint) files to .vtu format in order to visualize the results in Paraview or similar.

# # Usage: run from the directory where the .chk are stored and then do: $directory_of_scripts/fieldconvert.sh mesh.xml sessionFile.xml  

# # look for number of files of the form xxxx_i.chk in the directory

# # show error if there are exactly no 2 arguments
# if [ "$#" -ne 2 ]; then
#     echo "Usage: $0 mesh.xml sessionFile.xml"
#     exit 1
# fi


# # Directory to search (change '.' to the target directory if needed)
# directory=$(pwd)

# # Count the number of files matching the pattern
# folder_count=$(find "${directory}" -type d -name "*.chk" | wc -l)

# # extract name of $1 without extension
# name=$(echo $1 | cut -f 1 -d '.')

# for i in $(seq 0 $((folder_count-1))); do 
#     # check if theres is already a .vtu file, in that case, skip
#     if [ -f "${name}_${i}.vtu" ]; then
#         echo "File ${name}_${i}.vtu already exists. Skipping..."
#         continue
#     fi
#     # Convert the files to .vtu format
#     FieldConvert -f $1 $2 ${name}_${i}.chk ${name}_${i}.vtu;
# done

