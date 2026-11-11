@echo off
REM ==========================================================================
REM  SETUP_MAY_MOI.bat - Pineline V4: cai tren MAY MOI (nhay dup file nay)
REM  1) Tim Python 3.12 / 3.11 (py launcher, duong dan thuong gap, where python)
REM     - bo qua Microsoft Store stub (WindowsApps)
REM  2) Khong co -> hoi cai Python 3.12 bang winget (--yes = khong hoi)
REM  3) Chay: python scripts\setup_machine.py %*
REM     (detect may -> ke hoach -> cai venv/torch/requirements -> config -> doctor)
REM  Co: --dry-run --yes --cpu --gpu --cuda cu128 --envs-dir D:\envs --skip-vieneu
REM      --with-funasr --with-ollama --online-check
REM  Log: scratch\setup_bat.log (+ scratch\setup_<thoi gian>.log do Python ghi)
REM  File nay ASCII + CRLF (thong bao tieng Viet in tu Python).
REM ==========================================================================
setlocal EnableExtensions
cd /d "%~dp0"
chcp 65001 >nul
if not exist "%~dp0scratch" mkdir "%~dp0scratch"
set "LOG=%~dp0scratch\setup_bat.log"
echo.>> "%LOG%"
echo [%date% %time%] SETUP_MAY_MOI.bat %*>> "%LOG%"

set "AUTOYES="
for %%A in (%*) do (
  if /i "%%~A"=="--yes" set "AUTOYES=1"
  if /i "%%~A"=="-y" set "AUTOYES=1"
)

echo ==========================================================
echo   PINELINE V4 - SETUP MAY MOI
echo ==========================================================

call :find_python
if defined PY goto :have_python

echo [!] Khong tim thay Python 3.12 / 3.11 tren may nay.
echo [!] no python 3.12/3.11 found>> "%LOG%"
where winget >nul 2>&1
if errorlevel 1 goto :no_winget
set "ANS=N"
if defined AUTOYES set "ANS=Y"
if not defined AUTOYES set /p "ANS=Cai Python 3.12 bang winget ngay bay gio? [Y/N]: "
if /i not "%ANS%"=="Y" goto :need_python
echo Dang cai Python 3.12 (winget)...
echo winget install Python.Python.3.12>> "%LOG%"
winget install -e --id Python.Python.3.12 --accept-source-agreements --accept-package-agreements
echo winget rc=%ERRORLEVEL%>> "%LOG%"
call :find_python
if defined PY goto :have_python
echo [!] Da cai nhung chua thay python.exe - DONG cua so nay, mo lai SETUP_MAY_MOI.bat.
goto :fail

:no_winget
echo [!] Khong co winget. Tai Python 3.12 (64-bit) tu https://www.python.org/downloads/
echo     va TICK "Add python.exe to PATH", roi chay lai file nay.
goto :fail

:need_python
echo Can Python 3.12 (64-bit): https://www.python.org/downloads/  - tick "Add python.exe to PATH".
goto :fail

:have_python
echo Python: %PY%
echo python=%PY%>> "%LOG%"
"%PY%" "%~dp0scripts\setup_machine.py" %*
set "RC=%ERRORLEVEL%"
echo setup_machine rc=%RC%>> "%LOG%"
echo.
if "%RC%"=="0" (echo Hoan tat. Xem log trong thu muc scratch\) else (echo Ket thuc voi ma loi %RC% - xem log trong scratch\)
if not defined AUTOYES pause
exit /b %RC%

:fail
echo setup failed (no python)>> "%LOG%"
if not defined AUTOYES pause
exit /b 1

REM --------------------------------------------------------------------------
REM :find_python  -> dat bien PY (python 3.12 uu tien, roi 3.11)
REM --------------------------------------------------------------------------
:find_python
set "PY="
for %%V in (3.12 3.11) do call :try_launcher %%V
if defined PY exit /b 0
for %%P in ("%LOCALAPPDATA%\Programs\Python\Python312\python.exe" "%ProgramFiles%\Python312\python.exe" "C:\Python312\python.exe" "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" "%ProgramFiles%\Python311\python.exe" "C:\Python311\python.exe") do (
  if not defined PY if exist "%%~P" call :check_ver "%%~P"
)
if defined PY exit /b 0
for /f "delims=" %%P in ('where python 2^>nul') do (
  if not defined PY call :check_path "%%~P"
)
exit /b 0

:try_launcher
if defined PY exit /b 0
set "_LP=py"
where py >nul 2>&1
if errorlevel 1 (
  if exist "%WINDIR%\py.exe" (set "_LP=%WINDIR%\py.exe") else if exist "%LOCALAPPDATA%\Programs\Python\Launcher\py.exe" (set "_LP=%LOCALAPPDATA%\Programs\Python\Launcher\py.exe") else exit /b 0
)
"%_LP%" -%1 -c "import sys" >nul 2>&1
if errorlevel 1 exit /b 0
for /f "delims=" %%E in ('""%_LP%" -%1 -c "import sys;print(sys.executable)""') do set "PY=%%E"
exit /b 0

:check_path
REM bo qua Microsoft Store stub (WindowsApps\python.exe mo Store thay vi chay)
echo %~1| findstr /i "WindowsApps" >nul
if not errorlevel 1 exit /b 0
call :check_ver "%~1"
exit /b 0

:check_ver
"%~1" -c "import sys;sys.exit(0 if sys.version_info[:2] in ((3,11),(3,12)) else 1)" >nul 2>&1
if not errorlevel 1 set "PY=%~1"
exit /b 0
