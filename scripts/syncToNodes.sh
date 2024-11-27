#!/bin/bash

# Define local and remote paths
LOCAL_DIR="$HOME/Desktop/PhD"
REMOTE_USER="vb824"  
REMOTE_DIR="~/Desktop/PhD"

# List of remote hosts
HOSTS=("typhoon" "hpc")

# Loop through each host and sync the directories
for HOST in "${HOSTS[@]}"; do
    echo "Syncing with $HOST..."
    rsync -avz --progress "$LOCAL_DIR/docs" "$REMOTE_USER@$HOST:$REMOTE_DIR/"
    rsync -avz --progress "$LOCAL_DIR/scripts" "$REMOTE_USER@$HOST:$REMOTE_DIR/"
    rsync -avz --progress "$LOCAL_DIR/src/" "$REMOTE_USER@$HOST:$REMOTE_DIR/runs/"
done

