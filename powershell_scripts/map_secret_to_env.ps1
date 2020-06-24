<# 
.SYNOPSIS
  Map a python assignment string to a windows environment variable

.PARAMETER InputObject
    A filename for a python import file which contains assignment statements
    Comment lines or lines without '=' are skipped
    This script assumes input lines are of the form 
      $variable = valuestring
.EXAMPLE
  map_secret_to_env.ps1 secrets.py
.EXAMPLE
  map_secret_to_env.ps1 filename_secrets.py
#>

$numberofArgs = $($args.Count)
if ($numberofArgs -eq 0) {
    write-host("The secrets file location must be passed")
    exit 1
}

$secretsFile = $($args[0])    
Write-Host("Using Secrets File: $secretsFile")
$InputFile = Get-Content -Path $secretsFile
foreach ($line in $InputFile) {
    $Parameters = $line.Split('=',2)
    if ($Parameters.Count -eq 2){
        New-Item -ItemType Variable -Path ENV:\ -Name $Parameters[0].Trim() -Value $Parameters[1].Trim() -Force
    }    
}