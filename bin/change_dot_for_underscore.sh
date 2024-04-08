#!/bin/bash

# Navigate to the directory containing the files
directory=$1

# Loop through each file in the directory
for file in "$directory"/*.*; do
    # Extract the file extension
    extension="${file##*.}"
    # Extract the filename without extension
    filename="${file%.*}"
    # Replace dots with underscores only in the filename
    new_filename="${filename//./_}"
    # Create the new file name
    new_file="${new_filename}.${extension}"
    # Rename the file
    mv "$file" "$new_file"
    echo "Renamed '$file' to '$directory/$new_file'"
done

