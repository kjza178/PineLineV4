# `asr`

[← Index](../generated/module-index.md) · [Brain home](../README.md)

<!-- AUTO:START — sinh bởi scripts/brain_build.py 2026-11-11 02:37. Đừng sửa tay khối này. -->
**File:** `asr.py` · **Lớp:** `asr` · **442 dòng** (372 code) · **13 hàm**, **0 class** · sha1 `ee65c049d3`

> asr.py — STAGE 2 (phần đầu): tách audio + nhận diện lời (Whisper). Đầu vào : work/<job>/source.mp4  (từ stage download) Đầu ra  : work/<job>/audio.wav   (16kHz mono — dùng lại cho TTS/Demucs sau)

### Phụ thuộc

- **Gọi tới (import nội bộ):** [fileio](./fileio.md), [manifest](./manifest.md), [media_ts](./media_ts.md), [separate](./separate.md), [subs](./subs.md), [vram](./vram.md)
- **Được dùng bởi:** [firered_asr](./firered_asr.md), [fun_asr_nano](./fun_asr_nano.md), [paraformer_zh](./paraformer_zh.md), [scripts.check_batch4](./scripts.check_batch4.md), [sensevoice_asr](./sensevoice_asr.md), [separate](./separate.md), [server](./server.md)
- **Được nhắc tên file `.py` (subprocess/script) bởi:** [restart_server](./restart_server.md), [scripts.check_batch4](./scripts.check_batch4.md), [server](./server.md), [translate](./translate.md)
- **Test:** `tests/test_asr_demucs.py`
- **Thư viện ngoài:** `ctranslate2`, `faster_whisper`, `soundfile`

```mermaid
flowchart LR
  asr[[asr]]
  firered_asr[firered_asr] --> asr
  fun_asr_nano[fun_asr_nano] --> asr
  paraformer_zh[paraformer_zh] --> asr
  scripts_check_batch4[scripts.check_batch4] --> asr
  sensevoice_asr[sensevoice_asr] --> asr
  separate[separate] --> asr
  server[server] --> asr
  asr --> fileio[fileio]
  asr --> manifest[manifest]
  asr --> media_ts[media_ts]
  asr --> separate[separate]
  asr --> subs[subs]
  asr --> vram[vram]
```

### Hàm & class top-level

| Tên | Dòng | Dài | Tham số | Docstring |
|---|---:|---:|---|---|
| `_audio_marker` | 46 | 2 | `wav` |  |
| `_src_id` | 50 | 4 | `src` |  |
| `extract_audio` | 56 | 20 | `src, out_wav` | Tách audio về 16kHz mono PCM — chuẩn đầu vào Whisper. Ghi .partial rồi replace + marker nguồn. |
| `_wav_seconds` | 78 | 11 | `p` |  |
| `_probe_seconds` | 91 | 7 | `p` |  |
| `audio_wav_stale` | 100 | 28 | `src, wav, keep_legacy` | audio.wav có sẵn không dùng được: rỗng, marker khác nguồn / khác filter mốc, hoặc (chưa có |
| `ensure_audio_wav` | 130 | 12 | `src, wav, force, keep_legacy` | Trích audio.wav khi thiếu / hỏng / khác nguồn (hoặc force). True nếu vừa trích. |
| `resolve_asr_source` | 144 | 51 | `work_dir, video_src, force_demucs, device` | Xác định nguồn audio sạch và chuẩn xác cho ASR. |
| `_cut_wav_from` | 197 | 7 | `src_wav, out_wav, start_sec` | Cắt phần còn lại từ start_sec (resume ASR giữa chừng). |
| `pick_device` | 206 | 11 | `device` | Chọn cuda nếu có GPU, không thì cpu. Trả (device, compute_type). |
| `_salvage_asr` | 219 | 26 | `m, asr_path, rows, wav, total, err` | Crash/treo: giữ asr.json đã có, status pending để bấm Tiếp tục. |
| `run_asr` | 247 | 172 ⚠️ | `work_dir, model_size, lang, device, compute_type, force` |  |
| `main` | 421 | 18 | `argv` |  |

**Hàm dài ≥120 dòng:** `run_asr` (172, L247)

**File/artifact nhắc tới:** `asr.json`, `audio.wav`, `audio_resume.wav`, `sub.zh.srt`, `vocals.wav`

**Tín hiệu rủi ro (đếm tĩnh):** broad_except=8 · file_writes=2 · subprocess=3 · swallow_except=2 · threads=1

### Lịch sử (từ docs/)

- **Fix logs (2):**
  - [Job gốc sau split: part upload xong nhưng parent báo lỗi / chưa hoàn thành](../../fixes/2026-11-03-split-parent-false-failed.md)
  - [2026-10-06 — Đợt 4 review: tranh chấp ghi, một bản tiến trình, checkpoint an toàn](../../fixes/2026-10-06-batch4-write-races.md)
- **Reviews:** [2026-11-02-v4-structure-and-v2-port](../../reviews/2026-11-02-v4-structure-and-v2-port.md), [2026-10-06-code-review](../../reviews/2026-10-06-code-review.md)
- Nhắc trong CHANGELOG: **4** lần · DECISIONS: **0** lần

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
