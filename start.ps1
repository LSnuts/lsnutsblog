chcp 65001 > $null
Write-Host "=== 启动博客系统 ==="
Write-Host ""

$ROOT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$BACKEND_DIR = Join-Path $ROOT_DIR "backend"
$FRONTEND_DIR = Join-Path $ROOT_DIR "frontend"

$PYTHON_EXE = "python.exe"
if (Test-Path "D:\miniconda3\python.exe") { $PYTHON_EXE = "D:\miniconda3\python.exe" }

Write-Host "[1/3] 启动后端服务..."
$env:PYTHONPATH = "$BACKEND_DIR\lib;"
Start-Process -FilePath "cmd.exe" -WorkingDirectory $BACKEND_DIR -ArgumentList "/k", "set PYTHONPATH=$BACKEND_DIR\lib;%PYTHONPATH% && $PYTHON_EXE run.py"
Start-Sleep -Seconds 3

Write-Host "[2/3] 启动前端服务..."
Start-Process -FilePath "cmd.exe" -WorkingDirectory $FRONTEND_DIR -ArgumentList "/k", "npm run dev"
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "=== 启动完成! ==="
Write-Host "访问: http://localhost:5173"
Write-Host "账户: admin / admin123"
Write-Host ""
Read-Host "按 Enter 键退出"