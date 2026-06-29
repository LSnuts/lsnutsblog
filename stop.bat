@echo off
cd /d "%~dp0"

echo ================================
echo     STOP BLOG SYSTEM
echo ================================
echo.

echo [1/3] Stopping backend service (port 5000)...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5000" ^| findstr "LISTENING"') do (
    taskkill /F /PID %%a >nul 2>&1
    echo Killed PID: %%a
)
echo Backend service stopped

echo.
echo [2/3] Stopping frontend service (port 5173)...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5173" ^| findstr "LISTENING"') do (
    taskkill /F /PID %%a >nul 2>&1
    echo Killed PID: %%a
)
echo Frontend service stopped

echo.
echo [3/3] Stopping Cloudflare Tunnel...
taskkill /IM cloudflared.exe /F >nul 2>&1
echo Cloudflare Tunnel stopped

echo.
echo [4/4] Cleaning up related processes...
taskkill /FI "WINDOWTITLE eq Blog-Backend*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Blog-Frontend*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Cloudflare-Tunnel*" /F >nul 2>&1
echo Cleanup complete

echo.
echo ================================
echo     BLOG SYSTEM STOPPED!
echo ================================
echo.
pause