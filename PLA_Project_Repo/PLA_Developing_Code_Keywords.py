# Imports modules for CSV and Randomization
import csv
import random
from random import randint
import json
import pandas as pd
import os

# # Imports Addresses coming from a csv to be randomize over 47.000 addresses
def PandasExporting():
    csvfile = '/Users/HardyLewis/Desktop/PLA Work Folder/PLA_Project_Repo/addresses.csv'
    pandasread = pd.read_csv(csvfile,delimiter=';')
    #Keywords = []
    print(pandasread)
    #usablenums = []
    #randonAddresses = []
    #for column in pandasread:
        #i = 0 
        #while i<= 10:
            #randomAddresses.append(column)
            #print(randomAddressses)
        

    
PandasExporting()

