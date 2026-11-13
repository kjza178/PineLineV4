# 2026-11-13 — Brain: job đã xong bị heal «thất bại» + park tự động bị báo nhầm «HOLD / Cần bạn»

Agent N. Restart :8801 để có hiệu lực (brain/watch/heal chạy trong tiến trình server).
Bak `Z:\PinelineV2\.backup_edit_20261113_agentN\` (md5 trước khớp lúc đọc; `_v2_md5_before.txt`).

## Triệu chứng (Telegram 12/11)

- A) `⏸ Lớp học huyền thoại bị lộ P3 (2937ff) — Đã đặt HOLD: soát dở (simple) — còn 3 câu chưa soát. Cần bạn: duyệt bản dịch rồi bấm Chạy tiếp`.
  Thực tế: `agent.held_at=waiting_review` + `simple_park` + `review_retry_at` = **park tự động** của cổng simple, hàng đợi
  tự thử lại khi tới hạn (tối đa `QUEUE_REVIEW_RETRY_MAX`=3) — không cần người.
- B) `🩹 Xâm nhập trò chơi (2493d3) / Thiên phú vô song (ae9956) / Tu vi mỗi giây tăng vạn năm (ec10e4) — Brain: heal thất bại —
  chạy lại lồng tiếng: chưa dịch xong (thiếu script.json)`. Cả 3 job ĐÃ XONG (mọi stage done, có output.mp4; 2493d3 là parent
  đã ghép 4 part + đã đăng 12/11 16:21Z; ec10e4 đã đăng 08/11; ae9956 done, script.json đã dọn).

## Gốc lỗi

### B — bộ phát hiện nào chọn 3 job xong để heal

`agent_watch.watch_once` và `agent_brain._tick_inner` (rule path) cùng gọi `agent_heal.scan_problem_jobs` → `diagnose_job`
— hàm này **không biết job đã xong**, chỉ suy từ file:
1. `asr_bad`: `translate.status=done` mà **không có `asr.json`** (đã dọn / parent đã ghép không có asr.json) → issue + action aggressive `asr_run_force`.
2. `tts_not_started`: `translate=done` mà **không có `tts.json`** và tts không `running` — kể cả khi `tts.status=done` → action safe `tts_run`.
3. `_job_needs_attention` → True (2 mã trên), `ok_output` chỉ thêm khi KHÔNG có issue nào.
→ heal `tts_run` → hook trả «chưa dịch xong (thiếu script.json)» → `heal_summary=fail` → Telegram «🩹 heal thất bại»;
brain còn leo thang `heal aggressive` (log `agent_brain.log` 13:32). Không phải qa_hang / av-sync / output hỏng.
Thêm (dry-run): `2937ffd7989f` (ASR pending, dịch pending) bị bắt `tts_missing_clips` vì `stages.tts.n_missing=1466` cũ
→ sẽ chạy `tts_run` khi chưa dịch → cùng kiểu «heal thất bại».

### A — tin HOLD sai bản chất

`agent_brain.detect_stage_events` coi mọi `held_at/qa_blocked/hold_after_translate` là «hold_set» → `agent_brain_notify` luôn
in «Đã đặt HOLD … Cần bạn: duyệt bản dịch rồi bấm Chạy tiếp». Không phân biệt park tự động (waiting_review / split_parts) với
HOLD cần người; khi park → `review_failed` (cần người) lại KHÔNG báo vì cờ «held» không đổi.

## Sửa

| File | Thay đổi |
|---|---|
| `agent_hold.py` | MỚI `job_finished(wd, data)` — **một định nghĩa duy nhất**: không stage running VÀ (upload_status ∈ uploaded/published/public/success/done, hoặc mux done + output.mp4/output_full.mp4 không stale, hoặc parent đã ghép Full `split_info.status=merged`/`mux.is_full_merged`, hoặc mọi stage wired done, hoặc part `_pNN` của parent đã ghép/đã đăng). MỚI `hold_class`/`hold_info`/`AUTO_PARK`/`NEED_BY_HOLD`/`PARK_KEYS`. `manual_override` gỡ thêm `review_retries/review_retry_at/simple_park/split_wait_parts`. |
| `agent_heal.py` | `diagnose_job`: job xong → `finished=True`, issue `finished`, KHÔNG action; `heal_job` (plan & apply) trả `skipped: job đã xong`; `_job_needs_attention` False. Gốc: `tts_not_started` không bắt khi `tts.status=done`; `asr_bad` không bắt khi asr done + đã dịch xong (asr.json dọn); `tts_missing_clips` chỉ khi dịch đã xong. ⇒ `scan_problem_jobs`/`heal_failed_batch`/`agent_watch`/route `scan_failed` cùng bỏ job xong. |
| `agent_brain.py` | `job_finished` uỷ cho agent_hold. `sense_jobs` bỏ job xong; `apply_actions(heal_job)` bỏ job xong (`skipped=finished`); `_deep_focus` (deep tick LLM) bỏ job xong kể cả còn stage failed cũ, chỉ coi HOLD CẦN NGƯỜI là «held» (park không DECISION); nhắc lỗi (`remind_failed`) bỏ job xong. `detect_stage_events` → `_hold_event`: park/split_wait → `park_set` (1 tin khi mới park hoặc lượt park mới), HOLD cần người → `hold_set` (khi mới HOLD hoặc đổi loại, vd park → review_failed); state cũ không có `hold_cls` ⇒ không báo lại sau restart. `clear_stale_holds` gỡ thêm khoá park; part của parent đã ghép → gỡ im lặng (log, không tin). |
| `agent_brain_notify.py` | `park_set` → «⏸ <phim> — tạm dừng soát dở N câu, tự thử lại lúc HH:MM (lần k/max)» / «⏸ … — tạm dừng chờ part P3 soát dở, tự chạy tiếp khi part tới hạn», KHÔNG «HOLD/Cần bạn». `hold_set` → «⛔ <phim> — HOLD: lý do.» + «Cần bạn: …» theo loại. |
| `agent_brain_context.py` | snapshot LLM thêm `agent.hold_class`, `finished`; luật: finished → bỏ qua, park/split_wait → chỉ đợi. |
| `routes_agent.py` | `_agent_resume` («Chạy tiếp») gỡ thêm `review_retries/review_retry_at/simple_park/split_wait_parts` (trước: bộ đếm còn > max → lần park kế nhảy thẳng `review_failed`). |
| tests | MỚI `tests/test_brain_finished_hold.py` (23 ca); `test_agent_brain_notify.py::test_snapshot_hold_set` đổi kỳ vọng ⏸ → ⛔ (theo yêu cầu). |

## Bảng tạm dừng — vòng đời (ai đặt / ai gỡ / khi nào)

| Loại | Cờ manifest.agent | Ai đặt | Ai gỡ / khi nào | Tin Telegram (mới) |
|---|---|---|---|---|
| (a) park simple | `held_at=waiting_review`, `simple_park`, `review_retries=k`, `review_retry_at` | `server._auto_translate_simple` (cổng simple status park / lỗi) | Tới `review_retry_at` → `_queue_park_ready` → chạy lại; qua cổng → gỡ held_at + khoá park; người chạy tay (`agent_hold.manual_override`) / «Chạy tiếp» (`_agent_resume`) / job xong (`clear_stale_holds`) | ⏸ … tạm dừng soát dở N câu, tự thử lại lúc HH:MM (lần k/max) — 1 tin/lượt park |
| (a) park B2 legacy / fill_pending | `held_at=waiting_review`, `review_retries`, `review_retry_at` | `server._auto_gpu` (REVIEW còn câu chưa rv), `_park_fill_pending` (FILL_PENDING_PARK=1) | unrev=0 → gỡ (2185); tới hạn → chạy lại; tay/Chạy tiếp/job xong như trên | như trên |
| (b) review_failed | `held_at=review_failed`, `hold_after_translate=True`, `review_retries>max` | 3 nơi trên khi `n_try > QUEUE_REVIEW_RETRY_MAX` | Chỉ người: chạy tay (override) / «Chạy tiếp» (nay reset bộ đếm) / job xong | ⛔ … HOLD: lý do. Cần bạn: xem các câu chưa soát/dịch rồi bấm Chạy tiếp. |
| (c) qa_brain | `held_at=qa_brain`, `qa_blocked`, `hold_after_translate` | `_auto_gpu` (agent_quality high>0, không khi `hold_suppressed`/`qa_override`) | Brain quality_job khi high=0 (`hold_cleared qa_clean`); tay; Chạy tiếp (`qa_override`); job xong | ⛔ … Cần bạn: duyệt bản dịch rồi bấm Chạy tiếp (hoặc chạy tay Lồng tiếng). |
| (c) qa_gate | `held_at=qa_gate`, `qa_blocked`, `hold_after_translate` | `_auto_gpu` (run_qa_gate fail), `agent_qa_gate` | như qa_brain (agent_qa_gate gỡ khi pass) | như trên |
| (c) simple_gate | `held_at=simple_gate`, `hold_after_translate` | `_auto_translate_simple` (cổng simple status hold) | qa_override + chạy lại; tay; Chạy tiếp; job xong | như trên |
| (c)/(e) hold_after_translate | `hold_after_translate` (+`held_at=after_translate` do `_auto_gpu` đóng dấu) | UI/Agent `_agent_set_hold`, LLM tool `pineline_hold_after_translate`, brain runtime `set_hold` (bị chặn nếu `hold_suppressed`) | `_agent_set_hold(False)`, tay, Chạy tiếp, job xong | như trên |
| (d) split_parts | parent `held_at=split_parts`, `split_wait_parts=[…]`, `hold_reason` | `server._split_wait_parts` (agent M) — part park/HOLD sau vòng part | `_split_wait_clear` khi parent chạy lại vòng part; `_queue_park_ready(parent)` = part tới hạn/xong; job xong | ⏸ … tạm dừng chờ part Pn soát dở, tự chạy tiếp khi part tới hạn |
| (e) manual override | gỡ cờ + `hold_override{by:manual,stage,was,high,high_i}` | `agent_hold.manual_override` (HTTP tay UI, Agent chat/Telegram trong `user_context`) | — ; brain/auto không HOLD lại khi chưa có high QA mới (`hold_suppressed`) | 🔓 Đã gỡ HOLD vì bạn chạy tay … (giữ nguyên) |
| job xong còn cờ | bất kỳ ở trên | — | `clear_stale_holds` mỗi tick brain (nay gỡ cả khoá park; part của parent đã ghép → im lặng) | ✅ … Đã gỡ HOLD cũ (job lẻ / parent) |

Mâu thuẫn đã sửa: (1) «Chạy tiếp»/chạy tay để lại `review_retries` > max → park kế tiếp thành `review_failed` ngay;
(2) job xong còn `review_retry_at/simple_park/split_wait_parts`; (3) park → review_failed không có tin; (4) park báo «HOLD/Cần bạn»;
(5) deep tick LLM ra DECISION cho park và job xong có stage failed cũ.
Không đổi: `server.py` (`_queue_park_ready` / thứ tự cờ cứng thắng `held_at` vẫn như cũ — `hold_class` dùng cùng thứ tự).

## Dry-run CHỈ ĐỌC D:\PinelineV2_work (13/11, code mới, không ghi)

- finished (11): `2493d3c7cb29` + `_p01.._p04`, `2d3316593ea9`, `32da3d8f225b`, `365baf19df54`, `9dedde16e35b`, `ae9956bb8fb3`, `ec10e47767ed`.
- park tự động (1): `60892cc63cb7_p01` (simple, còn 1 câu, lần 1/3, `review_retry_at` 23:27 12/11 đã quá hạn — chờ hàng đợi sau restart). HOLD cần người: 0.
- `2937ffd7989f`: hiện KHÔNG park/HOLD (người chạy tay ASR 13:40Z 12/11 đã gỡ; ASR/dịch pending); trạng thái lúc báo (`was`) phân loại = park.
- `scan_problem_jobs` còn: `60892cc63cb7`, `60892cc63cb7_p02` (stale_or_running) — đúng là đang chạy/treo thật.

Tin mẫu (dữ liệu thật, giờ +07):
```
⏸ Lớp học huyền thoại bị lộ P3 (2937ff) — tạm dừng soát dở 3 câu, tự thử lại lúc 20:45 (lần 1/3)
⏸ Tạo Thần P1.1 (60892c_p01) — tạm dừng soát dở 1 câu, tự thử lại lúc 23:27 (lần 1/3)
⏸ Xâm nhập trò chơi (2493d3) — tạm dừng chờ part P3 soát dở, tự chạy tiếp khi part tới hạn
⛔ Lớp học huyền thoại bị lộ P3 (2937ff) — HOLD: dịch simple chưa xong sau 3 lượt — còn 3 câu chưa soát, cần người xem.
Cần bạn: xem các câu chưa soát/dịch rồi bấm Chạy tiếp.
⛔ Xâm nhập trò chơi P2 (2493d3_p02) — HOLD: QA gate block — 2 high.
Cần bạn: duyệt bản dịch rồi bấm Chạy tiếp (hoặc chạy tay Lồng tiếng).
```
(3 job 2493d3/ae9956/ec10e4: `heal_job` → «KHÔNG heal: job đã xong …», không tin.)

## Test

Bản sao cloud, `AGENT_BRAIN=0`, toàn bộ `tests/`: trước 608 pass / 14 fail / 6 error (môi trường: google.oauth2, fastapi.testclient,
pronoun…) → sau 631 pass, CÙNG 14 fail + 6 error. Gồm test_agent_brain_events / notify / hold_telegram / simple_junk_park / park_review_retry.

## Port (CHƯA làm)

V4/V5/V6 cần port: `agent_hold.py` (job_finished, hold_class/hold_info, manual_override), `agent_heal.py` (diagnose finished + 3 detector),
`agent_brain.py` (_hold_event, sense/apply/deep_focus/remind/clear_stale_holds), `agent_brain_notify.py` (park_set/⛔),
`agent_brain_context.py`, `routes_agent.py::_agent_resume`, `tests/test_brain_finished_hold.py`, `tests/test_agent_brain_notify.py`.
V6: tương ứng `state/job_state.py` đã có `park_ready`/`review_failed` — cần `job_finished` + phân loại tin.
