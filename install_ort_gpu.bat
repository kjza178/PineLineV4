@echo off
REM Cai onnxruntime-gpu cho vieneu_env (speaker/denoiser ONNX dung CUDA neu co).
REM G2P van chay CPU - khong the dua 100%% sang GPU.
REM Dung:  install_ort_gpu.bat [VPY]
REM   VPY = python.exe cua vieneu_env (mac dinh: %%VIENEU_PY%% > ..\vieneu_env > D:\vieneu_env)
setlocal
cd /d "%~dp0"
set "VPY=%~1"
if "%VPY%"=="" set "VPY=%VIENEU_PY%"
if "%VPY%"=="" if exist "%~dp0..\vieneu_env\Scripts\python.exe" set "VPY=%~dp0..\vieneu_env\Scripts\python.exe"
if "%VPY%"=="" if exist "D:\vieneu_env\Scripts\python.exe" set "VPY=D:\vieneu_env\Scripts\python.exe"
if "%VPY%"=="" goto :nopy
if not exist "%VPY%" goto :nopy
echo Python: %VPY%
echo [1/2] Go onnxruntime CPU...
"%VPY%" -m pip uninstall -y onnxruntime onnxruntime-gpu
echo [2/2] Cai onnxruntime-gpu...
"%VPY%" -m pip install --no-cache-dir onnxruntime-gpu
"%VPY%" -c "import onnxruntime as o; print('providers', o.get_available_providers())"
echo.
echo Xong. Restart Pineline + chay lai TTS.
echo Goi y: set VIENEU_BATCH=16  va  VIENEU_CPU_THREADS=2
if "%~1"=="" pause
endlocal
exit /b 0

:nopy
echo Khong thay vieneu_env python. Truyen duong dan: install_ort_gpu.bat "E:\envs\vieneu_env\Scripts\python.exe"
echo (hoac dat VIENEU_PY trong pineline.config.json roi set VIENEU_PY=... truoc khi chay)
if "%~1"=="" pause
endlocal
exit /b 1
