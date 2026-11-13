# Port V2 → V4: Brain bỏ qua job đã xong + phân loại park tự động (⏸) / HOLD cần người (⛔)

- **Date:** 2026-11-13 (agent R4)
- **Nguồn V2:** `docs/fixes/2026-11-13-brain-finished-hold.md` (agent N) — bản sao cùng thư mục này. Base diff = `Z:\PinelineV2\.backup_edit_20261113_agentN\`.
- **Khu vực V4:** `agent_hold.py`, `agent_heal.py`, `agent_brain.py`, `agent_brain_notify.py`, `agent_brain_context.py`, `routes_agent.py` (`_agent_resume`); tests `tests/test_agent_brain_notify.py` (snapshot hold_set ⏸ → ⛔), MỚI `tests/test_brain_finished_hold.py` (23 ca). V6: `scripts/test_v4_simple_demucs.bat` nhóm (1b).
- **Status:** trên đĩa V4. **Cần restart :8804** (brain/watch/heal chạy trong tiến trình server). Không đổi `server.py`.
- **Backup:** `Z:\PinelineV4\.backup_edit_20261113_agentR4\` (`_v4_md5_before.txt` khớp lúc đọc, `_md5_after.txt`, `_NEW_FILES.txt`; bat V6 ở `Z:\PinelineV6\.backup_edit_20261113_agentR4\scripts\`).

## Nội dung (tóm tắt — chi tiết ở doc V2)

- `agent_hold.job_finished(wd, data)` — định nghĩa duy nhất «job đã xong» (đã đăng / mux done + output không stale / parent đã ghép / mọi stage done / part của parent đã ghép). `hold_class`/`hold_info`/`AUTO_PARK`/`NEED_BY_HOLD`/`PARK_KEYS`; `manual_override` gỡ thêm `review_retries/review_retry_at/simple_park/split_wait_parts`.
- `agent_heal.diagnose_job`: job xong → issue `finished`, không action; `heal_job` trả skipped. 3 bộ phát hiện sửa gốc: `tts_not_started` (không bắt khi tts done), `asr_bad` (không bắt khi asr done + đã dịch, asr.json đã dọn), `tts_missing_clips` (chỉ khi dịch xong).
- `agent_brain`: sense/apply/deep_focus/remind_failed bỏ job xong; `_hold_event` → `park_set` (⏸ tự thử lại) vs `hold_set` (⛔ cần người, kể cả park → review_failed); `clear_stale_holds` gỡ khoá park, part của parent đã ghép gỡ im lặng.
- `agent_brain_notify`: tin ⏸ «tạm dừng soát dở N câu, tự thử lại lúc HH:MM (lần k/max)» / «chờ part Pn»; ⛔ «HOLD: lý do.» + «Cần bạn: …» theo loại.
- `agent_brain_context`: snapshot LLM thêm `agent.hold_class`, `finished`. `routes_agent._agent_resume` reset bộ đếm park.

## Cách port

Merge 3 chiều `git merge-file` (chỉ công cụ diff, không repo git): base = backup agentN V2, ours = V4, theirs = V2 hiện tại (md5 = `_md5_after.txt` của N). 7 file **0 xung đột**. Khác biệt V4 giữ nguyên: `agent_brain.py`/`agent_brain_context.py` ping qua `machine.llama_base_url()/aurora_base_url()/hongguo_base_url()`, `presets_active_json()`; `agent_heal.py` `.stop`/thư mục alias `D:/PinelineV4_work` + legacy V2. `agent_hold.py`, `agent_brain_notify.py`, `routes_agent.py`, `tests/test_agent_brain_notify.py` V4 = base V2 → nay = V2 sau N. CRLF/LF từng file như cũ, không BOM.

## Test

Bản sao cloud Linux (không fastapi/soundfile, KHÔNG stub), `AGENT_BRAIN=0`, `pytest -q tests --continue-on-collection-errors`:
trước 324 passed / 34 failed / 19 skipped / 10 error → sau **347 passed** / 34 failed / 19 skipped / 10 error, cùng tập fail/error (môi trường).
Nhóm (1b): events 11 + notify 28 + hold_telegram 14 + brain_finished_hold 23 = **76 passed**. `test_park_review_retry.py` cần fastapi thật (chạy bat trên Windows).
