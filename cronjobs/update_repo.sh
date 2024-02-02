#!/bin/bash

# GitHub Repo
BACKEND_URL="git@github.com:QuStackZW/rent-a-room.git"
FRONTEND_URL="git@github.com:QuStackZW/rent-a-room-client-side.git"

# Check if project directory exists
if [[ ! -d "/home/andilejaden/Workspace/rent-a-room/backend" ]]; then
    echo "Project directory does not exist."
    exit 1
fi

cd "/home/andilejaden/Workspace/rent-a-room/backend"

# Pull latest changes
git pull -q origin main

# Update dependencies with yarn
yarn install

# Exit with success or failure code
if [[ $? -eq 0 ]]; then
    echo "Successfully updated code."
    exit 0
else
    echo "Error updating code. Check logs for details."
    exit 1
fi
