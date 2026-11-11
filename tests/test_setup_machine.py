"""Test bộ cài máy mới: scripts/setup_machine.py + install.py (không cần Windows/GPU/mạng)."""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sm = _load("t_setup_machine", "scripts/setup_machine.py")

SMI_5060TI = "NVIDIA GeForce RTX 5060 Ti, 576.52, 16311 MiB, 12.0\n"
HEAD_5060TI = "| NVIDIA-SMI 576.52   Driver Version: 576.52   CUDA Version: 12.9     |\n"
SMI_3060 = "NVIDIA GeForce RTX 3060, 537.58, 12288 MiB, 8.6\n"
HEAD_3060 = "| NVIDIA-SMI 537.58                 Driver Version: 537.58       CUDA Version: 12.2     |\n"


def _runner(query_out: str, head_out: str, rc: int = 0):
    def run(cmd, timeout=20):
        if len(cmd) == 1:
            return rc, head_out
        return rc, query_out
    return run


# ── parse nvidia-smi ─────────────────────────────────────────────────────────
def test_parse_5060ti():
    g = sm.parse_gpu_query(SMI_5060TI)
    assert g == [{"name": "NVIDIA GeForce RTX 5060 Ti", "driver": "576.52", "mem_mb": 16311, "cc": 12.0}]
    assert sm.parse_cuda_version(HEAD_5060TI) == (12, 9)


def test_parse_3060_and_missing_cc():
    assert sm.parse_gpu_query(SMI_3060)[0]["cc"] == 8.6
    assert sm.parse_cuda_version(HEAD_3060) == (12, 2)
    g = sm.parse_gpu_query("Quadro P2000, 472.12, 5120 MiB\n")
    assert g[0]["cc"] is None and g[0]["mem_mb"] == 5120
    assert sm.parse_gpu_query("") == []
    assert sm.parse_gpu_query("NVIDIA-SMI has failed because it couldn't communicate\n") == []


def test_detect_gpu_info_runner():
    gi = sm.detect_gpu_info(_runner(SMI_5060TI, HEAD_5060TI), exe="nvidia-smi")
    assert gi["gpus"][0]["cc"] == 12.0 and gi["cuda"] == (12, 9)
    none = sm.detect_gpu_info(_runner("", "", rc=127), exe=None)
    assert none["gpus"] == [] and none["cuda"] is None


# ── build torch ──────────────────────────────────────────────────────────────
def test_build_5060ti_cu128():
    tb = sm.choose_torch_build(sm.parse_gpu_query(SMI_5060TI), (12, 9))
    assert tb["build"] == "cu128" and tb["gpu"] and not tb["warnings"]


def test_build_blackwell_old_driver_warns_but_cu128():
    gpus = [{"name": "NVIDIA GeForce RTX 5060 Ti", "driver": "560.94", "mem_mb": 16311, "cc": 12.0}]
    tb = sm.choose_torch_build(gpus, (12, 6))
    assert tb["build"] == "cu128" and any("DRIVER" in w for w in tb["warnings"])


def test_build_3060_driver_537_cu121():
    tb = sm.choose_torch_build(sm.parse_gpu_query(SMI_3060), (12, 2))
    assert tb["build"] == "cu121"


def test_build_by_cuda_ranges_and_driver_fallback():
    g = [{"name": "RTX 3060", "driver": "555.85", "mem_mb": 12288, "cc": 8.6}]
    assert sm.choose_torch_build(g, (12, 5))["build"] == "cu124"
    assert sm.choose_torch_build(g, (12, 8))["build"] == "cu128"
    # header không có → suy từ driver 555 → 12.5 → cu124
    assert sm.choose_torch_build(g, None)["build"] == "cu124"
    g2 = [{"name": "RTX 3060", "driver": "576.02", "mem_mb": 12288, "cc": 8.6}]
    assert sm.choose_torch_build(g2, None)["build"] == "cu128"


def test_build_old_driver_cpu_and_warn():
    g = [{"name": "GTX 1080", "driver": "472.12", "mem_mb": 8192, "cc": 6.1}]
    tb = sm.choose_torch_build(g, (11, 4))
    assert tb["build"] == "cpu" and tb["warnings"]
    assert sm.choose_torch_build(g, (11, 4), force_gpu=True)["build"] == "cu121"


def test_build_old_arch_new_driver_cu124():
    g = [{"name": "GTX 1080", "driver": "576.02", "mem_mb": 8192, "cc": 6.1}]
    assert sm.choose_torch_build(g, (12, 9))["build"] == "cu124"


def test_build_no_gpu_and_overrides():
    assert sm.choose_torch_build([], None)["build"] == "cpu"
    assert sm.choose_torch_build([], None, force_gpu=True)["build"] == "cu128"
    g = sm.parse_gpu_query(SMI_5060TI)
    assert sm.choose_torch_build(g, (12, 9), force_cpu=True)["build"] == "cpu"
    assert sm.choose_torch_build(g, (12, 9), cuda_override="cu124")["build"] == "cu124"
    assert sm.choose_torch_build([], None, cuda_override="cpu")["gpu"] is False


# ── profile ──────────────────────────────────────────────────────────────────
def test_profile_by_name_and_vram():
    assert sm.choose_profile(sm.parse_gpu_query(SMI_5060TI)[0])[0] == "rtx5060ti"
    assert sm.choose_profile(sm.parse_gpu_query(SMI_3060)[0])[0] == "rtx3060"
    assert sm.choose_profile({"name": "RTX 4080", "mem_mb": 16376})[0] == "rtx5060ti"
    assert sm.choose_profile({"name": "RTX 4070", "mem_mb": 12282})[0] == "rtx3060"
    assert sm.choose_profile({"name": "RTX 4060", "mem_mb": 8188})[0] == "small"
    assert sm.choose_profile(None)[0] == "cpu"
    assert sm.choose_profile({"name": "RTX 3060", "mem_mb": 12288}, use_gpu=False)[0] == "cpu"


def test_profile_keys_only_perf():
    k = sm.profile_perf_keys("rtx5060ti", ROOT)
    assert k["VIENEU_CPU_THREADS"] == "2" and k["RENDER_ENCODER"] == "nvenc"
    for bad in ("VIENEU_PY", "OMNI_PY", "HF_HOME", "SUB_WRAP_CHARS", "_note"):
        assert bad not in k
    k3 = sm.profile_perf_keys("rtx3060", ROOT)
    assert k3["TRANSLATE_BATCH"] == "100" and "VIENEU_CPU_THREADS" not in k3
    assert sm.profile_perf_keys("cpu", ROOT)["RENDER_ENCODER"] == "x264"
    assert sm.profile_perf_keys("small", ROOT)["VIENEU_BATCH"] == "4"


# ── nơi đặt venv / TEMP ──────────────────────────────────────────────────────
def test_envs_dir_default_when_enough(tmp_path):
    r = sm.choose_envs_dir(tmp_path, [], 15, free_fn=lambda p: 100.0)
    assert r["dir"] == tmp_path and not r["warning"]


def test_envs_dir_pick_biggest_drive(tmp_path):
    drives = [{"root": "C:\\", "free_gb": 20.0}, {"root": "E:\\", "free_gb": 400.0}]
    r = sm.choose_envs_dir(tmp_path, drives, 15, free_fn=lambda p: 5.0)
    assert str(r["dir"]).startswith("E:") and "PinelineEnvs" in str(r["dir"])


def test_envs_dir_none_enough_warns(tmp_path):
    r = sm.choose_envs_dir(tmp_path, [{"root": "C:\\", "free_gb": 3.0}], 15, free_fn=lambda p: 2.0)
    assert r["dir"] == tmp_path and r["warning"]


def test_envs_dir_reuse_existing(tmp_path):
    py = tmp_path / "X" / "pineline_env" / "Scripts" / "python.exe"
    py.parent.mkdir(parents=True)
    py.write_text("")
    r = sm.choose_envs_dir(tmp_path / "other", [], 15, existing_python=str(py), free_fn=lambda p: 0.0)
    assert r["dir"] == tmp_path / "X"
    (tmp_path / "Y" / "pineline_env").mkdir(parents=True)
    r2 = sm.choose_envs_dir(tmp_path / "Y", [], 15, free_fn=lambda p: 0.0)
    assert r2["dir"] == tmp_path / "Y" and not r2["warning"]


def test_temp_dir(tmp_path):
    assert str(sm.temp_dir_for(Path("E:\\PinelineEnvs"), tmp_path, is_win=True)).startswith("E:")
    assert sm.temp_dir_for(Path("/x"), tmp_path, is_win=False) == tmp_path / "scratch" / "tmp"


# ── gộp config ───────────────────────────────────────────────────────────────
def test_merge_keeps_user_keys(tmp_path):
    existing = {"LLM_API_KEY": "secret", "VIENEU_BATCH": "16", "HF_HOME": "", "_note": "x",
                "VIENEU_DEVICE": "cuda", "VIENEU_PY": str(tmp_path / "missing" / "python.exe")}
    upd = {"VIENEU_BATCH": "8", "HF_HOME": "E:/AI_CACHE", "TRANSLATE_BATCH": "50",
           "VIENEU_DEVICE": "cpu", "VIENEU_PY": "E:/envs/vieneu_env/Scripts/python.exe"}
    merged, ch = sm.merge_config(existing, upd, force={"VIENEU_DEVICE"})
    assert merged["LLM_API_KEY"] == "secret" and merged["_note"] == "x"
    assert merged["VIENEU_BATCH"] == "16"            # giữ giá trị người dùng
    assert merged["HF_HOME"] == "E:/AI_CACHE"        # rỗng → điền
    assert merged["TRANSLATE_BATCH"] == "50"         # thiếu → thêm
    assert merged["VIENEU_DEVICE"] == "cpu"          # force (phần cứng)
    assert merged["VIENEU_PY"].startswith("E:/envs")  # đường dẫn cũ không tồn tại → thay
    assert set(existing) <= set(merged)
    assert {c[0] for c in ch} == {"HF_HOME", "TRANSLATE_BATCH", "VIENEU_DEVICE", "VIENEU_PY"}


def test_merge_existing_path_kept(tmp_path):
    real = tmp_path / "python.exe"
    real.write_text("")
    merged, ch = sm.merge_config({"VIENEU_PY": str(real)}, {"VIENEU_PY": "E:/x/python.exe"})
    assert merged["VIENEU_PY"] == str(real) and not ch


def test_write_config_merged_file(tmp_path):
    p = tmp_path / "pineline.config.json"
    p.write_text(json.dumps({"LLM_API_KEY": "k", "SUB_FONT": "Arial"}), encoding="utf-8")
    ch = sm.write_config_merged(p, {"VIENEU_DEVICE": "cuda"}, dry_run=True)
    assert ch and "VIENEU_DEVICE" not in json.loads(p.read_text(encoding="utf-8"))   # dry-run không ghi
    sm.write_config_merged(p, {"VIENEU_DEVICE": "cuda"}, backup_dir=tmp_path / "bk")
    d = json.loads(p.read_text(encoding="utf-8"))
    assert d["LLM_API_KEY"] == "k" and d["SUB_FONT"] == "Arial" and d["VIENEU_DEVICE"] == "cuda"
    assert list((tmp_path / "bk").iterdir())
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    with pytest.raises(ValueError):
        sm.write_config_merged(bad, {"A": "1"})
    assert bad.read_text(encoding="utf-8") == "{not json"


def test_config_updates_cpu_forces_devices(tmp_path):
    plan = {"torch": {"gpu": False}, "envs_dir": tmp_path, "temp_dir": tmp_path / "t", "vieneu": True,
            "presets_missing": True, "perf": sm.profile_perf_keys("cpu", ROOT)}
    upd, force = sm.config_updates(plan, ROOT)
    assert upd["VIENEU_DEVICE"] == "cpu" and upd["AUTO_SWITCH_PRESETS"] == "0"
    assert upd["RENDER_ENCODER"] == "x264" and {"VIENEU_DEVICE", "RENDER_ENCODER"} <= force
    assert not any("KEY" in k for k in upd)


# ── install.py ───────────────────────────────────────────────────────────────
@pytest.fixture()
def inst(tmp_path, monkeypatch):
    mod = _load("t_install", "install.py")
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "setup_machine.py").write_text(
        (ROOT / "scripts" / "setup_machine.py").read_text(encoding="utf-8"), encoding="utf-8")
    return mod


def test_install_dry_run_no_pip_no_files(inst, tmp_path, monkeypatch):
    calls = []

    def boom(*a, **k):
        calls.append(a)
        raise AssertionError(f"subprocess gọi khi dry-run: {a}")

    monkeypatch.setattr(subprocess, "run", boom)
    monkeypatch.setattr(subprocess, "Popen", boom)
    cfg = tmp_path / "pineline.config.json"
    cfg.write_text(json.dumps({"LLM_API_KEY": "k"}), encoding="utf-8")
    before = sorted(p.name for p in tmp_path.iterdir())
    envs = tmp_path / "envs"
    rc = inst.main(["--dry-run", "--cpu", "--envs-dir", str(envs)])
    assert rc == 0 and not calls
    assert sorted(p.name for p in tmp_path.iterdir()) == before       # không tạo start.bat/.pineline_env_path
    assert not envs.exists()
    assert json.loads(cfg.read_text(encoding="utf-8")) == {"LLM_API_KEY": "k"}


def test_install_dry_run_gpu_auto_uses_setup_machine(inst, tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: (_ for _ in ()).throw(AssertionError("pip")))
    monkeypatch.setattr(subprocess, "Popen", lambda *a, **k: (_ for _ in ()).throw(AssertionError("popen")))
    rc = inst.main(["--dry-run", "--gpu", "--cuda", "cu128", "--envs-dir", str(tmp_path / "e")])
    out = capsys.readouterr().out
    assert rc == 0 and "whl/cu128" in out and "ollama pull" not in out


def test_launcher_points_to_real_entry(inst):
    t = inst.launcher_texts(Path("E:/envs/pineline_env/Scripts/python.exe"))
    assert inst.LAUNCHER_ENTRY_WIN in t["start.bat"] and "app.py" not in t["start.bat"].replace("app_desktop.py", "")
    assert inst.LAUNCHER_ENTRY_SH in t["start.sh"]
    assert (ROOT / inst.LAUNCHER_ENTRY_WIN).is_file() and (ROOT / inst.LAUNCHER_ENTRY_SH).is_file()
    assert "\r\n" in t["start.bat"]
    t["start.bat"].encode("ascii")


def test_install_merge_not_overwrite(inst, tmp_path):
    cfg = tmp_path / "pineline.config.json"
    cfg.write_text(json.dumps({"LLM_API_KEY": "k", "HF_HOME": "Q:/keep"}), encoding="utf-8")
    inst.DRY = False
    inst.merge_into_config(cfg, {"HF_HOME": str(tmp_path), "VIENEU_DEVICE": "cuda"})
    d = json.loads(cfg.read_text(encoding="utf-8"))
    assert d["LLM_API_KEY"] == "k" and d["VIENEU_DEVICE"] == "cuda"
    assert d["HF_HOME"] == str(tmp_path)   # Q:/keep không tồn tại → đường dẫn được thay


# ── requirements scanner ─────────────────────────────────────────────────────
def test_scanner_fixture(tmp_path):
    (tmp_path / "install").mkdir()
    (tmp_path / "install" / "requirements-main.txt").write_text("requests>=2\nPillow\n", encoding="utf-8")
    (tmp_path / "install" / "requirements-optional.txt").write_text("funasr\n", encoding="utf-8")
    (tmp_path / "a.py").write_text(
        "import os, json\nimport requests\nfrom PIL import Image\nimport b\nimport funasr\nimport psutil\n"
        "try:\n    from core import machine\nexcept ImportError:\n    import machine\nfrom . import x\n",
        encoding="utf-8")
    (tmp_path / "b.py").write_text("import torch\n", encoding="utf-8")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "t.py").write_text("import pytest_xyz\n", encoding="utf-8")
    rep = sm.requirements_report(tmp_path)
    assert set(rep["ok"]) == {"requests", "PIL"}
    assert set(rep["optional"]) == {"funasr"}
    assert "torch" in rep["provided"]
    assert set(rep["missing"]) == {"psutil", "machine"}


def test_real_repo_requirements_complete():
    rep = sm.requirements_report(ROOT)
    assert not rep["missing"], f"import bên thứ ba chưa có trong requirements: {rep['missing']}"
    for must in ("psutil", "fastapi", "uvicorn", "requests", "numpy"):
        assert must in rep["ok"]


# ── .bat ─────────────────────────────────────────────────────────────────────
@pytest.mark.parametrize("name", ["SETUP_MAY_MOI.bat", "run_v4.bat", "run_tele_cmd.bat",
                                  "install_funasr_safe.bat", "install_ort_gpu.bat"])
def test_bat_ascii_crlf(name):
    b = (ROOT / name).read_bytes()
    b.decode("ascii")
    assert b.count(b"\n") == b.count(b"\r\n")


def test_run_v4_prefers_env_path():
    s = (ROOT / "run_v4.bat").read_text(encoding="ascii")
    assert s.index(".pineline_env_path") < s.index(r"C:\Python312")
    assert 'set "TEMP=D:' not in s
    assert "setup_machine.py" in (ROOT / "SETUP_MAY_MOI.bat").read_text(encoding="ascii")


def test_dry_run_cli_subprocess(tmp_path):
    """Chạy thật `setup_machine.py --dry-run` (Linux/cloud: không GPU, không Windows) — phải thoát 0."""
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "setup_machine.py"), "--dry-run"],
                       capture_output=True, text=True, encoding="utf-8", timeout=120, cwd=str(ROOT))
    assert r.returncode == 0, r.stdout[-2000:] + r.stderr[-2000:]
    assert "KẾ HOẠCH" in r.stdout and "DRY-RUN xong" in r.stdout
