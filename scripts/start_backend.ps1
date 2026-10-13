# Start NEBULA FastAPI Backend
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$BackendDir = Join-Path $ProjectRoot "backend"
$PythonExe = Join-Path $BackendDir "venv\Scripts\python.exe"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "NEBULA: Starting Backend Service at http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "API v1 Health: http://127.0.0.1:8000/api/v1/health" -ForegroundColor Yellow
Write-Host "Docs: http://127.0.0.1:8000/docs" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan

Set-Location $BackendDir
& $PythonExe run.py
