<#
#
.SYNOPSIS
  Flatten a directory structure by moving all items to a designated directory
.DESCRIPTION
  Flattens a directory structure by moving all items in subfolders to a designated directory
.PARAMETER sourceDirectory
    The top level directory for deployment. Files in subdirectories will
    be MOVED to the destination directory
.PARAMETER destDirectory
    The destination directory for deployment. Files in subdirectories will
    be MOVED to the destination directory. Duplicate filenames will be overwritten
.EXAMPLE
  deploy_code.ps1 sourceDirectory destDirectory
.EXAMPLE
  deploy_code.ps1 zip_directory pythonscripts
.INPUTS
  <Inputs if any, otherwise state None>
.OUTPUTS
  <Outputs if any, otherwise state None - example: Log file stored in C:\Windows\Temp\<name>.log>
.NOTES
  Source:         https://gist.github.com/9to5IT
#>

#---------------------------------------------------------[Initialisations]--------------------------------------------------------

#Set Error Action to Silently Continue
#$ErrorActionPreference = "SilentlyContinue"

#---------------------------------------------------------[Script Parameters]------------------------------------------------------

#Param(
#  [Parameter(Mandatory=$true)]
#  [string]$srcDirectory,
#
#  [Parameter(Mandatory=$true)]
#  [string]$destDirectory
#)
#----------------------------------------------------------[Declarations]----------------------------------------------------------

#-----------------------------------------------------------[Execution]------------------------------------------------------------

Write-Host "Num Args:" $args.Length
if ($args.Length -ne 2) {
  Write-Error "An Input and Output directory must be specified" -ErrorAction Stop
}

$srcDirectory  = $args[0]
$destDirectory = $args[1]

Write-Output "Flattening $srcDirectory to $destDirectory"

Get-ChildItem -Path $srcDirectory -Recurse -File | Move-Item -Destination $destDirectory
#Get-ChildItem -Path $srcDirectory -Recurse -Directory | Remove-Item