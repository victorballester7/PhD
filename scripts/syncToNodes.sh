#!/bin/bash

# Define local and remote paths
LOCAL_DIR="$HOME/Desktop/PhD"
REMOTE_USER="vb824"   # Replace with your username on typhoon
REMOTE_HOST="typhoon"
REMOTE_DIR="~/Desktop/PhD"

# Sync docs and scripts directly
rsync -avz --progress "$LOCAL_DIR/docs" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/"
rsync -avz --progress "$LOCAL_DIR/scripts" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/"
rsync -avz --progress "$LOCAL_DIR/src/" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/runs/"

