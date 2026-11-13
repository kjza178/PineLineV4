# Port V2 → V4: preflight/chuẩn hoá video nguồn + extract_pcm bền + FireRed cắt ở khoảng lặng + câu ASR rác / parent chờ part

- **Date:** 2026-11-13 (agent Q4)
- **Nguồn V2:** `docs/fixes/2026-11-12-video-preflight.md` (agent K + mục C agent K2), `2026-11-13-firered-slice-silence.md` (L), `2026-11-13-simple-junk-park.md` (M) + phần chủ dự án thêm 12/11 trước K (`media_ts.extract_pcm_from_video`, chỗ gọi trong `asr.py`/`separate.py`; `server.py` cur_text parent «đã ghép từ N parts»). Bản sao 3 docs V2 nằm cùng thư mục này.
- **Khu vực V4:** `media_ts.py`, MỚI `source_preflight.py`, `text_junk.py`, `tools/preflight_scan.py`, `tools/asr_boundary_scan.py`; `asr.py`, `separate.py`, `ocr.py`, `hardsub_asr.py`, `render.py`, `mux.py`, `split_parts.py`, `download.py`, `agent_av_sync.py`, `firered_asr.py`, `translate_simple/{cfg,pipeline,stage_review,validate}.py`, `server.py`; tests MỚI `test_video_preflight`, `test_extract_pcm_robust`, `test_extract_pcm_timing`, `test_firered_slice_silence`, `test_simple_junk_park`; chỉnh `test_translate_simple.py`, `test_translate_simple_scenarios.py` (mỗi file 1 ca `SIMPLE_UNREVIEWED_TOLERANCE=0`). V6: `scripts/test_v4_simple_demucs.bat` (nhóm 1c).
- **Status:** trên đĩa V4. **Cần restart :8804** (server import/`_find_video`/download/split_wait + dịch simple in-process). ASR/Demucs/FireRed chạy tiến trình con → hiệu lực ngay lần chạy kế.
- **Backup:** `Z:\PinelineV4\.backup_edit_20261113_agentQ4\` (18 file gốc cùng đường dẫn tương đối, `_md5_before.txt`, `_md5_after.txt`, `_NEW_FILES.txt`, `_new\` = bản ghi vào, `V6_scripts_test_v4_simple_demucs.bat`, `_xfer\` = ảnh mã nguồn test, không secret).

## Cách port (merge 3 chiều, base = backup V2)

So md5 (bỏ CRLF) V4 hiện tại với bản gốc V2 trong backup:
- **V4 = base V2 → chép nguyên V2 hiện tại:** `ocr.py`, `hardsub_asr.py`, `render.py`, `mux.py`, `split_parts.py`, `download.py`, `agent_av_sync.py` (= V2 trước K); `firered_asr.py` (= V2 trước L; sau L+M); `translate_simple/{pipeline,stage_review,validate}.py`, `tests/test_translate_simple_scenarios.py` (= V2 trước M).
- **`media_ts.py`, `asr.py`, `separate.py`:** V4 = V2 trước phần chủ dự án (diff V4↔backup K chỉ đúng khối `extract_pcm_from_video` + 2 chỗ gọi) → chép V2 hiện tại (chủ dự án + K + K2). Giữ CRLF của `media_ts.py`.
- **`server.py`** (V4 khác V2: không B3 `fill_pending`, `LIBRARY_DIR`, comment F4/P4): áp diff `backup K → V2 hiện tại` bằng `patch -F0` (7 hunk sạch, lệch dòng −8/−132): `_split_wait_clear` ở `_run_merge` + đầu vòng part, `_split_wait_parts` trước «TẤT CẢ PART ĐÃ XONG», MỚI `_SPLIT_WAIT/_split_wait_clear/_split_wait_parts/_split_wait_ready`, `_finalize_imported_source` gắn `preflight_pending`, `_find_video` → `source_preflight.resolve_source_video` (chỉ đọc), `_queue_park_ready` nhánh `held_at=split_parts`. Thêm tay khối chủ dự án (heal parent: stage không phải mux mà cur_text «đang chạy/đang tự động dò/chia part» → «đã ghép từ N parts»). Giữ CRLF.
- **`translate_simple/cfg.py`**, **`tests/test_translate_simple.py`:** áp diff M (`unreviewed_tolerance`, `missing_batch`, docstring; 1 dòng env test) — giữ `pipeline_mode()` + test rollback riêng V4.
- **Mới (chép V2):** `source_preflight.py`, `text_junk.py`, `tools/preflight_scan.py`, `tools/asr_boundary_scan.py` (mặc định `work_root` đổi `D:/PinelineV2_work` → `work` như tools V4 khác), 5 test.
- Không có gì cần vào `machine.py`: cờ đọc env > `pineline.config.json` qua `config.py` (V4 = V2), cổng không dùng.

## Hành vi (tóm tắt — chi tiết ở docs V2)

- **Preflight:** tải xong (`download.py`) → kiểm + chuẩn hoá ngay; import file/D:\Lib → chỉ gắn `download.preflight_pending=true`, stage xử lý đầu tiên (asr/separate/ocr/hardsub/render/mux/split) chạy 1 lần (khoá `.preflight.lock`). Audio hỏng → `work/<job>/source_norm.*` (hình copy, tiếng dựng lại bám trục hình); fatal (không hình/tiếng/độ dài 0…) → stage fail `[preflight] nguồn video không dùng được: …`. Mọi `_find_video` + `asr.resolve_asr_source` đi qua `resolve_source_video` (`video_path_norm` > `video_path` > `source.*`). Job cũ không chạy lại tự động; quét chỉ đọc `python tools/preflight_scan.py --quick`.
- **extract_pcm_from_video:** nhận full chỉ khi thiếu ≤ `EXTRACT_FULL_TOL_SEC` (1 s) và không dài thừa; lỗi giải mã + đoạn 0 tuyệt đối ≥ 2 s (ffmpeg 8.x đệm im lặng) → head + chunk 30 s (khúc hỏng chia 5 s), mỗi khúc ép đúng số mẫu. File lành: 1 lệnh ffmpeg, PCM byte-giống.
- **FireRed:** slice `FIRERED_SLICE_SEC`=1200 cắt tại khoảng lặng gần mốc (±`FIRERED_CUT_SEARCH_SEC` 60) + đệm `FIRERED_SLICE_PAD_SEC` 2 s (không lặng: `FIRERED_SLICE_PAD_NOSIL_SEC` 10 s), giữ câu có tâm trong lõi; `0` = không chia. Lọc câu rác («None.», không chữ) ở `_parse_firered_result`. Quét asr.json cũ: `python tools/asr_boundary_scan.py work`.
- **Dịch simple:** câu zh rác → `vi="…"`, `rv=1`, `junk=1` (TTS slot im lặng); còn câu chưa soát → 1 lượt review bổ sung lô `SIMPLE_MISSING_BATCH` (4); còn ≤ `SIMPLE_UNREVIEWED_TOLERANCE` (trống = max(3, 0.2 % số câu); `0` = tắt) và có nháp → nhận nháp (`unreviewed_accepted`).
- **Parent/part:** part park/HOLD → parent `agent.held_at=split_parts` + `split_wait_parts`, không ghép hụt; `_queue_run_one` trả `held` (giữ ghế); `_queue_park_ready(parent)` True khi part tới hạn/hết HOLD/đã xong.

## Cờ (env > `pineline.config.json` > mặc định)

`VIDEO_PREFLIGHT=1`, `VIDEO_NORMALIZE=1`, `VIDEO_NORMALIZE_DRIFT=0`, `EXTRACT_FULL_TOL_SEC=1.0`, `FIRERED_SLICE_SEC=1200`, `FIRERED_CUT_SEARCH_SEC=60`, `FIRERED_SLICE_PAD_SEC=2`, `FIRERED_SLICE_PAD_NOSIL_SEC=10`, `FIRERED_SILENCE_DB=-40`, `FIRERED_MIN_SILENCE_SEC=0.3`, `SIMPLE_UNREVIEWED_TOLERANCE` (trống), `SIMPLE_MISSING_BATCH=4`. Không thêm khoá vào `config.json`/`pineline.config.json`.
Rollback nhanh: `VIDEO_PREFLIGHT=0`; `SIMPLE_UNREVIEWED_TOLERANCE=0`; `FIRERED_SLICE_SEC` giữ 1200 (cắt khoảng lặng không có cờ tắt riêng — rollback = chép `firered_asr.py` từ backup).

## Test (bản sao Linux cloud, ffmpeg 6.1.1, stub fastapi/yt_dlp/soundfile, `AGENT_BRAIN=0`)

- Toàn bộ `tests/`: trước **289 passed / 10 failed / 5 skipped / 6 error** → sau **377 passed / 10 failed / 5 skipped / 6 error**, cùng tập fail/error (môi trường: `fastapi.testclient`, `google.oauth2`, file .bat/`D:\…` không có trong bản sao, pronoun ×3 có sẵn, sfx/restart_guard).
- Nhóm mới (1c): **88 passed** (13 + 2 + 21 + 9 + 43). Nhóm (1) 108 passed + 4 skipped, nhóm (2) 37 passed + 3 failed có sẵn — trước/sau như nhau.
- Không chạy được ở bản sao: `tests/test_server_split.py` (cần `fastapi.testclient`) → chạy trên Windows bằng `... full`.

## Recheck (Windows, sau restart :8804)

1. `Z:\PinelineV6\scripts\test_v4_simple_demucs.bat` → nhóm (1c) 88 passed (ffmpeg 8.1.2 trong PATH); `... full` không thêm fail.
2. Import 1 video lành → manifest `download.preflight_pending=true`; chạy ASR → log `[preflight] nguồn lành`, không có `source_norm.*`.
3. Bản sao file AAC hỏng → log `[preflight] … đã chuẩn hoá → source_norm.*`; `audio.wav` dài đúng bằng hình.
4. Job FireRed dài > 20' → log `[firered] N slice, cắt tại khoảng lặng: …`.
5. Job split có part park → parent `agent.held_at=split_parts`, không «failed», tự chạy lại part khi tới `review_retry_at`.
- **Fail nếu:** stage báo `[preflight]` với video lành; preview/GET tạo `source_norm`; parent ghép Full khi part chưa xong.

## Rủi ro / khác V2

- `server._find_video` giờ phụ thuộc `source_preflight` (import trong hàm) — thiếu file → lỗi mọi preview; file đã có trong cây V4.
- Job V4 đang dở với asr.json cắt cứng 1200 s không tự sửa — chạy lại ASR (force) nếu cần.
- `tests/test_extract_pcm_timing.py` dùng ffmpeg thật (V2 đo 4.4/6.1/8.1.2).
