# FireRed LID AssertionError t_confidences <= 1.0

- **Date:** 2026-11-10
- **Job / khu vực:** `365baf19df54` ASR FireRed; `fireredlid/.../transformer_decoder.py`
- **Status:** fixed
- **Backup:** `Z:\PinelineV2_codebak\2026-11-10_firered-lid-conf\`

## Triệu chứng

Log ASR:
`assert torch.all(t_confidences <= 1.0)` → AssertionError trong LID; `LID: []`.
Job vẫn chạy tiếp (lid.py catch Exception) nhưng spam traceback; slice có thể ra text lỗi encoding (`Õù»…`).

## Root cause

`exp(log_prob)` sau beam + half/bf16/smoothing đôi khi > 1.0 → assert chết batch LID.

## Fix

Clamp `t_confidences` về `[0,1]` thay assert — cả **fireredlid** và **fireredasr2** `transformer_decoder.py`. Sync V2/V4/V5.

## Recheck

1. Chạy tiếp / job ASR mới với FireRed.
2. **Pass nếu:** không còn AssertionError `t_confidences`; LID trả lang hoặc `[]` im lặng không traceback.
3. **Fail nếu:** vẫn assert giữa decode.

## Liên quan

- Job `365baf19df54` lúc sửa: ASR ~46% slice 3/8, không chết job (đã catch).
- Subprocess ASR đang chạy có thể vẫn code cũ đến khi spawn lại.
