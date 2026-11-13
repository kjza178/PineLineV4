# Port V2 → V4: luồng dịch `translate_simple` (MẶC ĐỊNH) + Demucs trước ASR

- **Date:** 2026-11-12
- **Job / khu vực:** `translate_simple/` (mới) · `cloud_retry.py` (mới) · `server.py` (`_process_gpu`, `_auto_gpu`, `_run_stage("translate")`, `_translate_flow`, `_queue_park_ready`) · `asr.py` · `separate.py` · `llm.py` (4 dòng) · `install/requirements-optional.txt`
- **Status:** ported (agent F4) — **chờ restart :8804** + chạy test trên Windows
- **Backup:** `Z:\PinelineV4\.backup_edit_20261112_agentF4\` (file gốc giữ đường dẫn tương đối + `_xfer\v4_before.tgz` = ảnh mã nguồn V4 trước port, không secret)

## Triệu chứng / yêu cầu

V2 đã có luồng dịch gọn `translate_simple` (plan ∥ NMT nháp → REVIEW cloud áp cặp xưng hô → kiểm/vá → cổng) và Demucs chạy một lần trước ASR (chia khúc theo khoảng lặng, ghép đúng số mẫu). V4 (cây chạy độc lập trên máy khác) chưa có: dịch vẫn `run_translate` + `run_review`, ASR trên audio gốc (`ASR_USE_DEMUCS` mặc định 0), `separate.py` cũ cắt cứng 3600 s qua FLAC.

## Root cause

V4 là bản port phẳng của V2 trước 2026-11-12; các thay đổi `translate-simple`, `translate-simple-next`, `asr-demucs-default` chỉ làm ở V2.

## Evidence (so sánh từng module V2 ↔ V4, bỏ CRLF)

- `asr.py`, `separate.py` của V4 **trùng md5** bản V2 trước sửa (`.backup_edit_20261112_agentE`) → chép thẳng bản V2 mới.
- `split_parts.py`, `manifest.py`, `series_glossary.py`, `config.py`, `fileio.py`, `hardsub_asr.py`, `ocr.py`, `subs.py`, `media_ts.py`, `context_studio/schema.py`: giống hệt V2.
- `translate.py`: mọi hàm luồng simple dùng (`build_plan`, `_resolve_review_model`, `ensure_hard_terms`, `apply_hard_term_locks`, `heal_obvious_internal_stutter`, `clean_zh_spam`, `normalize_vi_thousands`, `translate_ready_for_tts`, `translate_coverage_gap`, `_ocr_name_hints`, `apply_asr_stutter_heal`) cùng chữ ký. `mt_zh_vi.py` khác V2 chỉ ở `machine.mt_model_dir()` (V4 machine-config) → không đụng.
- `llm.py` V4 = V2 + machine-config, nhưng THIẾU `response=r` trong `HTTPError` và `from last_err` → `cloud_retry` không đọc được mã 429/Retry-After.
- `server.py` V4 đã có B2 (`_REVIEW_RETRY_SEC/MAX`, park `waiting_review`) nhưng KHÔNG có B3 (`_fill_pending_park_on`, `_translate_gate_action`) → bản vá simple áp tay, bỏ phần B3.
- `cloud_retry.py`, `translate_simple/`, `data/lexicon/`, `tools/` không có ở V4.

## Fix

- **Mới (chép nguyên V2):** `translate_simple/*.py` (16 file), `cloud_retry.py`, `data/lexicon/{idioms_zh_vi,pronoun_rules_zh_vi}.json`, `tools/{collect_manual_edits,simple_stats}.py` (chỉ đổi ví dụ `--work` trong docstring sang `work` của V4).
- **`translate_simple/cfg.py`:** `pipeline_mode()` / `pipeline_is_simple()` — **mặc định simple**; `TRANSLATE_PIPELINE=legacy` (cũng nhận `old/off/0/false/no`) = rollback luồng cũ. Cờ con giữ mặc định 0: `SIMPLE_PAIR_RULES`, `SIMPLE_PAIR_FILL`, `SIMPLE_ZH_SOURCE`, `SIMPLE_LEARN_INFERRED`, `SIMPLE_LEXICON_EXCLUDE_GOLDEN`.
- **`server.py`:** `_translate_pipeline_simple()` (gọi `translate_simple.cfg`, fallback env cùng quy ước), `_simple_translate_run`, `_auto_translate_simple` (park `waiting_review` + `simple_park` / HOLD `simple_gate` / done → gỡ park); rẽ nhánh ở `_process_gpu`, `_auto_gpu` (bỏ vá lô + REVIEW-trong-ghế cũ + `run_review` của QA gate khi simple), `_run_stage("translate")`, `_translate_flow` (Dịch lại / Soát lại → `force` / `rereview`), `_queue_park_ready` (park simple chờ `review_retry_at`, không lặp nóng).
- **`asr.py` / `separate.py`:** bản V2 mới — `ASR_USE_DEMUCS` mặc định **1**, Demucs lỗi/OOM/thiếu gói → log + **fallback audio gốc** (ghi `stages.asr.demucs_fallback`), không fail job; ASR đã xong thì không chạy Demucs; `separate.py` chia khúc tại khoảng lặng (`split_parts.find_best_cut_point`) + cắt/ghép theo mẫu (WAV/RF64), env `DEMUCS_CHUNK_SEC`(1800) `DEMUCS_LONG_THRESHOLD_SEC`(2400) `DEMUCS_CHUNK_PAD_SEC`(5) `DEMUCS_CUT_SEARCH_SEC`(60).
- **`llm.py`:** `HTTPError(..., response=r)` ×2 + `raise LLMUnavailable(...) from last_err` ×2 (giữ nguyên machine-config V4).
- **`install/requirements-optional.txt`:** thêm `pypinyin` (tuỳ chọn; chỉ dùng khi `SIMPLE_ZH_SOURCE=1`, thiếu gói vẫn chạy). `test_setup_machine` đòi mọi import bên thứ ba có trong requirements.
- **Tests (chép V2, chỉnh theo V4):** `tests/test_translate_simple*.py` (4 file), `tests/test_separate_demucs_chunks.py`. Chỉnh: test mặc định → simple + test rollback `legacy`; golden/backup không hardcode ổ đĩa (env `TS_GOLDEN_DIR/TS_GOLDEN_WORK/TS_EVAL_SCRIPT/TS_NEXT_BACKUP`, mặc định cây anh em `..\PinelineV6`, `..\PinelineV2`).

## Mặc định & rollback (env hoặc `pineline.config.json`, server đọc khi gọi / sau restart)

| Khoá | Mặc định sau port | Rollback |
|---|---|---|
| `TRANSLATE_PIPELINE` | `simple` (không đặt) | `legacy` |
| `ASR_USE_DEMUCS` | `1` (fallback audio gốc khi lỗi) | `0` |
| `SIMPLE_PAIR_RULES` / `SIMPLE_PAIR_FILL` / `SIMPLE_ZH_SOURCE` / `SIMPLE_LEARN_INFERRED` / `SIMPLE_LEXICON_EXCLUDE_GOLDEN` | `0` | — |

Model REVIEW của simple: `SIMPLE_MODEL` (trống = `REVIEW_MODEL` như luồng cũ). Cổng/đường dẫn: không thêm khoá máy mới — LLM qua `llm.py` + `machine.py` sẵn có.

## Recheck

1. `Z:\PinelineV6\scripts\test_v4_simple_demucs.bat` (hoặc `... full`). Kỳ vọng: (1) 106 test mới, 0 failed; (2) nhóm cũ 74 test = 71 passed + 3 failed có sẵn từ trước port (pronoun_consistency ×1, pronoun_postpass ×2).
2. `python scripts\brain_build.py` + `python scripts\tree_audit.py --peers Z:\PinelineV2 Z:\PinelineV5` (ERROR = 0).
3. Restart :8804 khi queue rảnh. Job thử ngắn: log `[asr] Nguồn ASR = vocals.wav (Demucs)`; dịch có log `[simple] …`, `work/<job>/trace.jsonl` + log `dịch simple qua cổng (done) → tiếp TTS` hoặc `PARK`/`HOLD`.
4. **Pass nếu:** job qua ASR (Demucs hoặc fallback) → simple → TTS; `TRANSLATE_PIPELINE=legacy` trả về đúng luồng cũ.
5. **Fail nếu:** job kẹt `waiting_review` không tự chạy lại sau `QUEUE_REVIEW_RETRY_SEC`; Demucs lỗi làm fail ASR; `legacy` vẫn chạy simple.

## Rủi ro / khác V2

- `agent_autopilot` / `agent_heal` / sidecar gọi thẳng `run_translate` không rẽ nhánh (giống V2).
- V4 không có B3 (`fill_pending`) → nhánh legacy giữ hành vi B2 cũ của V4.
- Demucs mặc định bật: +thời gian GPU mỗi job, cần `demucs` + VRAM; lỗi → fallback.
- Luồng simple gọi cloud (Aurora/GPT) cho plan + review, KHÔNG fallback local → mất cloud = park/HOLD (thiết kế V2).

## Liên quan

- Bản sao docs V2: `docs/design/2026-11-12-translate-simple.md`, `docs/fixes/2026-11-12-translate-simple.md`, `docs/fixes/2026-11-12-translate-simple-next.md`, `docs/fixes/2026-11-12-asr-demucs-default.md`, `docs/reviews/2026-11-12-translate-simple-review.md`, `docs/reviews/2026-11-12-translate-simple-next-review.md`.
