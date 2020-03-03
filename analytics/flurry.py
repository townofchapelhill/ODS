# Import required libraries 
import requests
import json
import datetime
import time
import os
import traceback
# Import API secrets file
import secrets 
import filename_secrets
# Import and set up logger
import logging

#logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
log_file = os.path.join(filename_secrets.logfilesDirectory, "flurry_log.out")

# Set up a specific logger with our desired output level
logging.basicConfig(filename=log_file,format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)
#logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)

# Write date at beginning of log file
now = str(datetime.date.today())
#log_file.write(now +"\n")
logging.debug("Starting flurry.py at " + now)

# Access specific flurry query, pass header authentication, store data in var
def get_flurry():
    
    # Find date and create vars to hold the span of one day 
    # Write in format sierra understands
    now = str(datetime.date.today())
    one_day_ago = str(datetime.date.today() - datetime.timedelta(days=1))
    date_string = one_day_ago + "/" + now
    
    # Flurry API call, date string is updated to cover daily stats
    url = "https://api-metrics.flurry.com/public/v1/data/appUsage/day/company/app/language?metrics=sessions,activeDevices,newDevices,timeSpent,averageTimePerDevice,averageTimePerSession&dateTime=" + date_string
    # Take API token from secrets file
    headers = {"Authorization":"Bearer " + str(secrets.flurry_api_token)}
    # Access json data
    data = requests.get(url,headers=headers).json()
    data_list = data["rows"]
    
    # Write success to log file 
    #log_file.write("Flurry data successfully accessed." + "\n")
    logging.debug("Flurry API call successful")
    
    # Open the file to write/append to 
    # Stored in flurry folder with open data directory
    # Open CSV to store data
    full_filename = os.path.join(filename_secrets.productionStaging, "flurry.csv")

    try:
        flurrycsv = open(full_filename, "a", encoding='utf-8')
    except IOError:
        logging.debug("Cannot open output file " + flurrycsv)
    else:
        logging.debug("Succesfully opened output file " + flurrycsv)

    # Write CSV headings if the file is empty
    if os.stat(flurrycsv).st_size == 0:
        flurrycsv.write("Company Name, Average Time Per Session, Active Devices, Language, Time Spent, Sessions, Date and Time, Average Time Per Device, App Name, New Devices"+"\n")
        logging.debug("The file " + flurrycsv + "is empty. Writing headers to " + flurrycsv)

    # Set counter
    i = 0

    # Write/append the data to the file once the headings have been added
    # Write data in CSV format
    logging.debug("Writing data to " + flurrycsv)
    while i < len(data_list):
        flurrycsv.write(data_list[i]['company|name'] + ", ")
        flurrycsv.write(str(data_list[i]['averageTimePerSession'])+ ", ")
        flurrycsv.write(str(data_list[i]['activeDevices'])+ ", ")
        flurrycsv.write(data_list[i]['language|name']+ ", ")
        flurrycsv.write(str(data_list[i]['timeSpent'])+ ", ")
        flurrycsv.write(str(data_list[i]['sessions'])+ ", ")
        flurrycsv.write(data_list[i]['dateTime']+ ", ")
        flurrycsv.write(str(data_list[i]['averageTimePerDevice'])+ ", ")
        flurrycsv.write(data_list[i]['app|name']+ ", ")
        flurrycsv.write(str(data_list[i]['newDevices']))
        flurrycsv.write("\n")
        i += 1 
    flurrycsv.close()
    
    # Write success to log file 
    logging.debug("Writing data to " + flurrycsv + " complete")
    #log_file.write("Flurry data successfully written to flurrydata directory. \n")
   
# Main function
def main():
    # Handle exceptions, print errors to log file
    try:
        get_flurry()
    except Exception as exc:
        logging.debug("There was an error running the program.")
        logging.debug(traceback.format_exc() + "\n")

# Call main
if __name__== "__main__":
    main()
