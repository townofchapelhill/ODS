from xml.dom import minidom
from xml.dom.minidom import Document
import os, sys
import urllib.request
import csv
import re
import pathlib
import filename_secrets

# globals 
stagingDirectory = pathlib.Path(filename_secrets.productionStaging)
aggregateReservations = stagingDirectory.joinpath("aggregate_reservations.csv")
firstPass = True
# logging data
log_message={}

class Reservation(object):
    def __init__(self, startDate=None, startTime=None, endDate=None, endTime=None, description=None, location=None, status=None):
        self.startDate = ''
        self.startTime = ''
        self.endDate = ''
        self.endTime = ''
        self.description = ''
        self.location = ''
        self.status = ''

# GET request to Demco's XML feed to retrieve data
def get_reservations(day):
    # only returns one day at a time, hence the loop
    url = "http://chapelhill.evanced.info/spaces/patron/spacesxml?dm=xml&do=" + str(day)
    decoded_url = urllib.request.urlopen(url).read().decode('utf-8')
    stripped_url_list = "<root>" + decoded_url[52:-14] + "</root>" + "\n"
    parse_xml(stripped_url_list, day)

# Traverses and parses the XML to access desired data
def parse_xml(stripped_url_list, day):
    obj_reservations = []

    # try/catch handles days that return incompatible responses (typically holidays)
    # skips response that failed, moves onto next day
    try:
        xmldoc = minidom.parseString(stripped_url_list)
    except:
        log_message['Message'] = "Error parsing XML " + str(stripped_url_list) + " for day " + str(day)
        print(log_message)
        # print(f'Error parsing XML {stripped_url_list} for day {day}')
        return

    res_list = xmldoc.getElementsByTagName('item')
    # return on an empty list
    if len(res_list) == 0:
        return

    for item in res_list:
        # initialize new object
        new_res = Reservation()
        new_res.startDate = item.firstChild.firstChild.nodeValue

        # Node traversal
        startTime_list = item.getElementsByTagName('time')
        for time in startTime_list:
            new_res.startTime = time.firstChild.nodeValue
        
        endDate_list = item.getElementsByTagName('enddate')
        for endDate in endDate_list:
            new_res.endDate = endDate.firstChild.nodeValue
        
        endTime_list = item.getElementsByTagName('endtime')
        for endTime in endTime_list:
            new_res.endTime = endTime.firstChild.nodeValue

        description_list = item.getElementsByTagName('description')
        for description in description_list:
            new_res.description = description.firstChild.nodeValue

        location_list = item.getElementsByTagName('location')
        for location in location_list:
            new_res.location = location.firstChild.nodeValue

        status_list = item.getElementsByTagName('status')
        for status in status_list:
            new_res.status = status.firstChild.nodeValue
        
        obj_reservations.append(new_res.__dict__)
    
    write_csv(obj_reservations, day)

# writes the CSV
def write_csv(obj_reservations, day):
    global aggregateReservations, firstPass
    for res in obj_reservations:
        # remove any new line characters from the description columnS
        scrubbed_value = re.sub('[^A-Za-z0-9_\-\.: ]', ' ', str(res['description']))
        res['description'] = scrubbed_value

    with open(aggregateReservations, 'a') as res_headers:
        try:
            fieldnames = obj_reservations[0].keys()
            csv_writer = csv.DictWriter(res_headers, fieldnames=fieldnames, extrasaction='ignore', delimiter=',')
            if os.stat(aggregateReservations).st_size == 0:
                csv_writer.writeheader()
        except:
            pass

        for entry in obj_reservations:
            csv_writer.writerow(entry)
    return

# start script
if __name__ == '__main__':
    # accumulate all reservations for the past 143 days
    #for day in range(-143,0):
    #    get_reservations(day)

    # append only the previous day's reservations to the file
    get_reservations(0)
    
    log_message['Message'] = "Run Complete"
    print(log_message)