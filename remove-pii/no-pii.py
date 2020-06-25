# importing dependencies
import csv
import sys
import os
import pandas
import scrubadub
import datasync
import time

dirty_data = []

check_list = ['Email', 'Emails', 'Name', 'Names', 'Credit Card', 'Phone Number', 'Phone', 'Telephone',
'Credit Card Number', 'Email Address', 'Address', 'Street Address', 'First Name', 'Last Name', 'PIN Number', 'PIN',
'Member Name', 'Pass #', 'Pass Code', 'Fees/Tax', 'Amt Paid', 'Age', 'Full Name', 'Household #', 'Item Code',
'Member', 'Amount', 'User Name', 'Primary Contact', 'Email Address', 'Primary Guardian', 'Enrollee', 'Household'
'Property Owner', 'Property Address', 'Contractor Contact Details', 'Contractors']

to_drop = []

# select file to open, display data in command line
def findFile():
    for i in dirty_data:
        fileName = i
        print(os.path.abspath("../datasets/" + fileName) + ".csv")
        df = pandas.read_csv(os.path.abspath("../remove-pii/datasets/" + fileName) + ".csv", error_bad_lines=False, encoding='latin_1')
        print("===============================")
        confirmDelete(df, fileName)

# checks with user to confirm if more rows need cleaning
def checkFinished(df, fileName):
    print("============================================================")
    df.to_csv(fileName + "_scrubbed.csv", encoding='utf-8', index = False)
    print('Scrubbed file complete.')
    print("===============================")
    dirty_data.pop(0)
    findFile()

# scrubs the data from the chosen column
# only does one at a time, working on improving that
def scrubData(df, fileName):
    print("===============================")
    print("Scrubbing data... (larger datasets can take time)")
    print("===============================")
    # line 41 does all the work
    df.drop(to_drop, axis=1, inplace=True)
    to_drop.clear()
    checkFinished(df, fileName)

# iterates over list of common PII and compares against the names of column headers
# in a given .csv.  If there are any matches, those matches populate the "to_drop" list
def confirmDelete(df, fileName):
    for column in df:
        for i in check_list:
            if i == column:
                to_drop.append(i)
    print('Here are the Column headers that will be searched for: ')
    print(to_drop)
    scrubData(df, fileName)

# calls confirmDelete function
findFile()