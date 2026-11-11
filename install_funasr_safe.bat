@echo off
REM Cai FunASR KHONG lam mat torch CUDA.
REM Loi hay gap: `pip install funasr` keo torch +cpu -> mat GPU.
REM Dung:  install_funasr_safe.bat [PY] [BUILD]
REM   PY    = python.exe se cai vao (mac dinh: %%PINELINE_PY%% > .pineline_env_path > python)
REM   BUILD = cu128 | cu124 | cu121 | cpu   (mac dinh: %%TORCH_CUDA%% > cu128)
REM   Khong tham so = hanh vi cu (python he thong, --user, torch 2.11.0+cu128).
REM   Venv (PY tu tham so/.pineline_env_path) -> KHONG dung --user (pip cam --user trong venv).
setlocal
cd /d "%~dp0"
set "PY=%~1"
if "%PY%"=="" set "PY=%PINELINE_PY%"
if "%PY%"=="" if exist "%~dp0.pineline_env_path" set /p PY=<"%~dp0.pineline_env_path"
if "%PY%"=="" set "PY=python"
set "BUILD=%~2"
if "%BUILD%"=="" set "BUILD=%TORCH_CUDA%"
if "%BUILD%"=="" set "BUILD=cu128"
set "USERFLAG="
if /i "%PY%"=="python" set "USERFLAG=--user"

if /i "%PY%"=="python" (
  where python >nul 2>&1 || (echo [loi] khong thay python & exit /b 1)
) else (
  if not exist "%PY%" (echo [loi] khong thay python.exe da chi dinh trong tham so/.pineline_env_path & exit /b 1)
)
echo Python: %PY%   torch build: %BUILD%

echo [1/3] Cai funasr + deps (KHONG cai torch)...
"%PY%" -m pip install %USERFLAG% -U funasr modelscope modelscope-hub tiktoken ^
  jieba jamo jaconv kaldiio torch_complex tensorboardX umap-learn pynndescent ^
  oss2 aliyun-python-sdk-core aliyun-python-sdk-kms crcmod jmespath ^
  --no-deps 2>nul
"%PY%" -m pip install %USERFLAG% -U funasr modelscope tiktoken jieba jamo jaconv ^
  kaldiio torch_complex tensorboardX umap-learn pynndescent huggingface_hub ^
  hydra-core omegaconf librosa soundfile sentencepiece rapidfuzz scipy safetensors ^
  transformers websockets PyYAML regex requests tqdm

if /i "%BUILD%"=="cpu" goto :check_cpu
echo [2/3] Khoa lai torch %BUILD% (neu bi keo)...
if /i "%BUILD%"=="cu128" (
  "%PY%" -m pip install %USERFLAG% --force-reinstall ^
    "torch==2.11.0+cu128" "torchvision==0.26.0+cu128" "torchaudio==2.11.0+cu128" ^
    --index-url https://download.pytorch.org/whl/cu128
) else (
  "%PY%" -m pip install %USERFLAG% --force-reinstall torch torchvision torchaudio ^
    --index-url https://download.pytorch.org/whl/%BUILD%
)

echo [3/3] Kiem tra...
"%PY%" -c "import torch,funasr; assert torch.cuda.is_available(), 'CUDA mat'; print('OK torch', torch.__version__, 'cuda', torch.version.cuda, '| funasr', funasr.__version__)"
if errorlevel 1 exit /b 1
echo Xong.
endlocal
exit /b 0

:check_cpu
echo [2/3] BUILD=cpu - bo qua khoa torch CUDA.
echo [3/3] Kiem tra...
"%PY%" -c "import torch,funasr; print('OK torch', torch.__version__, '(cpu) | funasr', funasr.__version__)"
if errorlevel 1 exit /b 1
echo Xong.
endlocal
exit /b 0
