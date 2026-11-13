> **Bản sao từ V2** (`Z:\PinelineV2\docs\reviews\2026-11-12-translate-simple-review.md`) — tham chiếu cho port V4 2026-11-12 (agent F4, xem `docs/fixes/2026-11-12-port-simple-demucs.md`). Cổng/đường dẫn trong bài là của V2 (:8801); V4 = :8804. Khác biệt V4: mặc định `TRANSLATE_PIPELINE`=simple, rollback `legacy`.

# Review độc lập + test kịch bản — luồng dịch simple (`translate_simple/`)

- **Date:** 2026-11-12
- **Đối tượng:** `translate_simple/` (12 module), `data/lexicon/idioms_zh_vi.json`, rẽ nhánh `server.py`, `tests/test_translate_simple.py`, biến thể `simple` trong `Z:\PinelineV6\scripts\golden_ab.py`. Thiết kế `docs/design/2026-11-12-translate-simple.md`, fix log `docs/fixes/2026-11-12-translate-simple.md`, backup trước simple `.backup_edit_20261112_simple\`.
- **Cách làm:** tar MỚI của V2 (md5 khớp đĩa: `server.py` 79997d62…, `stage_review.py` 65d62752…, `pipeline.py` 4d5b5a89…) → cây cloud; diff `server.py` với backup; đọc từng module; viết 19 ca kịch bản mới + harness đối chiếu hành vi luồng mặc định. Không HTTP :8801/:8802/:8000/:8083/:3377, không LLM/GPU thật, không git. Stub fastapi/yt_dlp NGOÀI cây V2 (chỉ để import `server.py`).
- **Backup đợt review:** `Z:\PinelineV2\.backup_edit_20261112_simple_review\` (mọi file V2 bị đổi) + `Z:\PinelineV6\.backup_edit_20261112_simple_review\scripts\test_v2_translate_simple.bat`.

## Kết luận

**Sẵn sàng A/B: CÓ** (sau khi ghi bản sửa review này), với điều kiện:
1. Chạy khi V2 RẢNH (hàng đợi :8801 trống) — A/B dùng GPU NMT + GPT thật, tốn quota.
2. Trước đó chạy `Z:\PinelineV6\scripts\test_v2_translate_simple.bat` trên Windows → kỳ vọng simple **45 pass / 0 fail**, nhóm dịch cũ 3 fail có sẵn.
3. A/B **không cần restart :8801** (golden_ab chạy code V2 trong tiến trình con riêng, job tạm ở `D:\PinelineV6_work\golden_ab`). Bật simple cho production (`TRANSLATE_PIPELINE=simple` + restart) CHỈ sau khi A/B cho số tốt.
4. Đọc `golden_ab_result.json` của biến thể simple: `simple.status` = park/hold nghĩa là cổng chưa qua (vẫn chấm được, nhưng ghi chú khi so).

**Nhánh mặc định (không đặt `TRANSLATE_PIPELINE`) giữ nguyên hành vi** — chứng minh bằng harness: 10 kịch bản `_auto_gpu` giả (đủ câu; thiếu câu → review_fill / vá lô; còn câu chưa rv → REVIEW xong / REVIEW hỏng → park B2 / quá số lượt → review_failed; gỡ waiting_review; run_translate «stopped» / lỗi; hold_after_translate) + 6 ca `_queue_park_ready` + 3 ca `_translate_flow` + 2 ca `_process_gpu`, chạy ở 2 tiến trình (server.py mới vs backup): **vết JSON (chuỗi gọi hàm + agent/stages.translate cuối) trùng từng byte**. Diff tay: nhánh cũ chỉ bị thụt lề vào `else`, thêm `and not _simple` (False khi tắt) và `and not agent.get("simple_park")` (khoá chỉ nhánh simple ghi).

## Phát hiện

### Cao — ĐÃ SỬA

| # | Lỗi | Hậu quả | Sửa | Test |
|---|---|---|---|---|
| H1 | `stage_draft.build_plan` gọi `series_glossary.save_from` **trước** khi ghi `glossary.json` (save_from đọc file đó) và luồng simple **không bao giờ** save_from khi soát xong (luồng cũ có ở cuối `run_review`). | Tập mới không vào bảng bộ → **tập sau không thừa kế** nhân vật/cặp xưng hô của tập trước (nhiều tập liên tiếp mất nhất quán — đúng điểm yếu xưng hô simple muốn sửa). | Ghi plan vừa lập trước `save_from` (như `run_translate`); cổng `done` → `save_from(reason="hoàn thành rà soát (simple)")`. | `test_consecutive_episodes_share_series_table`, `test_series_learns_plan_even_when_review_parks` (fail trên bản cũ) |
| H2 | Lexicon `我去` gợi ý «vãi… (CẤM «tôi đi»)» cho **mọi** câu chứa chuỗi `我去` (dò chuỗi con). | 4 job golden có 31 câu chứa `我去`, chỉ ~10 là thán từ; `我去一趟` (golden: «Tôi đi một chuyến»), `我去上个洗手间`, `明天我去总部观战` bị ép bỏ nghĩa «đi». Tương tự `大爷的` khớp `王大爷的房子`. | Trường `re` (regex áp TỪNG câu ZH) trong lexicon; `我去` = `^\W*我去(?:\W|$)` (đứng riêng/đầu câu + dấu), `大爷的` = `(?:^\W*|你|去你)大爷的`. Regex hỏng → bỏ mục. Nay 10/31 câu được gợi ý. | `test_lexicon_context_regex_woqu`, `test_lexicon_bad_regex_entry_skipped` |

### Trung bình — ĐÃ SỬA

| # | Lỗi | Sửa | Test |
|---|---|---|---|
| M1 | Dòng cặp trong prompt `A → B: {self...} / {call...}` mơ hồ khi self/call nhiều dạng — plan thật: «Trần Phong → Cung Bản Nhất Lang: tôi / anh / ngươi», «Ân Thiên Tuyệt → đệ tử: bản tọa / vi sư / các ngươi / đồ nhi / 徒儿». Ghi chú cặp (vd «Luôn gọi Cố Thanh là học trưởng hoặc anh», «Không chuyển sang cô-em…») không vào prompt. | `A → B: tự xưng «x» hoặc «y» · gọi «z» (ghi chú ≤100 ký tự)`; bỏ dạng chữ Hán khỏi forms. | `test_pair_line_unambiguous_with_note_and_no_cjk` (+ helper FakeLLM cập nhật) |
| M2 | Model không trả `conf` (hoặc trả chữ) → conf=0 → bộ kiểm **bỏ qua đại từ im lặng** cho mọi câu. | `conf` thiếu/hỏng → `s_conf=null`; validate coi như đạt ngưỡng (vẫn kiểm nếu spk/to khớp cặp). Hàng luồng cũ (không có `s_conf`) vẫn bỏ qua. | `test_missing_conf_still_checked_by_validator`, `test_validate_conf_semantics` |
| M3 | `i` trả trùng với `vi` khác nhau → bản sau đè im lặng, vẫn rv. | Trùng-khác → bỏ i đó (không rv → lượt thử lại lô ½); trùng y hệt → nhận. | `test_duplicate_i_conflict_not_rv_then_retried` |
| M4 | `script.json` hỏng (không parse) → `load()` trả [] → dựng lại từ ASR và **ghi đè** (mất câu `manual` không dấu vết). | Chép `script.corrupt.<ts>.json` trước khi dựng lại (không chép được → ném lỗi, không ghi đè); trace ghi lại. | `test_corrupt_script_backed_up_before_rebuild` |

### Thấp — ĐÃ SỬA

- L1 `s_name_ok` (model xác nhận tên/danh xưng) giữ qua `vi` mới và qua `force` → cờ tên bị nuốt. Nay xoá khi câu được trả không có `ok`, và khi force. Test `test_name_ok_reset_when_vi_changes`.
- L2 `trace.jsonl` chỉ append, không giới hạn (mỗi lượt park ghi ≥2 dòng/câu khi cloud hỏng). Nay `SIMPLE_TRACE_MAX_MB` (8) → xoay `trace.1.jsonl` (≤2 file). Test `test_trace_rotates`.
- L3 Lexicon (chuyên môn ZH→VI): `嘲讽` CẤM «nhạo báng» trái luật `translate.py` («KHÔNG *mặc định*» — vẫn đúng khi thật sự chế giễu) → bỏ forbid, ghi chú; `君无戏言` thêm «quân vô hí ngôn / vua không nói đùa» (golden chấp nhận); `好大力气` ghi chú nghĩa khen sức («khỏe thật») khi đứng riêng; `脚盆` ghi chú nghĩa đen; `分分钟` thêm «trong một nốt nhạc / chớp mắt»; `见义勇为` thêm «thấy chuyện bất bình ra tay»; thêm `做鬼也不会放过` (biến thể 也 hay gặp hơn 都). 45 mục còn lại đúng nghĩa, giữ nguyên (`逆天而行` = «Nghịch Thiên Nhi Hành» khớp seed type=lock của `translate.py`). Tổng 52 mục.

### Đề xuất của chủ dự án — ĐÃ LÀM (an toàn, kiểm được)

**Cặp xưng hô thiếu trong plan** (vd golden 32da3d8f225b: Hà Hải Khôn→Mị Nương không có cặp): REVIEW được hướng dẫn ghi cặp mới vào khoá tuỳ chọn `"new_pairs"` (tự xưng/cách gọi đã dùng, ≤5/lô); `suggest.py` gộp (chuẩn hoá tên theo plan, bỏ cặp đã có / tự-với-tự / rác) + thống kê tất định `missing_pairs` (câu rv, conf ≥ 0,7, cả spk và to là nhân vật trong plan nhưng không có cặp) → `work_dir/plan_suggestions.json` (cộng dồn qua các lần chạy). **KHÔNG chèn vào `glossary.json` / bảng bộ** — người duyệt chép vào `pronouns` nếu đúng. Parse lỏng: `new_pairs` hỏng không ảnh hưởng rv. Tắt: `SIMPLE_SUGGEST_PAIRS=0`. Test `test_unknown_pair_suggestions_written_not_inserted` (tên không có trong plan như «Ông chủ quán» → không đề xuất, không cờ), `test_suggest_off_by_config`.

### CHƯA sửa — ghi nhận / đề xuất

- **N1 Token ra** (trả đủ mọi câu): lô 30 × ~60–80 token ≈ 2–2,5k < `SIMPLE_MAX_TOKENS` 8192 → khả thi. Có thể giảm 40–60 % token ra bằng sentinel `"vi":"="` cho câu giữ nguyên nháp (vẫn trả `i/spk/to/conf` mọi câu để giữ bằng chứng «đã xem»). Đổi parse/rv → **chỉ đề xuất**, làm khi A/B cho thấy token là vấn đề. Prompt vào tăng ~30 token/cặp do ghi chú (≤24 cặp ≈ +800 token/lô).
- **N2 Lệch số i** (model trả đúng tập i nhưng đặt vi lệch 1 câu) không phát hiện được. Nếu A/B thấy: thêm trường `zh4` (4 ký tự đầu zh) vào mỗi dòng trả và đối chiếu. Đổi schema → đề xuất.
- **N3** Plan file-mode lỗi → sample-mode dùng `LLM_MODEL` (cấu hình hiện tại `ollama/gemma4:31b-cloud` máy LAN — không phải llama GPU local, không switch preset). «Không fallback local» đúng với GPU/preset.
- **N4** `stop_check` không chạy trong plan (đến `PLAN_FILE_TIMEOUT` 900 s) và NMT — như luồng cũ; dừng có hiệu lực ngay sau plan ∥ NMT và giữa các lô review (đã test).
- **N5** Người sửa tay trên UI **trong lúc** simple đang review có thể bị ghi đè (store giữ rows trong RAM) — giống luồng cũ. Đề xuất: trước mỗi `save()` đọc lại câu `manual` từ đĩa và giữ.
- **N6** Tắt simple khi job đang park simple: `simple_park` còn → job chờ tới hạn `review_retry_at` rồi chạy luồng cũ (không kẹt, không lặp nóng). Có thể dọn khoá ở nhánh cũ sau.
- **N7** Sau cổng `done`, `_auto_gpu` vẫn chạy Second Brain (`scan_and_heal_job` — heal thành ngữ tất định, không đổi đại từ) + QA gate (snapshot/diff, `run_review` cũ bị bỏ qua) — chấp nhận. golden_ab không chạy 2 bước này → A/B đo đúng phần dịch.
- **N8** Cặp plan có `to` chung chung («đồng đội», «bố mẹ», «chung») không khớp spk/to model → không kiểm được; cờ `name` có thể báo nhầm khi zh có tên đầy đủ nhưng VI gọi danh xưng («Hà đội») — repair cho `ok:true`; tính vào ngưỡng hold 3 %.

## Đánh giá khác (không lỗi)

- **Race:** NMT dùng bản chụp rows, ghi store sau khi 2 thread join → không race plan ∥ NMT. 8 lô: `apply_result` + `save` trong lock; prompt đọc rows không khoá (chuỗi bất biến) → ngữ cảnh có thể là nháp hoặc bản đã soát tuỳ thời điểm (không xác định nhưng không hỏng). `progress` → `Manifest.update` chỉ ở thread chính. Vá tuần tự. 6 lần lặp toàn bộ test simple: ổn định.
- **rv chỉ khi hợp lệ:** đúng (parse chặt; câu thiếu/i lạ/i ngữ cảnh không rv; manual rv nhưng vi không đổi).
- **Resume:** câu đã rv không gửi lại; NMT chỉ câu chưa có vi; trường lạ giữ (test).
- **Cổng park/hold không lặp nóng:** `simple_park` → `_queue_park_ready` chờ `review_retry_at`; quá `QUEUE_REVIEW_RETRY_MAX` → `review_failed` + HOLD.
- **429 kéo dài:** 32 câu / 8 lô / 8 worker / `REVIEW_CLOUD_RETRY=6`: 34 lần gọi, chờ ~1 178 s (đồng hồ ảo, = ngân sách chung), park, không local / switch_preset. Dừng trong lúc chờ 429 → thoát ≤3 lần gọi.
- **Manifest:** mọi ghi qua `Manifest.update` (pipeline + `_auto_translate_simple`).
- **Prompt review (mục 8 thiết kế):** đủ rõ để GPT áp cặp (thứ tự ưu tiên nghĩa → xưng hô → tên → thành ngữ → văn phong; «nháp đúng thì GIỮ»; `khoa=true` trả y nguyên). Sau sửa M1 cặp không còn mơ hồ. JSON schema khả thi cho lô 30 (đã có `json_mode`).
- **Validate:** bộ trích đại từ = bản gọn `eval_translation.py` (khớp cụm dài nhất, loại ngôi 3/danh từ/danh xưng+Tên); ngưỡng conf 0,7 hợp lý.

## Kết quả test (cloud, số thật)

| Bộ | Trước (đĩa) | Sau (review) |
|---|---|---|
| `tests/test_translate_simple.py` (có golden) | 26 pass | 26 pass (2 dòng helper/assert đổi theo định dạng cặp mới) |
| `tests/test_translate_simple_scenarios.py` (19 ca MỚI) | — (chạy trên module cũ: **12 fail** / 7 pass) | **19 pass** |
| Nhóm dịch/review/pronoun (15 file: b3, b2, b2_review, b1, b1_scenarios, review_fail_not_rv, park_review_retry, review_parallel_workers, optimize_b5_b6, review_batches, pronoun_postpass, pronoun_consistency, translate_missing, review_pass1_upload, pronoun_qa_slim_plan) | 246 pass / 3 fail / 5 skip | 246 pass / 3 fail / 5 skip |
| Toàn bộ `tests/` (`--continue-on-collection-errors`) | 388 pass / 11 fail / 5 skip / 6 lỗi collect | 407 pass / 11 fail / 5 skip / 6 lỗi collect — **cùng danh sách fail** |
| Harness đối chiếu luồng mặc định (server.py mới vs backup) | — | vết trùng từng byte (21 kịch bản) |
| Đầu-cuối golden 32da3d8f225b (LLM echo) | pron 0,24 · idiom 0,875 · chrF 67,05 · unaligned 0 | y hệt |
| `golden_ab.py --dry-run` bộ thử nhỏ / full | — | 3 lượt / 16 lượt, không ghi gì |
| `golden_ab.py --variants simple --yes` với LLM echo (tiến trình con thật) | — | OK, ghi script/trace/plan_suggestions, chấm được (park do không NMT — đúng) |

3 fail có sẵn nhóm dịch: `test_pronoun_postpass::test_modernish_mixed`, `::test_detox_nguoi_ta`, `test_pronoun_consistency::test_filter_review_fixes_when_locked`. Fail/lỗi còn lại của toàn bộ = môi trường cloud (sfx_lib ×3, restart_guard ×2, asr_demucs, chatgpt_route ×2; collect ×6). Lệnh: `AGENT_BRAIN=0 PYTHONPATH=<stub> SMOKE_MISSING=yt_dlp,soundfile python3 -m pytest -q -p no:cacheprovider <file>` (+ `TS_GOLDEN_DIR/TS_GOLDEN_WORK/TS_EVAL_SCRIPT` cho ca golden).

## Chạy A/B (Windows, khi V2 rảnh)

```
Z:\PinelineV6\scripts\golden_ab_simple.bat dry        (xem kế hoạch, không chạy)
Z:\PinelineV6\scripts\golden_ab_simple.bat            (thử nhỏ: 32da3d8f225b × base,regex_mask_off,simple)
Z:\PinelineV6\scripts\golden_ab_simple.bat full       (4 job × base,regex_mask_off,nmt_hint_regex_mask_off,simple)
Z:\PinelineV6\scripts\golden_ab_simple.bat score      (chấm lại, không LLM)   / score full
```
In cảnh báo → `pause` (Ctrl+C để huỷ) → tự `--yes`. Kết quả `Z:\PinelineV6\docs\reviews\2026-11-12-golden-ab-simple-try.md` / `2026-11-12-golden-ab-simple.md`. Job tạm đã có kết quả bị BỎ QUA (không đốt lại quota) — muốn chạy lại: `python scripts\golden_ab.py --variants ... --jobs ... --force --yes`.

## File đổi (V2)

`translate_simple/{cfg, lexicon, pipeline, plan_view, script_store, stage_draft, stage_review, validate}.py`, **mới** `translate_simple/suggest.py`, `data/lexicon/idioms_zh_vi.json`, `tests/test_translate_simple.py` (helper), **mới** `tests/test_translate_simple_scenarios.py`, docs (review này, fix log, CHANGELOG, STATE, worklog, ghi chú ở thiết kế §8). `server.py` **không đổi**. V6: **mới** `scripts/golden_ab_simple.bat`, `scripts/test_v2_translate_simple.bat` (thêm file test). md5: xem fix log mục «Review độc lập».
