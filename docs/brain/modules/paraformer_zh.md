# `paraformer_zh`

[← Index](../generated/module-index.md) · [Brain home](../README.md)

<!-- AUTO:START — sinh bởi scripts/brain_build.py 2026-11-11 02:37. Đừng sửa tay khối này. -->
**File:** `paraformer_zh.py` · **Lớp:** `asr` · **309 dòng** (275 code) · **2 hàm**, **0 class** · sha1 `1493748661`

> paraformer_zh.py — STAGE ASR bằng FunASR Paraformer-zh (timestamp tốt cho phụ đề/TTS). Model : paraformer-zh (+ fsmn-vad + ct-punc) Đầu vào : work/<job>/source.mp4

### Phụ thuộc

- **Gọi tới (import nội bộ):** [asr](./asr.md), [asr_align_nano_para](./asr_align_nano_para.md), [asr_hybrid_progress](./asr_hybrid_progress.md), [asr_spam](./asr_spam.md), [asr_vad_utils](./asr_vad_utils.md), [fun_asr_nano](./fun_asr_nano.md), [manifest](./manifest.md), [subs](./subs.md), [vram](./vram.md)
- **Được dùng bởi:** [hybrid_asr](./hybrid_asr.md)
- **Được nhắc tên file `.py` (subprocess/script) bởi:** [fun_asr_nano](./fun_asr_nano.md), [restart_server](./restart_server.md), [server](./server.md)
- **Test:** ❌ chưa có test import trực tiếp
- **Thư viện ngoài:** `funasr`, `soundfile`

```mermaid
flowchart LR
  paraformer_zh[[paraformer_zh]]
  hybrid_asr[hybrid_asr] --> paraformer_zh
  paraformer_zh --> asr[asr]
  paraformer_zh --> asr_align_nano_para[asr_align_nano_para]
  paraformer_zh --> asr_hybrid_progress[asr_hybrid_progress]
  paraformer_zh --> asr_spam[asr_spam]
  paraformer_zh --> asr_vad_utils[asr_vad_utils]
  paraformer_zh --> fun_asr_nano[fun_asr_nano]
  paraformer_zh --> manifest[manifest]
  paraformer_zh --> subs[subs]
  paraformer_zh --> vram[vram]
```

### Hàm & class top-level

| Tên | Dòng | Dài | Tham số | Docstring |
|---|---:|---:|---|---|
| `run_asr_paraformer` | 45 | 245 ⚠️ | `work_dir, device, force, hub, sidecar, slice_mode` |  |
| `main` | 292 | 14 | `argv` |  |

**Hàm dài ≥120 dòng:** `run_asr_paraformer` (245, L45)

### Config / env keys (2)

`HF_HUB_DISABLE_SYMLINKS`, `HF_HUB_DISABLE_SYMLINKS_WARNING`

**File/artifact nhắc tới:** `.chars.json`, `.progress.json`, `asr.chars.json`, `asr.json`, `audio.wav`, `sub.zh.srt`

**Tín hiệu rủi ro (đếm tĩnh):** broad_except=3 · file_writes=8 · swallow_except=1

### Lịch sử (từ docs/)

- **Fix logs (1):**
  - [2026-10-06 — Đợt 4 review: tranh chấp ghi, một bản tiến trình, checkpoint an toàn](../../fixes/2026-10-06-batch4-write-races.md)
- **Reviews:** [2026-11-02-v4-structure-and-v2-port](../../reviews/2026-11-02-v4-structure-and-v2-port.md), [2026-10-06-code-review](../../reviews/2026-10-06-code-review.md)
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
