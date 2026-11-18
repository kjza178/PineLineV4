# `separate`

[← Index](../generated/module-index.md) · [Brain home](../README.md)

<!-- AUTO:START — sinh bởi scripts/brain_build.py 2026-11-17 19:05. Đừng sửa tay khối này. -->
**File:** `separate.py` · **Lớp:** `asr` · **570 dòng** (491 code) · **18 hàm**, **1 class** · sha1 `189ad6ef20`

> separate.py — Tách giọng/nền bằng Demucs (htdemucs --two-stems=vocals). Đầu vào : work/<job>/source.* (video) Đầu ra  : work/<job>/vocals.wav     (giọng Trung sạch — nguồn cho ASR, mặc định từ 2026-11-12)

### Phụ thuộc

- **Gọi tới (import nội bộ):** [manifest](./manifest.md), [media_ts](./media_ts.md), [source_preflight](./source_preflight.md), [split_parts](./split_parts.md), [vram](./vram.md)
- **Được dùng bởi:** [asr](./asr.md), [firered_asr](./firered_asr.md), [server](./server.md)
- **Được nhắc tên file `.py` (subprocess/script) bởi:** [asr](./asr.md), [restart_server](./restart_server.md), [server](./server.md)
- **Test:** `tests/test_firered_slice_silence.py`, `tests/test_separate_demucs_chunks.py`, `tests/test_simple_junk_park.py`, `tests/test_video_preflight.py`

```mermaid
flowchart LR
  separate[[separate]]
  asr[asr] --> separate
  firered_asr[firered_asr] --> separate
  server[server] --> separate
  separate --> manifest[manifest]
  separate --> media_ts[media_ts]
  separate --> source_preflight[source_preflight]
  separate --> split_parts[split_parts]
  separate --> vram[vram]
```

### Hàm & class top-level

| Tên | Dòng | Dài | Tham số | Docstring |
|---|---:|---:|---|---|
| **class `WavInfo`** | 78 | 2 method | |  |
| `_env_float` | 53 | 5 | `name, default` |  |
| `_cfg` | 61 | 7 | `` |  |
| `wav_info` | 95 | 39 | `path` | Đọc header WAV/RF64 (PCM/float/extensible). Không giải mã — chỉ vị trí data + số mẫu. |
| `_write_header` | 136 | 14 | `f, fmt_raw, data_bytes` | Header RIFF chuẩn; data ≥ ~4GB -> RF64 (ffmpeg/soundfile đọc được). |
| `_copy_frames` | 152 | 18 | `src, fsrc, start, count, fdst` | Chép `count` frame từ vị trí `start` của src; thiếu (vượt cuối file) -> đệm 0. |
| `write_wav_slice` | 172 | 13 | `src_path, out_path, start, count` | Ghi out = frames [start, start+count) của src (đệm 0 nếu src ngắn). Atomic (.partial). |
| `concat_wavs` | 187 | 24 | `parts, out_path, expect_frames` | Ghép WAV cùng định dạng theo mẫu (không re-encode). Kiểm tổng frame nếu có expect_frames. |
| `_frames_or_none` | 213 | 5 | `p` |  |
| `_find_video` | 222 | 4 | `work_dir` |  |
| `_probe_duration` | 228 | 11 | `path` | Lấy thời lượng file media (giây) qua ffprobe. |
| `_update_sep_progress` | 241 | 21 | `m, pct, cur_text` | Tiến độ stage 'separate' + đồng bộ sang 'asr' nếu ASR đang chờ tách giọng. |
| `_extract_orig_wav` | 264 | 8 | `video, out_wav` | Audio GỐC 44.1k stereo PCM s16 (RF64 khi >4GB) — chính xác theo mẫu để cắt/ghép. |
| `plan_chunks` | 274 | 32 | `n_frames, rate, cfg, cut_finder` | [(start, end)] theo mẫu, phủ kín [0, n_frames). Audio ≤ ngưỡng -> 1 khúc. |
| `_run_demucs_on_file` | 308 | 68 | `src_audio, tmp_out, device, work_dir, m, chunk_idx, n_chunks` | Chạy Demucs trên 1 file audio (ngắn hoặc 1 khúc) và trả về (no_vocals_wav, vocals_wav). |
| `outputs_valid` | 378 | 27 | `work_dir, video, st` | vocals.wav + no_vocals.wav đủ dùng lại? (kích thước + độ dài khớp gốc/video). |
| `_mark_done` | 407 | 8 | `m, work_dir, device, **extra` |  |
| `run_separate` | 417 | 141 ⚠️ | `work_dir, device, force` |  |
| `main` | 560 | 7 | `argv` |  |

**Hàm dài ≥120 dòng:** `run_separate` (141, L417)

### Config / env keys (4)

`DEMUCS_CHUNK_PAD_SEC`, `DEMUCS_CHUNK_SEC`, `DEMUCS_CUT_SEARCH_SEC`, `DEMUCS_LONG_THRESHOLD_SEC`

**File/artifact nhắc tới:** `no_vocals.wav`, `orig.wav`, `orig_audio.wav`, `plan.json`, `vocals.wav`

**Tín hiệu rủi ro (đếm tĩnh):** broad_except=7 · file_writes=1 · subprocess=2 · swallow_except=2

### Lịch sử (từ docs/)

- **Fix logs (5):**
  - [Port V2 → V4: preflight/chuẩn hoá video nguồn + extract_pcm bền + FireRed cắt ở khoảng lặng + câu ASR rác / pa](../../fixes/2026-11-13-port-preflight-slice-junk.md)
  - [firered-slice-silence: FireRed ASR chia slice tại khoảng lặng + đệm chồng lấn (hết cắt đôi/lặp/mất chữ ở biên ](../../fixes/2026-11-13-firered-slice-silence.md)
  - [Preflight + chuẩn hoá video nguồn trước khi vào job (+ 2 lỗi review extract_pcm)](../../fixes/2026-11-12-video-preflight.md)
  - [Port V2 → V4: luồng dịch `translate_simple` (MẶC ĐỊNH) + Demucs trước ASR](../../fixes/2026-11-12-port-simple-demucs.md)
  - [asr-demucs-default: ASR mặc định chạy trên giọng tách Demucs + separate.py chia khúc tại khoảng lặng, cắt/ghép](../../fixes/2026-11-12-asr-demucs-default.md)
- **Reviews:** [2026-11-02-v4-structure-and-v2-port](../../reviews/2026-11-02-v4-structure-and-v2-port.md), [2026-10-06-code-review](../../reviews/2026-10-06-code-review.md)
- Nhắc trong CHANGELOG: **5** lần · DECISIONS: **0** lần

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
