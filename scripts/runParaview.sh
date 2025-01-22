#!/bin/bash

if [[ -z $1 ]]; then
    echo "Usage: $0 <number_of_cores>"
    echo "Example: $0 4"
    exit 1
fi

NP=$1
PORT=22222

cd ParaView-*/bin
./mpiexec -np $NP ./pvserver --server-port=$PORT
