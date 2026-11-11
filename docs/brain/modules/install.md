# `install`

[← Index](../generated/module-index.md) · [Brain home](../README.md)

<!-- AUTO:START — sinh bởi scripts/brain_build.py 2026-11-11 02:37. Đừng sửa tay khối này. -->
**File:** `install.py` · **Lớp:** `ops` · **241 dòng** (189 code) · **11 hàm**, **0 class** · sha1 `0fd67d1656`

> install.py — Bộ cài Pineline TỰ DETECT máy + dựng môi trường trên BẤT KỲ máy nào. Chạy:  python install.py            (tự detect GPU/CPU) python install.py --cpu      (ép CPU, không CUDA)

### Phụ thuộc

- **Gọi tới (import nội bộ):** —
- **Được dùng bởi:** —
- **Được nhắc tên file `.py` (subprocess/script) bởi:** [clone_tts](./clone_tts.md), [config](./config.md)
- **Test:** ❌ chưa có test import trực tiếp

### Hàm & class top-level

| Tên | Dòng | Dài | Tham số | Docstring |
|---|---:|---:|---|---|
| `say` | 34 | 2 | `msg, c` |  |
| `run` | 38 | 3 | `cmd, **kw` |  |
| `_pip_env` | 47 | 6 | `` |  |
| `free_gb` | 55 | 5 | `path` |  |
| `venv_python` | 62 | 2 | `venv_dir` |  |
| `have` | 66 | 2 | `exe` |  |
| `detect_gpu` | 70 | 8 | `` |  |
| `create_venv` | 80 | 9 | `path` |  |
| `pip_install` | 91 | 5 | `py, *args, index_url` |  |
| `torch_index` | 98 | 2 | `gpu, cuda` |  |
| `main` | 102 | 136 ⚠️ | `` |  |

**Hàm dài ≥120 dòng:** `main` (136, L102)

**File/artifact nhắc tới:** `pineline.config.json`, `requirements-main.txt`, `requirements-vieneu.txt`

**Tín hiệu rủi ro (đếm tĩnh):** broad_except=5 · file_writes=3 · subprocess=2 · swallow_except=1

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
