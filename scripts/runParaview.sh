#!/bin/bash

if [[ -z $1 ]]; then
    echo "Usage: $0 <number_of_cores>"
    echo "Example: $0 4"
    exit 1
fi

# Prompt the user to select the execution mode: local or cluster
read -p "Run in nodes (n) or cluster (c)? [n/c]: " mode

# Validate user input
if [[ "$mode" != "n" && "$mode" != "c" ]]; then
    echo "Invalid option. Please choose 'n' for nodes or 'c' for cluster."
    exit 1
fi

NP=$1
if [[ "$mode" == "n" ]]; then
    PORT=33333
else
    PORT=22222
fi

cd ParaView-*/bin
./mpiexec -np $NP ./pvserver --server-port=$PORT
