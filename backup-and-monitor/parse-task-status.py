import csv
import os
import pathlib
import filename_secrets

class Task(object):
    def __init__(self, name=None, lastResult=None):
        self.name = ''
        self.lastResult = ''

def read_csv():
    task_list = []
    taskPath = pathlib.Path(filename_secrets.taskBackup)
    inputFile = taskPath.joinpath('script_status.csv')
    with open(inputFile, 'r', newline='') as old_file:
        has_header = next(old_file, None)
        old_file.seek(0)
        task_data = csv.reader(old_file, delimiter=",")
        if has_header:
            next(task_data)
        for row in task_data:
            if row[1][1:9] == "OpenData":
                new_task = Task()
                new_task.name = row[0]
                new_task.lastResult = row[2]
                new_task.resultCode = row[2]
                new_task.timeStamp  = row[3]
                task_list.append(new_task.__dict__)

    transform_and_write_result(task_list)

def transform_and_write_result(task_list):
    for entry in task_list:
        if int(entry['lastResult']) == 1 or int(entry['lastResult']) == 259:
            entry['lastResult'] = 'Broken'
        else:
            entry['lastResult'] = 'Working'
    stagingPath = pathlib.Path(filename_secrets.productionStaging)
    outputFile = stagingPath.joinpath('task-status.csv')
    with open(outputFile, 'w', newline='') as new_file:
        fieldnames = task_list[0].keys()
        csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames, extrasaction='ignore', delimiter=',')

        if os.stat(outputFile).st_size == 0:
            csv_writer.writeheader()

        for entry in task_list:
            csv_writer.writerow(entry)

read_csv()

    