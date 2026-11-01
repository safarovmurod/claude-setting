<#
  claude-setting bootstrap: репоро худаш мекашад ва профилро насб мекунад.
  Истифода: irm https://raw.githubusercontent.com/safarovmurod/claude-setting/main/bootstrap.ps1 | iex
  Ё:       .\bootstrap.ps1 -Action doctor
#>
param(
  [ValidateSet('install','doctor','uninstall')][string]$Action='install',
  [string]$Ref='main'
)
$ErrorActionPreference='Stop'
$ProgressPreference='SilentlyContinue'

$python=$null
foreach ($name in @('python','python3','py')) {
  $command=Get-Command $name -ErrorAction SilentlyContinue
  if ($command) { $python=$command.Source; break }
}
if (-not $python) {
  Write-Host 'Python 3.11+ ёфт нашуд. Онро насб кун: https://www.python.org/downloads/'
  exit 1
}

$version=(& $python -c 'import sys;print("%d.%d"%sys.version_info[:2])')
if ([version]$version -lt [version]'3.11') {
  Write-Host "Python $version кам аст, 3.11+ лозим: https://www.python.org/downloads/"
  exit 1
}

$work=Join-Path ([System.IO.Path]::GetTempPath()) ('claude-setting-'+[guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $work | Out-Null
try {
  $zip=Join-Path $work 'source.zip'
  $url="https://github.com/safarovmurod/claude-setting/archive/refs/heads/$Ref.zip"
  Write-Host "Кашида мешавад: $url"
  Invoke-WebRequest -Uri $url -OutFile $zip -UseBasicParsing
  Expand-Archive -LiteralPath $zip -DestinationPath $work -Force

  $source=Get-ChildItem -Path $work -Directory | Where-Object { Test-Path (Join-Path $_.FullName 'setup.py') } | Select-Object -First 1
  if (-not $source) { Write-Host 'Дар архив setup.py ёфт нашуд.'; exit 1 }

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
