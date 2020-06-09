###
### Update the building permits csv to include a geo_point_2d field

#import requests
#import json
import csv
import re
import secrets, filename_secrets
from pathlib import Path
import pandas

## Main

success_count = 0
fail_count = 0
delimiters = re.compile(r'-+|,')
eol = re.compile(r'\n|\r')

# build the filename
pin_file = Path(filename_secrets.workfilesDirectory, 'PIN_lookup_sorted.csv')
permits_file = Path(filename_secrets.productionStaging, 'permits.csv')
updated_permits_file = Path(filename_secrets.productionStaging, 'building_permits.csv')

# load the PIN file into a dictionary
# Fields expected are PIN (key) and geo_point_2d
# data is assumed to be deduplicated
PIN_lookup = {}
with open(pin_file, newline='\n') as csvfile:
    try:
        PIN_data = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in PIN_data:
            PIN_lookup[row[0]] = re.sub(eol, '', row[1])
    except KeyError:
        print(f'Could not create lookup for {row}')
# most common error values
PIN_lookup['nan'] = ""
PIN_lookup['9.80E+11'] = ""
PIN_lookup['9.80E+12'] = ""

# load the csv into a pandas dataframe
permits = pandas.read_csv(permits_file)
# create a new column in the dataframe
permits['geo_point_2d'] = ""

# iterate through the dataframe and update the geo point
for index, permit in permits.iterrows():
    # retrieve the coordinates from the dictionary
    try:
        # cleanup the PIN and only select the first number in the field
        PIN = re.sub(delimiters,'', str(permit['PIN']))
        PIN = re.sub(eol,'', PIN)
        PIN = PIN.split(maxsplit=1)[0]
        permits.at[index, 'geo_point_2d'] = PIN_lookup[PIN]
        success_count += 1
    except (KeyError,IndexError):
        print(f"PIN not found: {PIN}") 
        fail_count += 1

    #if ((success_count + fail_count) % 1000) == 0:
    #    print(f'records processed: {fail_count+success_count}, Success: {success_count}, Failed: {fail_count}')

# write the updated dataframe to the output csv
permits.to_csv(updated_permits_file, index=False)
print(f'Total records: {fail_count+success_count}, Success: {success_count}, Failed: {fail_count}')