@echo off
REM Pineline V4 — Desktop App Studio & Server
cd /d "%~dp0"
chcp 65001 >nul

set "PORT=8804"
set "TEMP=D:\PinelineV4_tmp"
set "TMP=D:\PinelineV4_tmp"
if not exist "%TEMP%" mkdir "%TEMP%"

echo ========================================================
echo   PineLine Studio V4 — High Performance Pipeline
echo ========================================================
echo.
echo [1] Chạy chế độ App Desktop (.exe native window mượt mà)
echo [2] Chạy chế độ Web Server (mở qua trình duyệt web)
echo.
set /p choice="Chọn chế độ [1/2] (mặc định 1): "
if "%choice%"=="" set choice=1

REM Pin Python 3.12 — PATH uu tien 3.15 sau update → thieu fastapi/requests
set "PY="
if exist "C:\Python312\python.exe" (
  set "PY=C:\Python312\python.exe"
)
if not defined PY if exist "%~dp0pineline_env\Scripts\python.exe" (
  set "PY=%~dp0pineline_env\Scripts\python.exe"
)
if not defined PY if exist "%~dp0.venv\Scripts\python.exe" (
  set "PY=%~dp0.venv\Scripts\python.exe"
)
if not defined PY (
  where python >nul 2>&1 && for /f "delims=" %%I in ('where python') do (
    if not defined PY set "PY=%%I"
  )
)
if not defined PY (
  echo [loi] Khong thay C:\Python312\python.exe
  pause
  exit /b 1
)

if "%choice%"=="1" (
    echo Dang khoi dong PineLine Studio Desktop...
    echo Python: %PY%
    "%PY%" app_desktop.py
) else (
    echo Dang khoi dong PineLine V4 Web Server...
    set "PORT=8804"
    echo Python: %PY%
    "%PY%" server.py --host 127.0.0.1 --port 8804
)
pause

