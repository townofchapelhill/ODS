<#
.SYNOPSIS
Download the dataset from the URL passed as a command line argument and store the contents 
in the filepath specificed in the second argument
.PARAMETER InputObject
2 arguments should be passed on the command line:
URL
output filename
.EXAMPLE
download_to_csv "https://anysite.com/download/some.csv" outputFile
#>

if ($args.Count -ne 2) {
  Write-Host("Expecting 2 parameters: URL, output filenames")
  exit 1 }

$URLPath = $args[0]
$localPath = $args[1]
Write-Host("Downloading $($args[0]), saving file to $($args[1])")
$wc = New-Object System.Net.Webclient
[Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12
$wc.DownloadFile($URLPath, $localPath)