C:\OpenData\PythonScripts\task-scheduler-status.ps1
$lastStatus = $LASTEXITCODE
Write-Output "Extract Task Scheduler Status completion: $lastStatus"
#if ($lastStatus -eq 0) {
python.exe C:\OpenData\PythonScripts\parse-task-status.py
$lastStatus = $LASTEXITCODE
Write-Output "Parse Task Scheduler Status completion: $lastStatus"
#}
exit $LASTEXITCODE