> **Bản sao từ V2** (`Z:\PinelineV2\docs\fixes\2026-11-12-translate-simple-next.md`) — tham chiếu cho port V4 2026-11-12 (agent F4, xem `docs/fixes/2026-11-12-port-simple-demucs.md`). Cổng/đường dẫn trong bài là của V2 (:8801); V4 = :8804. Khác biệt V4: mặc định `TRANSLATE_PIPELINE`=simple, rollback `legacy`.

# translate-simple «next»: lexicon src · bảng quy tắc xưng hô · bổ sung cặp thiếu · học lại · nguồn ZH · gỡ lặp ASR

- **Date:** 2026-11-12 (~khuya) — agent B (builder).
- **Nguồn:** chủ dự án (bước 0/2/6/8/1 + A/B), thiết kế V6 `docs/design/2026-11-11-translation-quality.md` (M1, M3, M7), A/B `Z:\PinelineV6\docs\reviews\2026-11-12-golden-ab-simple.md` (simple thắng, xưng hô 92 %); bổ sung của agent A (lỗi gỡ lặp ASR f0834acf0cc0 i=542, quan sát đổi cặp theo cảnh 32da).
- **Khu vực:** `translate_simple/{cfg, lexicon, pipeline, plan_view, post, suggest}.py`; **mới** `translate_simple/{pair_rules, pair_fill, zh_source}.py`, `data/lexicon/pronoun_rules_zh_vi.json`, `tools/collect_manual_edits.py`, `tools/simple_stats.py`, `tests/test_translate_simple_next.py`; `data/lexicon/idioms_zh_vi.json` (thêm `src`). V6: `scripts/golden_ab.py` (4 biến thể), `scripts/golden_ab_simple.bat` (chế độ `next`), `scripts/test_v2_translate_simple.bat` (thêm file test).
- **KHÔNG đổi:** `server.py`, `translate.py`, luồng cũ (`run_translate` + `run_review`), config.
- **Status:** trên đĩa V2 — chỉ có hiệu lực với job chạy `TRANSLATE_PIPELINE=simple` **sau restart :8801** (golden_ab chạy tiến trình con riêng, không cần restart). Mọi tính năng mới SAU CỜ, MẶC ĐỊNH TẮT; riêng gỡ lặp ASR là sửa lỗi của luồng simple (không cờ).
- **Backup:** `Z:\PinelineV2\.backup_edit_20261112_agentB\` (`translate_simple/{cfg,lexicon,pipeline,plan_view,post,suggest}.py`, `data/lexicon/idioms_zh_vi.json`, `docs/{CHANGELOG.md,STATE.md,worklog/2026-11-12.md,fixes/README.md}`); V6: `Z:\PinelineV6\.backup_edit_20261112_agentB\scripts\`.

## Cờ

| Cờ | Mặc định | Tác dụng khi bật |
|---|---|---|
| `SIMPLE_LEXICON_EXCLUDE_GOLDEN` | 0 | Bỏ mục lexicon `src=golden_derived` khỏi gợi ý (đo A/B trung thực — biến thể `simple_noleak`). |
| `SIMPLE_PAIR_RULES` | 0 | Sau plan: điền cặp xưng hô CÒN TRỐNG theo `data/lexicon/pronoun_rules_zh_vi.json` (src `rule`). |
| `SIMPLE_PAIR_FILL` | 0 | Sau review lượt 1: 1 lần gọi model bổ sung cặp thiếu (src `llm_fill`). |
| `SIMPLE_PAIR_FILL_MIN` / `_MODEL` / `_CONF` | 3 / (model REVIEW) / 0.6 | Số câu tối thiểu của cặp · model «mini» · conf tối thiểu nhận cặp. |
| `SIMPLE_LEARN_INFERRED` | 0 | Cổng done → cặp `rule`/`llm_fill` ghi vào `glossary.json` (rồi `series_glossary.save_from` → bảng bộ). |
| `SIMPLE_ZH_SOURCE` | 0 | Chọn nguồn ZH: phát hiện hardsub → OCR thắng ASR khi khớp (ASR giữ timing) + sửa tên gần đúng. |
| `SIMPLE_ZH_HS_SAMPLES` / `_HS_MIN_RATIO` | 24 / 0.3 | Số khung mẫu đều theo phim · tỉ lệ khung có chữ ở dải thoại để coi là hardsub. |
| `SIMPLE_ZH_NAMEFIX` / `_NAMEFIX_MIN` | 1 / 0.75 | (chỉ khi `SIMPLE_ZH_SOURCE=1`) sửa tên · điểm giống tối thiểu. |

Đặt bằng env hoặc `Z:\PinelineV2\pineline.config.json` (config.get: env > file > mặc định).

## Bước 0 — lexicon `src` (đo trung thực)

`idioms_zh_vi.json` mỗi mục có `src`: **14 `translate_rules`** (zh có thật trong luật `translate.py` — có từ 11-09, trước golden: 没大没小, 脑子进水, 吃醋, 打天下, 先下手为强, 穷酸, 眼馋, 好大力气, 废什么话, 嘲讽, 分手补偿, 脆皮, 运动员, 逆天而行), **38 `golden_derived`** (mọi mục KHÔNG có trong translate.py — ghi chú seed nói «+ lỗi golden V6»; không chứng minh được nguồn độc lập nên xếp an toàn vào golden_derived, kể cả biến thể ASR 手下留情/一盆黄土 và 做鬼也不会放过 thêm ở review), **0 `expert`** (dành cho mục mới thêm KHÔNG nhìn golden). Mục thiếu `src` được coi là golden_derived. Test khoá quy tắc: `src == translate_rules` ⇔ zh có trong translate.py. Thuật ngữ idiom của plan không bị loại.

## Bước 2 — bảng quy tắc xưng hô theo quan hệ

`data/lexicon/pronoun_rules_zh_vi.json` (viết tay theo quy ước lồng tiếng Việt, KHÔNG seed từ golden): 15 quan hệ — vợ↔chồng, người yêu, cha/mẹ↔con, ông bà↔cháu, anh/chị↔em ruột, sư phụ↔đồ đệ, sư huynh/tỷ↔sư đệ/muội, vua↔thần, chủ↔tớ, thầy/cô↔trò, sếp↔nhân viên, đàn anh/chị↔đàn em, tiền bối↔vãn bối (tuổi/địa vị), bạn bè ngang hàng, kẻ thù. Mỗi quan hệ: từ khoá VI+ZH (`pair_kw` hai chiều, `hi_kw`/`lo_kw` vai trên/dưới), dạng tự xưng/gọi theo thể loại `modern|ancient|xianxia` và theo giới người nói/người nghe. Phim `mixed` = hợp dạng modern + xianxia/ancient (nhận nhiều dạng → ít cờ sai).

`translate_simple/pair_rules.py`: quan hệ A↔B đọc từ `relationship_matrix` (lồng `{A:{B:"…"}}` hoặc phẳng `"A—B"`; vế đầu = A: «Anh trai và em gái ruột» ⇒ A anh) và `role`/`relation` («Em gái ruột của Lâm Phàm», «林凡的妹妹»). Từ khoá hai chiều (vợ chồng…) được che trước khi tìm vai (không đọc nhầm «vợ» trong «vợ chồng»). **Không đoán** khi mơ hồ: chỉ một vai không kèm «của <tên>» («Sư phụ»), anh em ruột không rõ ai lớn, người yêu/vợ chồng thiếu giới. **Chỉ điền cặp trống** (`PlanView.add_pair` không bao giờ đè cặp plan), src `rule`, ghi chú «suy theo quan hệ … — quy tắc» hiện trong prompt; KHÔNG ghi `glossary.json`. Cặp suy luận ghi `work_dir/plan_inferred.json` + `plan_suggestions.json` (khoá `inferred_pairs`).

## Bước 6 — bổ sung cặp thiếu (`pair_fill.py`)

Sau review lượt 1, trước hậu kỳ/kiểm: cặp spk→to (cả hai là nhân vật plan, chưa có cặp kể cả sau bước 2, câu rv conf ≥ `SIMPLE_CONF_MIN`) có ≥ `SIMPLE_PAIR_FILL_MIN` câu (tối đa 8 cặp) → **1 lần gọi** model (`SIMPLE_PAIR_FILL_MODEL`, trống = model REVIEW) với câu thoại THẬT hai chiều (≤12 câu/cặp: i, zh, vi hiện tại) + giới/vai/quan hệ + chiều ngược nếu có. Gọi qua `cloud_retry.call_with_cloud_retry(retries=0)` (cùng cơ chế, KHÔNG chờ/thử lại). Nhận cặp đúng cặp được hỏi, conf ≥ `SIMPLE_PAIR_FILL_CONF` → PlanView (src `llm_fill`, conf). Lỗi/429/JSON hỏng → bỏ qua bước, KHÔNG park. **«Đánh cờ để vá»** = bộ kiểm chạy với cặp mới: câu của cặp đó lệch dạng → cờ `pronoun` → vòng vá; câu đã đúng không gửi lại (tiết kiệm token). Chạy lại job: cặp `llm_fill` cũ trong `plan_inferred.json` được dùng lại, không gọi lại model.

## Bước 8 — học lại

- (a) `SIMPLE_LEARN_INFERRED=1` + cổng **done** → cặp rule/llm_fill thêm vào `glossary.json` (không đè, kèm `src`) TRƯỚC `series_glossary.save_from` ⇒ vào hồ sơ bộ phim. Mặc định 0: `glossary.json`/bảng bộ không bao giờ thấy cặp suy luận (tránh lan sai). Park/hold không bao giờ ghi.
- (b) `tools/collect_manual_edits.py --work <work> --out <dir> [--jobs a,b]`: CHỈ ĐỌC; câu `manual` → `<out>/<job>/{lines.gold.jsonl, pairs.json, characters.json, meta.json}` định dạng golden V6, `status=candidate`, `vi_system` = bản máy cuối trong `trace.jsonl` (không có trace → null, `evidence=none`), bỏ câu manual mà vi không đổi (chỉ dọn zh). Từ chối `--out` nằm trong `--work`. Người duyệt gắn `error_tags`; KHÔNG trộn vào golden_heldout.
- (c) `tools/simple_stats.py --work <work> [--json f] [--all]`: CHỈ ĐỌC; bảng theo job: cổng done/park/hold + lý do, % câu còn cờ theo loại, lô review lỗi, cặp thiếu, cặp rule/llm_fill, câu sửa tay, nguồn ZH.

## Bước 1 — nguồn ZH (`zh_source.py`, `SIMPLE_ZH_SOURCE=1`)

- **Phát hiện hardsub:** dùng cache của render nếu có (`hardsub_track.json`: `bands` rỗng = không; `hardsub_band.json`: `band` null = không); không có → lấy mẫu `SIMPLE_ZH_HS_SAMPLES` khung đều theo phim (`ffmpeg -ss`), RapidOCR, phân vùng bằng `ocr._classify_zone` + `ocr._meaningful` (watermark góc bị loại), tỉ lệ khung có chữ ở vùng thoại ≥ `SIMPLE_ZH_HS_MIN_RATIO` ⇒ có hardsub. Không video / thiếu RapidOCR ⇒ giữ ASR.
- **Có hardsub:** cue OCR từ `hardsub_asr.extract_hardsub_cues` (dùng lại `hardsub_cues.json` nếu có) → `hardsub_asr.merge_hardsub_into_asr` (đã có bảo vệ câu bên cạnh/mảnh/OCR rác): chữ OCR thắng ASR khi khớp thời gian + đủ giống, **timing ASR giữ nguyên**. Mỗi câu `zh_src` = `ocr` | `asr` (+ `zh_asr` = chữ ASR gốc).
- **Hotword:** `firered_asr.py` KHÔNG có tham số hotword/context ⇒ làm bước sửa tên có bảo vệ: tên/thuật ngữ ZH từ bảng bộ (`series_glossary`) + `glossary.json`; chỉ cửa sổ cùng độ dài, tên ≥3 chữ, lệch ĐÚNG 1 chữ, cửa sổ không phải tên đã biết, điểm ≥ `SIMPLE_ZH_NAMEFIX_MIN`; có `pypinyin` thì chữ lệch phải đồng âm (điểm (L−1+0,9)/L), không có thì tên 3 chữ không bao giờ bị sửa (0,667 < 0,75) — chỉ tên ≥4 chữ. Mọi lần thay ghi `zh_source.json.name_fixes` + `zh_src …+namefix`.
- Không ghi `asr.json`; bản dùng cho dịch `asr.zhsource.json`, báo cáo `zh_source.json`; câu đã có (chạy lại), không manual, chưa rv → cập nhật zh (giữ `zh_asr`). Lỗi bất kỳ ⇒ giữ ASR.
- **CHƯA chạy thật:** ffmpeg/RapidOCR/video thật, tỉ lệ ngưỡng 0,3 trên phim thật, `pypinyin` (V2 chưa cài — kiểm `python -c "import pypinyin"`), FireRed. Test dùng khung giả (hộp OCR toạ độ tay) + cue giả.

## Sửa lỗi (agent A): simple không gỡ lặp ASR

Luồng cũ gọi `translate.apply_asr_stutter_heal` (trong `apply_style_polish` và đầu `run_review`); simple chỉ `clean_zh_spam` ⇒ «杀吧杀吧，» giữ lặp, vi lặp theo. Nay simple dùng CÙNG hàm `translate.heal_obvious_internal_stutter`: zh của câu không manual, chưa rv (sau dựng script; câu đã soát giữ nguyên để zh/vi không lệch) — trace `asr_heal`; vi trong `post.apply` (trace `post` «gỡ lặp»). Tượng thanh (哈哈哈哈) giữ như luồng cũ. Không cờ (simple vốn chỉ chạy khi `TRANSLATE_PIPELINE=simple`). Luồng cũ không đổi (không sửa translate.py/server.py; nhóm test dịch cũ trước = sau).

## Quan sát (agent A): đổi cặp xưng hô theo cảnh — CHƯA sửa, đề xuất

32da simple đổi cặp 14 lần vs gold 28. Kiểm code: `PlanView` khoá cặp theo (who, to) DUY NHẤT, `setdefault` ⇒ plan có 2 cặp cùng (who,to) khác dạng thì cặp sau bị BỎ IM LẶNG; `pronouns` không có trường `range`/`scene` (schema plan `translate._plan_json_schema` không có; job work không thuộc golden/heldout đọc được: 60 cặp, 0 có range, 0 trùng khác dạng); quan hệ theo cảnh chỉ có ở `scenes[].pronouns_in_scene` (chữ tự do, vào prompt nhưng bộ kiểm KHÔNG dùng) ⇒ bộ kiểm + vá kéo xưng hô về MỘT bộ cho cả phim. Đề xuất (cần căn cứ A/B trước khi làm): (1) cho `pronouns[]` trường tuỳ chọn `range:[i0,i1]`/`scene_id`, `PlanView.pair(spk,to,i)` chọn cặp phủ câu i, hết khoảng thì cặp chung; (2) bộ kiểm hạ cờ pronoun xuống «mềm» khi cảnh có `pronouns_in_scene` khác cặp chung; (3) plan prompt yêu cầu tách cặp khi quan hệ đổi (giả thân phận, lộ thân phận, cưới…).

## Recheck (cloud, LLM/NMT/video giả)

- Test mới `tests/test_translate_simple_next.py`: **29 ca** (27 pass + 2 skip khi không có backup; có backup/`TS_NEXT_BACKUP` = 29 pass).
- **Cờ tắt = y hệt trước:** `test_flags_off_byte_identical_to_backup` dựng gói GỐC từ backup và chạy song song với bản mới trên 8 kịch bản (good, wrong→vá, hold, park, manual, bỏ sót + echo, cặp lạ + new_pairs + relationship_matrix, câu có thành ngữ translate_rules + golden_derived), × 2 (cờ không đặt / đặt «0» tường minh): prompt gửi LLM, `script.json`, `script.display.json`, `sub.vi.srt`, `glossary.json`, `style_lock.json`, `trace.jsonl` (bỏ ts), `manifest.json` + `plan_suggestions.json` (bỏ mốc giờ), kết quả run — **trùng từng byte**. Kiểm chứng ngược: bật `SIMPLE_PAIR_RULES` riêng bản mới ⇒ test báo khác. `test_flags_off_new_modules_never_called`: module mới bị thay bằng hàm ném lỗi, cờ mặc định ⇒ chạy bình thường, không file mới. Lưu ý: kịch bản không có câu lặp — với câu lặp ASR simple CỐ Ý khác (sửa lỗi ở trên).
- Simple cũ 41 pass + 4 skip (server/golden cần Windows) — trước = sau.
- Nhóm dịch cũ (15 file của bat): 231 pass / 8 fail / 11 skip / 2 lỗi collect — **trước = sau** (fail = môi trường cloud + fail có sẵn).
- Toàn bộ `tests/` (cloud, không fastapi/google): **338 → 367 pass**, 16 fail giống hệt (sfx_lib×5, restart_guard×2, asr_demucs, check_batch1-5, modernish_mixed, detox_nguoi_ta, filter_review_fixes_when_locked), 15 skip, 12 lỗi collect môi trường (trước = sau).

**Chỉ kiểm được trên Windows / chạy thật:** `Z:\PinelineV6\scripts\test_v2_translate_simple.bat` (kỳ vọng 74 pass), A/B thật (`golden_ab_simple.bat next`), video/OCR thật, chất lượng bảng quy tắc trên phim thật.

## Rủi ro

- Bảng quy tắc là quy ước chung — sai khi quan hệ đặc thù (giả thân phận, xưng hô trêu); bật `SIMPLE_PAIR_RULES` có thể thêm cờ pronoun ⇒ thêm vá/hold. Mixed nhận nhiều dạng ⇒ bộ kiểm lỏng hơn cho cặp rule.
- **Khai báo:** khi tìm định dạng `relationship_matrix`/`role` để viết parser, agent B đã xem cấu trúc `glossary.json` (plan máy sinh, KHÔNG phải nhãn golden) của 3 job work, trong đó `2493d3c7cb29_p01` và `2d3316593ea9` sau đó được agent A chọn làm held-out. Bảng quy tắc viết theo quy ước chung, nhưng vài từ khoá (đồng đội, bạn thân, cộng sự, đối địch) có trong mô tả của 2 job đó ⇒ điểm `simple_rules*` trên held-out 2 job này có thể hơi lạc quan; nên đánh giá thêm job held-out khác.
- `simple_rules_fill_zh` trong golden_ab: job tạm không có video ⇒ nguồn ZH = ASR (chỉ đo phần sửa tên).
- `pair_fill` thêm 1 lần gọi/job (≤8 cặp, ≤2048 token ra).

## md5 sau ghi

`translate_simple/cfg.py` cb4d7a14… · `translate_simple/lexicon.py` e6cd47a1… · `translate_simple/pipeline.py` 54357b2d… · `translate_simple/plan_view.py` 32092ee3… · `translate_simple/post.py` e75790d8… · `translate_simple/suggest.py` 51a9beec… · `translate_simple/pair_rules.py` 945e4728… · `translate_simple/pair_fill.py` 85ae1e5f… · `translate_simple/zh_source.py` c5683aa4… · `data/lexicon/idioms_zh_vi.json` dfbe4098… · `data/lexicon/pronoun_rules_zh_vi.json` a442fe66… · `tools/collect_manual_edits.py` 0568ed00… · `tools/simple_stats.py` afccdf75… · `tests/test_translate_simple_next.py` 3b55d7fc…. V6: `scripts/golden_ab.py` e06c67ad… · `scripts/golden_ab_simple.bat` 126f5c77… · `scripts/test_v2_translate_simple.bat` 6323ba80…. `server.py`, `translate.py` KHÔNG đổi.
