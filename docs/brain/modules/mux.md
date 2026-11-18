# `mux`

[← Index](../generated/module-index.md) · [Brain home](../README.md)

<!-- AUTO:START — sinh bởi scripts/brain_build.py 2026-11-17 19:05. Đừng sửa tay khối này. -->
**File:** `mux.py` · **Lớp:** `render` · **132 dòng** (105 code) · **5 hàm**, **0 class** · sha1 `3e03279212`

> mux.py — STAGE cuối: ghép track lồng tiếng vào video -> output.mp4 (thuyết minh). Kiểu thuyết minh: GIỮ video + GIỮ tiếng gốc nhưng hạ nhỏ, phủ giọng Việt lên trên. Dùng ducking ĐỘNG (sidechaincompress): tiếng gốc chỉ tụ

### Phụ thuộc

- **Gọi tới (import nội bộ):** [assemble](./assemble.md), [manifest](./manifest.md), [media_ts](./media_ts.md), [source_preflight](./source_preflight.md)
- **Được dùng bởi:** —
- **Test:** `tests/test_video_preflight.py`

```mermaid
flowchart LR
  mux[[mux]]
  mux --> assemble[assemble]
  mux --> manifest[manifest]
  mux --> media_ts[media_ts]
  mux --> source_preflight[source_preflight]
```

### Hàm & class top-level

| Tên | Dòng | Dài | Tham số | Docstring |
|---|---:|---:|---|---|
| `_find_video` | 31 | 4 | `work_dir, m` |  |
| `_pick_dub` | 37 | 17 | `work_dir, m` | Chọn track lồng tiếng: audio ngoài > dub_fit.wav > (tự ghép fit). |
| `_has_audio` | 56 | 11 | `path` | Video gốc có luồng audio không (để biết có ducking được không). |
| `run_mux` | 69 | 50 | `work_dir, orig_vol, out_name, force` |  |
| `main` | 121 | 8 | `argv` |  |

**File/artifact nhắc tới:** `dub_fit.wav`, `output.mp4`, `tts.json`

**Tín hiệu rủi ro (đếm tĩnh):** broad_except=2 · subprocess=2

### Lịch sử (từ docs/)

- **Fix logs (6):**
  - [Port V2 → V4: preflight/chuẩn hoá video nguồn + extract_pcm bền + FireRed cắt ở khoảng lặng + câu ASR rác / pa](../../fixes/2026-11-13-port-preflight-slice-junk.md)
  - [2026-11-13 — Brain: job đã xong bị heal «thất bại» + park tự động bị báo nhầm «HOLD / Cần bạn»](../../fixes/2026-11-13-brain-finished-hold.md)
  - [Preflight + chuẩn hoá video nguồn trước khi vào job (+ 2 lỗi review extract_pcm)](../../fixes/2026-11-12-video-preflight.md)
  - [2026-10-06 — Đợt 4 review: tranh chấp ghi, một bản tiến trình, checkpoint an toàn](../../fixes/2026-10-06-batch4-write-races.md)
  - [Nút Dừng không tắt được mux/ffmpeg](../../fixes/2026-09-24-stop-mux-ffmpeg.md)
  - [1-click (run-all) lỗi liên tục / kẹt mux running](../../fixes/2026-09-24-run-all-stale-mux.md)
- **Reviews:** [2026-10-06-code-review](../../reviews/2026-10-06-code-review.md)
- Nhắc trong CHANGELOG: **3** lần · DECISIONS: **0** lần

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
