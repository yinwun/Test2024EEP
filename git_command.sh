#!/bin/bash

# Get the current date in YYYY-MM-DD format
today=$(date +"%Y-%m-%d_%H-%M-%S-%3N")

# Set the branch name using the current date
BRANCH_NAME="branch_$today"

# Navigate to your Git repository
cd /mnt/c/Users/Test/Documents/GitHub/Test2024EEP || { echo "Repository not found"; exit 1; }

# Create the new branch
git checkout -b "$BRANCH_NAME"

# Stage all files
git add .

# Set commit message
COMMIT_MESSAGE="Initial commit"

# Commit the changes
git commit -m "$COMMIT_MESSAGE"

# Push the changes to the remote repository
git push -u origin "$BRANCH_NAME"

echo
echo "All operations completed successfully."
