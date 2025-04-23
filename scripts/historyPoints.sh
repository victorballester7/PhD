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

# Point 0: (-50, 1, 0)
# Point 1: (-30, 1, 0)
# Point 2: (-10, 1, 0)
# Point 3: (0, 1, 0)
# Point 4: (W / 4, 1, 0)
# Point 5: (W / 4, -D / 3, 0)
# Point 6: (W / 4, -2D / 3, 0)
# Point 7: (W / 2, 1, 0)
# Point 8: (W / 2, -D / 3, 0)
# Point 9: (W / 2, -2D / 3, 0)
# Point 10: (3W / 4, 1, 0)
# Point 11: (3W / 4, -D / 3, 0)
# Point 12: (3W / 4, -2D / 3, 0)
# Point 13: (W, 1, 0)
# Point 14: (W + 20, 1, 0)
# Point 15: (W + 60, 1, 0)
# Point 16: (W + 150, 1, 0)
# Point 17: (W + 300, 1, 0)
# Point 18: (W + 500, 1, 0)
# Point 19: (W + 700, 1, 0)
# Point 20: (W + 900, 1, 0)

historyPoints=(
    "-50 1 0"
    "-30 1 0"
    "-10 1 0"
    "0 1 0"
    "$(echo "$width / 4" | bc -l) 1 0"
    "$(echo "$width / 4" | bc -l) $(echo "-$depth / 3" | bc -l) 0"
    "$(echo "$width / 4" | bc -l) $(echo "-2 * $depth / 3" | bc -l) 0"
    "$(echo "$width / 2" | bc -l) 1 0"
    "$(echo "$width / 2" | bc -l) $(echo "-$depth / 3" | bc -l) 0"
    "$(echo "$width / 2" | bc -l) $(echo "-2 * $depth / 3" | bc -l) 0"
    "$(echo "3 * $width / 4" | bc -l) 1 0"
    "$(echo "3 * $width / 4" | bc -l) $(echo "-$depth / 3" | bc -l) 0"
    "$(echo "3 * $width / 4" | bc -l) $(echo "-2 * $depth / 3" | bc -l) 0"
    "$(echo "$width" | bc -l) 1 0"
    "$(echo "$width + 20" | bc -l) 1 0"
    "$(echo "$width + 60" | bc -l) 1 0"
    "$(echo "$width + 150" | bc -l) 1 0"
    "$(echo "$width + 300" | bc -l) 1 0"
    "$(echo "$width + 500" | bc -l) 1 0"
    "$(echo "$width + 700" | bc -l) 1 0"
    "$(echo "$width + 900" | bc -l) 1 0"
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
if [ $? -ne 0 ]; then
    echo -e "${RED}Error inserting history points into $sessionFile.${RESET}"
    exit 1
fi

echo -e "${GREEN}History points successfully added to $sessionFile.${RESET}"

