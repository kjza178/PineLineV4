# `sensevoice_asr`

[← Index](../generated/module-index.md) · [Brain home](../README.md)

<!-- AUTO:START — sinh bởi scripts/brain_build.py 2026-11-11 02:37. Đừng sửa tay khối này. -->
**File:** `sensevoice_asr.py` · **Lớp:** `asr` · **255 dòng** (220 code) · **4 hàm**, **0 class** · sha1 `d730c354e0`

> sensevoice_asr.py — STAGE ASR bằng FunASR SenseVoiceSmall (nhanh, đa ngôn ngữ). Model : iic/SenseVoiceSmall (+ fsmn-vad) Đầu vào : work/<job>/source.* hoặc audio.wav có sẵn

### Phụ thuộc

- **Gọi tới (import nội bộ):** [asr](./asr.md), [asr_spam](./asr_spam.md), [asr_vad_utils](./asr_vad_utils.md), [fun_asr_nano](./fun_asr_nano.md), [manifest](./manifest.md), [subs](./subs.md), [vram](./vram.md)
- **Được dùng bởi:** —
- **Được nhắc tên file `.py` (subprocess/script) bởi:** [restart_server](./restart_server.md), [server](./server.md)
- **Test:** ❌ chưa có test import trực tiếp
- **Thư viện ngoài:** `funasr`

```mermaid
flowchart LR
  sensevoice_asr[[sensevoice_asr]]
  sensevoice_asr --> asr[asr]
  sensevoice_asr --> asr_spam[asr_spam]
  sensevoice_asr --> asr_vad_utils[asr_vad_utils]
  sensevoice_asr --> fun_asr_nano[fun_asr_nano]
  sensevoice_asr --> manifest[manifest]
  sensevoice_asr --> subs[subs]
  sensevoice_asr --> vram[vram]
```

### Hàm & class top-level

| Tên | Dòng | Dài | Tham số | Docstring |
|---|---:|---:|---|---|
| `_clean_sv_text` | 51 | 12 | `text` |  |
| `_post_clean_segs` | 65 | 10 | `segs` |  |
| `run_asr_sensevoice` | 77 | 158 ⚠️ | `work_dir, device, force, language, hub, sidecar` | sidecar: ghi asr.<tag>.json + sub.zh.<tag>.srt, không đụng asr.json / manifest ASR chính. |
| `main` | 237 | 15 | `argv` |  |

**Hàm dài ≥120 dòng:** `run_asr_sensevoice` (158, L77)

### Config / env keys (3)

`ASR_VAD_MAX_SINGLE_SEGMENT_MS`, `HF_HUB_DISABLE_SYMLINKS`, `HF_HUB_DISABLE_SYMLINKS_WARNING`

**File/artifact nhắc tới:** `.progress.json`, `asr.json`, `audio.wav`, `sub.zh.srt`

**Tín hiệu rủi ro (đếm tĩnh):** broad_except=3 · file_writes=7

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
