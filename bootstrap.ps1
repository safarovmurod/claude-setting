#
# claude-setting bootstrap: downloads the repo, unpacks it and installs the profile.
#
#   irm https://raw.githubusercontent.com/safarovmurod/claude-setting/main/bootstrap.ps1 | iex
#
# Or, from a clone:  .\bootstrap.ps1 -Action doctor
#
# ASCII only on purpose: a UTF-8 BOM breaks `irm | iex`, and without a BOM
# Windows PowerShell 5.1 reads non-ASCII text in a .ps1 file as ANSI.
#
param(
  [ValidateSet('install','doctor','uninstall')][string]$Action='install',
  [string]$Ref='main'
)
$ErrorActionPreference='Stop'
$ProgressPreference='SilentlyContinue'
try { [Console]::OutputEncoding=[Text.Encoding]::UTF8 } catch {}
try { [Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12 } catch {}

$python=$null
foreach ($name in @('python','python3','py')) {
  $command=Get-Command $name -ErrorAction SilentlyContinue
  if ($command) { $python=$command.Source; break }
}
if (-not $python) {
  Write-Host 'Python 3.11+ was not found. Install it: https://www.python.org/downloads/'
  exit 1
}

# No inner quotes: PowerShell 5.1 drops them when it passes the argument to an exe.
& $python -c 'import sys;sys.exit(sys.version_info<(3,11))'
if ($LASTEXITCODE -ne 0) {
  Write-Host 'Python 3.11+ is required: https://www.python.org/downloads/'
  exit 1
}

# Run from a clone: install that clone, with no download at all.
$localSetup=if ($PSScriptRoot) { Join-Path $PSScriptRoot 'setup.py' } else { $null }
if ($localSetup -and (Test-Path -LiteralPath $localSetup)) {
  Write-Host "Source: $PSScriptRoot"
  & $python $localSetup $Action
  $code=$LASTEXITCODE
  if ($code -eq 0 -and $Action -eq 'install') {
    & $python $localSetup doctor
    $code=$LASTEXITCODE
  }
  exit $code
}

$work=Join-Path ([System.IO.Path]::GetTempPath()) ('claude-setting-'+[guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $work | Out-Null
try {
  $zip=Join-Path $work 'source.zip'
  $url="https://github.com/safarovmurod/claude-setting/archive/refs/heads/$Ref.zip"
  Write-Host "Downloading $url"
  Invoke-WebRequest -Uri $url -OutFile $zip -UseBasicParsing
  Expand-Archive -LiteralPath $zip -DestinationPath $work -Force

  $source=Get-ChildItem -Path $work -Directory | Where-Object { Test-Path (Join-Path $_.FullName 'setup.py') } | Select-Object -First 1
  if (-not $source) { Write-Host 'setup.py was not found in the downloaded archive.'; exit 1 }

  & $python (Join-Path $source.FullName 'setup.py') $Action
  $code=$LASTEXITCODE
  if ($code -eq 0 -and $Action -eq 'install') {
    & $python (Join-Path $source.FullName 'setup.py') doctor
    $code=$LASTEXITCODE
  }
  exit $code
}
finally {
  Remove-Item -LiteralPath $work -Recurse -Force -ErrorAction SilentlyContinue
}
