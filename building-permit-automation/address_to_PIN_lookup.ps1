<#
.SYNOPSIS
 Read the dataset and dedup the contents
 Sort ad dedup the addresses file
 Output only the PIN and geo_point_2d columns  
.PARAMETER InputObject
  2 arguments should be passed on the command line
    input filename
    output filename
.EXAMPLE
  address_to_PIN_loopkup inputFile outputFile
#>

# Bypass script signing for this instance
# Set-ExecutionPolicy -ExecutionPolicy ByPass -Scope CurrentUser -Force

if ($args.Count -ne 2) {
    Write-Host("Expecting 2 parameters: input, output filenames")
    exit 1
}
# 
#
# Map the network path to a drive letter for Windows
$InPath = Split-Path -Parent -Path $args[0]
$InFile = Split-Path -Leaf -Path $args[0]
$OutPath = Split-Path -Parent -Path $args[0]
$OutFile = Split-Path -Leaf -Path $args[1]

New-PSDrive -Name I -PSProvider "FileSystem" -Root $InPath
New-PSDrive -Name O -PSProvider "FileSystem" -Root $OutPath
Write-Host("Importing $($args[0])")
Write-Host("Exporting unique rows to $($args[1])")

$FileContent = Import-Csv -Delimiter ';' -Path I:$InFile
$FileContent | Sort-Object -Unique -Property PIN | Select-Object PIN, geo_point_2d | Export-Csv  -NoTypeInformation -Path O:$OutFile