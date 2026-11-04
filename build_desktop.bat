@echo off
REM Build PineLine V4 thanh file PineLine_Studio_V4.exe doc lap
cd /d "%~dp0"
chcp 65001 >nul

echo Dang build PineLine_Studio_V4.exe voi PyInstaller...
pyinstaller --noconfirm --onedir --windowed --name "PineLine_Studio_V4" --add-data "index3.html;." --add-data "static;static" app_desktop.py

echo.
echo Build hoan tat tai thu muc dist/PineLine_Studio_V4/
pause
