<# 
.SYNOPSIS
  Dump the Task Scheduler Jobs, pulling last run status
  Export the status data to a csv on the shared file systemm
.EXAMPLE
  task-scheduler-status
#>

# Run PowerShell with administrator permissions.
If(!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) 
{ 
    Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs; exit 
}
Else
{
    Import-Module C:\OpenData\PythonScripts\set-variables.psm1
    Invoke-mapSecrets C:\OpenData\PythonScripts\filename_secrets.py

    $taskPath = "\OpenData\"
    $outCsv = $taskBackup + "script_status.csv"
    Get-ScheduledTask |
        ForEach-Object { [pscustomobject]@{
            Name = $_.TaskName
            Path = $_.TaskPath
            LastResult = $(($_| Get-ScheduledTaskInfo).LastTaskResult)
            NextRun = $(($_| Get-ScheduledTaskInfo).NextRunTime)
            Status = $_.State
            Command = $_.Actions.execute
            Arguments = $_.Actions.Arguments
        }
    } |
    Export-Csv -Path $outCsv -NoTypeInformation
}
