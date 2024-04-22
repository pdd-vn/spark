import csv

import tqdm


def convert_tsv_to_csv(input_file, output_file):
  """
  Converts a TSV file to a CSV file.

  Args:
      input_file (str): Path to the input TSV file.
      output_file (str): Path to the output CSV file.
  """
  try:
    # Open the input TSV file in read mode
    with open(input_file, 'r') as tsvfile:
      # Open the output CSV file in write mode
      with open(output_file, 'w', newline='') as csvfile:
        # Create a CSV writer object
        csv_writer = csv.writer(csvfile)

        # Read the TSV file line by line
        for line in tqdm.tqdm(tsvfile):
          # Split the line based on tabs
          data = line.strip().split('\t')
          # Write the data to the CSV file
          csv_writer.writerow(data)

    print(f"Converted {input_file} to {output_file}")
  except FileNotFoundError:
    print(f"Error: Input file '{input_file}' not found.")

# Get the input and output filenames (can be modified to accept arguments)
# input_file = "samples/amazon_reviews_us_Baby_v1_00_sample.tsv"
# output_file = "samples/amazon_reviews_us_Baby_v1_00_sample.csv"

input_file = "raw/amazon_reviews_us_Baby_v1_00.tsv"
output_file = "raw/amazon_reviews_us_Baby_v1_00.csv"

# Call the conversion function
convert_tsv_to_csv(input_file, output_file)