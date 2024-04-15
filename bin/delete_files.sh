#!/bin/bash

# Define the array of allowed directory names
allowed_directories=("busco" "checkm2" "gtdbtk2" "gunc" "quast" "empty_bins")

# Specify the directory to check
directory_to_check=$1

# Loop through the directories in the parent directory
for dir in "${directory_to_check}"/*/; do
    # Check if it's a directory
    if [ -d "$dir" ]; then
        # Extract the directory name from the path
        dir_name=$(basename "$dir")
        # Check if the directory name is not in the allowed array
        if [[ ! " ${allowed_directories[@]} " =~ " ${dir_name} " ]]; then
            # Delete the directory
            rm -rf "$dir"
        fi
    fi
done
