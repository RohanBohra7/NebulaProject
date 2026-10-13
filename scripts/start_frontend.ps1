# Start NEBULA Vite React Frontend
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$FrontendDir = Join-Path $ProjectRoot "frontend"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "NEBULA: Starting Frontend Dev Server at http://localhost:5173" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan

Set-Location $FrontendDir
npm run dev
