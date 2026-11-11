@echo off
cd /d "%~dp0"
set "AGENT_TELEGRAM=1"
if "%PORT%"=="" set "PORT=8804"
set "PINELINE_BASE=http://127.0.0.1:%PORT%"
set "AUTOPILOT_PORT=8802"
set "AUTOPILOT_TICK_SEC=90"
set "RUNWATCH_SEC=90"
set "RUNWATCH_STUCK_MIN=30"
set "RUNWATCH_MAX_HEAL=2"
REM LLM /feed: base/key tu pineline.config.json (config.agent_llm); fallback openclaw
set "AGENT_MODEL=ollama/gemma4:31b-cloud"
set "AGENT_FALLBACK_MODEL=openclaw"
set "PYTHONIOENCODING=utf-8"

REM Python: pineline_env (.pineline_env_path do SETUP_MAY_MOI.bat ghi) > pineline_env canh code
REM   > C:\Python312 > .venv > PATH  (2026-11-11 installer; file ASCII + CRLF)
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

echo Starting Auto-pilot + Telegram sidecar for PineLine V4 (%PINELINE_BASE%)...
echo Python: %PY%
"%PY%" agent_tele_cmd.py
pause
