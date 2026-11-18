# `scripts.setup_machine`

[← Index](../generated/module-index.md) · [Brain home](../README.md)

<!-- AUTO:START — sinh bởi scripts/brain_build.py 2026-11-17 19:05. Đừng sửa tay khối này. -->
**File:** `scripts/setup_machine.py` · **Lớp:** `ops` · **1091 dòng** (924 code) · **48 hàm**, **1 class** · sha1 `c6bc68a413`

> setup_machine.py — Cài Pineline V4 trên MÁY MỚI: detect máy → lập kế hoạch → cài → cấu hình → kiểm. Thường KHÔNG chạy trực tiếp: nháy đúp `SETUP_MAY_MOI.bat` ở gốc V4 (nó tìm Python 3.12/3.11 rồi gọi file này). Chạy tay:

### Phụ thuộc

- **Gọi tới (import nội bộ):** —
- **Được dùng bởi:** —
- **Được nhắc tên file `.py` (subprocess/script) bởi:** [install](./install.md)
- **Test:** ❌ chưa có test import trực tiếp

### Hàm & class top-level

| Tên | Dòng | Dài | Tham số | Docstring |
|---|---:|---:|---|---|
| **class `Log`** | 71 | 4 method | |  |
| `_null_log` | 105 | 2 | `msg` |  |
| `run_capture` | 115 | 12 | `cmd, timeout` | Chạy lệnh ngắn, trả (rc, stdout+stderr). Không có lệnh → (127, ''). |
| `run_stream` | 129 | 18 | `cmd, log, cwd, env` | Chạy lệnh dài, in + ghi log từng dòng. |
| `_q` | 149 | 3 | `c` |  |
| `parse_gpu_query` | 157 | 25 | `text` | Parse `nvidia-smi --query-gpu=name,driver_version,memory.total,compute_cap --format=csv,noheader`. |
| `parse_cuda_version` | 184 | 4 | `text` | 'CUDA Version: 12.9' trong header `nvidia-smi` → (12, 9). |
| `driver_to_cuda` | 190 | 12 | `driver` | Ước lượng CUDA tối đa driver hỗ trợ (khi header không có). Bảng NVIDIA (nhánh driver chính). |
| `_nvidia_smi_exe` | 204 | 10 | `` |  |
| `detect_gpu_info` | 216 | 19 | `runner, exe` | {'gpus': [...], 'cuda': (12, 8)/None, 'smi': path/None, 'error': str}. |
| `_win_reg` | 237 | 8 | `path, name, hive` |  |
| `detect_os` | 247 | 23 | `` |  |
| `detect_cpu` | 272 | 13 | `` |  |
| `detect_ram_gb` | 287 | 25 | `` |  |
| `free_gb` | 314 | 8 | `path` |  |
| `detect_drives` | 324 | 33 | `` | Ổ đĩa cố định (Windows) / gốc + thư mục dự án (Linux/mac). [{'root','free_gb','total_gb'}]. |
| `read_config` | 359 | 6 | `path` |  |
| `_setting` | 367 | 3 | `cfg, key, default` |  |
| `find_llama_server` | 372 | 16 | `presets_dir` |  |
| `find_py_launcher` | 390 | 10 | `` |  |
| `detect_tools` | 402 | 23 | `cfg` |  |
| `detect` | 427 | 14 | `root, runner` |  |
| `_read_first_line` | 443 | 5 | `p` |  |
| `best_gpu` | 453 | 2 | `gpus` |  |
| `_fmt_cv` | 457 | 2 | `cv` |  |
| `choose_torch_build` | 461 | 55 | `gpus, cuda_ver, force_cpu, force_gpu, cuda_override` | Chọn build torch (index download.pytorch.org/whl/<build>). |
| `choose_profile` | 518 | 15 | `gpu, use_gpu` | Hồ sơ hiệu năng: rtx5060ti / rtx3060 / small / cpu. |
| `profile_perf_keys` | 535 | 17 | `profile, root` | Chỉ lấy key máy/hiệu năng (PERF_KEYS) từ file profile; không lấy đường dẫn/SUB_* của máy gốc. |
| `choose_envs_dir` | 554 | 24 | `default_dir, drives, need_gb, existing_python, free_fn` | Nơi đặt venv. Ưu tiên: venv đã có (.pineline_env_path / <default>/pineline_env) → thư mục cha của V4 |
| `temp_dir_for` | 580 | 6 | `envs_dir, root, is_win` | TEMP riêng cùng ổ với venv (Windows: <ổ>:\PinelineV4_tmp); khác: <V4>/scratch/tmp. |
| `venv_python` | 588 | 2 | `venv_dir, is_win` |  |
| `build_plan` | 592 | 34 | `det, args, root` |  |
| `merge_config` | 631 | 26 | `existing, updates, force, path_keys` | GỘP: không bao giờ xoá key cũ; key đã có giá trị thì GIỮ, trừ: |
| `write_config_merged` | 659 | 20 | `path, updates, force, backup_dir, dry_run, note` | Đọc → gộp → ghi atomic (backup bản cũ vào backup_dir). dry_run: chỉ trả thay đổi. |
| `config_updates` | 681 | 21 | `plan, root` |  |
| `_norm` | 727 | 2 | `name` |  |
| `parse_requirements` | 731 | 14 | `path` |  |
| `scan_third_party_imports` | 747 | 39 | `root, skip_dirs` | {top_module: {file,...}} các import tuyệt đối không phải stdlib / module nội bộ của V4. |
| `requirements_report` | 788 | 18 | `root` | {'ok': {...}, 'optional': {...}, 'provided': {...}, 'missing': {mod: (pip, files)}}. |
| `_table` | 811 | 3 | `log, rows, w` |  |
| `print_detect` | 816 | 28 | `det, log` |  |
| `print_plan` | 846 | 17 | `plan, log` |  |
| `refresh_path_windows` | 883 | 14 | `` | Sau winget: nạp lại PATH từ registry (tiến trình hiện tại không tự thấy PATH mới). |
| `install_tools` | 899 | 17 | `plan, det, log` |  |
| `install_cmd` | 918 | 15 | `plan, args, py, root, dry` |  |
| `install_funasr` | 935 | 11 | `plan, log, root` |  |
| `configure` | 951 | 34 | `plan, log, root, dry` |  |
| `parse_args` | 990 | 14 | `argv` |  |
| `main` | 1006 | 82 | `argv` |  |

### Config / env keys (3)

`LOCALAPPDATA`, `PATH`, `WINDIR`

**File/artifact nhắc tới:** `pineline.config.json`, `pineline.config.rtx3060.json`, `pineline.config.rtx5060ti.json`, `requirements-main.txt`, `requirements-optional.txt`

**Tín hiệu rủi ro (đếm tĩnh):** broad_except=4 · file_writes=2 · subprocess=2 · swallow_except=1

### Lịch sử (từ docs/)

- Fix logs: —
- Nhắc trong CHANGELOG: **0** lần · DECISIONS: **0** lần

<!-- AUTO:END -->

<!-- MANUAL:START -->
## Vai trò (viết tay)

_Chưa viết. 2–4 câu: module này chịu trách nhiệm gì trong pipeline, ai gọi nó, nó KHÔNG làm gì._

## Luồng chính

_Các hàm vào (entry) → bước chính → output/side effect. Ghi tên hàm thật._

## Bất biến & hợp đồng

_Điều luôn phải đúng (vd: chỉ ghi manifest qua `Manifest.update`; 1 job / ghế). Vi phạm = bug._

## Bẫy đã biết

_Lỗi từng gặp + link `docs/fixes/...`. Những chỗ dễ sửa sai._

## Ghi chú vận hành

_Config key quan trọng, cần restart gì khi sửa (:8801 / :8802 / hot-reload), cách test._
<!-- MANUAL:END -->
