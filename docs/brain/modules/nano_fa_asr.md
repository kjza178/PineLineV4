# `nano_fa_asr`

[← Index](../generated/module-index.md) · [Brain home](../README.md)

<!-- AUTO:START — sinh bởi scripts/brain_build.py 2026-11-11 02:37. Đừng sửa tay khối này. -->
**File:** `nano_fa_asr.py` · **Lớp:** `asr` · **337 dòng** (271 code) · **5 hàm**, **0 class** · sha1 `527d5c9718`

> nano_fa_asr.py — SOTA ASR: Fun-ASR-Nano (Chữ chuẩn nhất) + Direct Qwen3-ForcedAligner (Mốc chuẩn từng chữ). Kiến trúc sạch, chuẩn công nghiệp: 1) Fun-ASR-Nano nhận diện văn bản (hiểu ngữ cảnh, ít sai chữ, chống lặp qua V

### Phụ thuộc

- **Gọi tới (import nội bộ):** [asr_spam](./asr_spam.md), [fun_asr_nano](./fun_asr_nano.md), [manifest](./manifest.md), [subs](./subs.md), [vram](./vram.md)
- **Được dùng bởi:** —
- **Được nhắc tên file `.py` (subprocess/script) bởi:** [restart_server](./restart_server.md), [server](./server.md)
- **Test:** ❌ chưa có test import trực tiếp
- **Thư viện ngoài:** `numpy`, `qwen_asr`, `soundfile`, `torch`

```mermaid
flowchart LR
  nano_fa_asr[[nano_fa_asr]]
  nano_fa_asr --> asr_spam[asr_spam]
  nano_fa_asr --> fun_asr_nano[fun_asr_nano]
  nano_fa_asr --> manifest[manifest]
  nano_fa_asr --> subs[subs]
  nano_fa_asr --> vram[vram]
```

### Hàm & class top-level

| Tên | Dòng | Dài | Tham số | Docstring |
|---|---:|---:|---|---|
| `_merge_all_to_windows` | 39 | 34 | `rows, gap_s, max_win_s` | Gom các câu thoại gần nhau thành cửa sổ nhỏ (<=24s) để Forced Aligner xử lý tối ưu. |
| `align_nano_with_fa` | 75 | 121 ⚠️ | `rows, wav, device, pad_s, on_progress` | Căn mốc trực tiếp từng câu của Nano bằng Qwen3ForcedAligner. |
| `run_nano_fa` | 198 | 114 | `work_dir, device, force, hub_nano, sidecar` |  |
| `_torch_has_cuda` | 314 | 6 | `` |  |
| `main` | 322 | 11 | `argv` |  |

**Hàm dài ≥120 dòng:** `align_nano_with_fa` (121, L75)

### Config / env keys (4)

`ASR_FA_PAD_S`, `HF_HUB_DISABLE_SYMLINKS`, `HF_HUB_DISABLE_SYMLINKS_WARNING`, `QWEN3_FORCED_ALIGNER`

**File/artifact nhắc tới:** `asr.fun_nano.json`, `asr.json`, `asr.nano_fa.json`, `audio.wav`, `sub.zh.nano_fa.srt`, `sub.zh.srt`

**Tín hiệu rủi ro (đếm tĩnh):** broad_except=5 · file_writes=2

### Lịch sử (từ docs/)

- Fix logs: —
- **Reviews:** [2026-11-02-v4-structure-and-v2-port](../../reviews/2026-11-02-v4-structure-and-v2-port.md)
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
