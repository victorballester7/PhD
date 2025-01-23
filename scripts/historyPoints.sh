#!/bin/bash
# Description: This script inserts history points into a Nektar session .xml file 
# based on the depth and width of the domain using float division.

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 sessionFile.xml depth width"
    echo "Example: $0 sessionFile.xml 4 15"
    exit 1
fi

sessionFile=$1
depth=$2
width=$3
x0=$(echo "4 * $depth" | bc -l)

# Validate the existence of the session file
if [ ! -f "$sessionFile" ]; then
    echo "Error: File $sessionFile not found."
    exit 1
fi

# Use sed to remove only the lines between <PARAM NAME="Points"> and </PARAM>
sed '/<PARAM NAME="Points">/,/<\/PARAM>/ {
    /<PARAM NAME="Points">/b
    /<\/PARAM>/b
    d
}' "$sessionFile" > "file.tmp"

mv "file.tmp" "$sessionFile"

# Create the list of history points
historyPoints=(
    "$(echo "$x0 + $width / 4" | bc -l) $(echo "$depth / 2" | bc -l) 0"
    "$(echo "$x0 + $width / 4" | bc -l) $(echo "-$depth / 3" | bc -l) 0"
    "$(echo "$x0 + $width / 4" | bc -l) $(echo "-2 * $depth / 3" | bc -l) 0"
    "$(echo "$x0 + $width / 2" | bc -l) $(echo "$depth / 2" | bc -l) 0"
    "$(echo "$x0 + $width / 2" | bc -l) $(echo "-$depth / 3" | bc -l) 0"
    "$(echo "$x0 + $width / 2" | bc -l) $(echo "-2 * $depth / 3" | bc -l) 0"
    "$(echo "$x0 + 3 * $width / 4" | bc -l) $(echo "$depth / 2" | bc -l) 0"
    "$(echo "$x0 + 3 * $width / 4" | bc -l) $(echo "-$depth / 3" | bc -l) 0"
    "$(echo "$x0 + 3 * $width / 4" | bc -l) $(echo "-2 * $depth / 3" | bc -l) 0"
    "$(echo "$x0 + $width" | bc -l) $(echo "$depth / 2" | bc -l) 0"
    "$(echo "$x0 + 3 * $width / 2" | bc -l) $(echo "$depth / 2" | bc -l) 0"
    "$(echo "$x0 + 2 * $width" | bc -l) $(echo "$depth / 2" | bc -l) 0"
)

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

echo "History points successfully added to $sessionFile."
