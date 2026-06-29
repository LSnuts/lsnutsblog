@echo off
cd /d "%~dp0"

echo ================================
echo     STOP BLOG SYSTEM
echo ================================
echo.

echo [1/3] Stopping backend service...
taskkill /FI "WINDOWTITLE eq Blog-Backend" /F 2>nul
echo Backend service stopped

echo.
echo [2/3] Stopping frontend service...
taskkill /FI "WINDOWTITLE eq Blog-Frontend" /F 2>nul
echo Frontend service stopped

echo.
echo [3/3] Stopping Cloudflare Tunnel...
taskkill /FI "WINDOWTITLE eq Cloudflare-Tunnel" /F 2>nul
echo Cloudflare Tunnel stopped

echo.
echo ================================
echo     BLOG SYSTEM STOPPED!
echo ================================
echo.
pause