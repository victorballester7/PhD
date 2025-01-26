Those runs are to verify the correctness of the implementation of the domain, i.e. the independence of the distance lengths before and after the gap and the height of the domain.

The folders are named using the follwing convention: d4_w15_ioh, which means that the gap is taken as 4*deltaStar, the width of the gap is 15*deltaStar and i, o, h \in {1, 2, 3} represent the size of the inflow distance to the gap, outflow distance from the gap and the height of the domain, respectively. 3 being the largest value for each of the parameters and 1 the smallest. In the following table, the values of the parameters are given:

               1     2     3 
------------------------------
i (length/W)   1     3     5
o (length/W)   7     14    20
h (length/D)  

for folder in *; do
    if [ -d "$folder" ]; then  # Check if it's a directory
        mv "$folder" "${folder}_old"
    fi
done

