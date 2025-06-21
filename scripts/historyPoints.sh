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

# Point 0: (-100, 1, 0)
# Point 1: (-75, 1, 0)
# Point 2: (-50, 1, 0)
# Point 3: (-35, 1, 0)
# Point 4: (-25, 1, 0)
# Point 5: (-15, 1, 0)
# Point 6: (-10, 1, 0)
# Point 7: (-5, 1, 0)
# Point 8: (0, 1, 0)
# Point 9: (1, 1, 0)
# Point 10: (1, -D / 3, 0)
# Point 11: (1, -2D / 3, 0)
# Point 12: (5, 1, 0)
# Point 13: (5, -D / 3, 0)
# Point 14: (5, -2D / 3, 0)
# Point 15: (10, 1, 0)
# Point 16: (10, -D / 3, 0)
# Point 17: (10, -2D / 3, 0)
# ...
# Point 18: (W, 1, 0)
# Point 19: (W + 5, 1, 0)
# Point 20: (W + 10, 1, 0)
# Point 21: (W + 15, 1, 0)
# Point 22: (W + 25, 1, 0)
# Point 23: (W + 35, 1, 0)
# Point 24: (W + 50, 1, 0)
# Point 25: (W + 75, 1, 0)
# Point 26: (W + 100, 1, 0)
# Point 27: (W + 125, 1, 0)
# Point 28: (W + 150, 1, 0)
# Point 29: (W + 175, 1, 0)
# Point 30: (W + 200, 1, 0)
# Point 31: (W + 250, 1, 0)
# Point 32: (W + 300, 1, 0)
# Point 33: (W + 350, 1, 0)
# Point 34: (W + 400, 1, 0)
# Point 35: (W + 450, 1, 0)
# Point 36: (W + 500, 1, 0)
# Point 37: (W + 550, 1, 0)
# Point 38: (W + 600, 1, 0)
# Point 39: (W + 650, 1, 0)
# Point 40: (W + 700, 1, 0)
# Point 41: (W + 750, 1, 0)
# Point 42: (W + 800, 1, 0)
# Point 43: (W + 850, 1, 0)
# Point 44: (W + 900, 1, 0)
# Point 45: (W + 950, 1, 0)
# Point 46: (W + 1000, 1, 0)

historyPoints=()

# upstream points
for offset in 100 75 50 35 25 15 10 5; do
    historyPoints+=("-$offset 1 0")
done

historyPoints+=("0 1 0")

# points inside the gap
x=5
step=5
while (( $(echo "$x < $width" | bc -l) )); do
    historyPoints+=("$x 1 0")
    historyPoints+=("$x $(echo "-$depth / 2" | bc -l) 0")
    x=$(echo "$x + $step" | bc -l)
done

# downstream points
for offset in 0 5 10 15 25 35 50 75 100 125 150 175 200 225 250 275 300 325 350 375 400 425 450 475 500 525 550 575 600 625 650 675 700 725 750 775 800 825 850 875 900 925 950 975 1000; do
    x=$(echo "$width + $offset" | bc -l)
    historyPoints+=("$x 1 0")
done


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

