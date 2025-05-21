#!/bin/bash

# Define colors
RED="\e[31m"
GREEN="\e[32m"
YELLOW="\e[33m"
CYAN="\e[36m"
RESET="\e[0m"

# Define local and remote paths
LOCAL_DIR="$HOME/Desktop/PhD"
REMOTE_USER="vb824"  
REMOTE_DIR="~/Desktop/PhD"

# List of remote hosts
HOSTS=("typhoon" "hpc")
SYNC_DIRS=("${LOCAL_DIR}/docs" "${LOCAL_DIR}/scripts")

# I set the src directory separately as it is synced to the runs directory on the remote hosts (which does not exist locally)
SRC_DIR="${LOCAL_DIR}/src"
RUNS_DIR="${REMOTE_DIR}/runs"

# Loop through each host and sync the directories
for HOST in "${HOSTS[@]}"; do
    echo -e "${YELLOW}Syncing with $HOST...${RESET}"
    for DIR in "${SYNC_DIRS[@]}"; do
        rsync -avz --progress "$DIR" "$REMOTE_USER@$HOST:$REMOTE_DIR/"
    done
    rsync -avz --progress "$SRC_DIR/" "$REMOTE_USER@$HOST:$RUNS_DIR"

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Sync with $HOST completed successfully!${RESET}"
    else
        echo -e "${RED}Sync with $HOST failed!${RESET}"
    fi
done

