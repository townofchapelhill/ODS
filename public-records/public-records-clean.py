# Import Libraries
import pandas as pd
import os
import shutil
import re

# If previous cleaned file still present, delete it
def check_file_present():
    os.remove('//CHFS/Shared Documents/OpenData/datasets/staging/public-records-cleaned.csv')
    read_edit_file()

# Reads file, converts it to a dataframe, removes PII, writes CSV
def read_edit_file():
    # Read file
    data = pd.read_excel("//CHFS/Shared Documents/OpenData/Public Records Requests/Open Data Public Records Requests.xlsx", sheet_name=None)
    # Make dataframe
    df = pd.DataFrame(data['Public Records Requests'])
    # Remove new line character, street addresses, and email addresses (in that order)
    df = df.replace(r'\n',' ', regex=True)
    df = df.replace(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', 'REDACTED PHONE/PIN', regex=True)
    df = df.replace(r'[[\w\.-]+@[\w\.-]+(\.[\w]+)+', 'REDACTED EMAIL', regex=True)
    df = df.replace(r'(\b\d{1,3}(?:\s[a-zA-Z\u00C0-\u017F]+)+)', 'REDACTED ADDRESS', regex=True)
    # writes CSV
    df.to_csv('//CHFS/Shared Documents/OpenData/Public Records Requests/public-records-cleaned.csv')
    # Call function to move file
    move_file()

def move_file():
    # SRC Path/DEST path (fill in on OD server)
    source = "//CHFS/Shared Documents/OpenData/Public Records Requests/public-records-cleaned.csv"
    destination = "//CHFS/Shared Documents/OpenData/datasets/staging"
    # Does the actual moving
    shutil.move(source, destination)

# Begin script
check_file_present()