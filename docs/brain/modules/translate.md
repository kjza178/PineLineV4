# `translate`

[← Index](../generated/module-index.md) · [Brain home](../README.md)

<!-- AUTO:START — sinh bởi scripts/brain_build.py 2026-11-17 19:05. Đừng sửa tay khối này. -->
**File:** `translate.py` · **Lớp:** `translate` · **5167 dòng** (4588 code) · **104 hàm**, **1 class** · sha1 `2303556397`

> translate.py — STAGE dịch: "lập phương án" (hồ sơ nhân vật + XƯNG HÔ) rồi dịch CÓ NGỮ CẢNH, khớp độ dài. Nâng cấp so với bản cũ:

### Phụ thuộc

- **Gọi tới (import nội bộ):** [agent_hang_fix](./agent_hang_fix.md), [batch_config](./batch_config.md), [cloud_retry](./cloud_retry.md), [config](./config.md), [context_studio.schema](./context_studio.schema.md), [fileio](./fileio.md), [hv_auditor](./hv_auditor.md), [llm](./llm.md), [manifest](./manifest.md), [mt_zh_vi](./mt_zh_vi.md), [preset_switcher](./preset_switcher.md), [pronoun_consistency](./pronoun_consistency.md), [script_lint](./script_lint.md), [series_glossary](./series_glossary.md), [subs](./subs.md), [translate_simple.cfg](./translate_simple.cfg.md), [translate_simple.stage_draft](./translate_simple.stage_draft.md), [vram](./vram.md)
- **Được dùng bởi:** [agent_hang_fix](./agent_hang_fix.md), [agent_name_pass](./agent_name_pass.md), [agent_pronoun_pass](./agent_pronoun_pass.md), [asr_spam](./asr_spam.md), [ocr](./ocr.md), [pronoun_consistency](./pronoun_consistency.md), [scripts.check_batch2](./scripts.check_batch2.md), [server](./server.md), [translate_alts](./translate_alts.md), [translate_simple.cfg](./translate_simple.cfg.md), [translate_simple.pipeline](./translate_simple.pipeline.md), [translate_simple.post](./translate_simple.post.md), [translate_simple.script_store](./translate_simple.script_store.md), [translate_simple.stage_draft](./translate_simple.stage_draft.md)
- **Được nhắc tên file `.py` (subprocess/script) bởi:** [cloud_retry](./cloud_retry.md), [restart_server](./restart_server.md), [scripts.check_batch2](./scripts.check_batch2.md), [server](./server.md)
- **Test:** `tests/test_optimize_b5_b6.py`, `tests/test_pronoun_postpass.py`, `tests/test_pronoun_qa_slim_plan.py`, `tests/test_review_fail_not_rv.py`, `tests/test_review_parallel_workers.py`, `tests/test_review_pass1_upload.py`, `tests/test_simple_junk_park.py`, `tests/test_simple_r1_bugs.py`, `tests/test_translate_b1.py`, `tests/test_translate_b1_scenarios.py`, `tests/test_translate_b2.py`, `tests/test_translate_b2_review.py`, `tests/test_translate_b3.py`, `tests/test_translate_missing.py`, `tests/test_translate_simple.py`, `tests/test_translate_simple_next.py`, `tests/test_translate_simple_next_review.py`, `tests/test_translate_simple_scenarios.py`
- **Thư viện ngoài:** `requests`

```mermaid
flowchart LR
  translate[[translate]]
  agent_hang_fix[agent_hang_fix] --> translate
  agent_name_pass[agent_name_pass] --> translate
  agent_pronoun_pass[agent_pronoun_pass] --> translate
  asr_spam[asr_spam] --> translate
  ocr[ocr] --> translate
  pronoun_consistency[pronoun_consistency] --> translate
  scripts_check_batch2[scripts.check_batch2] --> translate
  server[server] --> translate
  translate --> agent_hang_fix[agent_hang_fix]
  translate --> batch_config[batch_config]
  translate --> cloud_retry[cloud_retry]
  translate --> config[config]
  translate --> context_studio_schema[context_studio.schema]
  translate --> fileio[fileio]
  translate --> hv_auditor[hv_auditor]
  translate --> llm[llm]
  translate --> manifest[manifest]
  translate --> mt_zh_vi[mt_zh_vi]
  translate --> preset_switcher[preset_switcher]
  translate --> pronoun_consistency[pronoun_consistency]
  translate --> script_lint[script_lint]
  translate --> series_glossary[series_glossary]
  translate --> subs[subs]
```

### Hàm & class top-level

| Tên | Dòng | Dài | Tham số | Docstring |
|---|---:|---:|---|---|
| **class `ReviewBadOutput`** | 2300 | 0 method | | fix 2026-11-11 translate-b1 C1: REVIEW LLM trả rỗng / JSON hỏng / cụt / thiếu «fixes». |
| `_tmodel` | 62 | 3 | `` | TRANSLATE_MODEL đọc lúc gọi (server import module 1 lần — MODEL ở trên bị đóng băng). |
| `_rmodel` | 67 | 2 | `` |  |
| `_resolve_review_model` | 71 | 24 | `work_dir, model` | REVIEW model thật: arg → (queue_opts backup Aurora) → REVIEW_MODEL. |
| `_is_llama_local_model` | 97 | 9 | `m` |  |
| `_is_cloud_model` | 108 | 5 | `m` | Model cloud (chatgpt/aurora/9router…): không rỗng, không local Ollama, không llama. |
| `_cloud_fill_model` | 115 | 29 | `work_dir, model` | fix 2026-11-11 translate-b2 (Việc B): model vá câu NMT sót (rỗng/còn chữ Hán). |
| `post_translate_gate_action` | 146 | 26 | `work_dir, n_miss, gap` | fix 2026-11-11 translate-b2: cổng server SAU run_translate (hàm thuần cho test). |
| `_log_vram` | 174 | 27 | `stage` | fix 2026-11-11 translate-b2: log VRAM nhẹ để đo thực tế — `[vram] <stage> used/total MiB`. |
| `_cloud_fill_call` | 203 | 10 | `fn, fill_model, label, what, work_dir` | Gọi 1 lô dịch-lấp bằng model cloud với retry Việc A (limit/5xx/timeout). |
| `_review_parallel_workers` | 215 | 36 | `work_dir, rmodel` | Số worker fan-out REVIEW. Local LLM = 1; aurora_parallel / REVIEW_PARALLEL>1 → N. |
| `_llm_error_status` | 265 | 17 | `e` | Mã HTTP của lỗi LLM: response.status_code nếu có, không thì mã ở các mẫu |
| `_classify_review_error` | 284 | 31 | `e` | fix 2026-11-11 translate-b1 C9: phân loại lỗi REVIEW theo KIỂU exception / mã HTTP. |
| `_new_review_fallback_state` | 317 | 10 | `` | Trạng thái fallback local DÙNG CHUNG cho mọi luồng của MỘT lượt run_review. |
| `_review_split_on_too_large` | 340 | 41 | `chunk_exp, plan_block, prev_ctx, target, model, plan, exemplars_poo…` | 413/context-length: chia đôi chunk_exp và soát từng nửa (nửa sau nhận nửa đầu làm |
| `_review_chunk_with_fallback` | 383 | 127 ⚠️ | `chunk_exp, chunk, plan_block, prev_ctx, target, rmodel, plan, exemp…` | Chạy 1 lô review_batch; cloud lỗi quota/timeout → fallback local. |
| `_meaning_rules` | 517 | 62 | `` | Quy tắc chống dịch đen / lệch ngữ cảnh (lồng tiếng phim). |
| `_style_rules` | 581 | 33 | `` | Quy tắc Manhua / short-drama: cứng Hán Việt + mềm hiện đại + xưng hô. |
| `_character_rules` | 616 | 13 | `` | Chống nhầm nhân vật / sai giới tính khi dịch thoại. |
| `_is_ancient_fantasy_genre` | 638 | 22 | `plan` | True khi phương án/genre thuộc tu tiên·cổ trang·wuxia·xianxia (không mixed đô thị). |
| `_is_mixed_genre` | 662 | 12 | `plan` |  |
| `_mixed_address_rules` | 676 | 19 | `` | Đô thị dị năng + võ/KH: xưng hô hiện đại + cổ phong Hán Việt. |
| `_ancient_address_rules` | 697 | 19 | `` | Chỉ inject khi genre tu tiên/cổ — không áp cho đô thị hiện đại. |
| `_translate_rules` | 718 | 8 | `plan` | Gộp nghĩa + văn phong + nhân vật (+ xưng hô theo genre). |
| `_ocr_name_hints` | 727 | 25 | `work_dir` | Tên/chữ trên hình từ ocr.json (nếu có) — gợi ý cho PLAN. |
| `_resolve_translate_mode` | 754 | 26 | `mode, model, n_todo` | Trả 'oneshot' / 'batch'. |
| `_has_cjk` | 782 | 3 | `text` | Còn ký tự Hán trong bản dịch = model dịch sót/hỏng (đặc biệt model nhỏ local). |
| `_salvage_mixed_vi` | 810 | 45 | `vi, zh, plan` | Cứu VI lẫn Hán (vd «Đạt được 100% 增幅.») — không thì trả '' để vá lại. |
| `_plan_mode` | 857 | 3 | `` | file = upload full ZH SRT (Aurora); sample = mẫu cũ (head/mid/tail). |
| `_plan_json_schema` | 862 | 24 | `target` |  |
| `_plan_seed_blocks` | 888 | 52 | `name_hints, series_plan, soft_ocr` | OCR = seed mềm (có thể sai). Series characters = kế thừa mạnh. |
| `_normalize_plan_data` | 942 | 27 | `data` |  |
| `_remap_scenes_cue_to_i` | 971 | 33 | `plan, cue_to_i` | Nếu GPT trả range theo số thứ tự cue SRT (1..N) → map về segment i. |
| `_build_plan_from_file` | 1006 | 86 | `work_dir, segments, target, model, name_hints, series_plan` | Upload full ZH SRT → GPT đọc file (Aurora) → glossary. OCR chỉ seed mềm. |
| `_build_plan_sample` | 1094 | 80 | `segments, target, model, name_hints, series_plan` | Fallback: mẫu head/mid/tail (plan cũ). |
| `build_plan` | 1176 | 76 | `segments, target, model, name_hints, series_plan, work_dir, before_…` | Lập glossary: mặc định upload full ZH SRT (PLAN_MODE=file); fallback sample. |
| `_plan_block` | 1254 | 110 | `p` | Đổ plan ra text nhét vào mọi prompt dịch. CHỐNG LỖI: model đôi khi trả |
| `_plan_block_for_qa` | 1366 | 72 | `p` | Plan block gọn cho pronoun-QA / GPT vá đỏ — chỉ genre+style+pronouns. |
| `_resolve_scene_context` | 1440 | 62 | `plan, rows` | Xác định phân cảnh hiện tại của lô câu thoại (Scene-based context injection). |
| `_norm_zh_cue` | 1541 | 6 | `zh` | Chuẩn hóa cue ZH để khớp lock (bỏ dấu câu/space). |
| `ensure_hard_terms` | 1549 | 81 | `plan` | Gắn seed chengyu/taunt vào glossary.terms (không đè bản tay đã có). |
| `hard_term_lock_map` | 1632 | 30 | `plan` | zh_norm → vi bắt buộc — CHỈ type=lock (+ seed lock). Chengyu/idiom = mềm trong prompt. |
| `apply_hard_term_locks` | 1664 | 39 | `rows, plan` | Post-pass: cue ZH khớp lock → ghi đè VI (chuẩn, không phụ thuộc LLM). |
| `normalize_vi_thousands` | 1711 | 14 | `text` | Dấu nghìn chuẩn Việt: 31 000 / 31,000 → 31.000. |
| `heal_obvious_internal_stutter` | 1727 | 46 | `text` | Gỡ một nhịp lặp ASR rõ ràng, không diễn giải hay viết lại câu. |
| `apply_asr_stutter_heal` | 1775 | 18 | `rows` | Heal only deterministic internal ASR repeats; preserve manual rows. |
| `apply_halfcue_dangling_heal` | 1795 | 33 | `rows` | Gỡ đuôi treo VI khi ASR cắt ý sang cue sau (之前。 / trước đó.). |
| `_cfg_flag` | 1830 | 7 | `key, default` | fix 2026-11-12 translate-b3: cờ bật/tắt đọc lúc gọi (env > pineline.config.json > mặc định). |
| `_pronoun_regex_mixed_on` | 1839 | 9 | `` | fix 2026-11-12 translate-b3 — PRONOUN_REGEX_MIXED (mặc định 1 = như cũ). |
| `apply_style_polish` | 1850 | 288 ⚠️ | `rows, plan` | Post-pass deterministic: sửa calque / văn mẫu thường gặp (mixed short-drama). |
| `_is_modernish_genre` | 2140 | 28 | `plan` | Chỉ đô thị THUẦN — không ép detox khi mixed (phim có thể sang tu tiên). |
| `_char_aliases` | 2170 | 16 | `plan` | vi_name_lower → {zh, vi, aliases…} để khớp tên trong câu. |
| `_pronoun_pairs` | 2188 | 14 | `plan` |  |
| `_detox_modern_pronouns` | 2204 | 24 | `vi, zh` | Ép Ta/Ngươi → Tôi/Cậu cho thoại đô thị (giữ «ông ta/cô ta/chúng ta»). |
| `apply_pronoun_postpass` | 2230 | 68 | `rows, plan` | Post-pass deterministic xưng hô — không phụ thuộc LLM nhớ ma trận. |
| `_parse_review_fixes` | 2305 | 54 | `text` | Parse CHẶT phản hồi REVIEW. Trả {i: vi} (có thể rỗng) hoặc None = không tin được. |
| `_scan_review_json` | 2361 | 24 | `t, max_starts` | Tìm giá trị JSON TRỌN hợp lệ cho REVIEW trong chuỗi có chữ thừa (xem _parse_review_fixes). |
| `_row_is_manual` | 2387 | 4 | `r` | fix 2026-11-11 translate-b1 C2: câu người sửa tay (server đặt manual=1/True) — |
| `_salvage_items` | 2393 | 23 | `text` | Vớt từng object {"i":.., "vi":..} kể cả khi JSON TỔNG THỂ hỏng (model |
| `translate_oneshot` | 2418 | 66 | `rows, plan_block, target, model, plan` | Dịch TOÀN BỘ danh sách câu trong 1 lần gọi LLM (llama-server ctx lớn). |
| `translate_batch` | 2486 | 85 | `rows, plan_block, prev_ctx, target, model, plan` | LƯỢT 1 — DỊCH NGHĨA KỊCH BẢN CHUẨN XÁC (Semantic Accuracy) theo Phân Cảnh (Scene) + Series Glossary. Trả {i: vi}. |
| `_translate_safe` | 2573 | 26 | `rows, plan_block, prev_ctx, target, model, plan` | Dịch 1 lô CÓ CHỐNG LỖI: nếu parse hỏng hoặc LLM nuốt câu, CHIA ĐÔI lô rồi thử lại. |
| `_style_voice_banner` | 2601 | 36 | `plan` | Gợi ý văn phong linh hoạt — KHÔNG khóa modern↔cổ (phim có thể đổi cảnh). |
| `_ts_srt` | 2639 | 11 | `sec` |  |
| `write_review_pair_srt` | 2652 | 27 | `work_dir, rows, name` | SRT ZH+VI có tag [i=N] để Pass1 đọc full mạch thoại. |
| `_heuristic_nonsense_flags` | 2681 | 38 | `rows` | Bắt đuôi treo / nửa câu VI rõ (bổ sung Pass1). |
| `_pass1_max_upload_bytes` | 2721 | 9 | `` | Trần 1 file upload Pass1 (mặc định 5MB). Lớn hơn → chia chunk upload full. |
| `_pass1_chunk_cues` | 2732 | 6 | `` | Số cue / chunk khi chia file (đọc full bằng nhiều upload). |
| `_pass1_chat_model` | 2740 | 4 | `use_model` |  |
| `_pass1_merge_chunk_results` | 2746 | 48 | `parts` | Gộp JSON Pass1 từ nhiều chunk file — phủ đủ toàn phim. |
| `_pass1_upload_one_srt` | 2796 | 45 | `srt_path, prompt, use_model, timeout, label, stop_path` | Upload 1 SRT + hỏi GPT đọc file. Trả dict JSON hoặc {}. |
| `_pass1_upload_full_via_chunks` | 2843 | 50 | `work_dir, rows, prompt, use_model, timeout` | Chia full script thành nhiều SRT → upload từng phần → GPT đọc hết (không chat sample). |
| `run_review_pass1_full_vi` | 2895 | 183 ⚠️ | `work_dir, rows, plan, model` | Pass1: GPT đọc FULL pair SRT qua upload file (không thay bằng chat mẫu). |
| `_style_exemplars` | 3080 | 36 | `plan, rows_pool, limit` | 3–5 câu mẫu giữ giọng (ưu tiên có tên NV glossary). |
| `_review_pronoun_mask_on` | 3127 | 7 | `` |  |
| `_mask_pronouns_vi` | 3136 | 8 | `vi` |  |
| `_unmask_pronouns_vi` | 3146 | 5 | `text, toks` |  |
| `_pronoun_forms` | 3153 | 7 | `vi` |  |
| `_review_pron_guide_on` | 3162 | 9 | `` | fix 2026-11-12 translate-b3: REVIEW được sửa xưng hô theo plan. |
| `_plan_pronoun_forms` | 3173 | 10 | `plan` | Các dạng tự xưng/cách gọi đã chốt trong plan.pronouns (chữ thường). |
| `_review_pron_guide_block` | 3185 | 20 | `plan` | Khối chỉ dẫn (G) — chỉ chèn khi `_review_pron_guide_on()`. |
| `_pronoun_plan_fixes` | 3207 | 40 | `fixes, rows, plan` | translate-b3: fix CHỈ đổi đại từ sang dạng có trong plan.pronouns → giữ (bộ lọc cosmetic |
| `review_batch` | 3249 | 170 ⚠️ | `rows, plan_block, prev_ctx, target, model, plan, exemplars_pool` | LƯỢT 2 — BẢN ĐỊA HÓA LỜI THOẠI LỒNG TIẾNG & KHỚP NHỊP PHỤ ĐỀ (Voice Dubbing Localization). |
| `_filter_cosmetic_nmt_fixes` | 3421 | 179 ⚠️ | `fixes, rows, plan` | Chỉ giữ A/C/D/E/F cứng; mặc định GIỮ NMT (bỏ polish GPT). |
| `run_review` | 3603 | 13 | `work_dir, batch, target, model, force` | LƯỢT 2 — xem `_run_review_impl`. translate-b2: bọc log VRAM đầu/cuối. |
| `_run_review_impl` | 3618 | 413 ⚠️ | `work_dir, batch, target, model, force` | LƯỢT 2: soát bản dịch nháp (script.json) bằng model chính xác (minimax) rồi |
| `count_script_missing` | 4033 | 10 | `work_dir` | Đếm câu trống trong script.json (nguồn sự thật cho UI / auto-vá). |
| `translate_coverage_gap` | 4045 | 35 | `work_dir` | Số câu ASR chưa có trong script (salvage lúc Dừng hay ghi thiếu). |
| `translate_ready_for_tts` | 4082 | 13 | `work_dir` | True chỉ khi dịch đủ coverage ASR + không còn VI trống. |
| `_trivial_vi` | 4097 | 39 | `zh` | Câu chỉ cười/thán từ — không cần LLM (model hay trả lại chữ Hán → _has_cjk xoá). |
| `_compress_zh_for_llm` | 4138 | 3 | `zh` | Rút chuỗi cười/spam trước khi gửi LLM (tránh timeout / trả Hán). |
| `clean_zh_spam` | 4143 | 35 | `zh, max_rep, max_len` | Rút 哈/呃/嗯/啊 spam + cụm chữ lặp (区域的区域的…) từ ASR. |
| `_halfcue_cfg` | 4193 | 16 | `` | HALFCUE_MERGE=1 → {gap, max_chars, max_cues}; 0 (mặc định) → None (tắt, như cũ). |
| `_hc_zh` | 4211 | 2 | `s` |  |
| `_hc_len` | 4215 | 2 | `zh` |  |
| `_zh_ends_sentence` | 4219 | 3 | `zh` |  |
| `halfcue_groups` | 4224 | 33 | `segments, gap, max_chars, max_cues` | i → group_id ("hc<i đầu>") cho cue thuộc nhóm ≥ 2 cue liên tiếp CÙNG một câu: |
| `halfcue_units` | 4259 | 30 | `items, groups, pos_of, failed` | Gom các item liên tiếp (theo thứ tự phim) cùng group_id thành 1 đơn vị dịch |
| `halfcue_split_vi` | 4291 | 47 | `vi, zh_parts` | Chia câu VI của một nhóm về lại các cue: mỗi điểm cắt chọn ranh giới dấu câu |
| `halfcue_expand` | 4340 | 25 | `vi_map, units, failed, assigned` | vi theo đơn vị → vi theo cue gốc. Nhóm chia được: mọi cue thành viên nhận phần |
| `_hc_payload` | 4367 | 2 | `units` |  |
| `_seg_row` | 4371 | 8 | `s, zh, vi, **extra` | Hàng script.json từ hàng ASR `s`: {i,start,end,zh,vi} + trường thêm của ASR. |
| `run_translate` | 4381 | 18 | `work_dir, batch, target, force, model, mode, auto_review` | Stage dịch — xem `_run_translate_impl`. translate-b2: bọc log VRAM đầu/cuối. |
| `_run_translate_impl` | 4401 | 743 ⚠️ | `work_dir, batch, target, force, model, mode, auto_review` |  |
| `main` | 5146 | 18 | `argv` |  |

**Hàm dài ≥120 dòng:** `_run_translate_impl` (743, L4401), `_run_review_impl` (413, L3618), `apply_style_polish` (288, L1850), `run_review_pass1_full_vi` (183, L2895), `_filter_cosmetic_nmt_fixes` (179, L3421), `review_batch` (170, L3249), `_review_chunk_with_fallback` (127, L383)

### Config / env keys (32)

`AURORA_REVIEW_MODEL`, `AUTO_REVIEW`, `AUTO_SWITCH_PRESETS`, `CHATGPT_TIMEOUT`, `FALLBACK_MODEL`, `LLM_MODEL`, `PLAN_FILE_TIMEOUT`, `PLAN_MODE`, `PLAN_MODEL`, `REVIEW_BACKUP`, `REVIEW_MODEL`, `REVIEW_PARALLEL`, `REVIEW_PARALLEL_DEFAULT`, `REVIEW_PARALLEL_MAX`, `REVIEW_PASS1_ALLOW_CHAT_FALLBACK`, `REVIEW_PASS1_CHUNK_CUES`, `REVIEW_PASS1_FALLBACK_CUES`, `REVIEW_PASS1_FULL_VI`, `REVIEW_PASS1_MAX_UPLOAD_BYTES`, `REVIEW_PASS1_MODEL`, `REVIEW_PASS1_TIMEOUT`, `REVIEW_PRESET`, `REVIEW_PRONOUN_MASK`, `REVIEW_RETRY_BACKOFF_SEC`, `TRANSLATE_BATCH`, `TRANSLATE_CTX_LINES`, `TRANSLATE_FILL_MODEL`, `TRANSLATE_FILL_ROUNDS`, `TRANSLATE_MODE`, `TRANSLATE_MODEL`, `TRANSLATE_ONESHOT_MAX`, `TRANSLATE_PRESET`

**File/artifact nhắc tới:** `asr.json`, `context_pack.json`, `glossary.json`, `ocr.json`, `review_pass1.json`, `script.display.json`, `script.json`, `style_lock.json`, `sub.review_pair.srt`, `sub.vi.srt`

**Tín hiệu rủi ro (đếm tĩnh):** broad_except=71 · file_writes=4 · pools=1 · sleep=1 · subprocess=1 · swallow_except=14

### Lịch sử (từ docs/)

- **Fix logs (27):**
  - [simple-junk-park: câu ASR rác «None.» làm dịch simple park mãi → part 1/2 kẹt, phim không ghép](../../fixes/2026-11-13-simple-junk-park.md)
  - [translate-simple: luồng dịch mới (plan ∥ NMT → review 1 lần/lô → vá câu bị cờ → cổng), sau cờ TRANSLATE_PIPELI](../../fixes/2026-11-12-translate-simple.md)
  - [translate-simple «next»: lexicon src · bảng quy tắc xưng hô · bổ sung cặp thiếu · học lại · nguồn ZH · gỡ lặp ](../../fixes/2026-11-12-translate-simple-next.md)
  - [Port V2 → V4: luồng dịch `translate_simple` (MẶC ĐỊNH) + Demucs trước ASR](../../fixes/2026-11-12-port-simple-demucs.md)
  - [Studio SOP: 1 job / ghế — ASR→NMT→Aurora∥ REVIEW→TTS→mux→Done→next](../../fixes/2026-11-11-studio-1job-pipeline.md)
  - [REVIEW lỗi bị coi là đã soát · park treo hàng đợi · Brain V4 điều khiển nhầm V2](../../fixes/2026-11-11-review-fail-park-port.md)
  - [Pass1 413 — chặn upload theo số cue, fallback chat phình](../../fixes/2026-11-11-pass1-upload-size.md)
  - [Tối ưu đợt 11/11: dừng REVIEW song song chậm · audio run-all/mux lệch queue · restart chờ vô hạn · ghi plan kh](../../fixes/2026-11-11-optimize-b5-b6-b8-b10.md)
  - [REVIEW CLI song song + heal làm UI mất/soát % tụt](../../fixes/2026-11-10-review-heal-parallel.md)
  - [UI «backup Aurora» không rà — Gemma bỏ sót NMT vô nghĩa](../../fixes/2026-11-10-review-gpt6-aurora.md)
  - [Mix #1+#3 + title→ngươi vào production](../../fixes/2026-11-10-mix13-title-nguoi.md)
  - [Brain HOLD vì high hang — cần LLM trace/xử lý rồi mới mở](../../fixes/2026-11-10-brain-hang-llm-fix.md)
  - [Stop lúc soát vẫn nhảy TTS / job không dừng](../../fixes/2026-11-09-stop-during-review-tts.md)
  - [REVIEW Pass1 full VI + duty F nửa câu vô nghĩa](../../fixes/2026-11-09-review-pass1-halfcue.md)
  - [GPT review viết lại NMT đã tốt (Lão tử…)](../../fixes/2026-11-09-review-keep-nmt.md)
  - [REVIEW bỏ sót ASR cắt lặp / chồng câu](../../fixes/2026-11-09-review-asr-merge.md)
  - [NMT draft + glossary gầy + REVIEW GPT mini](../../fixes/2026-11-09-mt-draft-slim-gloss.md)
  - [没大没小 → «chưa lớn không nhỏ» (calque vô nghĩa đã rv)](../../fixes/2026-11-09-meidameixiao-calque.md)
  - [HV Auditor: glossary khóa sai âm Hán Việt (逆→Nghị)](../../fixes/2026-11-09-hv-auditor.md)
  - [Dịch dừng giữa chừng → nhảy TTS với số câu dở (vd 64/398 vs ASR 2698)](../../fixes/2026-11-08-translate-partial-tts-jump.md)
  - [逆天而行 dịch sai «Nghị Thiên Nhi Hành» (đúng: Nghịch…)](../../fixes/2026-11-08-nghich-thien-ni-hanh.md)
  - [Bấm lồng tiếng / dịch xong rồi lại «force: dịch lại từ đầu»](../../fixes/2026-11-06-translate-force-wipe.md)
  - [Pronoun-QA GPT vá đỏ → Aurora 413 (payload quá lớn)](../../fixes/2026-11-06-pronoun-qa-413-slim.md)
  - [Lệch xưng hô sau dịch (Ta–Ngươi / sai self–call)](../../fixes/2026-11-02-pronoun-xung-ho.md)
  - [Đồng nhất xưng hô A–C (analyze full ZH → lock → ledger → QA)](../../fixes/2026-11-02-pronoun-consistency-abc.md)
  - … +2 file nữa
- **Reviews:** [2026-11-12-translate-simple-review](../../reviews/2026-11-12-translate-simple-review.md), [2026-11-12-translate-simple-next-review](../../reviews/2026-11-12-translate-simple-next-review.md), [2026-11-11-v4-v5-port-review](../../reviews/2026-11-11-v4-v5-port-review.md), [2026-11-10-review-parallel-aurora](../../reviews/2026-11-10-review-parallel-aurora.md), [2026-11-09-plan-file-review-style-code](../../reviews/2026-11-09-plan-file-review-style-code.md), [2026-11-09-mt-sandbox-job](../../reviews/2026-11-09-mt-sandbox-job.md), [2026-11-09-mt-keepnmt-final](../../reviews/2026-11-09-mt-keepnmt-final.md), [2026-11-09-mt-bench-verdict](../../reviews/2026-11-09-mt-bench-verdict.md), [2026-11-09-mt-60-zh-vi](../../reviews/2026-11-09-mt-60-zh-vi.md), [2026-11-09-glossary-nmt-poc-summary](../../reviews/2026-11-09-glossary-nmt-poc-summary.md)
- Nhắc trong CHANGELOG: **13** lần · DECISIONS: **0** lần

<!-- AUTO:END -->

<!-- MANUAL:START -->
## Vai trò (viết tay)

_Chưa viết. 2–4 câu: module này chịu trách nhiệm gì trong pipeline, ai gọi nó, nó KHÔNG làm gì._

## Luồng chính

_Các hàm vào (entry) → bước chính → output/side effect. Ghi tên hàm thật._

## Bất biến & hợp đồng

_Điều luôn phải đúng (vd: chỉ ghi manifest qua `Manifest.update`; 1 job / ghế). Vi phạm = bug._

## Bẫy đã biết

_Lỗi từng gặp + link `docs/fixes/...`. Những chỗ dễ sửa sai._

## Ghi chú vận hành

_Config key quan trọng, cần restart gì khi sửa (:8801 / :8802 / hot-reload), cách test._
<!-- MANUAL:END -->
