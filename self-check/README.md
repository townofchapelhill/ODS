# Self Check circulation dataset processing

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/5782c72547a6484aa3388715c21330ae)](https://app.codacy.com/app/TownofChapelHill/self-check?utm_source=github.com&utm_medium=referral&utm_content=townofchapelhill/self-check&utm_campaign=Badge_Grade_Dashboard)

## Convert the Self Check XML or Excel files to aggregated CSV

### Goal 
Process the XML or XLSX files to extract daily or hourly statistics

### Purpose 
Provides Hourly and Daily KPIs for the library Self-Check stations

### Methodology 
1. Scheduled report files from the Bibliotheca web portal are sent to the Opendata email
2. An outlook macro downloads the attachment to a predetermined folder on the town fileshare
3. OD script pulls file from folder, appends to existing file
4. OD powershell script dedups the data
5. OD loads to ODS and publishes on a regular schedule

### Data Source
libraryconnect.com - selfcheck reports sent to opendata@townofchapelhill.org
(for XLSX) a file_util module locates the input file

### Output 
A csv file is stored in a directory location set in an environment variable
(for XLSX) The filename selected is based on the last modification date of the input file
### Transformations

(for Hourly) Output is limited to Library Open Hours, which is stored in the code as a Dictionary - library_hours

### Constraints

#### Library Open Hours
Changes to Library Open Hours currently requires a code change.

#### report structure changes
Changes to the Bibliotheca file structure will require remapping the variables.
#### Input/Output Files
File locations are stored in filename_secrets.py or loaded into environment variables 

#### Libraries Required
[untangle (XML)](https://untangle.readthedocs.io/en/latest/) library via ```pip3 install untangle``` in the run environment

[openpyxl (xlsx)](https://openpyxl.readthedocs.io) library via ```pip install openpyxl``` in the run environment
