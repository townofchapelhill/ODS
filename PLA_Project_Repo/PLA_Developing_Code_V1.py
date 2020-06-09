# Imports modules for CSV and Randomization
import csv
import random
from random import randint
import json
import time

# Imports Addresses coming from a csv to be randomize over 47.000 addresses
def Address():
    csvfile = open("addresses.csv", "r")
    reader = csv.reader(csvfile, delimiter=";")
    #usablenums = []
    usabledata = []
    #totalcount = 0
    #for row in reader:
        #usablenums.append(row[0])
        #randomnums = []
        #i = 0
        #while i <= 1:
            #print(usablenums)
            #randomnums.append(random.choice(usablenums))
            #i = i + 1
            #totalcount = totalcount + 1
    for column in reader:
        usabledata.append(column[15])
        randomdata = []
        n = 0
        while n<= 1:
            print(usabledata)
            randomdata.append(random.choice(usabledata))
            n = n + 1
    #usablenums.sort()
    #Question = "What Range Are Your Looking For?"
    #print(Question)
    #FirstInput = input ("Type A Number Please> ")
    #if FirstInput == "Quit":
    #   print("Script Is Ending!")
    #   quit()
    #else:
        #print(FirstInput)
    #for num in usablenums:
        #while num < FirstInput:
            #print(num) 
    # RandNum = 0
    # for num in usablenums:
    #    random.uniform(num,1,100)
    #    num = RandNum
    #    return RandNum
    # counter = 0
    # for num in usablenums:
        # counter = counter + 1
        # return counter

        

# # Call address func

Address()




# JSON

# jsonfile = open("addresses.json", "r")
# sondata = json.load(jsonfile)

# for item in jsondata:
# print(item["datasetid"])
