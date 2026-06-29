@echo off
cd /d "%~dp0"

echo ================================
echo     START BLOG SYSTEM
echo ================================
echo.

set PYTHON_EXE=python.exe
if exist "D:\miniconda3\python.exe" set PYTHON_EXE=D:\miniconda3\python.exe
if exist "C:\Python39\python.exe" set PYTHON_EXE=C:\Python39\python.exe
if exist "C:\Python310\python.exe" set PYTHON_EXE=C:\Python310\python.exe

echo Using Python: %PYTHON_EXE%
echo.

echo [1/3] Starting backend service...
set BACKEND_DIR=%~dp0backend
start "Blog-Backend" cmd /k "title Blog-Backend && cd /d %BACKEND_DIR% && %PYTHON_EXE% run.py"
timeout /t 3 /nobreak >nul

echo [2/3] Starting frontend service...
set FRONTEND_DIR=%~dp0frontend
start "Blog-Frontend" cmd /k "title Blog-Frontend && cd /d %FRONTEND_DIR% && npm run dev"
timeout /t 3 /nobreak >nul

echo [3/3] Starting Cloudflare Tunnel...
set CLOUDFLARED_EXE=cloudflared.exe
if exist "C:\Users\ASUS\Downloads\cloudflared.exe" set CLOUDFLARED_EXE=C:\Users\ASUS\Downloads\cloudflared.exe
if exist "C:\cloudflared\cloudflared.exe" set CLOUDFLARED_EXE=C:\cloudflared\cloudflared.exe
start "Cloudflare-Tunnel" cmd /k "title Cloudflare-Tunnel && %CLOUDFLARED_EXE% tunnel run lsblog-tunnel"

echo.
echo ================================
echo     START COMPLETE!
echo ================================
echo Local:    http://localhost:5173
echo Remote:   https://lsblog.118201820.xyz
echo Admin:    http://localhost:5173/admin
echo Account:  admin / admin123
echo ================================
echo.
pause