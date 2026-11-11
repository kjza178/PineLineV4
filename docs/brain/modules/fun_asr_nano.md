# `fun_asr_nano`

[← Index](../generated/module-index.md) · [Brain home](../README.md)

<!-- AUTO:START — sinh bởi scripts/brain_build.py 2026-11-11 02:37. Đừng sửa tay khối này. -->
**File:** `fun_asr_nano.py` · **Lớp:** `asr` · **597 dòng** (521 code) · **11 hàm**, **0 class** · sha1 `6da7e78c85`

> fun_asr_nano.py — STAGE ASR bằng Fun-ASR-Nano (chất lượng tiếng Trung cao nhất). Model : FunAudioLLM/Fun-ASR-Nano-2512 (+ fsmn-vad cắt đoạn dài) Đầu vào : work/<job>/source.mp4

### Phụ thuộc

- **Gọi tới (import nội bộ):** [asr](./asr.md), [asr_hybrid_progress](./asr_hybrid_progress.md), [asr_spam](./asr_spam.md), [asr_vad_utils](./asr_vad_utils.md), [manifest](./manifest.md), [subs](./subs.md), [vram](./vram.md)
- **Được dùng bởi:** [asr_fix_align](./asr_fix_align.md), [asr_repair](./asr_repair.md), [firered_asr](./firered_asr.md), [hybrid_asr](./hybrid_asr.md), [nano_fa_asr](./nano_fa_asr.md), [paraformer_zh](./paraformer_zh.md), [sensevoice_asr](./sensevoice_asr.md)
- **Được nhắc tên file `.py` (subprocess/script) bởi:** [restart_server](./restart_server.md), [server](./server.md)
- **Test:** ❌ chưa có test import trực tiếp
- **Thư viện ngoài:** `funasr`, `soundfile`, `torch`, `transformers`

```mermaid
flowchart LR
  fun_asr_nano[[fun_asr_nano]]
  asr_fix_align[asr_fix_align] --> fun_asr_nano
  asr_repair[asr_repair] --> fun_asr_nano
  firered_asr[firered_asr] --> fun_asr_nano
  hybrid_asr[hybrid_asr] --> fun_asr_nano
  nano_fa_asr[nano_fa_asr] --> fun_asr_nano
  paraformer_zh[paraformer_zh] --> fun_asr_nano
  sensevoice_asr[sensevoice_asr] --> fun_asr_nano
  fun_asr_nano --> asr[asr]
  fun_asr_nano --> asr_hybrid_progress[asr_hybrid_progress]
  fun_asr_nano --> asr_spam[asr_spam]
  fun_asr_nano --> asr_vad_utils[asr_vad_utils]
  fun_asr_nano --> manifest[manifest]
  fun_asr_nano --> subs[subs]
  fun_asr_nano --> vram[vram]
```

### Hàm & class top-level

| Tên | Dòng | Dài | Tham số | Docstring |
|---|---:|---:|---|---|
| `_pick_device` | 44 | 10 | `device` |  |
| `_wav_dur` | 56 | 13 | `wav` |  |
| `_ms_to_s` | 71 | 6 | `v` | FunASR timestamp luôn là milliseconds. |
| `_split_text_by_punct` | 79 | 4 | `text` | Tách câu theo dấu câu (mỏng: gọi subs.split_text_by_punct). |
| `_spread_sentences` | 85 | 19 | `text, start, end` | Không có timestamp ký tự -> chia thời gian theo độ dài chữ. |
| `_parse_funasr_result` | 106 | 70 | `res, audio_dur` | Chuẩn hoá output FunASR -> [{start, end, text}, ...]. |
| `_split_by_punct` | 178 | 36 | `text, char_ts` | Gộp timestamp ký tự thành câu theo dấu câu Trung/Việt. |
| `_vad_ranges_chunked` | 216 | 77 | `vad_model, wav, audio_dur, vad_kw, chunk_s, overlap_s, on_progress` | VAD theo cửa sổ ~chunk_s — tránh treo generate() trên file dài. |
| `_vad_slice_asr` | 295 | 102 | `asr_model, vad_model, wav, language, on_progress, pad_s, overlap_s,…` | VAD cắt đoạn -> ASR từng đoạn có pad/overlap (Fun-ASR-Nano không có CTC ts). |
| `run_asr_nano` | 398 | 180 ⚠️ | `work_dir, device, force, language, hub, sidecar` | sidecar: ghi asr.<tag>.json + sub.zh.<tag>.srt, không đụng asr.json / manifest ASR chính. |
| `main` | 580 | 14 | `argv` |  |

**Hàm dài ≥120 dòng:** `run_asr_nano` (180, L398)

### Config / env keys (3)

`ASR_VAD_CHUNK_S`, `HF_HUB_DISABLE_SYMLINKS`, `HF_HUB_DISABLE_SYMLINKS_WARNING`

**File/artifact nhắc tới:** `.progress.json`, `asr.json`, `audio.wav`, `sub.zh.srt`

**Tín hiệu rủi ro (đếm tĩnh):** broad_except=12 · file_writes=7 · swallow_except=3

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
