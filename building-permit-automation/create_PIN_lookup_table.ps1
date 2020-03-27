<#
.SYNOPSIS
 Download the csv Address file from ODS
 Convert the file to a PIN lookup table
#>

write-output("Downloading the addresses.csv file from OpenDataSoft")
.\download_csv.ps1 "https://www.chapelhillopendata.org/explore/dataset/addresses/download/" "REDACTED FILE PATH"
Write-Output("Converting the Addresses file to a PIN_lookup file")
.\address_to_PIN_lookup.ps1 "REDACTED FILE PATH" "REDACTED FILE PATH"