chcp 65001 > $null
Write-Host "=== 停止博客系统 ==="
Write-Host ""

Write-Host "[1/2] 停止后端服务..."
Get-WmiObject Win32_Process -Filter "Name='cmd.exe' AND CommandLine LIKE '%run.py%'" 2>$null | ForEach-Object { $_.Terminate() } 2>$null
Write-Host "后端服务已停止"

Write-Host ""
Write-Host "[2/2] 停止前端服务..."
Get-WmiObject Win32_Process -Filter "Name='cmd.exe' AND CommandLine LIKE '%npm%dev%'" 2>$null | ForEach-Object { $_.Terminate() } 2>$null
Write-Host "前端服务已停止"

Write-Host ""
Write-Host "=== 博客系统已停止! ==="
Read-Host "按 Enter 键退出"