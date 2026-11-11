#!/usr/bin/env python3
"""setup_machine.py — Cài Pineline V4 trên MÁY MỚI: detect máy → lập kế hoạch → cài → cấu hình → kiểm.

Thường KHÔNG chạy trực tiếp: nháy đúp `SETUP_MAY_MOI.bat` ở gốc V4 (nó tìm Python 3.12/3.11 rồi gọi file này).

Chạy tay:
    python scripts/setup_machine.py --dry-run      chỉ detect + in kế hoạch (không cài, không ghi gì ngoài log)
    python scripts/setup_machine.py                detect → hỏi Y/N → cài → cấu hình → doctor
    python scripts/setup_machine.py --yes          không hỏi
Cờ khác: --cpu | --gpu | --cuda cu128|cu124|cu121|cpu | --envs-dir D:\\envs | --skip-vieneu
         --with-funasr | --with-ollama | --online-check | --scan-requirements

Các bước (mỗi bước in ra màn hình + ghi scratch/setup_<thời gian>.log):
  a) Detect: OS, CPU, RAM, ổ trống, GPU (nvidia-smi), công cụ (ffmpeg/git/winget/llama-server/ollama/py), presets.
     KHÔNG gọi mạng tới dịch vụ nào (Aurora/Hongguo/LLM) — chỉ doctor ở bước e (và chỉ khi --online-check).
  b) Kế hoạch: build torch theo GPU/driver, hồ sơ hiệu năng, nơi đặt venv, VieNeu/FunASR.
  c) Cài: công cụ thiếu (winget), venv + torch + requirements qua install.py (chạy lại = chỉ cập nhật).
  d) Cấu hình: thư mục work/voices/..., TEMP riêng, GỘP pineline.config.json (không xoá key cũ, không bí mật).
  e) Kiểm: scripts/check_env.py --offline bằng python của venv + danh sách VIỆC TAY còn lại.

Chỉ dùng stdlib (chạy được bằng Python hệ thống ≥ 3.10 trước khi có venv).
"""
from __future__ import annotations

import argparse
import ast
import datetime as _dt
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path, PureWindowsPath
from typing import Callable, Iterable

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
IS_WIN = os.name == "nt"

CONFIG_NAME = "pineline.config.json"
ENV_PATH_NAME = ".pineline_env_path"     # 1 dòng: python.exe của pineline_env (run_v4.bat đọc)
TMP_PATH_NAME = ".pineline_tmp_path"     # 1 dòng: thư mục TEMP riêng (run_v4.bat đọc)
PROFILE_FILES = {"rtx5060ti": "pineline.config.rtx5060ti.json", "rtx3060": "pineline.config.rtx3060.json"}
DEFAULT_PRESETS_DIR = r"E:\models\presets"
DEFAULT_START_SCRIPT = "start-model.ps1"
NEED_GB_GPU = 15.0   # 2 venv torch CUDA (~2.5–3.5GB/env) + requirements + cache HF
NEED_GB_CPU = 6.0
TORCH_BUILDS = ("cu128", "cu124", "cu121", "cpu")

# Key "máy/hiệu năng" lấy từ file profile (KHÔNG lấy đường dẫn venv/HF của máy gốc, KHÔNG lấy SUB_* layout).
PERF_KEYS = (
    "VIENEU_BATCH", "VIENEU_STALL_SEC", "VIENEU_BOOT_SEC", "VIENEU_CPU_THREADS", "VIENEU_LOW_PRIORITY",
    "ASR_STALL_SEC", "TRANSLATE_BATCH", "LLM_NUM_CTX", "RENDER_ENCODER",
)
# Giá trị dự phòng nếu thiếu file profile.
_BUILTIN_PROFILES: dict[str, dict[str, str]] = {
    "rtx5060ti": {"VIENEU_BATCH": "8", "VIENEU_CPU_THREADS": "2", "VIENEU_LOW_PRIORITY": "1",
                  "VIENEU_STALL_SEC": "600", "VIENEU_BOOT_SEC": "180", "ASR_STALL_SEC": "900",
                  "TRANSLATE_BATCH": "50", "LLM_NUM_CTX": "8192", "RENDER_ENCODER": "nvenc"},
    "rtx3060": {"VIENEU_BATCH": "8", "VIENEU_STALL_SEC": "600", "ASR_STALL_SEC": "900", "TRANSLATE_BATCH": "100"},
}
# Đường dẫn: nếu giá trị cũ trỏ tới chỗ KHÔNG tồn tại trên máy này (config chép từ máy cũ) → thay.
PATH_KEYS = ("VIENEU_PY", "HF_HOME", "PINELINE_TEMP")


# ═════════════════════════════════════════════════════════════════════════════
# Log
# ═════════════════════════════════════════════════════════════════════════════
class Log:
    def __init__(self, path: Path | None):
        self.path = path
        self._fh = None
        if path is not None:
            try:
                path.parent.mkdir(parents=True, exist_ok=True)
                self._fh = open(path, "a", encoding="utf-8")
            except OSError:
                self._fh = None

    def __call__(self, msg: str = "") -> None:
        print(msg, flush=True)
        if self._fh:
            try:
                self._fh.write(msg + "\n")
                self._fh.flush()
            except OSError:
                pass

    def quiet(self, msg: str) -> None:  # chỉ ghi log
        if self._fh:
            try:
                self._fh.write(msg + "\n")
                self._fh.flush()
            except OSError:
                pass

    def close(self) -> None:
        if self._fh:
            self._fh.close()
            self._fh = None


def _null_log(msg: str = "") -> None:  # pragma: no cover
    print(msg, flush=True)


# ═════════════════════════════════════════════════════════════════════════════
# Chạy lệnh
# ═════════════════════════════════════════════════════════════════════════════
Runner = Callable[[list, float], "tuple[int, str]"]


def run_capture(cmd: list, timeout: float = 20.0) -> tuple[int, str]:
    """Chạy lệnh ngắn, trả (rc, stdout+stderr). Không có lệnh → (127, '')."""
    try:
        r = subprocess.run([str(c) for c in cmd], capture_output=True, timeout=timeout,
                           text=True, encoding="utf-8", errors="replace")
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except FileNotFoundError:
        return 127, ""
    except subprocess.TimeoutExpired:
        return 124, ""
    except OSError as e:
        return 126, str(e)


def run_stream(cmd: list, log: Callable[[str], None], cwd: Path | None = None,
               env: dict | None = None) -> int:
    """Chạy lệnh dài, in + ghi log từng dòng."""
    log(f"  $ {' '.join(_q(c) for c in cmd)}")
    env = dict(os.environ if env is None else env)
    env.setdefault("PYTHONIOENCODING", "utf-8")   # con là Python: in tiếng Việt qua pipe không lỗi cp1252
    env.setdefault("PYTHONUNBUFFERED", "1")
    try:
        p = subprocess.Popen([str(c) for c in cmd], cwd=str(cwd) if cwd else None, env=env,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             text=True, encoding="utf-8", errors="replace")
    except OSError as e:
        log(f"  [LỖI] không chạy được: {e}")
        return 127
    assert p.stdout is not None
    for line in p.stdout:
        log("    " + line.rstrip("\r\n"))
    return p.wait()


def _q(c) -> str:
    s = str(c)
    return f'"{s}"' if (" " in s and not s.startswith('"')) else s


# ═════════════════════════════════════════════════════════════════════════════
# a) DETECT
# ═════════════════════════════════════════════════════════════════════════════
def parse_gpu_query(text: str) -> list[dict]:
    """Parse `nvidia-smi --query-gpu=name,driver_version,memory.total,compute_cap --format=csv,noheader`.

    Mỗi dòng: 'NVIDIA GeForce RTX 5060 Ti, 576.52, 16311 MiB, 12.0' (compute_cap có thể thiếu/[N/A])."""
    out: list[dict] = []
    for line in (text or "").splitlines():
        line = line.strip()
        if not line or line.lower().startswith(("name", "error", "failed", "nvidia-smi has failed")):
            continue
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 3:
            continue
        name, driver, mem = parts[0], parts[1], parts[2]
        m = re.search(r"(\d+)", mem)
        mem_mb = int(m.group(1)) if m else 0
        cc = None
        if len(parts) >= 4:
            try:
                cc = float(parts[3])
            except ValueError:
                cc = None
        if not re.match(r"^\d+(\.\d+)*$", driver):
            continue
        out.append({"name": name, "driver": driver, "mem_mb": mem_mb, "cc": cc})
    return out


def parse_cuda_version(text: str) -> tuple[int, int] | None:
    """'CUDA Version: 12.9' trong header `nvidia-smi` → (12, 9)."""
    m = re.search(r"CUDA Version\s*:\s*(\d+)\.(\d+)", text or "")
    return (int(m.group(1)), int(m.group(2))) if m else None


def driver_to_cuda(driver: str) -> tuple[int, int] | None:
    """Ước lượng CUDA tối đa driver hỗ trợ (khi header không có). Bảng NVIDIA (nhánh driver chính)."""
    try:
        major = int(str(driver).split(".")[0])
    except (ValueError, IndexError):
        return None
    table = ((570, (12, 8)), (560, (12, 6)), (555, (12, 5)), (550, (12, 4)), (545, (12, 3)),
             (535, (12, 2)), (530, (12, 1)), (525, (12, 0)), (520, (11, 8)), (450, (11, 0)))
    for floor, cv in table:
        if major >= floor:
            return cv
    return (10, 0)


def _nvidia_smi_exe() -> str | None:
    p = shutil.which("nvidia-smi")
    if p:
        return p
    if IS_WIN:
        for c in (r"C:\Windows\System32\nvidia-smi.exe",
                  r"C:\Program Files\NVIDIA Corporation\NVSMI\nvidia-smi.exe"):
            if Path(c).is_file():
                return c
    return None


def detect_gpu_info(runner: Runner = run_capture, exe: str | None = "auto") -> dict:
    """{'gpus': [...], 'cuda': (12, 8)|None, 'smi': path|None, 'error': str}."""
    smi = _nvidia_smi_exe() if exe == "auto" else exe
    info: dict = {"gpus": [], "cuda": None, "smi": smi, "error": ""}
    if not smi:
        info["error"] = "không có nvidia-smi"
        return info
    rc, out = runner([smi, "--query-gpu=name,driver_version,memory.total,compute_cap",
                      "--format=csv,noheader"], 20)
    if rc != 0:  # driver cũ không biết compute_cap
        rc, out = runner([smi, "--query-gpu=name,driver_version,memory.total", "--format=csv,noheader"], 20)
    if rc == 0:
        info["gpus"] = parse_gpu_query(out)
    else:
        info["error"] = (out or f"rc={rc}").strip()[:200]
    rc2, head = runner([smi], 20)
    if rc2 == 0:
        info["cuda"] = parse_cuda_version(head)
    return info


def _win_reg(path: str, name: str, hive: str = "HKLM") -> str:
    try:
        import winreg  # type: ignore
        h = winreg.HKEY_LOCAL_MACHINE if hive == "HKLM" else winreg.HKEY_CURRENT_USER
        with winreg.OpenKey(h, path) as k:
            return str(winreg.QueryValueEx(k, name)[0])
    except Exception:  # noqa: BLE001
        return ""


def detect_os() -> dict:
    d = {"system": platform.system(), "release": platform.release(), "version": platform.version(),
         "machine": platform.machine(), "is_windows": IS_WIN, "pretty": ""}
    if IS_WIN:
        prod = _win_reg(r"SOFTWARE\Microsoft\Windows NT\CurrentVersion", "ProductName")
        disp = _win_reg(r"SOFTWARE\Microsoft\Windows NT\CurrentVersion", "DisplayVersion")
        build = _win_reg(r"SOFTWARE\Microsoft\Windows NT\CurrentVersion", "CurrentBuild")
        try:
            if build and int(build) >= 22000 and "Windows 10" in prod:
                prod = prod.replace("Windows 10", "Windows 11")  # registry vẫn ghi "Windows 10" trên Win11
        except ValueError:
            pass
        d["pretty"] = " ".join(x for x in (prod, disp, f"(build {build})" if build else "") if x)
    else:
        try:
            for line in Path("/etc/os-release").read_text(encoding="utf-8").splitlines():
                if line.startswith("PRETTY_NAME="):
                    d["pretty"] = line.split("=", 1)[1].strip().strip('"')
        except OSError:
            pass
    if not d["pretty"]:
        d["pretty"] = f"{d['system']} {d['release']}"
    return d


def detect_cpu() -> dict:
    name = ""
    if IS_WIN:
        name = _win_reg(r"HARDWARE\DESCRIPTION\System\CentralProcessor\0", "ProcessorNameString").strip()
    else:
        try:
            for line in Path("/proc/cpuinfo").read_text(encoding="utf-8", errors="replace").splitlines():
                if line.lower().startswith("model name"):
                    name = line.split(":", 1)[1].strip()
                    break
        except OSError:
            pass
    return {"name": name or platform.processor() or "?", "threads": os.cpu_count() or 0}


def detect_ram_gb() -> float | None:
    if IS_WIN:
        try:
            import ctypes

            class MS(ctypes.Structure):
                _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                            ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                            ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                            ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                            ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
            st = MS()
            st.dwLength = ctypes.sizeof(MS)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(st)):  # type: ignore[attr-defined]
                return st.ullTotalPhys / 1024 ** 3
        except Exception:  # noqa: BLE001
            return None
        return None
    try:
        for line in Path("/proc/meminfo").read_text(encoding="utf-8").splitlines():
            if line.startswith("MemTotal:"):
                return int(line.split()[1]) / 1024 ** 2
    except (OSError, ValueError, IndexError):
        pass
    return None


def free_gb(path: Path) -> float:
    p = Path(path)
    while not p.exists() and p.parent != p:
        p = p.parent
    try:
        return shutil.disk_usage(str(p)).free / 1024 ** 3
    except OSError:
        return -1.0


def detect_drives() -> list[dict]:
    """Ổ đĩa cố định (Windows) / gốc + thư mục dự án (Linux/mac). [{'root','free_gb','total_gb'}]."""
    roots: list[str] = []
    if IS_WIN:
        try:
            import ctypes
            mask = ctypes.windll.kernel32.GetLogicalDrives()  # type: ignore[attr-defined]
            for i in range(26):
                if mask & (1 << i):
                    r = f"{chr(65 + i)}:\\"
                    t = ctypes.windll.kernel32.GetDriveTypeW(ctypes.c_wchar_p(r))  # type: ignore[attr-defined]
                    if t == 3:  # DRIVE_FIXED (bỏ USB, CD, ổ mạng)
                        roots.append(r)
        except Exception:  # noqa: BLE001
            roots = []
    else:
        roots = ["/", str(Path.home())]
    for extra in (ROOT.anchor or "", str(ROOT.parent)):
        if extra and extra not in roots and not IS_WIN:
            roots.append(extra)
    out = []
    seen = set()
    for r in roots:
        try:
            u = shutil.disk_usage(r)
        except OSError:
            continue
        key = (u.total, u.free) if not IS_WIN else r
        if key in seen:
            continue
        seen.add(key)
        out.append({"root": r, "free_gb": u.free / 1024 ** 3, "total_gb": u.total / 1024 ** 3})
    return out


def read_config(path: Path) -> dict:
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
        return d if isinstance(d, dict) else {}
    except (OSError, ValueError):
        return {}


def _setting(cfg: dict, key: str, default: str) -> str:
    v = os.environ.get(key) or cfg.get(key) or default
    return str(v).strip()


def find_llama_server(presets_dir: Path) -> str:
    exe = "llama-server.exe" if IS_WIN else "llama-server"
    p = shutil.which("llama-server")
    if p:
        return p
    for base in (presets_dir, presets_dir.parent):
        if not base.is_dir():
            continue
        try:
            for depth_glob in (exe, f"*/{exe}", f"*/*/{exe}"):
                hits = list(base.glob(depth_glob))
                if hits:
                    return str(hits[0])
        except OSError:
            continue
    return ""


def find_py_launcher() -> str:
    p = shutil.which("py")
    if p:
        return p
    if IS_WIN:
        for c in (Path(os.environ.get("WINDIR", r"C:\Windows")) / "py.exe",
                  Path(os.environ.get("LOCALAPPDATA", "")) / "Programs/Python/Launcher/py.exe"):
            if c.is_file():
                return str(c)
    return ""


def detect_tools(cfg: dict) -> dict:
    presets = Path(os.path.expandvars(_setting(cfg, "MODEL_PRESETS_DIR", DEFAULT_PRESETS_DIR)))
    script = Path(os.path.expandvars(_setting(cfg, "MODEL_START_SCRIPT", DEFAULT_START_SCRIPT)))
    if not script.is_absolute():
        script = presets / script
    winget = shutil.which("winget") or ""
    if not winget and IS_WIN:
        c = Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft/WindowsApps/winget.exe"
        winget = str(c) if c.exists() else ""
    return {
        "ffmpeg": shutil.which("ffmpeg") or "",
        "ffprobe": shutil.which("ffprobe") or "",
        "git": shutil.which("git") or "",
        "winget": winget,
        "ollama": shutil.which("ollama") or "",
        "py": find_py_launcher(),
        "llama-server": find_llama_server(presets),
        "presets_dir": str(presets),
        "presets_ok": presets.is_dir(),
        "start_script": str(script),
        "start_script_ok": script.is_file(),
        "start_cmd": _setting(cfg, "MODEL_START_CMD", ""),
    }


def detect(root: Path = ROOT, runner: Runner = run_capture) -> dict:
    cfg = read_config(root / CONFIG_NAME)
    return {
        "os": detect_os(),
        "python": {"version": sys.version.split()[0], "exe": sys.executable,
                   "ok": sys.version_info[:2] in ((3, 11), (3, 12))},
        "cpu": detect_cpu(),
        "ram_gb": detect_ram_gb(),
        "drives": detect_drives(),
        "gpu": detect_gpu_info(runner),
        "tools": detect_tools(cfg),
        "config_exists": (root / CONFIG_NAME).is_file(),
        "env_path_file": _read_first_line(root / ENV_PATH_NAME),
    }


def _read_first_line(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8-sig").splitlines()[0].strip().strip('"')
    except (OSError, IndexError):
        return ""


# ═════════════════════════════════════════════════════════════════════════════
# b) QUYẾT ĐỊNH
# ═════════════════════════════════════════════════════════════════════════════
def best_gpu(gpus: list[dict]) -> dict | None:
    return max(gpus, key=lambda g: g.get("mem_mb") or 0) if gpus else None


def _fmt_cv(cv) -> str:
    return f"{cv[0]}.{cv[1]}" if cv else "?"


def choose_torch_build(gpus: list[dict], cuda_ver: tuple[int, int] | None, *, force_cpu: bool = False,
                       force_gpu: bool = False, cuda_override: str | None = None) -> dict:
    """Chọn build torch (index download.pytorch.org/whl/<build>).

    Luật:
      compute_cap ≥ 12.0 (Blackwell, RTX 50) hoặc driver CUDA ≥ 12.8   → cu128
      CUDA 12.4–12.7 → cu124 ; 12.1–12.3 → cu121
      driver quá cũ (< 12.1) → cảnh báo cập nhật driver, đề xuất CPU (trừ khi --gpu)
      không GPU → cpu.  GPU cũ (compute_cap < 7.0, Maxwell/Pascal) mà driver ≥ 12.8 → cu124
      (bản cu128 mới bỏ kiến trúc cũ).
    """
    warns: list[str] = []
    if cuda_override:
        b = cuda_override.strip().lower()
        if b not in TORCH_BUILDS and not re.match(r"^cu\d{3}$", b):
            warns.append(f"--cuda '{cuda_override}' lạ — vẫn dùng như tên index của PyTorch")
        return {"build": b, "gpu": b != "cpu", "reason": f"ép bằng --cuda {b}", "warnings": warns}
    if force_cpu:
        return {"build": "cpu", "gpu": False, "reason": "ép --cpu", "warnings": warns}
    g = best_gpu(gpus)
    if g is None:
        if force_gpu:
            warns.append("--gpu nhưng không chạy được nvidia-smi → cài cu128; kiểm tra driver NVIDIA!")
            return {"build": "cu128", "gpu": True, "reason": "ép --gpu (không detect được GPU)", "warnings": warns}
        return {"build": "cpu", "gpu": False, "reason": "không thấy GPU NVIDIA (nvidia-smi)", "warnings": warns}
    cv = cuda_ver or driver_to_cuda(g.get("driver", ""))
    cc = g.get("cc")
    src = "nvidia-smi" if cuda_ver else f"suy từ driver {g.get('driver')}"
    if cc is not None and cc >= 12.0:
        if cv and cv < (12, 8):
            warns.append(f"GPU Blackwell (compute {cc}) cần driver hỗ trợ CUDA ≥ 12.8 (nhánh ≥ 570); "
                         f"driver hiện tại {g.get('driver')} (CUDA {_fmt_cv(cv)}) → CẬP NHẬT DRIVER NVIDIA "
                         f"rồi mới dùng được GPU.")
        return {"build": "cu128", "gpu": True,
                "reason": f"compute_cap {cc} ≥ 12.0 (Blackwell/RTX 50) → bắt buộc cu128", "warnings": warns}
    if cv is None:
        warns.append("không đọc được phiên bản CUDA của driver → chọn cu121 (tương thích rộng nhất)")
        return {"build": "cu121", "gpu": True, "reason": "CUDA không rõ", "warnings": warns}
    if cv >= (12, 8):
        if cc is not None and cc < 7.0:
            return {"build": "cu124", "gpu": True,
                    "reason": f"CUDA {_fmt_cv(cv)} ({src}) nhưng GPU cũ compute {cc} → cu124", "warnings": warns}
        return {"build": "cu128", "gpu": True, "reason": f"driver hỗ trợ CUDA {_fmt_cv(cv)} ({src}) ≥ 12.8",
                "warnings": warns}
    if cv >= (12, 4):
        return {"build": "cu124", "gpu": True, "reason": f"CUDA {_fmt_cv(cv)} ({src}) trong 12.4–12.7",
                "warnings": warns}
    if cv >= (12, 1):
        return {"build": "cu121", "gpu": True, "reason": f"CUDA {_fmt_cv(cv)} ({src}) trong 12.1–12.3",
                "warnings": warns}
    warns.append(f"Driver {g.get('driver')} quá cũ (CUDA {_fmt_cv(cv)} < 12.1) cho torch CUDA → "
                 f"cập nhật driver NVIDIA (khuyên) rồi chạy lại; tạm thời cài CPU.")
    if force_gpu:
        return {"build": "cu121", "gpu": True, "reason": "ép --gpu dù driver cũ", "warnings": warns}
    return {"build": "cpu", "gpu": False, "reason": f"driver quá cũ (CUDA {_fmt_cv(cv)})", "warnings": warns}


def choose_profile(gpu: dict | None, use_gpu: bool = True) -> tuple[str, str]:
    """Hồ sơ hiệu năng: rtx5060ti | rtx3060 | small | cpu."""
    if gpu is None or not use_gpu:
        return "cpu", "không dùng GPU"
    name = (gpu.get("name") or "").lower()
    mem = int(gpu.get("mem_mb") or 0)
    if "5060" in name:
        return "rtx5060ti", f"tên GPU khớp ({gpu.get('name')})"
    if "3060" in name:
        return "rtx3060", f"tên GPU khớp ({gpu.get('name')})"
    if mem >= 15000:
        return "rtx5060ti", f"VRAM {mem / 1024:.0f}GB ≥ 16GB → giống 5060 Ti"
    if mem >= 11000:
        return "rtx3060", f"VRAM {mem / 1024:.0f}GB ≈ 12GB → giống 3060"
    return "small", f"VRAM {mem / 1024:.0f}GB < 12GB → hồ sơ nhẹ"


def profile_perf_keys(profile: str, root: Path = ROOT) -> dict[str, str]:
    """Chỉ lấy key máy/hiệu năng (PERF_KEYS) từ file profile; không lấy đường dẫn/SUB_* của máy gốc."""
    def _load(name: str) -> dict[str, str]:
        f = root / PROFILE_FILES[name]
        data = read_config(f) if f.is_file() else {}
        src = data or _BUILTIN_PROFILES[name]
        return {k: str(src[k]) for k in PERF_KEYS if k in src}

    if profile in PROFILE_FILES:
        return _load(profile)
    if profile == "small":
        d = _load("rtx3060")
        d.update({"VIENEU_BATCH": "4", "TRANSLATE_BATCH": "50", "VIENEU_LOW_PRIORITY": "1"})
        return d
    # cpu
    return {"VIENEU_BATCH": "2", "VIENEU_LOW_PRIORITY": "1", "VIENEU_STALL_SEC": "1200",
            "ASR_STALL_SEC": "1800", "TRANSLATE_BATCH": "50", "RENDER_ENCODER": "x264"}


def choose_envs_dir(default_dir: Path, drives: list[dict], need_gb: float,
                    existing_python: str = "", free_fn: Callable[[Path], float] = free_gb) -> dict:
    """Nơi đặt venv. Ưu tiên: venv đã có (.pineline_env_path / <default>/pineline_env) → thư mục cha của V4
    nếu đủ chỗ → ổ cố định còn nhiều chỗ nhất (<ổ>\\PinelineEnvs) → (không ổ nào đủ) mặc định + cảnh báo."""
    if existing_python:
        ep = Path(existing_python)
        if ep.is_file():
            # <envs>/pineline_env/Scripts/python.exe  hoặc  <envs>/pineline_env/bin/python
            return {"dir": ep.parent.parent.parent, "reason": f"venv đã có ({ep}) → chỉ cập nhật", "warning": ""}
    default_dir = Path(default_dir)
    if (default_dir / "pineline_env").is_dir():
        return {"dir": default_dir, "reason": "venv đã có ở thư mục cha của V4 → chỉ cập nhật", "warning": ""}
    fd = free_fn(default_dir)
    if fd >= need_gb:
        return {"dir": default_dir, "reason": f"thư mục cha của V4, trống {fd:.0f}GB ≥ {need_gb:.0f}GB",
                "warning": ""}
    cands = sorted(drives, key=lambda d: d.get("free_gb", 0), reverse=True)
    if cands and cands[0].get("free_gb", 0) >= need_gb:
        best = cands[0]
        return {"dir": Path(best["root"]) / "PinelineEnvs",
                "reason": f"thư mục cha chỉ trống {fd:.0f}GB → chọn ổ {best['root']} (trống {best['free_gb']:.0f}GB)",
                "warning": ""}
    return {"dir": default_dir, "reason": f"không ổ nào đủ {need_gb:.0f}GB",
            "warning": f"Ổ gần đầy (cần ~{need_gb:.0f}GB). Dọn ổ hoặc dùng --envs-dir / --cpu."}


def temp_dir_for(envs_dir: Path, root: Path = ROOT, is_win: bool = IS_WIN) -> Path:
    """TEMP riêng cùng ổ với venv (Windows: <ổ>:\\PinelineV4_tmp); khác: <V4>/scratch/tmp."""
    drive = PureWindowsPath(str(envs_dir)).drive if is_win else ""
    if is_win and drive:
        return Path(str(PureWindowsPath(drive + "\\", "PinelineV4_tmp")))
    return root / "scratch" / "tmp"


def venv_python(venv_dir: Path, is_win: bool = IS_WIN) -> Path:
    return Path(venv_dir) / ("Scripts/python.exe" if is_win else "bin/python")


def build_plan(det: dict, args: argparse.Namespace, root: Path = ROOT) -> dict:
    gi = det["gpu"]
    tb = choose_torch_build(gi["gpus"], gi["cuda"], force_cpu=args.cpu, force_gpu=args.gpu,
                            cuda_override=args.cuda)
    g = best_gpu(gi["gpus"])
    profile, preason = choose_profile(g, tb["gpu"])
    need = NEED_GB_GPU if tb["gpu"] else NEED_GB_CPU
    if args.envs_dir:
        envs = {"dir": Path(args.envs_dir), "reason": "chỉ định --envs-dir", "warning": ""}
        fr = free_gb(envs["dir"])
        if 0 <= fr < need:
            envs["warning"] = f"--envs-dir chỉ trống {fr:.0f}GB (cần ~{need:.0f}GB)"
    else:
        envs = choose_envs_dir(root.parent, det["drives"], need, det.get("env_path_file", ""))
    t = det["tools"]
    winget_ids = []
    if not (t["ffmpeg"] and t["ffprobe"]):
        winget_ids.append("Gyan.FFmpeg")
    if not t["git"]:
        winget_ids.append("Git.Git")
    presets_missing = not t["start_cmd"] and not (t["presets_ok"] and t["start_script_ok"])
    return {
        "torch": tb,
        "profile": profile, "profile_reason": preason,
        "perf": profile_perf_keys(profile, root),
        "envs_dir": Path(envs["dir"]), "envs_reason": envs["reason"], "envs_warning": envs["warning"],
        "need_gb": need,
        "temp_dir": temp_dir_for(Path(envs["dir"]), root),
        "vieneu": not args.skip_vieneu,
        "funasr": bool(args.with_funasr),
        "ollama": bool(args.with_ollama),
        "winget": winget_ids,
        "presets_missing": presets_missing,
    }


# ═════════════════════════════════════════════════════════════════════════════
# d) CẤU HÌNH — gộp pineline.config.json
# ═════════════════════════════════════════════════════════════════════════════
def merge_config(existing: dict, updates: dict, force: Iterable[str] = (),
                 path_keys: Iterable[str] = PATH_KEYS) -> tuple[dict, list[tuple[str, str, str, str]]]:
    """GỘP: không bao giờ xoá key cũ; key đã có giá trị thì GIỮ, trừ:
      - key trong `force` (mâu thuẫn phần cứng, vd VIENEU_DEVICE=cuda trên máy không GPU),
      - key đường dẫn (`path_keys`) mà giá trị cũ trỏ tới chỗ không tồn tại (config chép từ máy cũ).
    Trả (dict mới, [(key, cũ, mới, lý do)])."""
    out = dict(existing)
    changes: list[tuple[str, str, str, str]] = []
    force, path_keys = set(force), set(path_keys)
    for k, v in updates.items():
        v = "" if v is None else str(v)
        old = existing.get(k)
        olds = "" if old is None else str(old)
        if k not in existing or olds.strip() == "":
            if olds != v:
                out[k] = v
                changes.append((k, olds, v, "thiếu"))
        elif olds == v:
            continue
        elif k in force:
            out[k] = v
            changes.append((k, olds, v, "theo phần cứng máy này"))
        elif k in path_keys and not Path(os.path.expandvars(olds)).exists():
            out[k] = v
            changes.append((k, olds, v, "đường dẫn cũ không tồn tại trên máy này"))
    return out, changes


def write_config_merged(path: Path, updates: dict, force: Iterable[str] = (), *,
                        backup_dir: Path | None = None, dry_run: bool = False,
                        note: str = "") -> list[tuple[str, str, str, str]]:
    """Đọc → gộp → ghi atomic (backup bản cũ vào backup_dir). dry_run: chỉ trả thay đổi."""
    existing = read_config(path) if path.is_file() else {}
    if path.is_file() and not existing and path.stat().st_size > 0:
        raise ValueError(f"{path.name} không phải JSON hợp lệ — sửa tay trước (không ghi đè)")
    if note and "_note" not in existing:
        updates = {"_note": note, **updates}
    merged, changes = merge_config(existing, updates, force)
    if dry_run or not changes:
        return changes
    if path.is_file() and backup_dir is not None:
        backup_dir.mkdir(parents=True, exist_ok=True)
        stamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
        shutil.copy2(path, backup_dir / f"{path.name}.{stamp}.bak")
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)
    return changes


def config_updates(plan: dict, root: Path = ROOT) -> tuple[dict, set]:
    gpu = plan["torch"]["gpu"]
    dev = "cuda" if gpu else "cpu"
    envs = Path(plan["envs_dir"])
    upd: dict[str, str] = {
        "VIENEU_DEVICE": dev,
        "OMNI_DEVICE": dev,
        "HF_HOME": str(envs / "AI_CACHE"),
        "PINELINE_TEMP": str(plan["temp_dir"]),
    }
    if plan["vieneu"]:
        upd["VIENEU_PY"] = str(venv_python(envs / "vieneu_env"))
    if plan["presets_missing"]:
        upd["AUTO_SWITCH_PRESETS"] = "0"
    for k, v in plan["perf"].items():
        upd.setdefault(k, v)
    force = {"VIENEU_DEVICE", "OMNI_DEVICE"} if not gpu else set()
    if not gpu:
        upd["RENDER_ENCODER"] = "x264"   # máy không NVIDIA: nvenc không chạy được
        force.add("RENDER_ENCODER")
    return upd, force


# ═════════════════════════════════════════════════════════════════════════════
# Quét import bên thứ ba ↔ requirements
# ═════════════════════════════════════════════════════════════════════════════
SCAN_SKIP_DIRS = {"tests", "vendor", "scripts", "docs", "install", "_to_delete", "finetune_xuyenthanh",
                  "work", "data", "models", "voices", "voice_samples", "assets", "static", "scratch",
                  "cookies", "claude_setup", "rvc_bridge", "__pycache__", ".git", "Pineline", "node_modules"}
# Tên package nội bộ của V5/V6 (V4 import trong try/except rồi fallback module phẳng) + module hệ thống Windows.
INTERNAL_NAMES = {"core", "agents", "__future__", "msvcrt", "winreg", "_winapi"}
# import name → tên pip
PIP_NAME = {
    "PIL": "pillow", "yt_dlp": "yt-dlp", "faster_whisper": "faster-whisper",
    "rapidocr_onnxruntime": "rapidocr-onnxruntime", "webview": "pywebview", "multipart": "python-multipart",
    "googleapiclient": "google-api-python-client", "google_auth_oauthlib": "google-auth-oauthlib",
    "google": "google-auth", "clr": "pythonnet", "qwen_asr": "qwen-asr", "huggingface_hub": "huggingface-hub",
    "sklearn": "scikit-learn", "cv2": "opencv-python", "yaml": "pyyaml", "fireredasr2s": "fireredasr2s",
}
# Có sẵn nhờ gói khác / cài riêng.
PROVIDED_BY = {"torch": "install.py (torch theo GPU)", "torchaudio": "install.py (torch theo GPU)",
               "ctranslate2": "faster-whisper", "onnxruntime": "rapidocr-onnxruntime",
               "starlette": "fastapi", "tokenizers": "faster-whisper",
               "fireredasr2s": "vendor/FireRedASR2S (FIRERED_ROOT, tuỳ chọn)"}


def _norm(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def parse_requirements(path: Path) -> set[str]:
    out: set[str] = set()
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return out
    for line in lines:
        line = line.split("#", 1)[0].strip()
        if not line or line.startswith("-"):
            continue
        m = re.match(r"^([A-Za-z0-9][A-Za-z0-9._-]*)", line)
        if m:
            out.add(_norm(m.group(1)))
    return out


def scan_third_party_imports(root: Path = ROOT, skip_dirs: Iterable[str] = SCAN_SKIP_DIRS) -> dict[str, set[str]]:
    """{top_module: {file,...}} các import tuyệt đối không phải stdlib / module nội bộ của V4."""
    skip = set(skip_dirs)
    root = Path(root)
    local = {p.stem for p in root.glob("*.py")}
    for p in root.iterdir():
        try:
            if p.is_dir():
                local.add(p.name)
        except OSError:   # junction/symlink hỏng (vd work → ổ không có)
            local.add(p.name)
    std = set(getattr(sys, "stdlib_module_names", ())) | set(sys.builtin_module_names)
    found: dict[str, set[str]] = {}
    for dirpath, dirnames, filenames in os.walk(root):
        rel = Path(dirpath).relative_to(root)
        if rel.parts and (rel.parts[0] in skip or rel.parts[0].startswith((".backup", ".")) ):
            dirnames[:] = []
            continue
        dirnames[:] = [d for d in dirnames if d not in skip and not d.startswith(".")]
        for fn in filenames:
            if not fn.endswith(".py"):
                continue
            p = Path(dirpath) / fn
            try:
                tree = ast.parse(p.read_text(encoding="utf-8", errors="replace"))
            except (SyntaxError, ValueError, OSError):
                continue
            for n in ast.walk(tree):
                mods: list[str] = []
                if isinstance(n, ast.Import):
                    mods = [a.name for a in n.names]
                elif isinstance(n, ast.ImportFrom) and n.level == 0 and n.module:
                    mods = [n.module]
                for m in mods:
                    top = m.split(".")[0]
                    if top in std or top in local or top in INTERNAL_NAMES:
                        continue
                    found.setdefault(top, set()).add(str(p.relative_to(root)).replace("\\", "/"))
    return found


def requirements_report(root: Path = ROOT) -> dict:
    """{'ok': {...}, 'optional': {...}, 'provided': {...}, 'missing': {mod: (pip, files)}}."""
    inst = root / "install"
    main = parse_requirements(inst / "requirements-main.txt")
    opt = parse_requirements(inst / "requirements-optional.txt")
    rep: dict = {"ok": {}, "optional": {}, "provided": {}, "missing": {}}
    for mod, files in sorted(scan_third_party_imports(root).items()):
        pip = PIP_NAME.get(mod, mod)
        n = _norm(pip)
        if n in main:
            rep["ok"][mod] = pip
        elif mod in PROVIDED_BY:
            rep["provided"][mod] = PROVIDED_BY[mod]
        elif n in opt:
            rep["optional"][mod] = pip
        else:
            rep["missing"][mod] = (pip, sorted(files))
    return rep


# ═════════════════════════════════════════════════════════════════════════════
# In bảng
# ═════════════════════════════════════════════════════════════════════════════
def _table(log, rows: list[tuple[str, str]], w: int = 22) -> None:
    for k, v in rows:
        log(f"  {k:<{w}} {v}")


def print_detect(det: dict, log) -> None:
    log("\n[a] DETECT MÁY")
    o, c, t, gi = det["os"], det["cpu"], det["tools"], det["gpu"]
    rows = [("Hệ điều hành", f"{o['pretty']} [{o['machine']}]" + ("" if o["is_windows"] else "  (KHÔNG phải Windows)")),
            ("Python đang chạy", f"{det['python']['version']} ({det['python']['exe']})"
             + ("" if det["python"]["ok"] else "  ← khuyên 3.11/3.12")),
            ("CPU", f"{c['name']} — {c['threads']} luồng"),
            ("RAM", f"{det['ram_gb']:.1f} GB" if det["ram_gb"] else "?")]
    for d in det["drives"]:
        rows.append((f"Ổ {d['root']}", f"trống {d['free_gb']:.1f} / {d['total_gb']:.0f} GB"))
    if gi["gpus"]:
        for i, g in enumerate(gi["gpus"]):
            rows.append((f"GPU {i}", f"{g['name']} | {g['mem_mb'] / 1024:.1f} GB | driver {g['driver']} | "
                                     f"compute {g['cc'] if g['cc'] is not None else '?'}"))
        rows.append(("CUDA (driver)", _fmt_cv(gi["cuda"]) if gi["cuda"] else "? (không đọc được header)"))
    else:
        rows.append(("GPU NVIDIA", f"KHÔNG ({gi['error'] or 'nvidia-smi không trả GPU'})"))
    for k in ("ffmpeg", "ffprobe", "git", "winget", "py", "llama-server", "ollama"):
        v = t[k]
        extra = "  (chỉ ghi nhận — không bắt buộc)" if k == "ollama" else ""
        rows.append((k, (v or "THIẾU") + extra))
    rows.append(("Presets llama", f"{t['presets_dir']} — {'CÓ' if t['presets_ok'] else 'KHÔNG'}; script "
                                   f"{'CÓ' if t['start_script_ok'] else 'KHÔNG'}"
                                   + ("; MODEL_START_CMD đặt" if t["start_cmd"] else "")))
    rows.append(("pineline.config.json", "CÓ (sẽ GỘP, không ghi đè)" if det["config_exists"] else "chưa có (sẽ tạo)"))
    if det.get("env_path_file"):
        rows.append((ENV_PATH_NAME, det["env_path_file"]))
    _table(log, rows)


def print_plan(plan: dict, log) -> None:
    tb = plan["torch"]
    log("\n[b] KẾ HOẠCH")
    rows = [("Torch build", f"{tb['build']}  — {tb['reason']}"),
            ("Hồ sơ hiệu năng", f"{plan['profile']}  — {plan['profile_reason']}"),
            ("  key hiệu năng", ", ".join(f"{k}={v}" for k, v in plan["perf"].items()) or "-"),
            ("Đặt venv", f"{plan['envs_dir']}  — {plan['envs_reason']}"),
            ("  pineline_env", str(venv_python(plan["envs_dir"] / "pineline_env"))),
            ("  vieneu_env", str(venv_python(plan["envs_dir"] / "vieneu_env")) if plan["vieneu"] else "BỎ QUA (--skip-vieneu)"),
            ("TEMP riêng", str(plan["temp_dir"])),
            ("Cài qua winget", ", ".join(plan["winget"]) or "không cần"),
            ("FunASR", "CÀI (--with-funasr)" if plan["funasr"] else "không (thêm --with-funasr nếu dùng Fun-ASR/Paraformer)"),
            ("Ollama pull", "CÓ (--with-ollama)" if plan["ollama"] else "không (Ollama không bắt buộc)"),
            ("Đổi preset llama", "TẮT (AUTO_SWITCH_PRESETS=0 — không có presets/script)" if plan["presets_missing"] else "giữ")]
    _table(log, rows)
    for w in tb["warnings"] + ([plan["envs_warning"]] if plan["envs_warning"] else []):
        log(f"  [CẢNH BÁO] {w}")


MANUAL_TODO = [
    "Chép từ máy cũ (không có trong git): voices/, voice_samples/, models/ (cdx23 tách nhạc nền…), cookies/",
    "Chép/điền key bí mật trong pineline.config.json (LLM_API_KEY, CLOUD_LLM_API_KEY…) — setup KHÔNG đặt bí mật",
    "Model MT zh→vi (HachimiMT ct2) → MT_MODEL_DIR / MT_ZH_VI_LOCAL (không có thì tự tải HF khi bật MT_ZH_VI=1)",
    "FireRed ASR (nếu dùng): FIRERED_ROOT + FIRERED_MODELS (scripts/download_firered_models.py)",
    "Upload YouTube (nếu dùng): yt_uploader + client_secret.json → YT_UPLOADER_DIR",
    "LLM dịch/review: cài llama.cpp (CUDA) + thư mục presets GGUF (MODEL_PRESETS_DIR, cổng :8083) "
    "HOẶC đặt LLM_BASE_URL/LLM_MODEL tới LLM OpenAI-compatible khác (Ollama /v1, 9router, OpenAI…)",
    "Aurora/ChatGPT proxy là TUỲ CHỌN — máy không có Aurora: đổi PLAN_MODEL/REVIEW_MODEL/REVIEW_PASS1_MODEL/"
    "AGENT_MODEL… khỏi 'chatgpt/...' (vd 'local')",
    "Hongguo Downloader là TUỲ CHỌN (chỉ khi tải phim Hongguo): HONGGUO_BASE_URL, LIBRARY_DIR",
    "Kiểm lại có mạng: <python venv> scripts\\check_env.py   (gọi thử LLM/Aurora/Hongguo)",
]


# ═════════════════════════════════════════════════════════════════════════════
# c) CÀI
# ═════════════════════════════════════════════════════════════════════════════
def refresh_path_windows() -> None:
    """Sau winget: nạp lại PATH từ registry (tiến trình hiện tại không tự thấy PATH mới)."""
    if not IS_WIN:
        return
    parts: list[str] = []
    for hive, key in (("HKLM", r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"),
                      ("HKCU", "Environment")):
        v = _win_reg(key, "Path", hive)
        if v:
            parts += [os.path.expandvars(x) for x in v.split(";") if x]
    links = Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft/WinGet/Links"
    parts.append(str(links))
    cur = os.environ.get("PATH", "").split(";")
    os.environ["PATH"] = ";".join(dict.fromkeys(cur + parts))


def install_tools(plan: dict, det: dict, log) -> None:
    ids = plan["winget"]
    if not ids:
        log("  Công cụ: đủ (ffmpeg/ffprobe/git).")
        return
    winget = det["tools"]["winget"]
    if not (IS_WIN and winget):
        log(f"  [!] Thiếu {', '.join(ids)} và không có winget → cài tay:")
        log("      ffmpeg: https://www.gyan.dev/ffmpeg/builds/ (thêm bin vào PATH)   git: https://git-scm.com")
        if not IS_WIN:
            log("      Linux: sudo apt-get install -y ffmpeg git")
        return
    for pid in ids:
        rc = run_stream([winget, "install", "-e", "--id", pid, "--accept-source-agreements",
                         "--accept-package-agreements"], log)
        log(f"  winget {pid}: {'OK' if rc == 0 else f'rc={rc} (có thể đã cài sẵn / cần quyền)'}")
    refresh_path_windows()


def install_cmd(plan: dict, args, py: str = sys.executable, root: Path = ROOT, dry: bool = False) -> list[str]:
    tb = plan["torch"]
    cmd = [py, str(root / "install.py"), "--envs-dir", str(plan["envs_dir"]),
           "--hf-home", str(Path(plan["envs_dir"]) / "AI_CACHE"), "--skip-tools"]
    if tb["build"] == "cpu":
        cmd += ["--cpu"]
    else:
        cmd += ["--gpu", "--cuda", tb["build"]]
    if not plan["vieneu"]:
        cmd.append("--skip-vieneu")
    if plan["ollama"]:
        cmd.append("--with-ollama")
    if dry:
        cmd.append("--dry-run")
    return cmd


def install_funasr(plan: dict, log, root: Path = ROOT) -> None:
    mpy = venv_python(Path(plan["envs_dir"]) / "pineline_env")
    bat = root / "install_funasr_safe.bat"
    if not IS_WIN:
        log(f"  [!] FunASR: không phải Windows → cài tay: {mpy} -m pip install -r install/requirements-optional.txt")
        return
    if not mpy.is_file():
        log(f"  [!] FunASR: chưa có {mpy} — bỏ qua")
        return
    rc = run_stream([str(bat), str(mpy), plan["torch"]["build"]], log, cwd=root)  # .bat chạy thẳng (tránh lỗi bỏ ngoặc kép của cmd /c)
    log(f"  FunASR: {'OK' if rc == 0 else f'LỖI rc={rc} — xem log, chạy lại install_funasr_safe.bat'}")


# ═════════════════════════════════════════════════════════════════════════════
# d) CẤU HÌNH
# ═════════════════════════════════════════════════════════════════════════════
def configure(plan: dict, log, root: Path = ROOT, dry: bool = False) -> None:
    log("\n[d] CẤU HÌNH")
    for name in ("work", "voices", "voice_samples", "cookies", "models"):
        p = root / name
        if os.path.lexists(p):   # junction/symlink cũ (kể cả hỏng) → để nguyên
            log(f"  {name}/ : đã có")
            continue
        log(f"  {name}/ : tạo" + (" (dry-run: bỏ qua)" if dry else ""))
        if not dry:
            p.mkdir(parents=True, exist_ok=True)
    td = Path(plan["temp_dir"])
    log(f"  TEMP riêng: {td}" + (" (dry-run: không tạo)" if dry else ""))
    if not dry:
        try:
            td.mkdir(parents=True, exist_ok=True)
            (root / TMP_PATH_NAME).write_text(str(td) + "\r\n", encoding="utf-8")
        except OSError as e:
            log(f"  [!] không tạo được {td}: {e}")
    upd, force = config_updates(plan, root)
    try:
        changes = write_config_merged(root / CONFIG_NAME, upd, force, backup_dir=root / "scratch" / "config_backup",
                                      dry_run=dry, note="Gộp bởi scripts/setup_machine.py (không xoá key cũ). Sửa tay được.")
    except ValueError as e:
        log(f"  [LỖI] {e}")
        return
    if not changes:
        log(f"  {CONFIG_NAME}: không cần đổi (giữ nguyên giá trị của bạn)")
    for k, old, new, why in changes:
        if k == "_note":
            continue
        log(f"  {CONFIG_NAME}: {k} = {new!r}  (cũ: {old!r} — {why})" + (" [dry-run]" if dry else ""))
    keep = [k for k in upd if k not in {c[0] for c in changes}]
    if keep:
        log(f"  giữ nguyên giá trị đang có: {', '.join(keep)}")


# ═════════════════════════════════════════════════════════════════════════════
# main
# ═════════════════════════════════════════════════════════════════════════════
def parse_args(argv=None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Detect máy + cài Pineline V4 (máy mới)")
    ap.add_argument("--dry-run", action="store_true", help="chỉ detect + in kế hoạch, không cài/ghi gì ngoài log")
    ap.add_argument("--yes", "-y", action="store_true", help="không hỏi xác nhận")
    ap.add_argument("--cpu", action="store_true", help="ép torch CPU")
    ap.add_argument("--gpu", action="store_true", help="ép torch CUDA")
    ap.add_argument("--cuda", default=None, help="ép build torch: cu128 | cu124 | cu121 | cpu")
    ap.add_argument("--envs-dir", default=None, help="nơi đặt venv (mặc định: tự chọn)")
    ap.add_argument("--skip-vieneu", action="store_true", help="không tạo vieneu_env (TTS)")
    ap.add_argument("--with-funasr", action="store_true", help="cài FunASR (Fun-ASR-Nano/Paraformer)")
    ap.add_argument("--with-ollama", action="store_true", help="pull model Ollama (không bắt buộc)")
    ap.add_argument("--online-check", action="store_true", help="doctor gọi thử LLM/Aurora/Hongguo")
    ap.add_argument("--scan-requirements", action="store_true", help="chỉ quét import ↔ requirements rồi thoát")
    return ap.parse_args(argv)


def main(argv=None) -> int:
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
        except Exception:  # noqa: BLE001
            pass
    args = parse_args(argv)
    if args.scan_requirements:
        rep = requirements_report(ROOT)
        for k in ("ok", "provided", "optional"):
            print(f"{k}: {', '.join(sorted(rep[k]))}")
        for mod, (pip, files) in rep["missing"].items():
            print(f"THIẾU: {mod} (pip {pip}) ← {', '.join(files[:3])}")
        return 1 if rep["missing"] else 0

    stamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    log = Log(ROOT / "scratch" / f"setup_{stamp}.log")
    log("=" * 72)
    log(f" PINELINE V4 — SETUP MÁY MỚI   {stamp}   {'(DRY-RUN)' if args.dry_run else ''}")
    log(f" Thư mục: {ROOT}")
    log(f" Log    : {log.path}")
    log("=" * 72)
    if sys.version_info < (3, 10):
        log("[LỖI] Cần Python ≥ 3.10 (khuyên 3.12).")
        return 1

    det = detect(ROOT)
    print_detect(det, log)
    if not det["os"]["is_windows"]:
        log("  [!] Không phải Windows: V4 thiết kế cho Windows (server dùng msvcrt). Chỉ detect/kế hoạch có ý nghĩa.")
    plan = build_plan(det, args, ROOT)
    print_plan(plan, log)
    icmd = install_cmd(plan, args)
    log(f"\n  Lệnh cài venv: {' '.join(_q(c) for c in icmd)}")

    if args.dry_run:
        log("\n[c] (dry-run) xem trước install.py --dry-run:")
        run_stream(install_cmd(plan, args, dry=True), log, cwd=ROOT)
        configure(plan, log, ROOT, dry=True)
        log("\n[e] (dry-run) bỏ qua doctor. VIỆC TAY sau khi cài:")
        for i, s in enumerate(MANUAL_TODO, 1):
            log(f"  {i}. {s}")
        log("\nDRY-RUN xong — không cài, không ghi file nào ngoài log.")
        log.close()
        return 0

    if not args.yes:
        try:
            ans = input("\nTiến hành cài theo kế hoạch trên? [Y/N]: ").strip().lower()
        except EOFError:
            ans = ""
        log.quiet(f"  trả lời: {ans!r}")
        if ans not in ("y", "yes", "c", "co", "có"):
            log("Huỷ — không cài gì.")
            log.close()
            return 2

    log("\n[c] CÀI")
    install_tools(plan, det, log)
    rc = run_stream(icmd, log, cwd=ROOT)
    if rc != 0:
        log(f"\n[LỖI] install.py thất bại (rc={rc}). Xem log: {log.path}")
        log("  Gợi ý: hết ổ → --envs-dir sang ổ khác; sai CUDA → --cuda cu124/cu121 hoặc --cpu; mạng chập → chạy lại.")
        log.close()
        return 1
    if plan["funasr"]:
        install_funasr(plan, log)

    configure(plan, log, ROOT, dry=False)

    log("\n[e] KIỂM (doctor)")
    mpy = venv_python(Path(plan["envs_dir"]) / "pineline_env")
    dpy = str(mpy) if mpy.is_file() else sys.executable
    dcmd = [dpy, str(ROOT / "scripts" / "check_env.py")] + ([] if args.online_check else ["--offline"])
    run_stream(dcmd, log, cwd=ROOT)
    log("\nVIỆC TAY còn lại:")
    for i, s in enumerate(MANUAL_TODO, 1):
        log(f"  {i}. {s}")
    log("\nXONG. Chạy app: nháy đúp run_v4.bat (dùng python của pineline_env qua .pineline_env_path).")
    log(f"Log: {log.path}")
    log.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
