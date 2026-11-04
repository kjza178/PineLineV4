# Job gốc sau split: part upload xong nhưng parent báo lỗi / chưa hoàn thành

- **Date:** 2026-11-03
- **Job / khu vực:** auto-split / `split_parts.merge_job_parts` / queue runner parent
- **Status:** fixed
- **Backup:** `Z:\PinelineV2_codebak\2026-11-03_split-parent-done\`

## Triệu chứng

Split → tạo `_p01…_pN` → part render + auto-upload OK. Job gốc UI/`status=failed` với `asr.error = pipeline kết thúc nhưng output chưa hoàn chỉnh` dù đã có `output.mp4` Full.

## Root cause

V2 `merge_job_parts` chỉ đánh `mux=done`. Queue runner gọi `is_wired_done` (cần download+asr+translate+tts+mux). Parent thiếu asr/translate/tts → `_failed(...)` ghi lỗi lên stage `early` (thường `asr`).

V4 merge đã đánh đủ stage; khi mới split, stage `early=running` có thể nhìn như kẹt — đã chuyển sang `pending` + cur_text chờ part.

## Evidence

- `09537b974243`: mux done Full, `output.mp4` ~6.4GB, asr=`failed` đúng câu trên.
- `b04b8b957d9f`: 5 part mux done + parent `output.mp4` ~21GB nhưng mux/asr còn pending/running giả.

## Fix

- V2 `split_parts.merge_job_parts`: đánh done đủ 5 stage + `split_info.status=merged` (giống V4).
- V2/V4 queue runner: heal parent đã có Full/merge trước khi `_failed`.
- V4 khi `return "split"`: clear running/failed trên asr…mux → pending «Chờ N part…».
- Heal tay 2 job trên → `status=done`.

## Recheck

1. Job dài ≥3h → auto-split → đợi hết part + merge.
2. **Pass nếu:** parent `overall status=done`, không còn `pipeline kết thúc nhưng output chưa hoàn chỉnh`; part vẫn upload bình thường.
3. **Fail nếu:** parent `asr/translate` failed trong khi `output.mp4` Full đã có.

## Liên quan

- Jobs healed: `09537b974243`, `b04b8b957d9f`
- Sync: V2 `split_parts.py`+`server.py`; V4/V5 `server.py`
