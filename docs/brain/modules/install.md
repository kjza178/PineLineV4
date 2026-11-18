# `install`

[← Index](../generated/module-index.md) · [Brain home](../README.md)

<!-- AUTO:START — sinh bởi scripts/brain_build.py 2026-11-17 19:05. Đừng sửa tay khối này. -->
**File:** `install.py` · **Lớp:** `ops` · **386 dòng** (325 code) · **16 hàm**, **0 class** · sha1 `02798f09f6`

> install.py — Dựng venv + torch + requirements cho Pineline V4 trên BẤT KỲ máy nào. Máy mới: KHÔNG cần gọi tay — nháy đúp `SETUP_MAY_MOI.bat` (detect máy → gọi file này với tham số đúng). Chạy tay:

### Phụ thuộc

- **Gọi tới (import nội bộ):** —
- **Được dùng bởi:** —
- **Được nhắc tên file `.py` (subprocess/script) bởi:** [clone_tts](./clone_tts.md), [config](./config.md), [machine](./machine.md), [scripts.check_env](./scripts.check_env.md), [scripts.setup_machine](./scripts.setup_machine.md)
- **Test:** ❌ chưa có test import trực tiếp

### Hàm & class top-level

| Tên | Dòng | Dài | Tham số | Docstring |
|---|---:|---:|---|---|
| `say` | 50 | 2 | `msg, c` |  |
| `run` | 54 | 5 | `cmd, **kw` |  |
| `_load_setup_machine` | 61 | 11 | `` | scripts/setup_machine.py (stdlib) — detect GPU + chọn build + gộp config. None nếu lỗi. |
| `_pip_env` | 74 | 8 | `tmp` | TEMP + pip tạm CÙNG Ổ với venv (tránh đầy ổ C:). Tắt cache để khỏi giữ ~2.5GB torch. |
| `free_gb` | 84 | 8 | `path` |  |
| `venv_python` | 94 | 2 | `venv_dir` |  |
| `have` | 98 | 2 | `exe` |  |
| `detect_gpu` | 102 | 8 | `` |  |
| `auto_build` | 112 | 17 | `force_cpu, force_gpu` | (build, lý do) — dùng luật của scripts/setup_machine.py; dự phòng: có GPU → cu124, không → cpu. |
| `create_venv` | 131 | 9 | `path` |  |
| `pip_install` | 142 | 5 | `py, *args, index_url, tmp` |  |
| `torch_index` | 149 | 2 | `build` |  |
| `installed_torch_build` | 153 | 15 | `py` | 'cu128' / 'cpu' / None (chưa có torch). Đọc hậu tố +cuXXX của torch.__version__. |
| `merge_into_config` | 170 | 17 | `path, updates, force` | GỘP (không ghi đè): dùng merge của setup_machine; dự phòng: chỉ thêm key thiếu. |
| `launcher_texts` | 189 | 13 | `mpy_abs` | Nội dung start.bat / start.sh — trỏ entry THẬT của V4 (app_desktop.py / server.py). |
| `main` | 204 | 179 ⚠️ | `argv` |  |

**Hàm dài ≥120 dòng:** `main` (179, L204)

**File/artifact nhắc tới:** `pineline.config.json`, `requirements-main.txt`, `requirements-vieneu.txt`

**Tín hiệu rủi ro (đếm tĩnh):** broad_except=10 · file_writes=2 · global_stmt=1 · subprocess=4 · swallow_except=2

### Lịch sử (từ docs/)

- Fix logs: —
- **Reviews:** [2026-10-06-code-review](../../reviews/2026-10-06-code-review.md)
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
