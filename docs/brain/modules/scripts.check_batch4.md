# `scripts.check_batch4`

[← Index](../generated/module-index.md) · [Brain home](../README.md)

<!-- AUTO:START — sinh bởi scripts/brain_build.py 2026-11-11 02:37. Đừng sửa tay khối này. -->
**File:** `scripts/check_batch4.py` · **Lớp:** `ops` · **452 dòng** (370 code) · **6 hàm**, **2 class** · sha1 `a85f33b7d3`

> Kiểm thử đợt 4 (tranh chấp ghi manifest, claim endpoint, single-instance, worker khởi động). Chạy trên thư mục tạm; import server như pytest (không nạp hàng đợi thật).

### Phụ thuộc

- **Gọi tới (import nội bộ):** [agent_autopilot](./agent_autopilot.md), [agent_core](./agent_core.md), [asr](./asr.md), [assemble](./assemble.md), [clone_tts](./clone_tts.md), [job_queue](./job_queue.md), [manifest](./manifest.md), [render](./render.md), [server](./server.md)
- **Được dùng bởi:** —
- **Test:** ❌ chưa có test import trực tiếp
- **Thư viện ngoài:** `psutil`, `pytest`

```mermaid
flowchart LR
  scripts_check_batch4[[scripts.check_batch4]]
  scripts_check_batch4 --> agent_autopilot[agent_autopilot]
  scripts_check_batch4 --> agent_core[agent_core]
  scripts_check_batch4 --> asr[asr]
  scripts_check_batch4 --> assemble[assemble]
  scripts_check_batch4 --> clone_tts[clone_tts]
  scripts_check_batch4 --> job_queue[job_queue]
  scripts_check_batch4 --> manifest[manifest]
  scripts_check_batch4 --> render[render]
  scripts_check_batch4 --> server[server]
```

### Hàm & class top-level

| Tên | Dòng | Dài | Tham số | Docstring |
|---|---:|---:|---|---|
| **class `M`** | 316 | 1 method | |  |
| **class `_Boom`** | 411 | 0 method | |  |
| `check` | 19 | 4 | `name, cond` |  |
| `fake_post` | 254 | 3 | `base, path, body, timeout` |  |
| `fake_baf` | 305 | 3 | `cmd, work_dir, dub, nv, voc, audio_mode, vv, ov` |  |
| `fake_ff` | 310 | 4 | `cmd, total, m, cwd, hi` |  |
| `mk_wav` | 345 | 6 | `p, sec, sr` |  |
| `fake_worker` | 415 | 3 | `engine, ref, ref_text, out_dir, speed, todo, on_prog` |  |

**File/artifact nhắc tới:** `.server_test.lock`, `.sidecar_18902.lock`, `_keys.json`, `_vieneu_job.json`, `audio.partial.wav`, `audio.wav`, `audio.wav.json`, `dub.wav`, `dub_fit.partial.wav`, `dub_fit.wav`, `manifest.json`, `mixed_audio.json`, `no_vocals.wav`, `ref.wav`, `script.json`, `seg_0000.wav`, `seg_0001.wav`, `source.m4a`, `tts.json`, `tts_config.json`, `v.mp4`, `vocals.wav`

**Tín hiệu rủi ro (đếm tĩnh):** broad_except=1 · file_writes=11 · global_stmt=1 · subprocess=5

### Lịch sử (từ docs/)

- **Fix logs (2):**
  - [2026-10-06 — Đợt 5 review: agent an toàn hơn](../../fixes/2026-10-06-batch5-agent-safety.md)
  - [2026-10-06 — Đợt 4 review: tranh chấp ghi, một bản tiến trình, checkpoint an toàn](../../fixes/2026-10-06-batch4-write-races.md)
- Nhắc trong CHANGELOG: **1** lần · DECISIONS: **0** lần

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
