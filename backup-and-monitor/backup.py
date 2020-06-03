import csv
import os
import glob
import re
import pathlib
from xml.dom import minidom
from xml.dom.minidom import Document
import filename_secrets

# Object for storing data from XML file
class Task(object):
    def __init__(self, name=None, description=None, interval=None, path=None):
        self.name = ''
        self.description = ''
        self.interval = ''
        self.path = ''

# Loops through the XML files outputted from the task scheduler backup command
# calls "parse_xml()" function for each file, deletes XML file when done
def main_loop():
    obj_tasks = []
    path = filename_secrets.taskBackup
    for infile in glob.glob(os.path.join(path, '*.xml') ):
        # initialize new object
        new_task = Task()
        # grab task name
        split_path = str(infile).split("\\")
        title = split_path[1]
        new_task.name = title[:-4]
        # parse the XML content
        parse_xml(infile, new_task)
        # when done parsing, append new_task as dict
        obj_tasks.append(new_task.__dict__)
        # delete XML
        # os.remove(infile)
    # calls format_data()
    format_data(obj_tasks)

# Uses minidom to grab the desired elements out of each XML file
def parse_xml(filename, new_task):
    xmldoc = minidom.parse(filename)

    # grabs description
    description = xmldoc.getElementsByTagName('Description')
    for item in description:
        new_task.description = item.firstChild.nodeValue

    # grabs interval
    interval = xmldoc.getElementsByTagName('Interval')
    for item in interval:
        new_task.interval = item.firstChild.nodeValue

    # grabs path
    path = xmldoc.getElementsByTagName('Command')
    for item in path:
        new_task.path = item.firstChild.nodeValue

# Deals with missing of hard to read data from XML files
def format_data(obj_tasks):
    for entry in obj_tasks:
        if entry['description'] == '':
            entry['description'] = 'Task missing description'
        
        if entry['interval'] == '':
            entry['interval'] = 'Daily'
        else:
            entry['interval'] = entry['interval'][2:]

    write_csv(obj_tasks)

# writes csv output to consolidate desired info
def write_csv(obj_tasks):
    # Create Path to backup directory
    path =  pathlib.Path(filename_secrets.taskBackup)
    # Open csv
    outFile = path.joinpath("task_scheduler_backup.csv")
    with open(outFile, "w") as file:
        fieldnames = obj_tasks[0].keys()
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction='ignore', delimiter=',')
        csv_writer.writeheader()

        for entry in obj_tasks:
            csv_writer.writerow(entry)
        
# begins script
main_loop()