<#
#
.SYNOPSIS
  <Overview of script>
.DESCRIPTION
  <Brief description of script>
.PARAMETER <Parameter_Name>
    <Brief description of parameter input required. Repeat this attribute if required>
.INPUTS
  <Inputs if any, otherwise state None>
.OUTPUTS
  <Outputs if any, otherwise state None - example: Log file stored in C:\Windows\Temp\<name>.log>
.NOTES
  Source:         https://gist.github.com/9to5IT

.PARAMETER InputObject
  The main parameter. Is passed via the pipline and is named "InputObject" by convention
.PARAMETER Number
  A numeric value. ValidateRange keeps this value between 0 and 10
.PARAMETER AGroup
  A string parameter used to show how parameter sets work
.PARAMETER BGroup
  A string parameter used to show how parameter sets work

.EXAMPLE
  <Example goes here. Repeat this attribute for more than one example>
  .EXAMPLE
  "inputText" | Invoke-Boilerplate -Number 10
.EXAMPLE
  1..10 | % {[PSCustomObject]@{
      InputObject = "inputText"
      Number = 5
      AGroup = "Test String"
  } | Invoke-Boilerplate -Number 10
  #>

#---------------------------------------------------------[Initialisations]--------------------------------------------------------

#Set Error Action to Silently Continue
$ErrorActionPreference = "SilentlyContinue"

#Dot Source required Function Libraries
# . "C:\Scripts\Functions\Logging_Functions.ps1"

Import-Module C:\OpenData\PythonScripts\set-variables.psm1

#---------------------------------------------------------[Script Parameters]------------------------------------------------------

Param (
  #Script parameters go here
)

#----------------------------------------------------------[Declarations]----------------------------------------------------------

#Log File Info
# $sLogPath = "C:\Windows\Temp"
# $sLogName = "<script_name>.log"
# $sLogFile = Join-Path -Path $sLogPath -ChildPath $sLogName

#-----------------------------------------------------------[Functions]------------------------------------------------------------

<#
Function <FunctionName>{
  Param()
  
  Begin{
    Log-Write -LogPath $sLogFile -LineValue "<description of what is going on>..."
  }
  
  Process{
    Try{
      <code goes here>
    }
    
    Catch{
      Log-Error -LogPath $sLogFile -ErrorDesc $_.Exception -ExitGracefully $True
      Break
    }
  }
  
  End{
    If($?){
      Log-Write -LogPath $sLogFile -LineValue "Completed Successfully."
      Log-Write -LogPath $sLogFile -LineValue " "
    }
  }
}
#>

#-----------------------------------------------------------[Execution]------------------------------------------------------------

#Log-Start -LogPath $sLogPath -LogName $sLogName -ScriptVersion $sScriptVersion
#Script Execution goes here
#Log-Finish -LogPath $sLogFile


Function Invoke-Boilerplate {
    [CmdletBinding()]
    param (
        [ValidateScript( { $_.StartsWith("TestValue") })]
        [Parameter(ValueFromPipeline)]
        [String]
        $InputObject,

        [ValidateRange(0, 10)]
        [Parameter(Mandatory, ValueFromPipelineByPropertyName)]
        [Int]
        $Number,
        
        [Parameter(ValueFromPipelineByPropertyName, ParameterSetName = "ParamA")]
        [String]
        $AGroup,

        [Parameter(ValueFromPipelineByPropertyName, ParameterSetName = "ParamB")]
        [String]
        $BGroup
    )
    process {
        foreach ($value in $InputObject) {
            if ($AGroup) {
                # Do A group stuff
            }
            elseif ($BGroup) {
                # Do B group stuff
            }
            else {
                # Do other stuff
            }
        }
    }
}