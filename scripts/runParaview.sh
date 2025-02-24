#!/bin/bash

# Define colors
RED="\e[31m"
GREEN="\e[32m"
YELLOW="\e[33m"
CYAN="\e[36m"
RESET="\e[0m"

if [[ -z $1 ]]; then
    echo -e "${RED}Usage: $0 <number_of_cores>${RESET}"
    echo -e "${YELLOW}Example: $0 4${RESET}"
    exit 1
fi

# Prompt the user to select the execution mode: local or cluster
read -n 1 -p "$(echo -e "${CYAN}Run in nodes (n) or cluster (c)? [n/c]: ${RESET}")" mode

# Validate user input
if [[ "$mode" != "n" && "$mode" != "c" ]]; then
    echo -e "${RED}Invalid option. Please choose 'n' for nodes or 'c' for cluster.${RESET}"
    exit 1
fi

NP=$1
PORT=22222  # Default to cluster port
[[ "$mode" == "n" ]] && PORT=33333

echo -e "${YELLOW}Using $NP cores.${RESET}"
echo -e "${YELLOW}Starting ParaView server on port $PORT...${RESET}"

cd ParaView-*/bin || { echo -e "${RED}Error: Could not change directory to ParaView-*/bin${RESET}"; exit 1; }
./mpiexec -np $NP ./pvserver --server-port=$PORT

echo -e "${GREEN}ParaView server started successfully.${RESET}"

