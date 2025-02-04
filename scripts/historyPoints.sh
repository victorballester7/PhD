#!/bin/bash
# Description: This script inserts history points into a Nektar session .xml file 
# based on the depth and width of the domain using float division.

# Define colors
RED="\e[31m"
GREEN="\e[32m"
YELLOW="\e[33m"
CYAN="\e[36m"
RESET="\e[0m"

# Check argument count
if [ "$#" -ne 3 ]; then
    echo -e "${RED}Usage: $0 sessionFile.xml depth width${RESET}"
    echo -e "${YELLOW}Example: $0 sessionFile.xml 4 15${RESET}"
    exit 1
fi

sessionFile=$1
depth=$2
width=$3

# Validate the existence of the session file
if [ ! -f "$sessionFile" ]; then
    echo -e "${RED}Error: File $sessionFile not found.${RESET}"
    exit 1
fi

echo -e "${CYAN}Processing session file: $sessionFile${RESET}"

# Use sed to remove only the lines between <PARAM NAME="Points"> and </PARAM>
sed '/<PARAM NAME="Points">/,/<\/PARAM>/ {
    /<PARAM NAME="Points">/b
    /<\/PARAM>/b
    d
}' "$sessionFile" > "file.tmp"

mv "file.tmp" "$sessionFile"
echo -e "${GREEN}Previous history points removed.${RESET}"

# Create the list of history points
historyPoints=(
    "$(echo "$width / 4" | bc -l) $(echo "$depth / 2" | bc -l) 0"
    "$(echo "$width / 4" | bc -l) $(echo "-$depth / 3" | bc -l) 0"
    "$(echo "$width / 4" | bc -l) $(echo "-2 * $depth / 3" | bc -l) 0"
    "$(echo "$width / 2" | bc -l) $(echo "$depth / 2" | bc -l) 0"
    "$(echo "$width / 2" | bc -l) $(echo "-$depth / 3" | bc -l) 0"
    "$(echo "$width / 2" | bc -l) $(echo "-2 * $depth / 3" | bc -l) 0"
    "$(echo "3 * $width / 4" | bc -l) $(echo "$depth / 2" | bc -l) 0"
    "$(echo "3 * $width / 4" | bc -l) $(echo "-$depth / 3" | bc -l) 0"
    "$(echo "3 * $width / 4" | bc -l) $(echo "-2 * $depth / 3" | bc -l) 0"
    "$(echo "$width" | bc -l) $(echo "$depth / 2" | bc -l) 0"
    "$(echo "3 * $width / 2" | bc -l) $(echo "$depth / 2" | bc -l) 0"
    "$(echo "2 * $width" | bc -l) $(echo "$depth / 2" | bc -l) 0"
)

echo -e "${CYAN}Inserting history points into $sessionFile...${RESET}"

# Insert the history points into the session file
awk -v points="${historyPoints[*]}" '
    BEGIN { split(points, arr, " ") }
    /<PARAM NAME="Points">/ {
        print
        for (i = 1; i <= length(arr); i++) {
            if (i % 3 == 1) x = arr[i]
            else if (i % 3 == 2) y = arr[i]
            else print "    " x, y, arr[i]
        }
        next
    }
    { print }
' "$sessionFile" > temp.xml && mv temp.xml "$sessionFile"

echo -e "${GREEN}History points successfully added to $sessionFile.${RESET}"

