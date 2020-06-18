from xml.dom import minidom
from xml.dom.minidom import Document
import pathlib
import urllib.request
import csv
import re
import os, sys
import filename_secrets

# global file locations
stagingDirectory = pathlib.Path(filename_secrets.productionStaging)
newReservations = stagingDirectory.joinpath("new_reservations.csv")

# logging data
log_message={}

# Constructor to hold data
class Reservation(object):
    def __init__(self, startDate=None, startTime=None, endDate=None, endTime=None, description=None, location=None, status=None):
        self.startDate = ''
        self.startTime = ''
        self.endDate = ''
        self.endTime = ''
        self.description = ''
        self.location = ''
        self.status = ''

# Clears previous file to write new one, ensuring CSV always shows 30 days from current day
def clear_file():
    global newReservations
    try:
        if os.stat(newReservations).st_size != 0:
            os.remove(newReservations)
    except:
        log_message['Message'] = "File cound not be deleted " + str(newReservations)
        print(log_message)
        # print(f'{newReservations} could not be deleted')
    return

# GET request to Demco's XML feed to retrieve data
def get_reservations(day):
    global reservationsXML

    # only returns one day at a time, hence the loop
    url = "http://chapelhill.evanced.info/spaces/patron/spacesxml?dm=xml&do=" + str(day)
    decoded_url = urllib.request.urlopen(url).read().decode('utf-8')
    stripped_url_list = "<root>" + decoded_url[52:-14] + "</root>" + "\n"

    parse_xml(stripped_url_list, day)

# Traverses and parses the XML to access desired data
def parse_xml(stripped_url_list, day):
    global reservationsXML
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
    global newReservations
    for res in obj_reservations:
        # remove any new line characters from the description columnS
        scrubbed_value = re.sub('[^A-Za-z0-9_\-\.: ]', ' ', str(res['description']))
        res['description'] = scrubbed_value

    with open(newReservations, 'a') as res_headers:
        try:
            fieldnames = obj_reservations[0].keys()
            csv_writer = csv.DictWriter(res_headers, fieldnames=fieldnames, extrasaction='ignore', delimiter=',')
            if os.stat(newReservations).st_size == 0:
                csv_writer.writeheader()
        except:
            pass

        for entry in obj_reservations:
            csv_writer.writerow(entry)
    return

# start script
if __name__ == '__main__':
    clear_file()
    for day in range(30):
        get_reservations(day)
    log_message['Message'] = "Run Complete"
    print(log_message)