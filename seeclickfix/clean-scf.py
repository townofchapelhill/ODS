# Imports dependencies
import re
import os
import csv
import pathlib
import secrets, filename_secrets
from more_itertools import unique_everseen

# clean function
def clean():
    
    # opens original file to read & second file to write the cleaned version
    stagingPath = pathlib.Path(filename_secrets.productionStaging)
    inputFile = stagingPath.joinpath('seeclickfix_all.csv')
    outputFile = stagingPath.joinpath('seeclickfix_clean.csv')
    with open(inputFile, "r") as infile, open(outputFile, "w") as outfile:

        # assigning vairables
        reader = csv.reader(infile)
        headers = next(reader, None)
        writer = csv.writer(outfile)
        cleaned_lines = []
        seen = set()
        
        # if the target CSV has headers, write them
        if headers:
            writer.writerow(headers)

        # loops through each row in file
        for row in reader:
            cleaned_row = []

            # loops through each entry in row, removing any non alphanumeric characters
            # stores new entry in cleaned_row list
            for entry in row:
                scrubbed_entry = re.sub('[^A-Za-z0-9_\-\.: ]', '', str(entry))
                cleaned_row.append(scrubbed_entry)
                if len(cleaned_row) >= 39:
                    cleaned_lines.append(cleaned_row)

        # writes the clean data to the new file
        for line in cleaned_lines:
            writer.writerow(unique_everseen(line))

# starts the program
if __name__ == '__main__':
    clean()