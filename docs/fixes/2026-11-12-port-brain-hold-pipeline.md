# Port V2 → V4: Second Brain (tin Telegram theo mẫu + gỡ HOLD khi chạy tay) + đóng dấu luồng dịch theo job

- **Date:** 2026-11-12 (agent P4)
- **Nguồn V2:** `docs/fixes/2026-11-12-brain-telegram-hold.md` (agent G), `2026-11-12-brain-notify-v2.md` (agent H), `2026-11-12-translate-simple-default.md` (agent F2). Diff lấy đúng phần thay đổi từ backup `Z:\PinelineV2\.backup_edit_20261112_agent{G,H,F2}\`.
- **Khu vực V4:** `agent_brain.py`, `agent_heal.py`, `agent_watch.py`, MỚI `agent_brain_notify.py`, `agent_hold.py`, `server.py`, `routes_agent.py`, `translate_simple/cfg.py`, `config.json` + `pineline.config.json` (2 khoá), tests `tests/test_agent_brain_events.py` (MỚI), `tests/test_agent_brain_notify.py` (MỚI), `tests/test_translate_simple.py` (+6 `test_f2_*`). V6: `scripts/test_v4_simple_demucs.bat`.
- **Status:** trên đĩa V4. **Có hiệu lực sau khi restart :8804** (brain/watcher/server in-process). Không cần restart :8802.
- **Backup:** `Z:\PinelineV4\.backup_edit_20261112_agentP4\` (cùng đường dẫn tương đối; `pineline.config.json.bak`; `V6_scripts_test_v4_simple_demucs.bat`; `_md5_before.txt`, `_md5_after.txt`; `_xfer\` = ảnh mã nguồn để test, không secret).

## Đã port

### 1. Second Brain (G + H)
- `agent_brain.py`, `agent_heal.py`, `agent_watch.py` = bản V2 hiện tại + **giữ khác biệt riêng V4**: `machine` (`_machine.llama_base_url()/aurora_base_url()` cho ping LLM), đường `.stop`/thư mục alt `D:/PinelineV4_work` + `D:/PinelineV2_work` trong `agent_heal`, watcher đọc `TELEGRAM_BOT_TOKEN/ALLOWED_USERS` qua `config.get` trước, banner «Pineline V4 watcher ON». Cách làm: diff(V2 trước G, V4) áp lên V2 mới → không mất phần V4.
- MỚI chép nguyên V2: `agent_brain_notify.py` (tin do code dựng theo mẫu), `agent_hold.py` (gỡ HOLD khi chạy tay, `hold_suppressed`, `auto_context`).
- `server.py` (phần H): `Request` import; `_manual_hold_override` + gọi trong 5 route chạy tay (`/run/{stage}`, `/translate-fill`, `/tts`, `/translate`, `/mux`, tham số `request: Request = None`); `_auto_gpu` HOLD qa_brain tôn trọng `hold_override`; `_run_engine` giữ 40 dòng đuôi + `_save_engine_tail` (`work/<job>/engine_fail_<script>.log` + `stages.<stage>.engine_tail` qua `Manifest.update`).
- `routes_agent.py`: `_agent_set_hold(enabled=True)` trong `auto_context` bị chặn nếu `hold_suppressed`; hook `_HEAL_HOOKS.job_active` (`_job_proc_alive` / `_job_lineage_busy` — V4 có sẵn cả hai). (V4 `routes_agent.py` trước port giống hệt V2 trước H.)
- **Config:** `AGENT_BRAIN_TELEGRAM=events`, `AGENT_BRAIN_TG_SEC=600` — sửa đúng 2 dòng trong `config.json` (mặc định repo, giữ CRLF) **và** `pineline.config.json` (file máy của V4 đang ghi đè `report`/`120` → nếu không sửa sẽ vẫn spam; sửa tại chỗ, không chép đi đâu). Khoá brain không phụ thuộc máy → không đưa vào `machine.py`. Khoá H (`AGENT_BRAIN_REMIND_SEC` 7200, `AGENT_BRAIN_REMIND_MAX` 3, `AGENT_BRAIN_TZ`, `AGENT_HEAL_START_DELAY_SEC` 180) = mặc định trong code như V2.

### 2. Đóng dấu luồng dịch theo job (F2)
- `translate_simple/cfg.py` = V2 F2 (`pipeline_default()`, `_infer_job_pipeline`, `job_pipeline(wd, fresh=, stamp=)`, `PIPELINE_SIMPLE/LEGACY`, `LEGACY_VALUES`) + **giữ `pipeline_mode()` của V4** (F4; = `pipeline_default()`), test V4 còn dùng.
- `server.py`: `_translate_pipeline_simple(wd=None, *, fresh=False)` hỏi `cfg.job_pipeline`; lỗi đọc job → luồng cũ (như V2); lỗi import khi không có `wd` → fallback env như V4 F4. Điểm gọi: `_process_gpu`, `_auto_gpu`, `_run_stage("translate")` (`force` = fresh), `_translate_flow` (Dịch LẠI = mặc định, Soát lại = luồng job), `retranslate_job` (chốt luồng trước khi đánh running), `translate-fill` (simple → `pipeline.run` không force; cũ → `run_translate` lô 25; trả `pipeline`), `_run_requested_review` (bước văn phong).
- Job dở luồng cũ (script.json / stage translate đã chạy, park `waiting_review`, HOLD…) → suy `legacy` và làm nốt bằng luồng cũ; dấu vết simple (`mode=simple` / `agent.simple_park`) → simple; chưa dịch → mặc định (simple, rollback `TRANSLATE_PIPELINE=legacy`).

### 3. Test flake `_VOLATILE`
- V4 `tests/test_translate_simple_next.py` **đã có** sẵn (`"applied_at"` trong `_VOLATILE`, glossary.json qua `_strip`) — giống V2, không sửa.

### 4. Agent I2 (lệnh Telegram người dùng = chạy tay → gỡ HOLD) — ĐÃ PORT (agent P4b)
- Nguồn: V2 `docs/fixes/2026-11-12-brain-notify-v2.md` mục D; diff V2 hiện tại ↔ `Z:\PinelineV2\.backup_edit_20261112_agentI2\`.
- `agent_hold.py`, `routes_agent.py`: V4 trước đó **giống hệt** V2 trước I2 (md5 khớp) → chép nguyên V2 sau I2: `user_context`, `user_caller`, `request_source`, `manual_source`; `maybe_manual_override` dùng `manual_source` (source `run_stage+agent_chat:telegram`…); `api_agent_chat`/`api_agent_confirm` nhận `request: Request` → `_agent_user_ctx`; `_HEAL_HOOKS`/`_AV_SYNC_HOOKS` bọc `_as_auto` (heal/av-sync luôn tự động); `_agent_run_stage("tts")` ngữ cảnh người không gỡ HOLD trước claim, sau claim OK → `_agent_mark_qa_override` (`Manifest.update`).
- `agent_autopilot.py`: áp chọn lọc (giữ `DEFAULT_BASE` cổng `PORT`/8804 của V4): `caller_headers()`, `_post(headers=)`, `agent_chat/agent_confirm(caller=, source=)`; mặc định không gắn header → tick Auto-pilot không đổi.
- `agent_tele_cmd.py`: áp chọn lọc (giữ `hg.DEFAULT_BASE` của V4): `_agent_ask` gắn `caller="user", source="telegram"` chỉ khi có `uid`; `_confirm_callback` (người bấm ✅) gắn như trên.
- MỚI `tests/test_agent_hold_telegram.py` (chép nguyên V2, 14 ca).
- **Không tính tay:** brain in-process/HTTP header `brain`, Auto-pilot/script không header, heal/av-sync hook, `/cmd` nội bộ không uid. `pineline_resume_job` vẫn gỡ HOLD kiểu cũ (ngoài phạm vi, như V2).
- **Hiệu lực:** restart :8804 **và** tiến trình bot Telegram `agent_tele_cmd` của V4 (nếu đang chạy). Recheck: gõ Telegram «lồng tiếng lại <job HOLD>» (hoặc bấm ✅ lệnh force) → manifest `agent.hold_override.source` chứa `agent_chat:telegram`/`agent_confirm:telegram` + 1 tin «🔓 … Đã gỡ HOLD vì bạn chạy tay …»; brain tick không tạo `hold_override`.
- **Test (bản sao Linux, không fastapi, `AGENT_BRAIN=0`):** `test_agent_hold_telegram` trước port 14/14 fail → sau 14/14 pass; nhóm 1b (+events+notify) = 53 passed. Toàn bộ `tests/`: trước 200 passed / 22 failed (+14 fail của test mới) / 15 skipped / 11 error thu thập → sau 214 passed / 22 failed / 15 skipped / 11 error, cùng tập fail môi trường.
- **Backup / rollback:** `Z:\PinelineV4\.backup_edit_20261112_agentP4b\` (4 file .py, `docs\`, `v6scripts\`, `_md5_before.txt`, `_md5_after.txt`, `_new\`, `_src_for_tests.tgz` không secret). Rollback: chép lại 4 file .py; test mới chuyển vào `_to_delete`.

## Khác biệt V4 cần biết
- Cổng V4 = **:8804** (brain dùng `PINELINE_PORT` — `server.py --port` tự đặt env). Desktop pywebview gọi API từ WebView (UA trình duyệt) → được tính là chạy tay; Python `requests/urllib/httpx` (tele_cmd, auto_publisher…) → không.
- V4 không có B3 (`fill_pending`) — nhánh legacy giữ hành vi B2 cũ của V4 (như F4).
- Nội dung docstring/log của module brain còn nhắc «:8801» (lịch sử V2) — chỉ là chữ, không ảnh hưởng.

## Recheck (sau restart :8804)
- `work/logs/agent_brain.log`: `brain start … tg=events heal_delay=180s`; `agent_watch.log`: `hoãn heal 180s sau khởi động`.
- Telegram: tin theo mẫu (không `|`, `<badge>`, «Brain DECISION», «Brain báo cáo» 2'); job xong còn cờ HOLD → 1 tin «✅ … — xong, có video. Đã gỡ HOLD cũ.».
- Chạy tay TTS/mux trên job HOLD → manifest `agent.hold_override`, tin «🔓 … Đã gỡ HOLD vì bạn chạy tay …».
- Job mới → manifest `translate_pipeline=simple`, `translate_pipeline_why=default`; job V4 đang dở luồng cũ → `legacy`/`inferred`.
- **Fail nếu:** còn tin mỗi 2–3 phút; job đã override bị HOLD lại khi QA không có high mới; job dở luồng cũ bị chạy simple khi chưa bấm Dịch LẠI.

## Test (bản sao Linux, stub fastapi/soundfile, `AGENT_BRAIN=0`)
- Toàn bộ `tests/` V4: trước **265 passed / 33 failed / 4 skipped** → sau **310 passed / 33 failed / 4 skipped**, cùng tập fail (môi trường: thiếu data/lexicon, ffmpeg, D:\…).
- Mới: `test_agent_brain_events.py` + `test_agent_brain_notify.py` = 39 passed; `test_translate_simple.py` +6 `test_f2_*` pass. Nhóm (1) bat: 106 → 112 test.
- Windows: `Z:\PinelineV6\scripts\test_v4_simple_demucs.bat` (nhóm 1b mới: 39 passed).

## Rollback
Chép lại file từ `.backup_edit_20261112_agentP4\` (xoá = chuyển 2 file mới `agent_brain_notify.py`, `agent_hold.py` + 2 test vào `_to_delete`). Chỉ luồng dịch: `TRANSLATE_PIPELINE=legacy`. Chỉ Telegram: `AGENT_BRAIN_TELEGRAM=report` (hoặc `off`).
