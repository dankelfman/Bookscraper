import pandas as pd
import os

# Base directory where your CSV files are located
base_dir = 'D:\\Coding\\Results\\'

# List of your CSV files (replace with your actual file names)
csv_files = ['url_status_1.csv', 'url_status_2.csv', 'url_status_3.csv', 'url_status_4.csv', 'url_status_5.csv', 'url_status_6.csv', 'url_status_7.csv']

# Prepend the base directory to each filename
csv_files = [os.path.join(base_dir, file) for file in csv_files]

# Empty list to store dataframes
dataframes = []

# Loop through the CSV files and append to the list
for file in csv_files:
    if os.path.isfile(file):
        df = pd.read_csv(file, header=0)
        dataframes.append(df)
    else:
        print(f"File not found: {file}")

# Check if any dataframes were added
if dataframes:
    # Concatenate all dataframes in the list
    merged_df = pd.concat(dataframes, ignore_index=True)

    # Save the merged dataframe to a new CSV file in the same directory
    output_file = os.path.join(base_dir, 'merged.csv')
    merged_df.to_csv(output_file, index=False)

    print(f"CSV files have been merged into {output_file}")
else:
    print("No CSV files were found to merge.")
