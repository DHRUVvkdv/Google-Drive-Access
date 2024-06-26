#!/bin/bash

# List of all file types
file_types=("document" "spreadsheet" "presentation" "drawing" "form" "script" "site" "pdf" "folder")

# Loop through each file type and run the Python script
for type in "${file_types[@]}"
do
    echo "Processing $type files..."
    python3 script.py "$type"
    echo "Finished processing $type files."
    echo ""
done

echo "All file types processed."