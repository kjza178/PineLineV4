# Mix #1+#3 + title→ngươi vào production

- **Date:** 2026-11-10
- **Job / khu vực:** `agent_pronoun_pass` / `translate.review_batch` / UI batch
- **Status:** fixed

## Triệu chứng

REVIEW/LLM đổi ngôi lung tung (cậu↔ông↔ngươi) quanh danh xưng bậc (Môn chủ/Điện chủ…); harness tmp đã ổn nhưng chưa wire.

## Root cause

Pronoun-QA chỉ theo glossary pairs; không có policy title cửa sổ → formal 2nd. Style review không đóng băng đại từ.

## Evidence

- Tmp mix v2 `pronoun_mix_13_v2`: prefer=ngươi, 0 ông loạn (trước đó 10 cậu→ông)
- Policy: `D:\PinelineV2_tmp\pronoun_register_POLICY.md`

## Fix

- Thêm `pronoun_register_policy.py` (V2/V4/V5)
- `#3` trong `agent_pronoun_pass`: scan title+cậu, prompt register, normalize ông/ngươi, mech còn sót — `PRONOUN_TITLE_POLICY=1`
- `#1` trong `review_batch`: mask/unmask đại từ, reject flip ngôi — `REVIEW_PRONOUN_MASK=1`
- UI: `review_backup` = `off` | `aurora_parallel` (lưu queue_opts; fan-out parallel chưa bật)
- Bak: `Z:\PinelineV2_codebak\2026-11-10_mix13-review-backup\` + zip `Z:\PinelineV2_backup_2026-11-10_0847.zip`

## Recheck

1. Job có Môn chủ/Điện chủ + «cậu» trong ±2 cue → chạy pronoun pass / review
2. Log: `[pronoun] title-policy mode=… prefer=ngươi`
3. **Pass nếu:** cậu trong cửa sổ title → ngươi (mixed/ancient); style review không đổi tôi↔ta / cậu↔ngươi nhờ mask
4. **Fail nếu:** vẫn cậu cạnh Môn chủ sau pass, hoặc REVIEW đổi ngôi khi mask=1

## Liên quan

- Config: `PRONOUN_TITLE_POLICY`, `REVIEW_PRONOUN_MASK`, `REVIEW_BACKUP` / batch `review_backup`
- Parallel Aurora: chỉ UI lựa chọn backup — chưa wire `run_review` fan-out
