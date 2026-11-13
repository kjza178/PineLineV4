# Preflight + chuẩn hoá video nguồn trước khi vào job (+ 2 lỗi review extract_pcm)

- **Date:** 2026-11-12/13 (agent K)
- **Khu vực:** `media_ts.extract_pcm_from_video`, MỚI `source_preflight.py`, `download.py`, `server.py` (import + `_find_video`), `asr.py`, `separate.py`, `ocr.py`, `hardsub_asr.py`, `render.py`, `mux.py`, `split_parts.py`, `agent_av_sync.py`, MỚI `tools/preflight_scan.py`
- **Status:** fixed (chờ restart :8801 cho phần import/download/render; ASR tiến trình con có hiệu lực ngay)

## A. Hai lỗi review `extract_pcm_from_video`

1. **CAO — nhận full khi got ≥ 0.85×video:** có thể mất tới 15 % cuối phim mà không báo.
   Sửa: nhận `full`/`full_soft` chỉ khi thiếu ≤ `EXTRACT_FULL_TOL_SEC` (mặc định 1.0 s, env/config).
   Thiếu hơn (kể cả rc=0) → giữ head + chunk phần còn (nhánh có sẵn).
   **Thêm (phát hiện khi đo file thật):** bản full còn có thể **DÀI hơn hình** — `merged.mp4.bak_aac_corrupt`
   với ffmpeg 4.4: rc=0, ra 7810.9 s trong khi hình/luồng tiếng khai 7741.4 s (AAC rác sinh thêm 69 s mẫu →
   ASR/sub trôi tới 69 s). Nay: dài hơn `max(hình, luồng tiếng khai báo) + tol` → bỏ bản full, chunk lại từ 0
   (`info.overlong_full_sec`). File lành dài hơn hình chút ít / luồng tiếng tự khai dài hơn → giữ như cũ.
2. **TRUNG BÌNH — khúc ≥85 % cửa sổ nhận nguyên:** các khúc sau bị dồn sớm. Sửa: `_force_wav_frames` ép
   MỖI khúc (và head) đúng số mẫu cửa sổ `round(t_end·ar) − round(t_start·ar)` (thiếu → đệm im lặng ở đuôi,
   thừa → cắt); khúc chết = `_write_silence_frames` đúng số mẫu. `info.n_fixed_len` = số khúc phải chỉnh.
   Đo: giả lập mỗi khúc thiếu 2–12 % → code cũ bíp ở 53 s ra 50.30 s (trôi −2.7 s); code mới ±0 ms.
   File thật hỏng: 41/259 khúc phải chỉnh độ dài.

File lành: vẫn đúng 1 lệnh ffmpeg, PCM byte-giống lệnh cũ (test). `-fflags +discardcorrupt` trên file lành:
không đổi mẫu nào (test md5 PCM so với lệnh không có cờ).

## B. Preflight / chuẩn hoá nguồn

**Ở đâu chạy**
- `download.py` `download_video`: ngay sau `mark_done` → `source_preflight.after_download` (đang ở hàng tải).
  Fatal → stage **download failed** với lý do rõ.
- `server._finalize_imported_source` (import file/đường dẫn D:\Lib, upload, inplace): chỉ gắn
  `download.preflight_pending=true` — KHÔNG chạy trong request HTTP. Stage xử lý đầu tiên (asr/separate/ocr/
  hardsub/render/mux/split) gọi `stage_source_video()` → `ensure_preflight` chạy 1 lần (khoá `.preflight.lock`).
  Fatal → stage đó fail với `[preflight] nguồn video không dùng được: …` (không còn «ASR mã 1»).
- `split_parts.split_job_to_subjobs`: kiểm job cha trước (qua `render._find_video`), cắt part từ nguồn đã
  chuẩn hoá; sub-job kế thừa (`preflight.action=inherited`) hoặc `preflight_pending` nếu cha chuẩn hoá lỗi/tắt.

**Kiểm gì** (`check_source`, chỉ đọc): ffprobe (có hình + tiếng, codec, kênh, sample rate, độ dài hình vs tiếng,
nghi VFR r/avg_frame_rate), giải mã thử TOÀN BỘ audio `-af AUDIO_TS_FIX -ac 1 -ar 16000 -f null` (bắt lỗi AAC /
rematrix / mốc; phân loại dòng lỗi), drift `media_ts.audio_ts_drift`, giải mã 3 khung đầu + 3 khung giữa.

**Kết quả → manifest `stages.download`:**
- lành → `preflight={ok:true, action:"none", …}`;
- lỗi audio → `normalize_source`: `-c:v copy` hình + audio dựng lại bằng `extract_pcm_from_video` (bám trục hình,
  đúng độ dài, chỗ chết = im lặng) → AAC 192k cùng kênh/sr → `work/<job>/source_norm.<mp4|mkv>` (file gốc / D:\Lib
  không đụng); kiểm lại (có hình+tiếng, lệch độ dài ≤1 s, giải mã audio rc=0). Ghi `video_path_norm`, `norm_reason`,
  `norm_silence_sec`, `preflight.action="normalized"`; chuẩn hoá lỗi → `normalize_failed` (dùng nguồn gốc, extract
  vẫn tự cứu); tiếng ≥90 % phải thay im lặng → fatal;
- fatal: không đọc được file / không có hình / không có tiếng / độ dài 0 / hình không giải mã được.

**Một hàm resolve nguồn:** `source_preflight.resolve_source_video` (chỉ đọc: `video_path_norm` còn file →
`video_path` → `source.*`). `stage_source_video` = ensure + resolve. Đổi sang:
`asr.resolve_asr_source` (mọi engine ASR), `separate._find_video` (Demucs → `no_vocals`/`vocals` từ nguồn chuẩn hoá),
`ocr._find_video`, `hardsub_asr._find_video`, `render._find_video` (render + detect_overlays/hardsub_track; mux tiếng
gốc/nền lấy từ nguồn chuẩn hoá), `mux._find_video`, `split_parts` (qua render), `server._find_video` (chỉ resolve —
preview/kiểm tồn tại, không side effect), `agent_av_sync` (chẩn đoán). `ensure_job_audio_ts` nhận nguồn chuẩn hoá →
drift 0 → không dời mốc.

**Cờ** (env > `pineline.config.json` > mặc định): `VIDEO_PREFLIGHT=1`, `VIDEO_NORMALIZE=1` (chỉ chạy khi có lỗi),
`VIDEO_NORMALIZE_DRIFT=0` (drift dồn mẫu một mình chỉ là cảnh báo — AUDIO_TS_FIX + ensure_job_audio_ts đã xử lý),
`EXTRACT_FULL_TOL_SEC=1.0`.

**Job cũ:** không có `preflight_pending` → không chạy lại tự động. Quét chỉ-đọc:
`python tools/preflight_scan.py [--quick] [--jobs a,b] [--json out.json]`; chạy cho 1 job:
`python source_preflight.py work/<job> --run` (không `--run` = chỉ in kết quả kiểm).

## Đo thời gian (VM Linux 2 nhân, ffmpeg 4.4, đọc D:\Lib qua mount)

| Video | Kết quả | Thời gian |
|---|---|---|
| `曝光神话…第三季\merged.mp4` (2 h 09', hevc 1080p, AAC stereo, 535 MB) | lành | **9.2 s** (giải mã audio 8.8 s); `--quick` 0.37 s |
| `…\merged.mp4.bak_aac_corrupt` (cùng phim, AAC hỏng) | `AAC hỏng (122 555 dòng)` | kiểm **11.9 s** |
| — chuẩn hoá file hỏng trên | full ra 7810.9 s → chunk lại 259 khúc, 41 khúc chỉnh độ dài, 0 s im lặng | **127 s** tổng (trích 51 s, AAC+remux ~55 s, kiểm lại ~10 s); ra 7741.47 s, giải mã rc=0, 0 lỗi |

Đối chiếu tương quan chéo tiếng chuẩn hoá vs giải mã trực tiếp từng cửa sổ của file gốc ở vùng lành (300/1500/3000 s):
lệch ±23 ms (= 1 khung AAC). (So với `merged.mp4` đã remux từ tập lẻ: 55–135 ms — bản đó dùng nguồn audio khác.)
Ghi chú: trên Windows ffmpeg mới, file này chết rematrix -22 ở ~2051 s (nhánh salvage+chunk), Linux 4.4 thì rc=0
nhưng dài thừa — cả hai nay đều ra đúng độ dài.

## C. Bổ sung 2026-11-13 (agent K2) — «đủ dài» không chứng minh nội dung đúng

**Phiên bản ffmpeg:** production = `ffmpeg version 8.1.2-full_build-www.gyan.dev` (Windows); VM test = ffmpeg 4.4.2 (Linux), cloud test = 6.1.1.
Hành vi khác nhau khi AAC chết giữa file: 8.1.2 → rc=0, độ dài ĐỦ nhưng sau điểm hỏng toàn mẫu 0 (ffmpeg đệm im lặng
tới hết) — user chạy `test_corrupt_aac_full_length_and_timing` trên 8.1.2: bíp chỉ còn 3/13/23 s, mất hết sau ~25 s;
4.4 → rc=0 nhưng DÀI thừa (7810.9 s vs 7741.4 s); Windows cũ hơn → rc=-22 rematrix. Không cờ nào khác nhau giữa các
bản được dùng (`-fflags +discardcorrupt`, `aresample=async=1:min_hard_comp=0.01:first_pts=0` hợp lệ ở cả 4.4 và 8.x).

**Sửa `media_ts.extract_pcm_from_video`:**
- Lượt full giữ stderr (`-loglevel error` sẵn có) → `_decode_errors`: đếm dòng lỗi GIẢI MÃ theo từ khoá chịu được cả
  thông điệp 4.4 lẫn 8.x (`aac`, «Invalid data», «Error while decoding», «Error submitting packet to decoder»,
  «channel element», rematrix/reinitializ, «Number of bands», SBR, «invalid bitstream»…), bỏ cảnh báo dts/pts của muxer.
- Có lỗi giải mã hoặc rc≠0 → `_dead_zero_run(part, 2 s)`: đoạn mẫu 0 tuyệt đối ≥ 2 s SAU khi đã có tiếng = điểm decoder
  chết → giữ head tới đó (cắt đúng mẫu) + chunk phần còn (`info.dead_at`, `decode_errors`). Không có lỗi/stderr →
  chỉ tin đuôi 0 tuyệt đối ≥ 5 s kéo tới HẾT file (phòng ffmpeg không in lỗi). Lỗi lẻ tẻ mà không có đoạn 0 dài →
  giữ full như cũ (full_soft ghi `decode_errors`). Không có mốc thời gian lỗi trong log `-loglevel error` → dùng đoạn 0.
- Khúc chunk 30 s: có lỗi + ĐUÔI 0 ≥ 1 s tới hết khúc → coi khúc hỏng, chia khúc con 5 s (decoder mới ở mốc sau
  thường hồi phục). Khúc con: nhận cả đuôi 0. Im lặng tự nhiên giữa khúc KHÔNG bị loại — đo thật: luật «mọi đoạn 0
  ≥ 1 s» làm mất 1375 s tiếng, luật «đuôi khúc» còn 30 s, thêm «khúc con nhận đuôi 0» còn 0 s.
- File lành: vẫn 1 lệnh ffmpeg, PCM giống từng byte (test cũ giữ nguyên); chỉ đọc lại wav khi không có lỗi để dò đuôi 0.

**Đo lại `merged.mp4.bak_aac_corrupt` (VM, 4.4, 16 k mono):** 122 553 dòng lỗi, đoạn chết từ 69.4 s → head + 287 khúc,
7741.451 s, im lặng 0 s, 58 s. `merged.mp4` lành: full, 7.8 s.

**Test thêm** (`tests/test_extract_pcm_timing.py`, mô phỏng độc lập phiên bản: chạy full thật rồi xoá tiếng từ mốc chết +
gắn stderr kiểu 8.1.2 / 4.4 / rỗng): đuôi 0 sau lỗi (3 biến thể), đoạn 0 giữa phim có lỗi, lỗi mà không đoạn 0 → full,
bộ phân loại lỗi 4.4/8.x, bộ dò đoạn 0, khúc có đuôi 0 bị loại / im lặng giữa khúc được giữ. 6 ca fail trên bản trước.
Toàn bộ `tests/` (cloud): 571 pass, cùng 31 fail môi trường. Backup `.backup_edit_20261113_agentK2\`.

## Test

- MỚI `tests/test_extract_pcm_timing.py` (12): ngưỡng full ±tol (rc 0/≠0, cấu hình), dài thừa → chunk lại,
  `_force_wav_frames`, mốc bíp từng khúc (ffmpeg thật, khúc thiếu ngẫu nhiên), salvage head + chunk, AAC hỏng giả lập
  (ghi rác vào mdat), file lành byte-giống + discardcorrupt trung tính.
- MỚI `tests/test_video_preflight.py` (13): resolve thứ tự, mọi `_find_video` + `asr.resolve_asr_source` trả nguồn
  chuẩn hoá, job cũ không chạy lại, pending chạy 1 lần + fatal raise, cờ tắt, kế thừa split, check lành/hỏng/không
  tiếng/không hình, chuẩn hoá (gốc không đổi md5, bíp đúng mốc, drift 0, số gói hình y nguyên), NORMALIZE=0, scan
  chỉ đọc, import gắn pending + `server._find_video` chỉ đọc.
- Toàn bộ `tests/` (cloud, stub fastapi/google): 537 → 562 pass, cùng 31 fail môi trường (danh sách trùng); gồm
  `test_firered_slice_silence.py`, `test_separate_demucs_chunks.py`, `test_asr_demucs.py`, `test_extract_pcm_robust.py`.

## Recheck

1. Restart :8801. Import 1 video lành → manifest `download.preflight_pending=true`; chạy ASR → log `[preflight] nguồn
   lành (…s)`, `download.preflight.ok=true`, không có `source_norm.*`.
2. Import `merged.mp4.bak_aac_corrupt` (bản sao) → ASR: log `[preflight] … AAC hỏng` → `đã chuẩn hoá → source_norm.mkv`;
   `audio.wav` ≈ 7741.45 s; render ra tiếng khớp hình.
3. Video không có tiếng → stage fail `[preflight] nguồn video không dùng được: nguồn KHÔNG có luồng tiếng …`.
4. `python tools/preflight_scan.py --quick` → bảng job, không file nào trong work đổi.

## Port

Chưa port. Cần mang sang V4/V5/V6: `media_ts.py` (2 fix + overlong), `source_preflight.py`, `tools/preflight_scan.py`,
chỗ gọi trong `download.py`, `server.py` (`_finalize_imported_source`, `_find_video`), `asr.py`, `separate.py`, `ocr.py`,
`hardsub_asr.py`, `render.py`, `mux.py`, `split_parts.py`, `agent_av_sync.py`, 2 file test. V6: ghi manifest qua
`state/job_state.py`, `video_path_norm` vào `core.instance`/pipeline gate, render worker dùng resolver.

Backup: `Z:\PinelineV2\.backup_edit_20261112_agentK\` (+ `_md5_before.txt`, `_md5_after.txt`).
