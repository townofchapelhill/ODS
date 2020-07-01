# Read the 'clean' fire dispatch dataset and dedup the contents
$P = Import-Csv  -Path "<REDACTED PATH>\fire_dept_dispatches.csv" 
$P | Sort-Object -Descending -Unique -Property Date,CAD | 
  Export-Csv -NoTypeInformation -Path "<REDACTED PATH>\fire_dept_dispatches_dedup.csv"
