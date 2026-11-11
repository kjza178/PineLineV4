# `manifest`

[← Index](../generated/module-index.md) · [Brain home](../README.md)

<!-- AUTO:START — sinh bởi scripts/brain_build.py 2026-11-11 02:37. Đừng sửa tay khối này. -->
**File:** `manifest.py` · **Lớp:** `control` · **242 dòng** (190 code) · **4 hàm**, **1 class** · sha1 `12aa6e37d2`

> manifest.py — Trạng thái/checkpoint cho pipeline. Mỗi job (mỗi video) có một thư mục làm việc riêng chứa manifest.json. Mỗi stage ghi trạng thái vào đây; crash/mất điện thì resume từ stage cuối

### Phụ thuộc

- **Gọi tới (import nội bộ):** [fileio](./fileio.md)
- **Được dùng bởi:** [agent_brain](./agent_brain.md), [agent_hang_fix](./agent_hang_fix.md), [agent_name_pass](./agent_name_pass.md), [agent_pronoun_pass](./agent_pronoun_pass.md), [agent_qa_gate](./agent_qa_gate.md), [asr](./asr.md), [asr_hybrid_progress](./asr_hybrid_progress.md), [auto_publisher](./auto_publisher.md), [clone_tts](./clone_tts.md), [download](./download.md), [firered_asr](./firered_asr.md), [fun_asr_nano](./fun_asr_nano.md), [hardsub_asr](./hardsub_asr.md), [hybrid_asr](./hybrid_asr.md), [mux](./mux.md), [nano_fa_asr](./nano_fa_asr.md), [ocr](./ocr.md), [paraformer_zh](./paraformer_zh.md), [pronoun_consistency](./pronoun_consistency.md), [render](./render.md), [routes_agent](./routes_agent.md), [scripts.check_batch4](./scripts.check_batch4.md), [sensevoice_asr](./sensevoice_asr.md), [separate](./separate.md), [server](./server.md), [split_parts](./split_parts.md), [translate](./translate.md), [translate_alts](./translate_alts.md)
- **Được nhắc tên file `.py` (subprocess/script) bởi:** [restart_server](./restart_server.md)
- **Test:** `tests/test_agent_core_smoke.py`, `tests/test_asr_demucs.py`

```mermaid
flowchart LR
  manifest[[manifest]]
  agent_brain[agent_brain] --> manifest
  agent_hang_fix[agent_hang_fix] --> manifest
  agent_name_pass[agent_name_pass] --> manifest
  agent_pronoun_pass[agent_pronoun_pass] --> manifest
  agent_qa_gate[agent_qa_gate] --> manifest
  asr[asr] --> manifest
  asr_hybrid_progress[asr_hybrid_progress] --> manifest
  auto_publisher[auto_publisher] --> manifest
  clone_tts[clone_tts] --> manifest
  download[download] --> manifest
  firered_asr[firered_asr] --> manifest
  fun_asr_nano[fun_asr_nano] --> manifest
  hardsub_asr[hardsub_asr] --> manifest
  hybrid_asr[hybrid_asr] --> manifest
  mux[mux] --> manifest
  manifest --> fileio[fileio]
```

### Hàm & class top-level

| Tên | Dòng | Dài | Tham số | Docstring |
|---|---:|---:|---|---|
| **class `Manifest`** | 96 | 11 method | |  |
| `_now` | 26 | 2 | `` |  |
| `_lock_for` | 39 | 8 | `path` |  |
| `_merge3` | 52 | 22 | `base, mine, theirs` | Gộp 3 chiều dict JSON. Key mình không đổi so với lúc load → lấy bản đĩa (người khác |
| `_xproc_lock` | 77 | 17 | `path` | Khoá liên tiến trình (server + subprocess asr/tts cùng ghi). Không lấy được thì vẫn ghi |

**File/artifact nhắc tới:** `manifest.json`

**Tín hiệu rủi ro (đếm tĩnh):** broad_except=2 · file_writes=2 · sleep=3

### Lịch sử (từ docs/)

- **Fix logs (2):**
  - [REVIEW CLI song song + heal làm UI mất/soát % tụt](../../fixes/2026-11-10-review-heal-parallel.md)
  - [2026-10-06 — Đợt 4 review: tranh chấp ghi, một bản tiến trình, checkpoint an toàn](../../fixes/2026-10-06-batch4-write-races.md)
- **Reviews:** [2026-10-06-code-review](../../reviews/2026-10-06-code-review.md)
- Nhắc trong CHANGELOG: **1** lần · DECISIONS: **1** lần

<!-- AUTO:END -->

<!-- MANUAL:START -->
## Vai trò (viết tay)

Trạng thái/checkpoint của **mỗi job**: `work/<job>/manifest.json` (`stages.{download,asr,translate,tts,mux}` + `agent`, opts, title…). Mọi stage, server, agent và cả subprocess ASR/TTS đều đọc-ghi file này ⇒ đây là **trái tim đồng thời** của hệ thống (~26 module nhắc tới `manifest.json`, xem `generated/artifacts-ports.md`). Không chứa logic pipeline.

## Luồng chính

- `Manifest(work_dir)` → `load()` (khoá theo path, retry 6 lần nếu đọc trúng lúc ghi; hỏng → `_load_failed=True`, giữ data cũ).
- **Ghi an toàn — ưu tiên `update(fn)`**: khoá thread (`_lock_for`) + khoá liên tiến trình (`_xproc_lock` → `fileio.file_lock`) → đọc lại đĩa → `fn(data)` → `_write_locked`. Trả `False` nếu đĩa hỏng/thiếu `stages` hoặc `fn` trả `False`.
- `save()`: cho object sống lâu — gộp 3 chiều `_merge3(base, mine, disk)` (mình không đổi key → lấy đĩa; cả hai đổi dict → gộp sâu; còn lại mình thắng).
- `_write_locked`: ghi tmp riêng theo pid+thread → `os.replace` (retry ~2.5s cho WinError 5/32) → bó tay thì ghi thẳng.
- Helper stage: `mark_running`, `set_stage`, `mark_done`, `mark_failed`, `is_done`, `stage`.

## Bất biến & hợp đồng

- Không bao giờ ghi manifest bằng `json.dump` trực tiếp ngoài module này — dùng `update(fn)` (đọc-sửa-ghi nguyên tử) hoặc `save()`.
- Không ghi đè bằng data rỗng: `save()` bỏ qua nếu `_load_failed` hoặc `stages` rỗng trong khi đĩa còn `stages`.
- `fn` trong `update` phải nhanh và không gọi I/O nặng (đang giữ khoá liên tiến trình, timeout 5s).

## Bẫy đã biết

- `_xproc_lock` **không lấy được khoá vẫn ghi** (log `[manifest] không lấy được khoá … — ghi không khoá`) → lúc tranh chấp nặng có thể mất cập nhật của tiến trình khác. Grep log này khi nghi race. (chưa xác minh tần suất)
- Fallback cuối của `_write_locked` ghi **không atomic** → mất điện đúng lúc đó có thể hỏng file; `load()` sẽ đánh dấu `_load_failed` thay vì xoá.
- `save()` "mình thắng" khi cả hai đổi cùng key không phải dict → object giữ lâu có thể ghi đè giá trị mới của người khác (vd `status`). Ưu tiên `update`.
- Lịch sử: wipe dữ liệu job (`docs/fixes/2026-10-06-batch1-data-loss.md`, `batch4-write-races.md`), mất `script.json` sau restart (`2026-11-10-05670-script-wipe.md` — khác file nhưng cùng loại).

## Ghi chú vận hành

Import ở mọi nơi ⇒ sửa module này cần restart **:8801 và :8802**, subprocess ASR/TTS mới sẽ tự nạp. Test: `tests/test_job_queue*.py`, `scripts/check_batch4.py` (races).
<!-- MANUAL:END -->
