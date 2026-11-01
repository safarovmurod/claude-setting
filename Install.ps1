param([ValidateSet('install','doctor','uninstall')][string]$Action='install')
$ErrorActionPreference='Stop'
& python (Join-Path $PSScriptRoot 'setup.py') $Action
exit $LASTEXITCODE
