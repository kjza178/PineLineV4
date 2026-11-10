# Brain thật: perceive → ACT → CLEAR/HOLD cửa TTS

- **Date:** 2026-11-10
- **Job / khu vực:** `agent_brain.py` quality_job / sense_jobs
- **Status:** fixed (chờ restart nạp)
- **Backup:** zip `Z:\PinelineV2_backup_2026-11-10_2137.zip`; codebak `Z:\PinelineV2_codebak\2026-11-10_brain-real-loop\`

## Triệu chứng

Brain chỉ HOLD/spam, không biết job đang soát, không ACT/CLEAR, không báo kết quả xử lý.

## Root cause

`quality_job` = scan → HOLD nếu high; `hang_fix` skip khi busy → không đóng vòng.

## Fix

Policy 4 bước:

1. **Perceive** `_qa_pipeline_phase`: `mid_review` | `pre_tts` | `post_tts` | `idle`
2. **Act** chỉ khi không mid/post; `scan_and_heal_job`; TG `Brain ACT …`
3. **Close** high=0 → CLEAR + TG; high>0 chỉ **HOLD ở pre_tts**
4. **Report** ACT/CLEAR/HOLD — không HOLD giữa soát

`sense_jobs` bỏ mid_review/post_tts khỏi quality_scan.

## Recheck

1. Job đang review → log `skip — đang review` / không có trong quality_scan; không HOLD.
2. Job translate done, còn high → ACT rồi HOLD pre-TTS + message có healed/fix.
3. high=0 → CLEAR + “mở TTS/mux”.
4. **Pass nếu:** không HOLD mid-review; có ACT/CLEAR trên TG khi mode=report.
5. **Fail nếu:** lại HOLD khi `review_done < review_total`.

## Liên quan

- Follow-up của `2026-11-10-review-heal-parallel.md`
- **Restart :8801** (after-current ASR) để nạp

## Follow-up — quyết định qua AI agent

- **Date:** 2026-11-10 ~21:40
- Rule path **không auto-HOLD**; ghi `brain_pending_decisions.json` + TG `NEED-LLM`.
- `BRAIN_LLM_INSTRUCTION`: mỗi job phải A–E (đang làm gì / ổn? / lỗi / plan / tool) + `DECISION` block.
- `llm_tick` deep per focus job → TG `Brain DECISION …`.
- Snapshot job có `phase` cho agent.
- Sync V2/V4/V5. Cần restart nạp.
