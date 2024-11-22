#!/bin/bash

# Description: This script converts the output (checkpoint) files to .vtu format in order to visualize the results in Paraview or similar.

# Usage: run from the directory where the .chk are stored and then do: $directory_of_scripts/fieldconvert.sh mesh.xml sessionFile.xml  

# look for number of files of the form xxxx_i.chk in the directory

# show error if there are exactly no 2 arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 mesh.xml sessionFile.xml"
    exit 1
fi


# Directory to search (change '.' to the target directory if needed)
directory=$(pwd)

# Count the number of files matching the pattern
folder_count=$(find "${directory}" -type d -name "*.chk" | wc -l)

# extract name of $1 without extension
name=$(echo $1 | cut -f 1 -d '.')

for i in $(seq 0 $((folder_count-1))); do 
    # check if theres is already a .vtu file, in that case, skip
    if [ -f "${name}_${i}.vtu" ]; then
        echo "File ${name}_${i}.vtu already exists. Skipping..."
        continue
    fi
    # Convert the files to .vtu format
    FieldConvert -f $1 $2 ${name}_${i}.chk ${name}_${i}.vtu;
done
if [ -f "${name}.fld" ]; then
    FieldConvert -f $1 $2 ${name}.fld ${name}_${folder_count}.vtu
fi
