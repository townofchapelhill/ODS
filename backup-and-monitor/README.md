# backup-and-monitor README

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/5a7ea515a9014b9a9fd39c0492299661)](https://app.codacy.com/app/TownofChapelHill/backup-and-monitor?utm_source=github.com&utm_medium=referral&utm_content=townofchapelhill/backup-and-monitor&utm_campaign=Badge_Grade_Dashboard)

This repository stores all of the scripts used to create the Task Scheduler backup &amp; monitoring systems for Chapel Hill Open Data

<strong>task-scheduler-backup.ps1</strong>

This is a Powershell script that serves 2 purposes.  The first is to retrieve the XML data for all Open Data tasks in the Task Scheduler on the server.  The second is to produce a CSV with the status of all tasks run from the task manager on this server.  The end product of both of these functions is deposited in the "Task Scheduler Backup" folder on the sharedrive.

<strong>task-scheduler-status.ps1</strong>

This powershell script is an edited version of task-scheduler-backup.ps1 that produces a CSV with the status of all tasks run from the task manager on this server.

<strong>parse-task-status.py & backup.py</strong>

These two scripts are in Python 3 and exist to parse and aggregate the data we need to monitor the health of our task system.  

"backup.py" loops through the XML files output from the Powershell script and consolidates that info within a CSV that lives in the backup folder.  The purpose is to ensure we have a copy of all tasks, their descriptions, and their runtime intervals in the event of a server crash or etc.

"parse-task-status.py" simply reads the CSV produced by the status monitoring function from the Powershell script and grabs the status for all the tasks under the "OpenData" directory.  The script also does some transformation of the contents in the "lastResult" column.  This transformation is designed to increase readability, but it is not 100% accurate.  It will catch and 0x1 and 0x103 (the most common), but it is not designed to catch any others.  Fine tuning may be needed in the future.
