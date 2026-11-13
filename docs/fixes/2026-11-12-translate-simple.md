> **Bản sao từ V2** (`Z:\PinelineV2\docs\fixes\2026-11-12-translate-simple.md`) — tham chiếu cho port V4 2026-11-12 (agent F4, xem `docs/fixes/2026-11-12-port-simple-demucs.md`). Cổng/đường dẫn trong bài là của V2 (:8801); V4 = :8804. Khác biệt V4: mặc định `TRANSLATE_PIPELINE`=simple, rollback `legacy`.

# translate-simple: luồng dịch mới (plan ∥ NMT → review 1 lần/lô → vá câu bị cờ → cổng), sau cờ TRANSLATE_PIPELINE=simple

- **Date:** 2026-11-12
- **Nguồn:** thiết kế chủ dự án duyệt; baseline golden `Z:\PinelineV6\docs\reviews\2026-11-11-translation-baseline.md`, review kiến trúc `Z:\PinelineV6\docs\design\2026-11-11-translate-architecture-review.md`.
- **Khu vực:** `translate_simple/` (mới: `cfg, script_store, plan_view, lexicon, stage_draft, stage_review, post, validate, repair, gate, pipeline`), `data/lexicon/idioms_zh_vi.json` (mới), `server.py` (rẽ nhánh), `tests/test_translate_simple.py` (mới). V6: `scripts/golden_ab.py` (biến thể `simple`), `scripts/test_v2_translate_simple.bat` (mới).
- **Status:** trên đĩa V2 — **mặc định TẮT** (không đặt `TRANSLATE_PIPELINE` = luồng cũ y nguyên, có test chứng minh). Bật = `TRANSLATE_PIPELINE=simple` **sau restart :8801**.
- **Backup:** `Z:\PinelineV2\.backup_edit_20261112_simple\` (`server.py`, `docs/CHANGELOG.md`, `docs/STATE.md`, `docs/worklog/2026-11-12.md`, `docs/fixes/README.md`); V6: `Z:\PinelineV6\.backup_edit_20261112_simple\scripts\golden_ab.py`.
- **Thiết kế:** `docs/design/2026-11-12-translate-simple.md` (khối, cấu hình, so sánh luồng cũ, prompt mẫu trên golden 32da3d8f225b).

## Triệu chứng

Xưng hô đúng 47 % trên golden dù plan có ĐÚNG cặp; câu trống có 3 đường vá chồng nhau; 6 cơ chế xưng hô đá nhau (NMT mù plan, mask đại từ ở REVIEW, lọc fix cosmetic, regex mixed ép tôi–cậu, pronoun-QA, register policy). Không đo được câu nào REVIEW đã thật sự xem (REVIEW chỉ trả fix).

## Nguyên nhân

Kiến trúc: quyết định xưng hô rải ở nhiều lớp, lớp sau không biết lớp trước; LLM duy nhất có ngữ cảnh lại bị cấm đổi đại từ.

## Sửa

Package mới `translate_simple/` (6 bước, xem thiết kế). Quyết định đáng chú ý:
1. **REVIEW trả ĐỦ mọi câu** `{i, vi, spk, to, conf}`; parse chặt; câu không trả hợp lệ → không rv (cổng park).
2. **Hậu kỳ chỉ còn** chuẩn số + khoá thuật ngữ type=lock. Không regex đại từ, không pronoun-QA, không pass1.
3. **Bộ kiểm** (port bộ trích đại từ của `eval_translation.py`) chỉ đánh cờ; vá đúng câu bị cờ, ≤2 lượt.
4. **Một chính sách retry**: `cloud_retry.call_with_cloud_retry`; **không fallback local / switch_preset** (kể cả `REVIEW_LOCAL_FALLBACK=1`) — lỗi → park B2. Lý do: thiết kế mục 5.
5. **Plan ∥ NMT**: NMT chọn flavor base/QT theo glossary cũ / bảng bộ / base (plan tập mới chưa có); `SIMPLE_NMT_WAIT_PLAN=1` để tuần tự.
6. `server.py`: `_translate_pipeline_simple`, `_simple_translate_run`, `_auto_translate_simple` (mới); `_auto_gpu` (nhánh simple thay run_translate + vá miss/gap + khối unrev; QA gate không chạy run_review cũ lần 2), `_process_gpu`, `_run_stage("translate")`, `_translate_flow` rẽ nhánh; `_queue_park_ready` thêm điều kiện `simple_park` (chờ tới hạn, không lặp nóng). Nhánh mặc định không đổi dòng logic nào (chỉ thụt lề `try: run_translate` vào `else`).
7. `trace.jsonl` trong work dir: mọi lần đổi vi (bước/i/cũ→mới/lý do), lô lỗi, cờ hết, cổng.

## Recheck

**Đã chạy ở cloud** (Python 3.13 + pytest, stub fastapi `/home/claude/stubs` như các đợt trước; không mạng/LLM/GPU; cây V2 tar ngày 12/11, md5 `translate.py` 73cddc6a…, `server.py` 262ab046… khớp đĩa):
- `tests/test_translate_simple.py`: **26 ca — 26 pass** khi có golden + work (đặt `TS_GOLDEN_DIR/TS_GOLDEN_WORK/TS_EVAL_SCRIPT`), 25 pass + 1 skip khi không có. Pass: script_store giữ manual + trường lạ + post-split; plan∥NMT chạy SONG SONG thật (2 Event chờ chéo); NMT tắt/lỗi → nháp rỗng; review áp cặp plan (Lâm→Tô anh/em), câu trống dịch trong cùng lô (`dich=true`), gợi ý 我去 (CẤM «tôi đi»); manual không đổi; parse chặt (rỗng/cụt/fence/thiếu lines → không rv + park); trả thiếu câu → chỉ câu trả mới rv; 429×2 rồi OK → done; 429 mãi → park, không local; validate bắt «tôi…cậu» khi plan anh/em (conf 0.9), bỏ qua conf 0.3, ngôi 3/«chúng ta» không tính; repair chỉ gửi câu bị cờ, đúng 2 lượt; cổng done/park/hold; trace; lô 30/30/10 + ngữ cảnh ±4; **server mặc định gọi run_translate (luồng cũ), simple gọi pipeline.run** + park/hold/done stamp + `_queue_park_ready`; `_translate_flow` rẽ nhánh; **switch_preset không bao giờ bị gọi** (fixture kiểm mọi ca).
- Đầu-cuối trên cửa sổ golden 32da3d8f225b (164 câu, LLM giả «echo nháp», nháp = vi hiện có): ghi script/srt/trace/manifest, `eval_translation` chấm được: pron_acc 0,24 · idiom 0,875 · chrF 67,05 · unaligned 0 — **trùng baseline của job** (đúng kỳ vọng với echo → chứng minh đường ghi/chấm không làm hỏng dữ liệu).
- Nhóm test dịch cũ (b1, b1_scenarios, b2, b2_review, b3, review_fail_not_rv, park_review_retry, review_parallel_workers, optimize_b5_b6, review_batches, pronoun_postpass, pronoun_consistency, translate_missing, review_pass1_upload, pronoun_qa_slim_plan): **trước 246 pass / 3 fail / 5 skip — sau 246 / 3 / 5**, cùng 3 fail có sẵn (`test_pronoun_postpass::test_modernish_mixed`, `::test_detox_nguoi_ta`, `test_pronoun_consistency::test_filter_review_fixes_when_locked` — đã ghi ở fix b3).
- Toàn bộ `tests/` (`--continue-on-collection-errors`): trước 362 pass / 11 fail / 5 skip / 6 lỗi thu thập (môi trường cloud) → sau 387 / 11 / 6 / 6, cùng danh sách fail.
- `golden_ab.py --dry-run --variants simple,base`: OK; chạy thật `run_variant(...,'simple')` với `llm.chat` giả (sitecustomize, không NMT) trên job tạm cloud: tiến trình con gọi `translate_simple.pipeline.run`, ghi `golden_ab_result.json`, `score()` chấm được (cổng park vì không NMT + echo còn chữ Hán — đúng hành vi).

**Chỉ kiểm được trên Windows / chạy thật:** `Z:\PinelineV6\scripts\test_v2_translate_simple.bat` (fastapi thật); chất lượng thật (model có trả đủ 30 câu/lô, spk/to/conf), điểm golden A/B (`golden_ab.py --variants base,simple`), thời gian/token, NMT ∥ plan upload trên GPU thật.

Pass (cloud) · Windows: chờ chạy bat.

## Review độc lập 2026-11-12 (simple_review)

Chi tiết: `docs/reviews/2026-11-12-translate-simple-review.md`. Backup trước sửa: `Z:\PinelineV2\.backup_edit_20261112_simple_review\` (+ `Z:\PinelineV6\.backup_edit_20261112_simple_review\scripts\test_v2_translate_simple.bat`).

**Triệu chứng / Nguyên nhân / Sửa** (đã sửa, có test):
- H1 bảng bộ không học tập mới: `save_from` chạy trước khi ghi `glossary.json`, không save khi xong → `stage_draft` ghi plan trước `save_from`; `pipeline` cổng done → `save_from`.
- H2 lexicon `我去` CẤM «tôi đi» cho mọi câu chứa chuỗi (我去一趟/我去上个洗手间 bị ép sai) → trường `re` (regex từng câu ZH) cho `我去`, `大爷的`.
- M1 dòng cặp mơ hồ («tôi / anh / ngươi») + ghi chú cặp không vào prompt → `tự xưng «x» hoặc «y» · gọi «z» (ghi chú)`, bỏ dạng chữ Hán.
- M2 thiếu `conf` → bộ kiểm bỏ đại từ im lặng → `s_conf=null` vẫn kiểm. M3 `i` trùng vi khác → bỏ (thử lại). M4 `script.json` hỏng → sao lưu `script.corrupt.<ts>.json` trước khi dựng lại.
- L1 `s_name_ok` reset khi vi mới/force. L2 `trace.jsonl` xoay ở `SIMPLE_TRACE_MAX_MB` (8). L3 lexicon: 嘲讽 bỏ CẤM «nhạo báng», 君无戏言 + «quân vô hí ngôn», 做鬼也不会放过 (mới), ghi chú 好大力气/脚盆/大爷的 — 52 mục.
- Mới: đề xuất cặp xưng hô thiếu → `plan_suggestions.json` (`new_pairs` của REVIEW + `missing_pairs` tất định), KHÔNG chèn plan/bảng bộ; tắt `SIMPLE_SUGGEST_PAIRS=0`.
- V6: `scripts/golden_ab_simple.bat` (mới), `scripts/test_v2_translate_simple.bat` thêm `tests\test_translate_simple_scenarios.py`.

**md5 sau ghi:** `translate_simple/cfg.py` 5832f4fd… · `lexicon.py` bbb346a9… · `pipeline.py` 73c13600… · `plan_view.py` 88fcf2b4… · `script_store.py` a6df4efb… · `stage_draft.py` 06de0699… · `stage_review.py` 95c988a3… · `suggest.py` (mới) f3290521… · `validate.py` 1d89c2f2… · `data/lexicon/idioms_zh_vi.json` 600a910f… · `tests/test_translate_simple.py` 4dca23eb… · `tests/test_translate_simple_scenarios.py` (mới) eca344a0… · V6 `scripts/golden_ab_simple.bat` (mới) af1c4e2d… · `scripts/test_v2_translate_simple.bat` 0c763dde…. `server.py` KHÔNG đổi (79997d62…).

**Recheck (cloud, số thật):** simple 26 → 45 pass (19 ca mới; trên module cũ 12/19 fail); nhóm dịch cũ 246/3/5 trước = sau; toàn bộ `tests/` 388 → 407 pass, cùng 11 fail + 6 lỗi collect môi trường; harness luồng mặc định server.py mới vs backup: 21 kịch bản trùng từng byte; golden e2e echo không đổi; `golden_ab.py --dry-run` (3 / 16 lượt) và chạy biến thể simple với LLM echo qua tiến trình con: OK. **Chỉ Windows:** `test_v2_translate_simple.bat` (kỳ vọng 45 pass), A/B thật (`golden_ab_simple.bat`).

Pass (cloud) · Windows: chờ chạy bat.
