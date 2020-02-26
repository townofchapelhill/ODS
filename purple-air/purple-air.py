# Dependencies
import requests
import json
import csv
import re
import os
import datetime
import traceback
import filename_secrets

# Open log file
logfilename = os.path.join(filename_secrets.productionStaging, "purpleairlog.txt")
log = open(logfilename, "a")
now = datetime.datetime.now()


def get_purple_air():
    # GET data by device ID
    url = "https://www.purpleair.com/json?show=10586"
    response = requests.get(url)

    try:
        data = json.loads(response.content.decode('utf-8'))
    except RuntimeError:
        log.write(now.strftime("%Y-%m-%d %H:%M") + ": Could not load data from url. \n")
        log.write(traceback.format_exc())

    # Record successfuly GET call in log file
    log.write(now.strftime("%Y-%m-%d %H:%M") + ": Data loaded from url successfully. \n")
    return data

# Retrieves data from Purple Air sensor API
def get_data(info_sheet):
    # stores response info as a variable
    purple_air_info = get_purple_air()

    # creates ordered list of float/integers from stats
    p = re.compile(r"[-+]?\d*\.\d+|\d+")
    stats_0 = p.findall(purple_air_info["results"][0]["Stats"])
    stats_1 = p.findall(purple_air_info["results"][1]["Stats"])

    # deletes unwanted indexes in lists
    for i in sorted([1, 3, 5, 7, 9, 11], reverse=True):
        del stats_0[i]
        del stats_1[i]

    # writes air quality data to CSV
    writer = csv.writer(info_sheet)
    writer.writerow([ 
                     datetime.datetime.utcfromtimestamp(purple_air_info["results"][0]["LastSeen"]).replace(tzinfo=datetime.timezone.utc),
                     purple_air_info["results"][0]["PM2_5Value"],
                     # I have no idea why this syntax is so weird, but it works
                     stats_0[1],
                     stats_0[2],
                     stats_0[3],
                     stats_0[4],
                     stats_0[5],
                     stats_0[6],
                     purple_air_info["results"][0]["temp_f"],
                     purple_air_info["results"][0]["humidity"], 
                     purple_air_info["results"][0]["pressure"],
                     purple_air_info["results"][0]["Label"], 
                     purple_air_info["results"][0]["DEVICE_LOCATIONTYPE"],
                     purple_air_info["results"][0]["Lat"], 
                     purple_air_info["results"][0]["Lon"],
                     purple_air_info["results"][0]["Uptime"],
                     purple_air_info["results"][0]["RSSI"], 
                     purple_air_info["results"][0]["AGE"]
                     ])


# main function to create log and call get_data
def write_sheet():
    infofilename = os.path.join(filename_secrets.productionStaging, "purple-air.csv")
    info_sheet = open(infofilename, "a")

    # if there is data in the response, write CSV headers
    if os.stat(infofilename).st_size == 0:
        writer = csv.writer(info_sheet)
        writer.writerow(["Last Check", "Current Particulate Matter 2.5 Value (PM 2.5)", "PM 2.5 10 Minute Avg.", "PM 2.5 30 Minute Avg.", 
                         "PM 2.5 1 Hour Avg.", "PM 2.5 6 Hour Avg.", "PM 2.5 24 Hour Avg.", "PM 2.5 One Week Avg.",
                          "Temp (F)", "Humidity (%)", "Pressure (mbar)",
                         "Site Label", "Inside/Outside", "Latitude", "Longitude", "Uptime (Seconds)", "RSSI (WiFi signal strength dBm)", 
                         "Hardware Issues", "Age of Data at Check (minutes)"])

    try:
        get_data(info_sheet)
    except RuntimeError:
        # If write function fails, record in log file
        log.write(now.strftime("%Y-%m-%d %H:%M") + ": Could not gather data. \n")
        log.write(traceback.format_exc())
    # Record Success in log file    
    log.write(now.strftime("%Y-%m-%d %H:%M") + ": Data gathered successfully. \n")

    # Close open files
    info_sheet.close()
    log.close()


# Begin program
write_sheet()
