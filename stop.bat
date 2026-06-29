@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ================================
echo     停止博客系统
echo ================================
echo.

echo [1/3] 停止后端服务...
taskkill /F /IM python.exe 2>nul
echo 后端服务已停止

echo.
echo [2/3] 停止前端服务...
taskkill /F /IM node.exe 2>nul
echo 前端服务已停止

echo.
echo [3/3] 关闭相关窗口...
taskkill /FI "WINDOWTITLE eq 博客后端" /F 2>nul
taskkill /FI "WINDOWTITLE eq 博客前端" /F 2>nul
echo 相关窗口已关闭

echo.
echo ================================
echo     博客系统已停止！
echo ================================
echo.
pause