# public-records
Small utility built to clean the Public records Request .xlsx file received on the Open Data Server

<strong>Purpose:</strong>

This script is intended to automate the ETL process for our Public Records Requests dataset.  It grabs the .xlsx file that gets dropped into the Public Records folder on the share drive and performs a regex cleaning operations to remove any sensitive information.

Due to the nature of the data, the cleaning functions are not 100% effective. Some of the process is currently handled manually, but an improvement to the cleaning functions would be a welcome addition.
