#!/usr/bin/env python3
"""install.py — Dựng venv + torch + requirements cho Pineline V4 trên BẤT KỲ máy nào.

Máy mới: KHÔNG cần gọi tay — nháy đúp `SETUP_MAY_MOI.bat` (detect máy → gọi file này với tham số đúng).

Chạy tay:
       python install.py                      (tự detect GPU → chọn build torch như scripts/setup_machine.py)
       python install.py --cpu                (ép CPU, không CUDA)
       python install.py --gpu --cuda cu128   (ép GPU + build CUDA: cu128 | cu124 | cu121)
       python install.py --skip-vieneu        (bỏ qua env VieNeu)
       python install.py --dry-run            (chỉ in việc sẽ làm — không pip, không tạo/ghi file)

Nó sẽ:
  1. Nhận diện GPU NVIDIA + CUDA của driver (scripts/setup_machine.py) → build torch.
  2. Tạo/cập nhật 2 venv: pineline_env (app chính) + vieneu_env (TTS). Venv có rồi → chỉ cập nhật.
  3. Cài torch/torchaudio đúng build (đổi build → cài lại) + requirements.
  4. GỘP pineline.config.json (giữ mọi key bạn đã có; chỉ thêm key thiếu / sửa đường dẫn không tồn tại).
  5. Ghi .pineline_env_path (run_v4.bat đọc) + start.bat / start.sh (mở app_desktop.py / server.py đúng venv).
  6. Kiểm ffmpeg. Ollama KHÔNG bắt buộc (V4 dịch qua llama-server :8083 / LLM_BASE_URL);
     chỉ pull model Ollama khi có --with-ollama.
Model (VieNeu, Whisper, RapidOCR...) TỰ TẢI từ HuggingFace lần chạy đầu — cần mạng.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INSTALL = ROOT / "install"
IS_WIN = platform.system() == "Windows"
_COLOR = (not IS_WIN) and hasattr(sys.stdout, "isatty") and sys.stdout.isatty()
GREEN, YEL, RED, RST = ("\033[92m", "\033[93m", "\033[91m", "\033[0m") if _COLOR else ("", "", "", "")

# Entry thật của V4 (launcher start.bat / start.sh trỏ vào đây — run_v4.bat cũng dùng 2 file này).
LAUNCHER_ENTRY_WIN = "app_desktop.py"      # cửa sổ desktop (tự bật server.py ở PORT)
LAUNCHER_ENTRY_SH = "server.py"            # web server (--host 127.0.0.1 --port $PORT)
DEFAULT_PORT = "8804"
ENV_PATH_NAME = ".pineline_env_path"

DRY = False   # --dry-run: run() chỉ in lệnh, không ghi file nào


def say(msg, c=""):
    print(f"{c}{msg}{RST}", flush=True)


def run(cmd, **kw):
    say(f"  {'[dry-run] ' if DRY else ''}$ {' '.join(str(c) for c in cmd)}", YEL)
    if DRY:
        return subprocess.CompletedProcess([str(c) for c in cmd], 0, "", "")
    return subprocess.run([str(c) for c in cmd], **kw)


def _load_setup_machine():
    """scripts/setup_machine.py (stdlib) — detect GPU + chọn build + gộp config. None nếu lỗi."""
    p = ROOT / "scripts" / "setup_machine.py"
    try:
        spec = importlib.util.spec_from_file_location("pineline_setup_machine", p)
        mod = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
        spec.loader.exec_module(mod)  # type: ignore[union-attr]
        return mod
    except Exception as e:  # noqa: BLE001
        say(f"  [!] không nạp được scripts/setup_machine.py ({e}) — dùng detect đơn giản", YEL)
        return None


def _pip_env(tmp: Path):
    """TEMP + pip tạm CÙNG Ổ với venv (tránh đầy ổ C:). Tắt cache để khỏi giữ ~2.5GB torch."""
    if not DRY:
        tmp.mkdir(parents=True, exist_ok=True)
    e = dict(os.environ)
    e.update({"TMPDIR": str(tmp), "TEMP": str(tmp), "TMP": str(tmp),
              "PIP_NO_CACHE_DIR": "1", "PIP_CACHE_DIR": str(tmp / "pipcache")})
    return e


def free_gb(path: Path) -> float:
    p = Path(path)
    while not p.exists() and p.parent != p:
        p = p.parent
    try:
        return shutil.disk_usage(str(p)).free / 1e9
    except Exception:  # noqa: BLE001
        return 999.0


def venv_python(venv_dir: Path) -> Path:
    return venv_dir / ("Scripts/python.exe" if IS_WIN else "bin/python")


def have(exe: str) -> bool:
    return shutil.which(exe) is not None


def detect_gpu() -> bool:
    if have("nvidia-smi"):
        try:
            r = subprocess.run(["nvidia-smi"], capture_output=True)
            return r.returncode == 0
        except Exception:  # noqa: BLE001
            return False
    return False


def auto_build(force_cpu: bool, force_gpu: bool) -> tuple[str, str]:
    """(build, lý do) — dùng luật của scripts/setup_machine.py; dự phòng: có GPU → cu124, không → cpu."""
    sm = _load_setup_machine()
    if sm is not None:
        try:
            gi = sm.detect_gpu_info()
            tb = sm.choose_torch_build(gi["gpus"], gi["cuda"], force_cpu=force_cpu, force_gpu=force_gpu)
            for w in tb["warnings"]:
                say(f"  [CẢNH BÁO] {w}", YEL)
            return tb["build"], tb["reason"]
        except Exception as e:  # noqa: BLE001
            say(f"  [!] detect GPU lỗi: {e}", YEL)
    if force_cpu:
        return "cpu", "ép --cpu"
    if force_gpu or detect_gpu():
        return "cu124", "có nvidia-smi (detect đơn giản)"
    return "cpu", "không thấy GPU"


def create_venv(path: Path) -> Path:
    py = venv_python(path)
    if py.exists():
        say(f"  venv đã có: {path} → chỉ cập nhật", GREEN)
        return py
    say(f"  Tạo venv: {path}")
    run([sys.executable, "-m", "venv", str(path)], check=True)
    run([str(py), "-m", "pip", "install", "-U", "pip", "-q"])
    return py


def pip_install(py: Path, *args, index_url: str | None = None, tmp: Path):
    cmd = [str(py), "-m", "pip", "install", "--no-cache-dir", *args]
    if index_url:
        cmd += ["--index-url", index_url]
    run(cmd, check=True, env=_pip_env(tmp))   # cache tắt + TEMP cùng ổ -> đỡ đầy C:


def torch_index(build: str) -> str:
    return f"https://download.pytorch.org/whl/{build}"


def installed_torch_build(py: Path) -> str | None:
    """'cu128' / 'cpu' / None (chưa có torch). Đọc hậu tố +cuXXX của torch.__version__."""
    if DRY or not py.exists():
        return None
    try:
        r = subprocess.run([str(py), "-c", "import torch;print(torch.__version__)"],
                           capture_output=True, text=True, timeout=180)
    except Exception:  # noqa: BLE001
        return None
    if r.returncode != 0:
        return None
    v = (r.stdout or "").strip().splitlines()[-1] if r.stdout.strip() else ""
    if "+" in v:
        return v.split("+", 1)[1].strip()
    return "cpu" if v else None   # bản PyPI (Windows) không hậu tố = CPU


def merge_into_config(path: Path, updates: dict, force=()) -> list:
    """GỘP (không ghi đè): dùng merge của setup_machine; dự phòng: chỉ thêm key thiếu."""
    sm = _load_setup_machine()
    if sm is not None:
        return sm.write_config_merged(path, updates, force, backup_dir=ROOT / "scratch" / "config_backup",
                                      dry_run=DRY, note="install.py gộp (giữ key cũ). Sửa tay nếu dời venv/cache.")
    try:
        cur = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    except Exception:  # noqa: BLE001
        say(f"  [!] {path.name} không đọc được — KHÔNG ghi đè, bỏ qua", RED)
        return []
    changes = [(k, "", str(v), "thiếu") for k, v in updates.items() if not str(cur.get(k, "")).strip()]
    if changes and not DRY:
        for k, _o, v, _w in changes:
            cur[k] = v
        path.write_text(json.dumps(cur, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return changes


def launcher_texts(mpy_abs: Path) -> dict[str, str]:
    """Nội dung start.bat / start.sh — trỏ entry THẬT của V4 (app_desktop.py / server.py)."""
    bat = ("@echo off\r\n"
           "REM Sinh boi install.py - mo Pineline V4 bang python cua pineline_env\r\n"
           'cd /d "%~dp0"\r\n'
           f'if "%PORT%"=="" set "PORT={DEFAULT_PORT}"\r\n'
           f'"{mpy_abs}" "%~dp0{LAUNCHER_ENTRY_WIN}" %*\r\n'
           "pause\r\n")
    sh = ("#!/bin/sh\n"
          "# Sinh bởi install.py — chạy web server Pineline V4 bằng python của pineline_env\n"
          'cd "$(dirname "$0")" || exit 1\n'
          f'exec "{mpy_abs}" "{LAUNCHER_ENTRY_SH}" --host 127.0.0.1 --port "${{PORT:-{DEFAULT_PORT}}}" "$@"\n')
    return {"start.bat": bat, "start.sh": sh}


def main(argv=None):
    global DRY
    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
        except Exception:  # noqa: BLE001
            pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--gpu", action="store_true", help="ép dùng GPU (CUDA)")
    ap.add_argument("--cpu", action="store_true", help="ép dùng CPU (không CUDA)")
    ap.add_argument("--cuda", default=None,
                    help="build CUDA cho torch (cu128|cu124|cu121). Mặc định: tự chọn theo GPU/driver")
    ap.add_argument("--skip-vieneu", action="store_true", help="bỏ qua env VieNeu")
    ap.add_argument("--with-ollama", action="store_true", help="pull model Ollama (KHÔNG bắt buộc)")
    ap.add_argument("--skip-ollama-pull", action="store_true", help="(giữ cho tương thích — mặc định đã không pull)")
    ap.add_argument("--ollama-models", default="gemma4,gemma3:12b",
                    help="model Ollama cần pull khi --with-ollama (ngăn bằng phẩy)")
    ap.add_argument("--envs-dir", default=str(ROOT.parent),
                    help="nơi đặt venv (mặc định: cạnh thư mục Pineline)")
    ap.add_argument("--hf-home", default=None, help="cache HuggingFace (mặc định <V4>/.cache/hf)")
    ap.add_argument("--skip-tools", action="store_true", help="không tự cài ffmpeg (setup_machine đã lo)")
    ap.add_argument("--dry-run", action="store_true", help="chỉ in việc sẽ làm — không pip, không ghi file")
    args = ap.parse_args(argv)
    DRY = bool(args.dry_run)

    if args.cpu:
        build, why = "cpu", "ép --cpu"
    elif args.cuda:
        build, why = args.cuda.strip().lower(), "chỉ định --cuda"
    else:
        build, why = auto_build(False, args.gpu)
    gpu = build != "cpu"
    envs = Path(args.envs_dir)
    pip_tmp = envs / ".pip_tmp"
    say("=" * 64)
    say(f" PINELINE INSTALLER{'  (DRY-RUN: không cài, không ghi file)' if DRY else ''}", GREEN)
    say(f"  OS        : {platform.system()} {platform.machine()}")
    say(f"  Python    : {sys.version.split()[0]} ({sys.executable})")
    say(f"  Torch     : {build}  ({why})")
    say(f"  Đặt venv  : {envs}")
    say("=" * 64)
    if sys.version_info < (3, 10):
        say("[LỖI] Cần Python >= 3.10.", RED); sys.exit(1)

    # Kiểm dung lượng: torch CUDA ~2.5GB/env + requirements -> cần dư ~10GB (GPU) / 4GB (CPU).
    need = 10 if gpu else 4
    fr = free_gb(envs)
    say(f"  Trống ở {envs.drive or envs}: {fr:.1f} GB (cần ~{need} GB)")
    if fr < need:
        say(f"[CẢNH BÁO] Ổ gần đầy! Dễ lỗi 'No space left'. Hãy dọn ổ, đổi --envs-dir sang ổ"
            f" khác, hoặc dùng --cpu (torch CPU nhẹ hơn nhiều).", RED)

    tindex = torch_index(build)

    def _install_torch(py, extra=()):
        cur = installed_torch_build(py)
        args_ = ["torch", "torchaudio", *extra]
        if cur == build:
            say(f"  torch đã đúng build {build} → bỏ qua", GREEN)
            return
        if cur:
            say(f"  torch đang là {cur} ≠ {build} → cài lại", YEL)
            args_ = ["--force-reinstall", *args_]
        try:
            pip_install(py, *args_, index_url=tindex, tmp=pip_tmp)
        except subprocess.CalledProcessError:
            say("[LỖI] Cài torch thất bại. Nguyên nhân hay gặp:", RED)
            say(f"  - HẾT Ổ (No space): dọn ổ hoặc chạy lại với --envs-dir sang ổ nhiều chỗ,\n"
                f"    hoặc --cpu (torch CPU chỉ ~200MB thay vì ~2.5GB).", YEL)
            say(f"  - Sai build CUDA: thử --cuda cu124 / cu121 / cu128 khớp máy (xem nvidia-smi).", YEL)
            sys.exit(1)

    # 1) ENV CHÍNH (app) --------------------------------------------------
    say("\n[1/3] ENV CHÍNH (app: server/asr/ocr/demucs/render)...", GREEN)
    main_env = envs / "pineline_env"
    mpy = create_venv(main_env)
    _install_torch(mpy)
    try:
        pip_install(mpy, "-r", str(INSTALL / "requirements-main.txt"), tmp=pip_tmp)
    except subprocess.CalledProcessError:
        say("[LỖI] Cài requirements-main thất bại (mạng / hết ổ). Chạy lại — venv có rồi sẽ chỉ cập nhật.", RED)
        sys.exit(1)

    updates: dict[str, str] = {}
    # 2) ENV VIENEU (TTS) -------------------------------------------------
    if not args.skip_vieneu:
        say("\n[2/3] ENV VIENEU (TTS lồng tiếng)...", GREEN)
        vieneu_env = envs / "vieneu_env"
        vpy = create_venv(vieneu_env)
        try:
            # torch cho VieNeu: bản MỚI NHẤT theo index đã chọn (KHÔNG ghim 2.5.1 — RTX 50/Blackwell cần cu128).
            _install_torch(vpy)
            pip_install(vpy, "-r", str(INSTALL / "requirements-vieneu.txt"), tmp=pip_tmp)
        except subprocess.CalledProcessError:
            say("[LỖI] Cài env VieNeu thất bại (hết ổ / sai CUDA). Xem gợi ý ở trên.", RED)
            sys.exit(1)
        updates["VIENEU_PY"] = str(venv_python(vieneu_env))
        updates["VIENEU_DEVICE"] = "cuda" if gpu else "cpu"

    # 3) CONFIG (GỘP) + LAUNCHER + KIỂM NGOÀI -----------------------------
    say("\n[3/3] Gộp config + launcher + kiểm công cụ ngoài...", GREEN)
    updates["HF_HOME"] = args.hf_home or str(ROOT / ".cache" / "hf")
    # OmniVoice là TÙY CHỌN (repo riêng OmniVoiceStudio) — chỉ thêm key trống nếu chưa có.
    updates.update({"OMNI_PY": "", "OMNI_CWD": "", "OMNI_MODEL": "splendor1811/omnivoice-vietnamese",
                    "OMNI_DEVICE": "cuda" if gpu else "cpu"})
    updates = {k: v for k, v in updates.items() if v != ""}
    force = () if gpu else ("VIENEU_DEVICE", "OMNI_DEVICE")
    cfg = ROOT / "pineline.config.json"
    try:
        changes = merge_into_config(cfg, updates, force)
    except ValueError as e:
        say(f"  [LỖI] {e}", RED)
        changes = []
    for k, old, new, why_ in changes:
        if k != "_note":
            say(f"  pineline.config.json: {k} = {new!r} ({why_}{'; cũ ' + repr(old) if old else ''})", GREEN)
    if not changes:
        say("  pineline.config.json: giữ nguyên (đã đủ key)", GREEN)

    mpy_abs = venv_python(main_env).absolute()
    if DRY:
        say(f"  [dry-run] sẽ ghi {ENV_PATH_NAME} = {mpy_abs}", YEL)
        say("  [dry-run] sẽ ghi start.bat / start.sh → " + LAUNCHER_ENTRY_WIN + " / " + LAUNCHER_ENTRY_SH, YEL)
    else:
        (ROOT / ENV_PATH_NAME).write_text(f"{mpy_abs}\r\n", encoding="utf-8")
        say(f"  -> {ENV_PATH_NAME} (run_v4.bat dùng python này)", GREEN)
        for name, text in launcher_texts(mpy_abs).items():
            with open(ROOT / name, "w", encoding="utf-8", newline="") as fh:
                fh.write(text)
        try:
            os.chmod(ROOT / "start.sh", 0o755)
        except Exception:  # noqa: BLE001
            pass
        say(f"  -> start.bat / start.sh (mở {LAUNCHER_ENTRY_WIN} / {LAUNCHER_ENTRY_SH} đúng venv)", GREEN)

    say("\n  Công cụ ngoài:")
    if not have("ffmpeg") and not args.skip_tools:
        say("    ffmpeg THIẾU -> thử tự cài...", YEL)
        try:
            if IS_WIN and have("winget"):
                run(["winget", "install", "-e", "--id", "Gyan.FFmpeg",
                     "--accept-source-agreements", "--accept-package-agreements"])
            elif platform.system() == "Linux" and have("apt-get"):
                run(["sudo", "apt-get", "install", "-y", "ffmpeg"])
            elif platform.system() == "Darwin" and have("brew"):
                run(["brew", "install", "ffmpeg"])
        except Exception as e:  # noqa: BLE001
            say(f"    tự cài lỗi: {e}", YEL)
    ok_ff = have("ffmpeg")
    say(f"    ffmpeg : {'OK' if ok_ff else 'THIẾU -> cài tay + MỞ LẠI terminal'}",
        GREEN if ok_ff else RED)
    if not ok_ff:
        say("      Windows: winget install Gyan.FFmpeg  (rồi mở lại cmd). Hoặc tải gyan.dev + thêm PATH.", YEL)
    say(f"    ollama : {'có' if have('ollama') else 'không có'} (KHÔNG bắt buộc — V4 dịch qua llama-server"
        f" :8083 / LLM_BASE_URL)")

    # Ollama: chỉ pull khi người dùng yêu cầu rõ (--with-ollama).
    if args.with_ollama:
        if have("ollama"):
            for mdl in [x.strip() for x in args.ollama_models.split(",") if x.strip()]:
                say(f"\n  Pull model Ollama '{mdl}' (có thể vài GB, lần đầu)...", GREEN)
                try:
                    run(["ollama", "pull", mdl])
                except Exception as e:  # noqa: BLE001
                    say(f"    [!] pull '{mdl}' lỗi: {e}. Chạy tay sau: ollama pull {mdl}", YEL)
        else:
            say("  --with-ollama nhưng chưa cài Ollama (https://ollama.com) — bỏ qua pull.", YEL)

    say("\n" + "=" * 64)
    say(" XONG!" + (" (dry-run — chưa làm gì)" if DRY else "") + " Bước tiếp:", GREEN)
    if not ok_ff:
        say("  - Cài ffmpeg + thêm vào PATH (https://ffmpeg.org).", YEL)
    say("  - LLM dịch/review: llama-server + presets (MODEL_PRESETS_DIR) HOẶC đặt LLM_BASE_URL/LLM_MODEL.")
    say("  - (Tùy chọn) OmniVoice: clone repo OmniVoiceStudio, tạo venv, rồi điền")
    say("    OMNI_PY / OMNI_CWD trong pineline.config.json. Không có cũng chạy được (dùng VieNeu).")
    say("  - Kiểm máy: " + f'"{mpy_abs}" scripts\\check_env.py --offline')
    say("  - CHẠY APP:  nháy đúp run_v4.bat  (hoặc start.bat; Linux/macOS: ./start.sh)", GREEN)
    say("=" * 64)
    return 0


if __name__ == "__main__":
    sys.exit(main())
