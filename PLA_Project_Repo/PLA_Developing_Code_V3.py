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
    pandasread = pd.read_csv(csvfile,delimiter=';',index_col=11)
    df = pd.DataFrame.to_csv(pandasread,sep=',',columns=11,chunksize=47000)
    for column in df:
        Address = []
        Address.append(column)    
        print(Address)
    #usablenums = []
    #randonAddresses = []
    #for column in pandasread:
        #i = 0 
        #while i<= 10:
            #randomAddresses.append(column)
            #print(randomAddressses)
        

    
PandasExporting()


