#!/bin/bash

# Get the input file name as the first argument
input_file="$1"

# Check if a file is provided
if [ -z "$input_file" ]; then
  echo "Please provide a TSV file name as an argument."
  exit 1
fi

# Get the filename without extension
filename="${input_file%.*}"

# Output file with .csv extension
output_file="$filename.csv"

# Convert the file using awk (tab to comma, enclose in double quotes)
awk -v ORS='\n' 'BEGIN{FS="\t"} {OFS=","} {for (i=1; i<=NF; ++i) printf "\"%s\"%s", $i, (i<NF) ? "," : "" }' "$input_file" > "$output_file"

echo "Converted $input_file to $output_file"