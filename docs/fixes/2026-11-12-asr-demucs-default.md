> **Bản sao từ V2** (`Z:\PinelineV2\docs\fixes\2026-11-12-asr-demucs-default.md`) — tham chiếu cho port V4 2026-11-12 (agent F4, xem `docs/fixes/2026-11-12-port-simple-demucs.md`). Cổng/đường dẫn trong bài là của V2 (:8801); V4 = :8804. Khác biệt V4: mặc định `TRANSLATE_PIPELINE`=simple, rollback `legacy`.

# asr-demucs-default: ASR mặc định chạy trên giọng tách Demucs + separate.py chia khúc tại khoảng lặng, cắt/ghép theo mẫu

- **Date:** 2026-11-12
- **Nguồn:** quyết định chủ dự án (A: mọi job/part `_pNN` chạy Demucs trước ASR, MỘT lần/job, dùng lại cả cho render; B: bỏ cắt cứng 60' `ffmpeg -f segment` FLAC).
- **Khu vực:** `separate.py` (viết lại phần chia khúc), `asr.py` (`resolve_asr_source`, mới `asr_use_demucs`, `_asr_ui_phase`), test mới `tests/test_separate_demucs_chunks.py` (19 ca). V6: `scripts/asr_demucs_compare.py` + `.bat` (mới), `scratch/voice_exp/embed_campplus.py` (`--vocals`).
- **Status:** trên đĩa V2. **Có hiệu lực NGAY cho mọi lần ASR mới** (engine ASR chạy tiến trình con, nạp `asr.py`/`separate.py` mới mỗi lần) và cho bước `separate`/1-click render (server `importlib.reload(separate)`). Riêng nhánh render tự tách nền trong `_do_render` dùng `run_separate` import lúc khởi động — bản cũ tới khi restart :8801 (tương thích: thấy file + stage done thì bỏ qua).
- **Backup:** `Z:\PinelineV2\.backup_edit_20261112_agentE\` (`separate.py`, `asr.py`, `tests/test_asr_demucs.py`, `docs/CHANGELOG.md`, `docs/STATE.md`, `docs/worklog/2026-11-12.md`, `docs/fixes/README.md`); V6: `Z:\PinelineV6\.backup_edit_20261112_agentE\scratch\voice_exp\embed_campplus.py`.

## Triệu chứng / lý do

ASR chạy trên audio gốc (nhạc nền + SFX lẫn thoại). Trước đây `resolve_asr_source` cố ý KHÔNG dùng Demucs (`ASR_USE_DEMUCS` mặc định 0) với lý do «nuốt chữ, mất âm, méo tiếng hoặc lệch timing ở các ranh giới chunk trên video dài». Lý do đó đến từ cách chia khúc cũ của `separate.py`: phim > 70' bị `ffmpeg -f segment -segment_time 3600` cắt FLAC **cứng mỗi 60'** (giữa câu thoại, không ngữ cảnh 2 bên), ghép lại bằng `concat -c copy` — độ dài không đảm bảo khớp từng mẫu.

## Nguyên nhân

Cắt theo thời gian tuyệt đối, không nhìn nội dung, không đệm ngữ cảnh cho Demucs, không kiểm tổng số mẫu sau ghép.

## Sửa

1. **separate.py**
   - Trích audio gốc 1 lần: WAV PCM s16 44.1k stereo (`-rf64 auto`, cùng `AUDIO_TS_FIX`) → `_demucs_chunks/orig.wav`.
   - Audio ≤ `DEMUCS_LONG_THRESHOLD_SEC` (2400 s) → 1 lượt. Dài hơn → chia ~`DEMUCS_CHUNK_SEC` (1800 s)/khúc; **điểm chia dời vào khoảng lặng gần nhất** (`split_parts.find_best_cut_point`, bán kính `DEMUCS_CUT_SEARCH_SEC` 60 s; không thấy/vô lý → điểm mục tiêu).
   - Cắt khúc **theo số mẫu** bằng đọc/ghi WAV thuần Python (RIFF/RF64, không re-encode); mỗi khúc đưa Demucs thêm `DEMUCS_CHUNK_PAD_SEC` (5 s) ngữ cảnh 2 bên rồi **cắt bỏ phần đệm theo mẫu**. Demucs trả lệch số mẫu → đệm/cắt về đúng + log; khác 44.1k → lỗi (→ ASR fallback).
   - Ghép → `vocals.wav`/`no_vocals.wav`, **kiểm tổng = đúng số mẫu audio gốc**, ghi `n_frames`, `n_chunks`, `cut_points_sec` vào manifest.
   - Resume: `plan.json` (chữ ký video + tham số) + khúc đã xong được dùng lại.
   - **Dùng lại** khi đã có kết quả hợp lệ: stage có `n_frames` → 2 file phải đúng số mẫu; kết quả cũ (chưa có `n_frames`) → 2 file dài bằng nhau và lệch video ≤ max(2 s, 0,2 %). Hợp lệ mà manifest chưa done → đánh done (`reused`).
   - **Không còn ghi/ghi đè `audio.wav`** (trước đây cả nhánh skip lẫn nhánh chạy đều trích `audio.wav` từ vocals — kể cả khi render tự tách nền trên job ASR xong rồi). `audio.wav` do bước ASR quản qua marker nguồn (`audio.wav.json`).
   - Tiến độ ghi qua `Manifest.update`; ASR đang chạy → stage asr hiện `phase=separate` + «Tách giọng Demucs (khúc i/n): x%».
2. **asr.py `resolve_asr_source`**
   - `ASR_USE_DEMUCS` mặc định **1** (tắt: `0/false/no/off`).
   - ASR đã xong (manifest done + `asr.json`) và không force → **không chạy Demucs**, giữ nguồn theo marker hiện có.
   - Demucs lỗi/OOM/thiếu gói `demucs`/ffmpeg lỗi → log `[asr] CẢNH BÁO: Demucs lỗi … -> FALLBACK ASR trên audio gốc`, stage `separate` = failed (có error), stage `asr` tiếp tục trên audio trích từ video (hành vi cũ). Cờ `.stop` (Dừng) thì KHÔNG nuốt lỗi.
   - `force` của ASR **không** ép tách lại Demucs (Demucs 1 lần/job; muốn tách lại: chạy stage separate với force).
3. Nơi dùng `audio.wav` đã rà: các engine ASR + `asr_repair`/`asr_retry_nano`/`asr_fix_align`/`nano_fa_asr` (dùng giọng sạch — đúng ý), `media_ts.ensure_job_audio_ts` (chỉ so ĐỘ DÀI — test chứng minh audio.wav từ vocals dài bằng gốc), `agent_heal` (chỉ xoá khi reset ASR). TTS/render/mixed/dub_fit/hardsub/OCR **không** đọc `audio.wav` (render lấy `[0:a]` từ video hoặc `no_vocals.wav`). ⇒ Không cần `orig_audio.wav` riêng.

## RAM — có cần chia khúc với part ≤ 3 h?

Demucs (`python -m demucs`) nạp CẢ file vào RAM CPU: vào float32 stereo 1,27 GB/giờ; `apply_model` (BagOfModels + split) giữ tensor ra 4 stem ×2 (estimates + out ≈ 2×5,1 GB/giờ) + bản đệm shift ⇒ đỉnh lý thuyết **~12–14 GB/giờ audio**; ghi chú thực đo cũ «12 h ≈ 70 GB» ⇒ **~6 GB/giờ**. Part 2,5 h chạy 1 lượt ⇒ **15–33 GB** — quá rủi ro khi llama-server/Ollama/server cùng chạy. ⇒ GIỮ chia khúc, nhưng theo (1)(2) ở trên; khúc 30' ⇒ đỉnh ~3–7 GB. VRAM không đổi (htdemucs chạy theo đoạn ~7,8 s, ~4–6 GB).

## Cờ / env

| Env | Mặc định | Ý nghĩa |
|---|---|---|
| `ASR_USE_DEMUCS` | `1` | `0` = rollback: ASR trên audio gốc |
| `DEMUCS_LONG_THRESHOLD_SEC` | `2400` (cũ 4200) | dài hơn mới chia khúc |
| `DEMUCS_CHUNK_SEC` | `1800` (cũ 3600) | độ dài mục tiêu mỗi khúc |
| `DEMUCS_CHUNK_PAD_SEC` | `5` | ngữ cảnh đệm 2 bên mỗi khúc |
| `DEMUCS_CUT_SEARCH_SEC` | `60` | bán kính tìm khoảng lặng |

## Rủi ro

- ASR mỗi job/part thêm 1 lần Demucs (GPU ~3–6 phút/2,5 h ước tính; CPU rất chậm). Nếu GPU đang bị llama-server :8083 giữ → Demucs OOM → **fallback** (job không hỏng, nhưng ASR trên audio gốc). `free_gpu_vram` chỉ stop Ollama + xả cache torch — KHÔNG đụng :8000/:8083 (đã kiểm `vram.py`).
- Đĩa tạm: part 2,5 h ≈ 1,6 GB orig.wav + 2×1,6 GB khúc + 2×1,6 GB kết quả (đỉnh ~6–8 GB) trong `work/<job>/_demucs_chunks`.
- Chất lượng ASR trên vocals CHƯA đo trên phim thật (Demucs có thể làm mất phụ âm/tiếng thì thầm, hoặc lọt nhạc có lời). Đo bằng `Z:\PinelineV6\scripts\asr_demucs_compare.bat run` khi V2 rảnh.
- Render chế độ `duck`/`duck_bgm`: code sẵn có ưu tiên `no_vocals.wav` thay `[0:a]` khi file tồn tại ⇒ job MỚI (đã có no_vocals từ bước ASR) render duck sẽ là «nền Demucs + sidechain» thay vì tiếng gốc hạ thấp. Mặc định batch là `sfx_lib` (không ảnh hưởng).
- Engine `nano_fa`: nếu `asr.fun_nano.json` đã có (resume) thì không qua `resolve_asr_source` ⇒ aligner chạy trên `audio.wav` hiện có (không đổi).
- Job đang ASR dở (`fun_asr_nano` resume có `keep_legacy`): marker khác nguồn ⇒ `audio.wav` trích lại từ vocals, mốc thời gian cùng trục nên phần đã có vẫn khớp.

## Rollback

Thêm `"ASR_USE_DEMUCS": "0"` vào `pineline.config.json` (config.inject_env chép vào env lúc khởi động → tiến trình con ASR kế thừa; **cần restart :8801**) hoặc `set ASR_USE_DEMUCS=0` trước `run_v2.bat` → hành vi ASR cũ (audio.wav trích thẳng từ video). Hiện key này CHƯA có trong config ⇒ mặc định 1. Code cũ: chép lại từ `.backup_edit_20261112_agentE\`.

## Port

V4 `separate.py` + `asr.py`; V5 `engines/separate.py` + `engines/asr/asr.py`; V6 `engines/separate.py` + `engines/asr/asr.py` — vẫn bản CŨ (segment FLAC 60', `ASR_USE_DEMUCS` mặc định 0). **CHƯA sửa** — sync sau khi A/B đạt.

## Recheck

- [x] `python -m pytest -q tests\test_separate_demucs_chunks.py tests\test_asr_demucs.py` → 22 pass (bản sao cloud). Toàn bộ `tests`: 375 → 395 pass; fail 16 → 15 (`test_asr_demucs::...triggers_separate...` nay pass), không fail mới.
- [ ] Trên Windows: `python -m pytest -q tests\test_separate_demucs_chunks.py tests\test_asr_demucs.py` (cần ffmpeg — 3 ca dùng ffmpeg thật).
- [ ] Job mới đầu tiên sau fix: log có `[asr] Nguồn ASR = vocals.wav (Demucs)`; manifest `separate.n_frames` có; `vocals.wav`/`no_vocals.wav` cùng số mẫu.
- [ ] Nếu thấy `[asr] CẢNH BÁO: Demucs lỗi` → xem `stages.separate.error`.
- [ ] `Z:\PinelineV6\scripts\asr_demucs_compare.bat run` → `Z:\PinelineV6\docs\reviews\2026-11-12-asr-demucs-compare.md`, nghe clip `D:\PinelineV6_work\asr_demucs_cmp\<job>\clips\`.
