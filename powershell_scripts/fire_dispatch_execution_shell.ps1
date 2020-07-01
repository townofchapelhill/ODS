python C:\OpenData\PythonScripts\read-email-ems.py
$lastStatus = $LASTEXITCODE
Write-Output "read-email completed: $lastStatus"
if ($lastStatus -eq 0) {
    C:\OpenData\PythonScripts\fire_dispatch_dedup.ps1
    $lastStatus = $?
    Write-Output "deduplication completed: $lastStatus"
} else { Write-Output "read-email failed with error $lastStatus"}
Write-Output "Exiting with status: $lastStatus"
exit $LASTEXITCODE