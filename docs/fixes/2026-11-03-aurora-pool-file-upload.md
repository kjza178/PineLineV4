# Aurora upload/file-QA bị 401 dù 58 session sống

- **Date:** 2026-11-03
- **Job / khu vực:** `llm.aurora_upload_file` / `chatgpt_chat_with_file` / pronoun analyze mode=file
- **Status:** fixed
- **Backup:** `Z:\PinelineV2_codebak\2026-11-03_aurora-pool-file\`

## Triệu chứng

Pronoun analyze mode `file` báo 401 / invalidated oauth / token expired. UI Aurora vẫn hiện ~59 hồ sơ / ~58 session sống.

## Root cause

`data/chatgpt_token.txt` (JWT ChatGPT free) đã hết hạn (`exp` trước now). Pineline gắn Bearer JWT này vào mọi request → Aurora **không** xoay pool session sống. Chat noauth và `POST /v1/files` noauth qua `http://192.168.31.247:5005` đều 200 khi không gửi token local.

## Evidence

- JWT payload: `exp=1792508391` (đã qua) — email trong token cũ không còn dùng.
- `curl` noauth `POST /v1/files` → `file_0000…` HTTP 200.
- Chat noauth → 200 `"OK"`.
- Sau khi bỏ Bearer hết hạn: upload `(aurora-pool)` + `chatgpt+file/... (pool)` OK ~27s.

## Fix

- `llm._jwt_expired` + bỏ qua `chatgpt_token.txt` hết hạn.
- `aurora_upload_file` / `chatgpt_chat_with_file`: ưu tiên Aurora pool (không Bearer).
- Đổi tên token hết hạn → `data/chatgpt_token.txt.expired` (V2/V4/V5).
- Sync `llm.py` → V2/V5.

## Recheck

1. `python -c "from llm import aurora_upload_file, chatgpt_chat_with_file; ..."` upload SRT nhỏ + chat `input_file`.
2. Log phải có `(aurora-pool)` / `(pool)`, không 401 token_expired.
3. **Pass nếu:** có `file_id` + nội dung trả về (kể cả JSON rỗng cũng OK cho smoke).
4. **Fail nếu:** 401 `token_expired` / `invalidated oauth` khi không set `CHATGPT_FORCE_TOKEN=1`.

## Liên quan

- Aurora `CHATGPT_BASE_URL=http://192.168.31.247:5005/v1`
- Config `PRONOUN_ANALYZE_MODE=file`
- `CHATGPT_FORCE_TOKEN=1` chỉ khi cố ý dùng token local còn hạn

## Follow-up

- **2026-11-03 01:43 — lệch account pool:** `POST /v1/files` Acquire account A; `chat` + `input_file` Acquire account B → model trả «không đọc được file» → `analyze` fallback `mode=fast` (8 lô). Vá Aurora sticky (`UploadedFile.AccountID`, `pool.GetByID`, header `X-Aurora-Account-Id`); Pineline `chatgpt_chat_with_file(base=, account_id=)` + từ chối response UNREAD. Binary: `Z:\aurora\aurora` (backup `aurora.bak_before_sticky`).
- **Recheck sau restart Aurora:** upload SRT full → header có `X-Aurora-Account-Id` → chat cùng host đọc được dialogue ZH (không còn error unread) → log `FILE LOCK` 1 lần, không `analyze 3/8`.
