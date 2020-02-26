<# 
.SYNOPSIS
  Map a python assignment string to a session variable

.PARAMETER InputObject
    A filename for a python import file which contains assignment statements
    Comment lines or lines without '=' are skipped
    This script assumes input lines are of the form 
      $variable = valuestring
.EXAMPLE
  map_secret_to_env.psm1 secrets.py
.EXAMPLE
  map_secret_to_env.psm1 filename_secrets.py
#>
Function Invoke-mapSecrets {
  [CmdletBinding()]
  param (
    [Parameter(Mandatory, ValueFromPipeline)]
    [String]
    $secretsFile
  )
  process {
    # Write-Host("Using Secrets File: $secretsFile")
    $InputFile = Get-Content -Path $secretsFile
    foreach ($line in $InputFile) {
      $Parameters = $line.Split('=',2)
      
      if ($Parameters.Count -eq 2){
        $pValue = $Parameters[1] -replace "`"", ""
        Set-Variable -Name $Parameters[0].Trim() -Value $pValue.Trim() -Force -Scope Global
        #Get-Variable -Name $Parameters[0].Trim()
      }
    }
  }    
}
Export-ModuleMember -Function Invoke-mapSecrets