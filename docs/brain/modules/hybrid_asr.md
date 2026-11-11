# `hybrid_asr`

[← Index](../generated/module-index.md) · [Brain home](../README.md)

<!-- AUTO:START — sinh bởi scripts/brain_build.py 2026-11-11 02:37. Đừng sửa tay khối này. -->
**File:** `hybrid_asr.py` · **Lớp:** `asr` · **202 dòng** (177 code) · **3 hàm**, **0 class** · sha1 `5b270b9037`

> hybrid_asr.py — ASR chốt: Nano chữ + Para timing + ForcedAlign + Repair. Pipeline (sidecar rồi promote → asr.json): 1) Fun-ASR-Nano     → asr.fun_nano.json

### Phụ thuộc

- **Gọi tới (import nội bộ):** [asr_align_nano_para](./asr_align_nano_para.md), [asr_fix_align](./asr_fix_align.md), [asr_repair](./asr_repair.md), [asr_spam](./asr_spam.md), [fun_asr_nano](./fun_asr_nano.md), [manifest](./manifest.md), [paraformer_zh](./paraformer_zh.md), [subs](./subs.md), [vram](./vram.md)
- **Được dùng bởi:** —
- **Được nhắc tên file `.py` (subprocess/script) bởi:** [restart_server](./restart_server.md), [server](./server.md)
- **Test:** ❌ chưa có test import trực tiếp

```mermaid
flowchart LR
  hybrid_asr[[hybrid_asr]]
  hybrid_asr --> asr_align_nano_para[asr_align_nano_para]
  hybrid_asr --> asr_fix_align[asr_fix_align]
  hybrid_asr --> asr_repair[asr_repair]
  hybrid_asr --> asr_spam[asr_spam]
  hybrid_asr --> fun_asr_nano[fun_asr_nano]
  hybrid_asr --> manifest[manifest]
  hybrid_asr --> paraformer_zh[paraformer_zh]
  hybrid_asr --> subs[subs]
  hybrid_asr --> vram[vram]
```

### Hàm & class top-level

| Tên | Dòng | Dài | Tham số | Docstring |
|---|---:|---:|---|---|
| `_prog` | 45 | 8 | `m, **fields` |  |
| `run_hybrid_fa` | 55 | 123 ⚠️ | `work_dir, device, force, no_fa, no_repair, hub_nano, hub_para` |  |
| `main` | 180 | 19 | `argv` |  |

**Hàm dài ≥120 dòng:** `run_hybrid_fa` (123, L55)

### Config / env keys (2)

`HF_HUB_DISABLE_SYMLINKS`, `HF_HUB_DISABLE_SYMLINKS_WARNING`

**File/artifact nhắc tới:** `asr.aligned_fa.json`, `asr.aligned_fix.json`, `asr.aligned_repaired.json`, `asr.fun_nano.json`, `asr.json`, `asr.paraformer_zh.chars.json`, `asr.paraformer_zh.json`, `audio.wav`, `sub.zh.aligned_fa.srt`, `sub.zh.aligned_fix.srt`, `sub.zh.aligned_repaired.srt`, `sub.zh.srt`

**Tín hiệu rủi ro (đếm tĩnh):** broad_except=2 · file_writes=3

### Lịch sử (từ docs/)

- Fix logs: —
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
