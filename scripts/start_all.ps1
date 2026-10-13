# Start NEBULA Backend and Frontend concurrently
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "NEBULA: Launching Full Astronomical Exploration Platform..." -ForegroundColor Green
Write-Host "1. Backend: http://127.0.0.1:8000" -ForegroundColor Yellow
Write-Host "2. Frontend: http://localhost:5173" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan

Start-Process powershell -ArgumentList "-NoExit", "-File", (Join-Path $ScriptDir "start_backend.ps1")
Start-Process powershell -ArgumentList "-NoExit", "-File", (Join-Path $ScriptDir "start_frontend.ps1")
