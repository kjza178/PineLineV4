# simple-junk-park: câu ASR rác «None.» làm dịch simple park mãi → part 1/2 kẹt, phim không ghép

- **Date:** 2026-11-13
- **Nguồn:** agent M. Sự cố thật `D:\PinelineV2_work\60892cc63cb7_p01` (part 1/2 của `60892cc63cb7`, 5150 câu).
- **Khu vực:** MỚI `text_junk.py`; `firered_asr.py` (`_parse_firered_result` → lọc, thân cũ thành `_parse_firered_result_raw`; phần slice của agent L giữ nguyên); `translate_simple/pipeline.py` (`_mark_junk`, `_review_missing`, `_accept_unreviewed`, `_brain_line`), `translate_simple/cfg.py` (`unreviewed_tolerance`, `missing_batch`), `translate_simple/stage_review.py` (bỏ câu junk, tham số `batch`), `translate_simple/validate.py` (junk không cờ); `server.py` (`_SPLIT_WAIT`, `_split_wait_clear`, `_split_wait_parts`, `_split_wait_ready`, nhánh `split_parts` trong `_queue_park_ready`, 2 dòng gọi trong `_check_and_run_auto_split_parts`). Test MỚI `tests/test_simple_junk_park.py` (42); `tests/test_translate_simple.py` + `tests/test_translate_simple_scenarios.py` mỗi file 1 ca đặt `SIMPLE_UNREVIEWED_TOLERANCE=0`.
- **Backup:** `Z:\PinelineV2\.backup_edit_20261113_agentM\` (bản gốc từng file — md5 khớp lúc đọc; `patch_server.py` = phép vá server.py; `PinelineV6_scripts\test_v2_translate_simple.bat`).
- **Status:** trên đĩa V2. **Cần restart :8801** cho dịch simple + server (xem «Nạp code»). FireRed có hiệu lực ngay lần ASR kế tiếp.

## Hiện tượng

`asr.json` / `script.json` câu i=1039 (1904.45–1904.93 s) có `zh = "None."`. Review GPT không trả câu này (2 lượt: review + review-retry), repair không đụng (không có cờ) → cổng simple `park: còn 1 câu chưa soát` (`agent.held_at=waiting_review`, `simple_park`, `review_retries=1`). Retry sẽ park lại y hệt → sau `QUEUE_REVIEW_RETRY_MAX` (3) → HOLD `review_failed`.

## Nguồn «None.»

Không phải `str(None)`: FireRedASR2 AED (`fireredasr2/asr.py`) trả `text.lower()` → đoạn ồn 0.48 s giải mã thành token tiếng Anh **«none»**; FireRedPunc `RuleBaedTxtFix.fix` thêm «。» → `^([a-z]+)。` → «none.» rồi viết hoa chữ đầu → **«None.»**. Vendor (`vendor/FireRedASR2S`) không sửa; chặn tại `_parse_firered_result` (mọi nhánh sentences/words/text).

## Sửa

1. **ASR** `text_junk.is_junk_text`: rác = không có ký tự CJK/chữ/số nào (rỗng, chỉ dấu/ký hiệu) hoặc lõi chữ là `none|null|nan` (± dấu, hoa thường). «OK.», «123», «None of that.», «哈哈。» không rác. `_parse_firered_result` bỏ câu rác, in `[firered_asr] bỏ N câu rác (None/không chữ): [...]` mỗi slice.
2. **Dịch simple** `_mark_junk` (ngay sau gỡ lặp ZH, trước plan/NMT): câu zh rác (không manual) → `vi="…"`, `rv=1`, `junk=1`, `skip_tts=1`, trace `junk`. Không gửi review (kể cả rereview), bộ kiểm không cờ, không đếm «chưa soát».
   - **Vì sao «…» chứ không vi rỗng:** vi rỗng bị `translate.count_script_missing`/`translate_ready_for_tts` đếm «câu VI trống» (chặn TTS) và cổng simple `n_missing` → park. «…» là quy ước sẵn của luồng cũ (`translate._trivial_vi`); TTS `clone_tts._is_trivial_vi("…")` = True → `_silence_entry`: wav im lặng đúng độ dài slot (0.48 s), không gọi engine, không lệch timeline, không báo thiếu. `skip_tts` chỉ là cờ ghi chú (TTS chưa đọc).
   - zh hết rác (vd sync nguồn OCR) → gỡ cờ, xoá «…», dịch lại.
3. **Cổng simple** (sau repair):
   - còn câu chưa rv → **1 lượt review CHỈ các câu đó**, lô `SIMPLE_MISSING_BATCH` (4) → hậu kỳ + kiểm lại đúng các câu đó (`simple.review.review_missing`).
   - còn ≤ `SIMPLE_UNREVIEWED_TOLERANCE` (trống = max(3, 0.2 % số câu) → 5150 câu: 10; `0` = tắt) **và** mọi câu đó có bản nháp vi (không trống, không chữ Hán) → nhận nháp: `rv=1` + `unreviewed_accepted=1` (rv để các cổng rv khác — `job_queue`, `agent_qa_gate`, `_queue_park_ready` — nhất quán), trace `unreviewed_accepted` từng câu + dòng `gate`; manifest `stages.translate.simple.unreviewed_accepted` / `accept_reason`, `cur_text` «… · nhận N câu nháp chưa soát»; brain: 1 dòng `need` (chỉ khi `agent_brain` đang chạy trong tiến trình). Vượt ngưỡng / thiếu nháp → park như cũ. Review sau trả câu đó → gỡ `unreviewed_accepted`.
4. **Part/parent** — hành vi CŨ (đúng như code): hàng đợi chạy parent `60892cc63cb7`; `_check_and_run_auto_split_parts` chạy tuần tự `_auto_gpu(p01)` → park → return → `_auto_gpu(p02)` → xong → in «TẤT CẢ PART ĐÃ XONG» → `merge_job_parts` trả lỗi (thiếu p01) → return True → `_queue_run_one(parent)`: không wired-done, parent không HOLD → **`failed` «pipeline kết thúc nhưng output chưa hoàn chỉnh»** → hàng đợi bỏ parent, lấy job kế. Part KHÔNG nằm trong hàng đợi nên **không ai quay lại p01** khi tới `review_retry_at` → **kẹt vĩnh viễn (bug)** tới khi người chạy lại parent; mỗi lần chạy lại parent thì p01 retry ngay (không chờ hạn) và tăng `review_retries`.
   **Sửa tối thiểu:** sau vòng part, còn part chưa xong mà part đó park/HOLD → KHÔNG ghép; parent `agent.held_at=split_parts` + `split_wait_parts=[…]` + `hold_reason`, `stages.mux` pending «chờ … chưa ghép Full» → `_queue_run_one` trả `held` (giữ ghế, như job thường park). `_queue_park_ready(parent)` = True khi một part chờ sẵn sàng (`_queue_park_ready(part)`: tới hạn `review_retry_at` / hết HOLD) hoặc đã xong → hàng đợi chạy lại parent → vòng part bỏ part xong, chạy lại part park; đầu vòng gỡ dấu chờ. Part HOLD `review_failed` → parent giữ ghế tới khi người gỡ HOLD part (như job thường). Part chưa xong mà KHÔNG park (lỗi lạ) → như cũ. Chạy qua UI 1-click (không qua hàng đợi) thì không có ai thăm dò — như job thường.

## Gỡ job đang kẹt `60892cc63cb7_p01` (KHÔNG sửa dữ liệu work)

Lúc vá (17:5x 12/11 UTC): hàng đợi `current=60892cc63cb7`, p02 đang «simple · review lô 154/173» trong tiến trình :8801 CŨ.
- **Restart :8801 SAU khi p02 xong** (code cũ): parent sẽ `failed` và rời hàng đợi → sau restart: thêm lại parent `60892cc63cb7` vào hàng đợi (hoặc bấm «Chạy tự động» trên parent). Vòng part bỏ qua p02 (đã mux), chạy p01: ASR có sẵn → simple: `_mark_junk` i=1039 → «…» rv → review 0 câu → cổng done (53 cờ ≤ 154) → gỡ `waiting_review`/`simple_park`/`review_retries` → TTS (i=1039 slot im lặng) → render → ghép Full tự động.
- **Restart trước khi p02 xong**: hàng đợi tự nạp lại parent ở đầu → vòng part chạy p01 (qua như trên) rồi p02 tiếp.
- Hoặc chạy riêng «Chạy tự động» trên `60892cc63cb7_p01`: mux xong → `_notify_parent_after_part_done` tự xếp ghép Full khi p02 đã xong.
Không cần sửa tay `manifest.json`/`script.json`.

## Nạp code

- `translate_simple` được `server.py` import trong tiến trình (`_simple_translate_run`: `from translate_simple import pipeline` lúc gọi, **không reload** — module đã nạp nằm trong `sys.modules`) → **cần restart :8801**. `text_junk` nạp lần đầu sau restart.
- `server.py` (part/parent) → **cần restart :8801**.
- `firered_asr.py` chạy tiến trình con (`_run_engine`) → hiệu lực ngay lần ASR FireRed kế tiếp.

## Test

Cloud (bản sao, stub fastapi/yt_dlp/soundfile chỉ để import server; không GPU/LLM/HTTP), toàn bộ `tests/` trên mã hiện tại (gồm sửa của agent K): trước 14 fail / 556 pass / 8 skip / 6 error → sau 14 fail / 598 pass / 8 skip / 6 error (cùng tập fail môi trường; +42 test mới). Ca chính: tái hiện đúng trạng thái đĩa (5150 câu, i=1039 «None.» chưa rv, agent park) → done, GPT không nhận i=1039, `translate_ready_for_tts` ok, slot im lặng 0.48 s; chạy mới 5150 câu GPT luôn bỏ «None.» → done; đối chứng tắt luật → park «còn 1 câu chưa soát»; ngưỡng (nhận 2 câu, vượt 4>3 park, thiếu nháp park, 0 tắt, lượt bổ sung cứu được → không accepted); parse FireRed (sentences/words/text, qua `transcribe_sliced`); parent giữ ghế / quay lại part tới hạn / HOLD part chặn / vòng part không ghép hụt.
`Z:\PinelineV6\scripts\test_v2_translate_simple.bat`: thêm `tests\test_simple_junk_park.py`, kỳ vọng nhóm 1: 130 pass.

## Port V4/V5/V6 (CHƯA làm)

`text_junk.py` (mới); `firered_asr._parse_firered_result` (+`_raw`); `translate_simple/{cfg,pipeline,stage_review,validate}.py`; `server.py` (`_split_wait_*`, `_queue_park_ready`, `_check_and_run_auto_split_parts`) — V5/V6 theo vị trí tương ứng trong layout package; `tests/test_simple_junk_park.py` (+ env tolerance=0 ở 2 ca cũ).
