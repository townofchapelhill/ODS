# public-records
Small utility built to clean the Public records Request .xlsx file received on the Open Data Server

<strong>Note: This script is redundant. The Public Records Officer manually creates this dataset and all information is redacted before submisssion.</strong>

This script is intended to automate the ETL process for our Public Records Requests dataset.  It grabs the .xlsx file that gets dropped into the Public Records folder on the share drive and performs a regex cleaning operations to remove any sensitive information.
