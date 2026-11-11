@echo off
REM Pineline V4 - Desktop App Studio & Server
REM 2026-11-11 installer: uu tien python cua pineline_env (file .pineline_env_path do
REM   SETUP_MAY_MOI.bat / install.py ghi - venv co the o thu muc cha / o khac) TRUOC C:\Python312.
REM   TEMP: PINELINE_TEMP > .pineline_tmp_path > D:\PinelineV4_tmp (chi neu DA CO, may goc)
REM   > %~dp0scratch\tmp. File ASCII + CRLF.
cd /d "%~dp0"
chcp 65001 >nul

set "PORT=8804"

set "PTMP="
if defined PINELINE_TEMP set "PTMP=%PINELINE_TEMP%"
if not defined PTMP if exist "%~dp0.pineline_tmp_path" set /p PTMP=<"%~dp0.pineline_tmp_path"
if not defined PTMP if exist "D:\PinelineV4_tmp\" set "PTMP=D:\PinelineV4_tmp"
if not defined PTMP set "PTMP=%~dp0scratch\tmp"
if not exist "%PTMP%" mkdir "%PTMP%"
set "TEMP=%PTMP%"
set "TMP=%PTMP%"

echo ========================================================
echo   PineLine Studio V4 - High Performance Pipeline
echo ========================================================
echo.
echo [1] Chay che do App Desktop (cua so native)
echo [2] Chay che do Web Server (mo qua trinh duyet web)
echo.
set /p choice="Chon che do [1/2] (mac dinh 1): "
if "%choice%"=="" set choice=1

REM Python: pineline_env (.pineline_env_path) > pineline_env canh code > C:\Python312 > .venv > PATH
set "PY="
if exist "%~dp0.pineline_env_path" set /p PY=<"%~dp0.pineline_env_path"
if defined PY if not exist "%PY%" set "PY="
if not defined PY if exist "%~dp0pineline_env\Scripts\python.exe" set "PY=%~dp0pineline_env\Scripts\python.exe"
if not defined PY if exist "C:\Python312\python.exe" set "PY=C:\Python312\python.exe"
if not defined PY if exist "%~dp0.venv\Scripts\python.exe" set "PY=%~dp0.venv\Scripts\python.exe"
if not defined PY (
  where python >nul 2>&1 && for /f "delims=" %%I in ('where python') do (
    if not defined PY set "PY=%%I"
  )
)
if not defined PY (
  echo [loi] Khong thay Python. Chay SETUP_MAY_MOI.bat truoc.
  pause
  exit /b 1
)

echo Python: %PY%
if "%choice%"=="1" (
    echo Dang khoi dong PineLine Studio Desktop...
    "%PY%" app_desktop.py
) else (
    echo Dang khoi dong PineLine V4 Web Server...
    set "PORT=8804"
    "%PY%" server.py --host 127.0.0.1 --port 8804
)
pause
