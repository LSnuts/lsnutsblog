@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ================================
echo     启动博客系统
echo ================================
echo.

echo [1/3] 启动后端服务...
cd backend
start "博客后端" cmd /k "set PYTHONPATH=%cd%\lib && python run.py"
cd ..
timeout /t 3 /nobreak >nul

echo [2/3] 启动前端服务...
cd frontend
start "博客前端" cmd /k "npm run dev"
cd ..
timeout /t 3 /nobreak >nul

echo.
echo ================================
echo     启动完成！
echo ================================
echo 访问地址：http://localhost:5173
echo 管理后台：http://localhost:5173/admin
echo 账号：admin / admin123
echo ================================
echo.
pause