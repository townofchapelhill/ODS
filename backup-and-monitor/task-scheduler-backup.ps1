# Run PowerShell with administrator permissions.
If(!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) 
{ 
    Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs; exit 
}
Else
{
    Import-Module C:\OpenData\PythonScripts\set-variables.psm1
    Invoke-mapSecrets C:\OpenData\PythonScripts\filename_secrets.py

    # Lines 9-11 retrieve scheduled task info for the purpose of creating a backup map
    $x = New-Object -ComObject("Schedule.Service");
    $x.Connect();
    $x.GetFolder("\OpenData").GetTasks(1) | 
        % {
            $_.XML | 
            Out-File  $taskBackup"$($_.Name).xml"
          }

    # Lines 14-27 retrieve the status of all scheduled tasks to monitor the status of the scripts
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