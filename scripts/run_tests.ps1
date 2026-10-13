# Run all NEBULA Automated Verification Tests
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$BackendDir = Join-Path $ProjectRoot "backend"
$PythonExe = Join-Path $BackendDir "venv\Scripts\python.exe"
$FrontendDir = Join-Path $ProjectRoot "frontend"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Running NEBULA Scientific & API Test Suite..." -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan

Set-Location $BackendDir
& $PythonExe -m pytest -v

Write-Host "`nRunning NEBULA Frontend TypeScript and Bundler Verification..." -ForegroundColor Green
Set-Location $FrontendDir
npm run build
