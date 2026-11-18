# Index module

_Sinh tự động bởi `scripts/brain_build.py` lúc 2026-11-17 19:05. Đừng sửa tay — chạy lại script._


Tổng: **148 module** (+64 test), **82,976 dòng**. Cột *Manual* = thẻ đã có phần viết tay (✅) hay chưa (·).

## control (13)

| Module | Dòng | Hàm | Routes | Fix | Test | Manual | Tóm tắt |
|---|---:|---:|---:|---:|---:|:-:|---|
| [server](../modules/server.md) | 7322 | 198 | 68 | 43 | 8 | · | server.py — Backend web Phase 1 (FastAPI). Bọc engine (download -> asr -> translate) thành |
| [routes_hg](../modules/routes_hg.md) | 1107 | 58 | 62 | 7 | 1 | · | Cầu nối Hongguo 2.x (helper RPC stdio): /api/hg/* (= /api/hg2/*). Tách từ server.py (đợt 7 |
| [routes_agent](../modules/routes_agent.md) | 815 | 47 | 18 | 7 | 1 | · | AI Agent nhúng (agent_core): hook cho Runtime + /api/agent/*. Tách từ server.py (đợt 7). C |
| [job_queue](../modules/job_queue.md) | 667 | 33 |  | 10 | 3 | ✅ |  |
| [routes_uploader_settings](../modules/routes_uploader_settings.md) | 611 | 23 | 31 | 3 | ❌ | · | routes_uploader_settings.py — API Router cho Quản lý Cài đặt (Settings) & YouTube Uploader |
| [routes_films](../modules/routes_films.md) | 370 | 31 | 31 | 2 | ❌ | · | FastAPI Router cho Thư viện Phim & Database (đồng bộ trực tiếp trong Pineline V4). Thay vì |
| [batch_config](../modules/batch_config.md) | 295 | 14 |  | 4 | 1 | · | Cấu hình batch dùng chung — 1 nguồn duy nhất cho Auto-pilot, Agent (queue_add), Telegram ( |
| [manifest](../modules/manifest.md) | 262 | 4 |  | 5 | 6 | ✅ | manifest.py — Trạng thái/checkpoint cho pipeline. Mỗi job (mỗi video) có một thư mục làm v |
| [restart_server](../modules/restart_server.md) | 250 | 9 |  | 8 |  | · | Restart server Pineline (giữ sidecar), khôi phục hàng đợi + Auto-pilot. Port mặc định V4:  |
| [config](../modules/config.md) | 194 | 8 |  | 5 | 2 | ✅ | config.py — Cấu hình/đường dẫn PORTABLE cho Pineline. Thứ tự ưu tiên khi lấy 1 giá trị: bi |
| [app_desktop](../modules/app_desktop.md) | 147 | 4 |  |  |  | · | app_desktop.py — Desktop App Studio cho Pineline V4. Sử dụng Microsoft Edge WebView2 (nati |
| [routes_ui](../modules/routes_ui.md) | 108 | 10 | 14 | 2 |  | · | Trang UI: /, /ui3, /ui4, /hongguo, /hongguo2, /films/ui, /studio, /v5-map. /hongguo2 = ski |
| [fileio](../modules/fileio.md) | 104 | 4 |  | 3 |  | · | Ghi file an toàn giữa nhiều tiến trình (server :8801, sidecar :8802, script). atomic_write |

## agent (20)

| Module | Dòng | Hàm | Routes | Fix | Test | Manual | Tóm tắt |
|---|---:|---:|---:|---:|---:|:-:|---|
| [agent_brain](../modules/agent_brain.md) | 2201 | 82 |  | 9 | 6 | · | Second Brain — daemon nền full-silent. Sensors → incidents → policy → actuators. Bật: AGEN |
| [agent_core](../modules/agent_core.md) | 2115 | 32 |  | 6 | 3 | · | agent_core.py — AI Agent nhúng trong Pineline V2. Không gọi HTTP self. Tools gọi runtime đ |
| [agent_hongguo](../modules/agent_hongguo.md) | 1570 | 36 |  | 4 | ❌ | · | agent_hongguo.py — Tích hợp bộ tool Hongguo Downloader & Auto-chain cho Pineline AI Agent. |
| [agent_heal](../modules/agent_heal.md) | 830 | 15 |  | 6 | 5 | · | agent_heal.py — Chẩn đoán + heal job lỗi (an toàn theo cấp). safe: heal stale running, vá  |
| [agent_qa_ask](../modules/agent_qa_ask.md) | 777 | 44 |  |  | 1 | · | Second Brain — HOLD QA hỏi người qua Telegram + tự xử lý khi quá hạn (2026-11-17 qaask). V |
| [agent_av_sync](../modules/agent_av_sync.md) | 569 | 11 |  | 5 | ❌ | · | AV sync diagnose + heal — phát hiện lệch sub/audio / audio cụt sau mux. Các class chính: a |
| [agent_brain_notify](../modules/agent_brain_notify.md) | 485 | 17 |  | 3 | 2 | · | Mẫu tin Telegram của Second Brain — do CODE dựng, không dùng văn tự do của LLM (fix 2026-1 |
| [agent_tool_loop](../modules/agent_tool_loop.md) | 476 | 11 |  | 1 | 1 | · | Tool loop — điều khiển pipeline theo bước, chờ kết quả thật. Khác `pineline_run_stage` (fi |
| [agent_hold](../modules/agent_hold.md) | 432 | 21 |  | 3 | 3 | · | agent_hold.py — gỡ HOLD khi người dùng CHẠY TAY 1 bước + chặn brain/auto đặt lại HOLD (fix |
| [agent_watch](../modules/agent_watch.md) | 408 | 20 |  | 3 | 1 | · | Watcher A: định kỳ scan → heal safe + log + Telegram (tuỳ chọn). Env: AGENT_WATCH=1 |
| [agent_quality](../modules/agent_quality.md) | 389 | 6 |  | 1 | 3 | · | Deterministic VI quality scan + safe heals (Second Brain L2). Port từ D:\PinelineV2_tmp\_q |
| [agent_hang_fix](../modules/agent_hang_fix.md) | 368 | 9 |  | 2 | 4 | · | Second Brain — pass LLM trace + xử lý high `hang` (đuôi treo / nửa câu). Không chỉ merge m |
| [agent_brain_context](../modules/agent_brain_context.md) | 287 | 8 |  | 4 | 1 | · | System snapshot cho Second Brain LLM — toàn hệ, không chỉ 1 job. |
| [agent_stage_io](../modules/agent_stage_io.md) | 286 | 14 |  |  |  | · | Peek / tóm tắt từng stage — chỉ đọc disk (an toàn). |
| [agent_pronoun_pass](../modules/agent_pronoun_pass.md) | 258 | 4 |  | 3 | 2 | · | Rà XƯNG HÔ trong bản dịch theo glossary.pronouns + genre. 1. Quét deterministic (cùng appl |
| [agent_qa_gate](../modules/agent_qa_gate.md) | 226 | 8 |  | 2 |  | · | Gate QA: translate → review → diff → mới cho TTS. |
| [agent_qa_fix](../modules/agent_qa_fix.md) | 202 | 9 |  |  | 1 | · | Second Brain — xử lý cờ QA HIGH loại khác `hang` (2026-11-17). Vì sao: trước đây chỉ `hang |
| [agent_retry](../modules/agent_retry.md) | 196 | 8 |  |  | 1 | · | Second Brain — tự thử lại stage FAILED (2026-11-17). Vì sao: L1 heal của brain chỉ chạy kh |
| [agent_name_pass](../modules/agent_name_pass.md) | 138 | 5 |  | 1 | 2 | · | Rà TÊN NHÂN VẬT trong bản dịch theo bảng nhân vật (glossary.json). 1. Quét: câu nào zh có  |
| [agent_error_class](../modules/agent_error_class.md) | 121 | 3 |  |  |  | · | Phân loại lỗi theo log / cur_text / error (ASR · TTS · mux · …). |

## sidecar (3)

| Module | Dòng | Hàm | Routes | Fix | Test | Manual | Tóm tắt |
|---|---:|---:|---:|---:|---:|:-:|---|
| [agent_tele_cmd](../modules/agent_tele_cmd.md) | 2464 | 42 |  | 14 | 1 | · | Sidecar: Telegram lệnh + Auto-pilot + HTTP :8802 KHÔNG restart Pineline server — chỉ gọi A |
| [agent_feeder](../modules/agent_feeder.md) | 2066 | 68 |  | 8 | ❌ | · | Feeder + Run-watch cho Auto-pilot (chạy trong sidecar :8802, chỉ gọi API :8801). Feeder —  |
| [agent_autopilot](../modules/agent_autopilot.md) | 348 | 17 |  | 7 | 1 | · | Auto-pilot — queue need_queue + heal safe qua HTTP Pineline (:8801). Chạy trong sidecar (a |

## source (6)

| Module | Dòng | Hàm | Routes | Fix | Test | Manual | Tóm tắt |
|---|---:|---:|---:|---:|---:|:-:|---|
| [hongguo_bridge](../modules/hongguo_bridge.md) | 3676 | 110 |  | 16 | 2 | · | hongguo_bridge.py — client Hongguo 2.x qua helper RPC (hongguo_rpc). 2026-11-16: bỏ hẳn Do |
| [hongguo_rpc](../modules/hongguo_rpc.md) | 1435 | 57 |  | 10 | ❌ | · | hongguo_rpc.py — JSON-RPC stdio client cho Hongguo WinUI 2.x helper.jar. Không dùng HTTP : |
| [download](../modules/download.md) | 706 | 20 |  | 4 | ❌ | · | download.py — STAGE 1: Tải video (Douyin / Bilibili / TikTok / ...). Engine: yt-dlp. Tự re |
| [hg_merge_check](../modules/hg_merge_check.md) | 480 | 17 |  | 1 | 1 | · | hg_merge_check.py — kiểm tra + chuẩn hoá các tập TRƯỚC khi gộp, và kiểm file SAU khi gộp ( |
| [hongguo_license_ensure](../modules/hongguo_license_ensure.md) | 285 | 11 |  |  |  | · | Ensure Hongguo 2.x helper is license-proved (same process as hongguo_rpc). Uses DPAPI key  |
| [playlist](../modules/playlist.md) | 214 | 5 |  |  |  | · | playlist.py — Bóc 1 link thành DANH SÁCH video rồi tải hàng loạt. Vì sao tách riêng: Pinel |

## asr (17)

| Module | Dòng | Hàm | Routes | Fix | Test | Manual | Tóm tắt |
|---|---:|---:|---:|---:|---:|:-:|---|
| [fun_asr_nano](../modules/fun_asr_nano.md) | 597 | 11 |  | 3 | ❌ | · | fun_asr_nano.py — STAGE ASR bằng Fun-ASR-Nano (chất lượng tiếng Trung cao nhất). Model : F |
| [separate](../modules/separate.md) | 570 | 18 |  | 5 | 4 | · | separate.py — Tách giọng/nền bằng Demucs (htdemucs --two-stems=vocals). Đầu vào : work/<jo |
| [firered_asr](../modules/firered_asr.md) | 565 | 14 |  | 6 | 2 | · | firered_asr.py — STAGE ASR bằng FireRedASR2-AED (system VAD+LID+ASR+Punc). Cần clone repo  |
| [asr_repair](../modules/asr_repair.md) | 546 | 16 |  | 1 | ❌ | · | asr_repair.py — Hậu kỳ Hybrid: A lấp lỗ + B sửa nghe sai + FA. A) Gap: Para có thoại, bản  |
| [asr](../modules/asr.md) | 488 | 16 |  | 10 | 3 | · | asr.py — STAGE 2 (phần đầu): tách audio + nhận diện lời (Whisper). Đầu vào : work/<job>/so |
| [asr_spam](../modules/asr_spam.md) | 464 | 14 |  |  | ❌ | · | asr_spam.py — Chặn ASR nuốt tiếng nền (cười/rên 哈·啊·呃 lặp). Không dựa vào check tay: sau m |
| [hardsub_asr](../modules/hardsub_asr.md) | 447 | 12 |  | 4 | 2 | · | hardsub_asr.py — OCR hardsub chỉ để RÀ SOÁT / SỬA sub ZH (asr · srt). Một nhiệm vụ: RapidO |
| [asr_align_nano_para](../modules/asr_align_nano_para.md) | 384 | 10 |  |  | ❌ | · | asr_align_nano_para.py — Hybrid A: chữ Fun-ASR-Nano + timestamp Paraformer (char-ts). Đầu  |
| [nano_fa_asr](../modules/nano_fa_asr.md) | 337 | 5 |  | 1 | ❌ | · | nano_fa_asr.py — SOTA ASR: Fun-ASR-Nano (Chữ chuẩn nhất) + Direct Qwen3-ForcedAligner (Mốc |
| [asr_fix_align](../modules/asr_fix_align.md) | 330 | 7 |  | 1 | ❌ | · | asr_fix_align.py — Phương án 3: fix monotonic_fix Bước 1 (fallback): chỗ timing bịa/đảo →  |
| [paraformer_zh](../modules/paraformer_zh.md) | 309 | 2 |  | 2 | ❌ | · | paraformer_zh.py — STAGE ASR bằng FunASR Paraformer-zh (timestamp tốt cho phụ đề/TTS). Mod |
| [ocr](../modules/ocr.md) | 268 | 8 |  | 4 |  | · | ocr.py — STAGE OCR: đọc chữ TRÊN HÌNH (tên nhân vật / địa danh / caption / thẻ) mà KHÔNG n |
| [sensevoice_asr](../modules/sensevoice_asr.md) | 255 | 4 |  | 2 |  | · | sensevoice_asr.py — STAGE ASR bằng FunASR SenseVoiceSmall (nhanh, đa ngôn ngữ). Model : ii |
| [hybrid_asr](../modules/hybrid_asr.md) | 202 | 3 |  |  |  | · | hybrid_asr.py — ASR chốt: Nano chữ + Para timing + ForcedAlign + Repair. Pipeline (sidecar |
| [asr_vad_utils](../modules/asr_vad_utils.md) | 158 | 5 |  |  |  | · | asr_vad_utils.py — VAD kwargs FunASR thật + pad/overlap khi cắt đoạn. FunASR fsmn-vad (1.4 |
| [tools.asr_boundary_scan](../modules/tools.asr_boundary_scan.md) | 146 | 4 |  | 2 |  | · | tools/asr_boundary_scan.py — CHỈ ĐỌC: tìm câu ASR nghi bị cắt ở biên slice cứng k×1200 s.  |
| [asr_hybrid_progress](../modules/asr_hybrid_progress.md) | 144 | 5 |  |  |  | · | asr_hybrid_progress.py — Đưa tiến độ sidecar (Nano/Para) vào stages.asr cho UI Hybrid. UI  |

## translate (27)

| Module | Dòng | Hàm | Routes | Fix | Test | Manual | Tóm tắt |
|---|---:|---:|---:|---:|---:|:-:|---|
| [translate](../modules/translate.md) | 5167 | 104 |  | 27 | 18 | · | translate.py — STAGE dịch: "lập phương án" (hồ sơ nhân vật + XƯNG HÔ) rồi dịch CÓ NGỮ CẢNH |
| [llm](../modules/llm.md) | 1167 | 29 |  | 8 | 11 | · | llm.py — Gọi LLM qua 9router API (tương thích chuẩn OpenAI). Cấu hình qua config.json / pi |
| [pronoun_consistency](../modules/pronoun_consistency.md) | 872 | 30 |  | 2 | 5 | · | Đồng nhất xưng hô không cần diarization (A–C + vá câu đỏ). A) analyze_full_zh: quét TOÀN B |
| [translate_simple.pipeline](../modules/translate_simple.pipeline.md) | 497 | 15 |  | 4 | 6 | · | Điểm vào luồng dịch simple: `run(work_dir, target, *, progress, stop_check) -> dict`. Ghi: |
| [hv_auditor](../modules/hv_auditor.md) | 475 | 15 |  | 1 | ❌ | · | Hán-Việt auditor — chống glossary khóa sai âm (vd 逆→Nghị thay vì Nghịch). 1) Unihan kVietn |
| [translate_alts](../modules/translate_alts.md) | 377 | 5 |  | 1 | ❌ | · | Phương án dịch tối ưu — ngữ cảnh + văn phong (trọng tâm Pineline). Quét câu dễ lệch / đa n |
| [translate_simple.cfg](../modules/translate_simple.cfg.md) | 372 | 46 |  | 6 | 4 | · | Cấu hình luồng simple — mọi khoá prefix SIMPLE_ đọc qua config.get (env > pineline.config. |
| [translate_simple.stage_review](../modules/translate_simple.stage_review.md) | 372 | 9 |  | 2 | 6 | · | Bước 3: REVIEW cloud theo lô — MỘT lần gọi/lô làm hết: sửa nghĩa, áp xưng hô theo cặp plan |
| [translate_simple.zh_source](../modules/translate_simple.zh_source.md) | 353 | 11 |  | 1 | 2 | · | Bước 1 (2026-11-12 next) — chọn NGUỒN chữ ZH cho luồng simple (cờ SIMPLE_ZH_SOURCE=1, mặc  |
| [translate_simple.stage_draft](../modules/translate_simple.stage_draft.md) | 349 | 7 |  | 1 | 4 | · | Bước 2: Plan (cloud) ∥ NMT nháp (GPU) — chạy SONG SONG bằng 2 thread. Plan: dùng lại gloss |
| [pronoun_register_policy](../modules/pronoun_register_policy.md) | 307 | 10 |  | 1 | 2 | · | Policy xưng hô tổng quát cho mix #1+#3 — không gắn 1 job/phim. Mục tiêu: - Phát hiện cửa s |
| [mt_zh_vi](../modules/mt_zh_vi.md) | 302 | 14 |  | 3 | 6 | · | NMT ZH→VI (HachimiMT) — DỊCH CHÍNH; LLM chỉ rà soát (run_review). Config: MT_ZH_VI=1       |
| [translate_simple.pair_rules](../modules/translate_simple.pair_rules.md) | 295 | 15 |  | 1 | 2 | · | Bước 2 (2026-11-12 next) — điền cặp xưng hô CÒN TRỐNG theo bảng quy tắc quan hệ (cờ SIMPLE |
| [translate_simple.zh_ocr_target](../modules/translate_simple.zh_ocr_target.md) | 279 | 11 |  |  |  | · | OCR hardsub CÓ CHỌN LỌC cho luồng simple — SIMPLE_ZH_OCR_MODE=targeted (mặc định) — 2026-1 |
| [translate_simple.validate](../modules/translate_simple.validate.md) | 236 | 8 |  | 2 | 4 | · | Bộ kiểm tất định — chỉ ĐÁNH CỜ, không sửa. Cờ (row["s_flags"] = list mã): empty    vi trốn |
| [translate_simple.plan_view](../modules/translate_simple.plan_view.md) | 215 | 5 |  | 2 | 7 | · | Đọc plan (glossary.json) cho luồng simple: nhân vật, cặp xưng hô, cảnh, thuật ngữ — và khố |
| [series_glossary](../modules/series_glossary.md) | 199 | 11 |  | 6 | 7 | · | Bảng nhân vật / thuật ngữ / xưng hô dùng chung cho CẢ BỘ (mọi mùa). - apply(work_dir, plan |
| [translate_simple.script_store](../modules/translate_simple.script_store.md) | 184 | 3 |  | 1 | 6 | · | Một cửa đọc/ghi script.json + trace.jsonl cho luồng simple. - Ghi atomic (fileio.atomic_wr |
| [title_mt](../modules/title_mt.md) | 172 | 6 |  | 1 |  | · | Dịch thô tiêu đề Trung → Việt (Google gtx, không cần API key). Chỉ để duyệt Hongguo cho bi |
| [script_lint](../modules/script_lint.md) | 170 | 10 |  |  |  | · | Soát lỗi máy móc bản dịch VI (script.json) — chạy SAU review/polish, trước TTS. autofix_ro |
| [translate_simple.pair_fill](../modules/translate_simple.pair_fill.md) | 134 | 6 |  | 1 | 1 | · | Bước 6 (2026-11-12 next) — bổ sung cặp xưng hô THIẾU bằng 1 lần gọi model (cờ SIMPLE_PAIR_ |
| [translate_simple.lexicon](../modules/translate_simple.lexicon.md) | 110 | 4 |  | 2 | 3 | · | Gợi ý thành ngữ / lóng ZH→VI cho prompt review (dò chuỗi con trong ZH của lô). Nguồn: data |
| [translate_simple.suggest](../modules/translate_simple.suggest.md) | 94 | 4 |  | 2 |  | · | Đề xuất cặp xưng hô CHƯA có trong plan (review 2026-11-12) → work_dir/plan_suggestions.jso |
| [translate_simple.post](../modules/translate_simple.post.md) | 76 | 3 |  | 1 | 1 | · | Hậu kỳ tất định của luồng simple — KHÔNG regex đổi đại từ: 1) chuẩn dấu nghìn (translate.n |
| [translate_simple.repair](../modules/translate_simple.repair.md) | 56 | 1 |  |  |  | · | Bước 5: vá ĐÚNG các câu bị bộ kiểm đánh cờ — tối đa SIMPLE_REPAIR_ROUNDS (≤2) lượt. Mỗi lư |
| [translate_simple.gate](../modules/translate_simple.gate.md) | 49 | 1 |  | 1 | 2 | · | Bước 6: cổng của luồng simple (hàm thuần — test được). done  : đủ câu so ASR (translate_co |
| [translate_simple.__init__](../modules/translate_simple.__init__.md) | 17 | 0 |  |  |  | · | translate_simple — luồng dịch ZH→VI gọn (2026-11-12, chủ dự án duyệt). V4 (port 2026-11-12 |

## tts (3)

| Module | Dòng | Hàm | Routes | Fix | Test | Manual | Tóm tắt |
|---|---:|---:|---:|---:|---:|:-:|---|
| [clone_tts](../modules/clone_tts.md) | 1115 | 38 |  | 1 | 1 | · | clone_tts.py — STAGE Lồng tiếng bằng TTS zero-shot clone tiếng Việt. Hai engine, cùng regi |
| [rvc_bridge.vieneu_batch](../modules/rvc_bridge.vieneu_batch.md) | 183 | 5 |  | 1 |  | · | Worker VieNeu-TTS v3-Turbo (chạy trong D:/vieneu_env). Đọc job json: {out_dir, ref, text,  |
| [rvc_bridge.omnivoice_batch](../modules/rvc_bridge.omnivoice_batch.md) | 47 | 1 |  | 1 |  | · | Worker omnivoice-vietnamese (chạy trong D:/OmniVoiceStudio-v2/.venv). Đọc job json: {out_d |

## render (8)

| Module | Dòng | Hàm | Routes | Fix | Test | Manual | Tóm tắt |
|---|---:|---:|---:|---:|---:|:-:|---|
| [render](../modules/render.md) | 3143 | 75 |  | 17 | 5 | · | render.py — STAGE 7 (Ghép + xuất): ráp video lồng tiếng "sạch như bản localize". Video (1  |
| [subs](../modules/subs.md) | 1106 | 34 |  | 1 | ❌ | · | subs.py — Sinh phụ đề .srt từ danh sách câu có timestamp. Dùng chung: asr.json (tiếng Trun |
| [split_parts](../modules/split_parts.md) | 1100 | 27 |  | 11 | 4 | · | split_parts.py — Tự động tính toán và chia video dài (3h-12h+) thành các Part 2-2.5h để ch |
| [media_ts](../modules/media_ts.md) | 1014 | 32 |  | 7 | 3 | · | Mốc thời gian tiếng của file nguồn — sửa tiếng "dồn mẫu" ở file ghép nhiều tập. File ghép  |
| [render_fx](../modules/render_fx.md) | 564 | 32 |  |  | ❌ | · | Helpers: uniqueness filters + library BGM paths (copyright-safe audio). |
| [sfx_lib](../modules/sfx_lib.md) | 438 | 21 |  | 3 | 1 | · | sfx_lib.py — chế độ audio `sfx_lib`: giọng Việt + TIẾNG ĐỘNG gốc + NHẠC KHO SẠCH theo mức. |
| [assemble](../modules/assemble.md) | 417 | 16 |  | 2 | ❌ | · | assemble.py — Ghép clip TTS thành MỘT track + kiểm khớp SRT. Hai chế độ: - assemble()      |
| [mux](../modules/mux.md) | 132 | 5 |  | 6 | 1 | · | mux.py — STAGE cuối: ghép track lồng tiếng vào video -> output.mp4 (thuyết minh). Kiểu thu |

## publish (7)

| Module | Dòng | Hàm | Routes | Fix | Test | Manual | Tóm tắt |
|---|---:|---:|---:|---:|---:|:-:|---|
| [meta_studio](../modules/meta_studio.md) | 2084 | 33 |  | 4 | 2 | · | meta_studio.py — Module sinh Metadata YouTube (Title / Description / Tags / AI Image Promp |
| [auto_publisher](../modules/auto_publisher.md) | 1567 | 36 |  | 5 | 3 | · | auto_publisher.py — Tự động hoá toàn trình: Sau khi render xong → Tự tạo Metadata SEO & Th |
| [test_channel](../modules/test_channel.md) | 1444 | 38 |  | 4 | ❌ | · | test_channel.py — Quản lý Kênh Phụ Test (Burner Channel) độc lập trong Pineline. Chức năng |
| [film_db](../modules/film_db.md) | 1091 | 42 |  | 5 | 3 | · | Database phim đã làm (SQLite) — nguồn sự thật lâu dài, không mất khi xoá thư mục job. film |
| [uploader_settings_api](../modules/uploader_settings_api.md) | 675 | 31 |  | 3 | ❌ | · | Settings + YouTube Uploader API — dùng được từ sidecar :8802 (stdlib) và FastAPI. Trả về ( |
| [canva_client](../modules/canva_client.md) | 394 | 12 |  |  | ❌ | · | canva_client.py — Tích hợp Canva Connect API chính thức cho Pineline. Quản lý OAuth2 (PKCE |
| [films_merge_api](../modules/films_merge_api.md) | 174 | 10 |  | 1 |  | · | Gộp parts (split jobs) + scan job đã làm sẵn sàng merge — dùng từ sidecar :8802. |

## context (9)

| Module | Dòng | Hàm | Routes | Fix | Test | Manual | Tóm tắt |
|---|---:|---:|---:|---:|---:|:-:|---|
| [context_studio.character_mapper](../modules/context_studio.character_mapper.md) | 353 | 10 |  |  | ❌ | · | 02 — Character + relation map: ai tự xưng gì khi nói với ai. |
| [context_studio.address_lexicon](../modules/context_studio.address_lexicon.md) | 338 | 4 |  |  | ❌ | · | Kho xưng hô cổ trang / võ hiệp / tu tiên (VN dịch Trung). Nguồn tham chiếu (quy ước văn họ |
| [context_studio.analyzer](../modules/context_studio.analyzer.md) | 264 | 5 |  |  |  | · | 01 — Context analyzer: SRT Trung → glossary draft (+ style_lock). |
| [context_studio.schema](../modules/context_studio.schema.md) | 129 | 3 |  | 1 |  | · | Heuristic number / name flags — không sửa transcript. |
| [context_studio.app_streamlit](../modules/context_studio.app_streamlit.md) | 108 | 0 |  |  |  | · | Streamlit UI stub — Context Detection trước khi dịch Pineline. Chạy: pip install streamlit |
| [context_studio.srt_io](../modules/context_studio.srt_io.md) | 99 | 4 |  |  |  | · | Parse SRT / asr.json → list[{i, start, end, text}]. |
| [context_studio.exporter](../modules/context_studio.exporter.md) | 73 | 1 |  |  |  | · | 05 — Export context pack vào thư mục job Pineline (hoặc out/). |
| [context_studio.__main__](../modules/context_studio.__main__.md) | 67 | 1 |  |  |  | · | CLI: python -m context_studio analyze <srt/asr.json> -o work/<job> Chỉ PRE-SCAN — không dị |
| [context_studio.__init__](../modules/context_studio.__init__.md) | 6 | 0 |  |  |  | · | Context Studio — PRE-SCAN SRT Trung → context pack cho Pineline dịch. Không dịch. Chỉ phân |

## core (2)

| Module | Dòng | Hàm | Routes | Fix | Test | Manual | Tóm tắt |
|---|---:|---:|---:|---:|---:|:-:|---|
| [core.timeutil](../modules/core.timeutil.md) | 42 | 3 |  |  | 1 | · | core/timeutil.py — MỘT kiểu mốc thời gian cho manifest (port từ V6). Quy ước (fix 2026-11- |
| [core.__init__](../modules/core.__init__.md) | 1 | 0 |  |  |  | · | core/ — tiện ích dùng chung (timeutil, …). Port nhẹ từ V6. |

## ops (24)

| Module | Dòng | Hàm | Routes | Fix | Test | Manual | Tóm tắt |
|---|---:|---:|---:|---:|---:|:-:|---|
| [scripts.setup_machine](../modules/scripts.setup_machine.md) | 1091 | 48 |  |  | ❌ | · | setup_machine.py — Cài Pineline V4 trên MÁY MỚI: detect máy → lập kế hoạch → cài → cấu hìn |
| [scripts.brain_build](../modules/scripts.brain_build.md) | 857 | 23 |  | 1 | ❌ | · | brain_build.py — Sinh/làm mới phần TỰ ĐỘNG của Second Brain (docs/brain/). Đọc mã nguồn bằ |
| [scripts.check_batch4](../modules/scripts.check_batch4.md) | 452 | 6 |  | 2 | ❌ | · | Kiểm thử đợt 4 (tranh chấp ghi manifest, claim endpoint, single-instance, worker khởi động |
| [lib_check](../modules/lib_check.md) | 411 | 9 |  | 1 | ❌ | · | lib_check.py — Kiểm tra bản quyền / Block YouTube cho Phim trong Thư viện gốc (D:\Lib) trư |
| [install](../modules/install.md) | 386 | 16 |  |  | ❌ | · | install.py — Dựng venv + torch + requirements cho Pineline V4 trên BẤT KỲ máy nào. Máy mới |
| [scripts.sync_from_v2](../modules/scripts.sync_from_v2.md) | 368 | 12 |  |  | ❌ | · | sync_from_v2.py — Đồng bộ code từ cây nguồn (V2, bố cục phẳng) sang cây đích. Thay cho việ |
| [check_block](../modules/check_block.md) | 350 | 4 |  |  | ❌ | · | check_block.py — Module kiểm tra trạng thái Bản quyền / Block YouTube (Cơ chế 1: Không cần |
| [scripts.check_batch5](../modules/scripts.check_batch5.md) | 347 | 6 |  | 1 | ❌ | · | Kiểm thử đợt 5 (agent an toàn): lệnh / bắt buộc, phân tầng tool + xác nhận ✅/❌, hg_auto_fl |
| [scripts.check_env](../modules/scripts.check_env.md) | 319 | 15 |  | 1 | ❌ | · | check_env.py — "Doctor" kiểm tra máy trước khi chạy Pineline (máy mới / máy khác cấu hình) |
| [scripts.check_batch2](../modules/scripts.check_batch2.md) | 305 | 9 | 2 | 2 | ❌ | · | Kiểm thử đợt 2 (bảo mật + config 1 nguồn + LLM lỗi dừng stage). KHÔNG chạm server/sidecar  |
| [scripts.check_batch1](../modules/scripts.check_batch1.md) | 294 | 11 |  | 2 |  | · | Test đợt 1 (chặn mất dữ liệu) — chỉ dùng thư mục tạm, không đụng job/queue/thư viện thật. |
| [migrate_work](../modules/migrate_work.md) | 292 | 12 |  | 2 | 1 | · | Chuyển Z:\PinelineV2\work sang ổ khác (mặc định D:\PinelineV2_work) giữa 2 job, không mất  |
| [preset_switcher](../modules/preset_switcher.md) | 242 | 6 |  | 2 | 5 | · | preset_switcher.py — Tự động chuyển đổi Preset Model trên llama-server (:8083) Quản lý bộ  |
| [scripts.tree_audit](../modules/scripts.tree_audit.md) | 226 | 9 |  | 3 |  | · | tree_audit.py — Kiểm tra sức khoẻ cây code Pineline (V2/V4/V5) sau mỗi lần sync/port. Chỉ  |
| [pick_dirs_dialog](../modules/pick_dirs_dialog.md) | 204 | 4 |  |  |  | · | Hộp thoại chọn NHIỀU folder cùng lúc (Listbox multi-select). Chạy: python pick_dirs_dialog |
| [scripts.check_batch3](../modules/scripts.check_batch3.md) | 197 | 1 |  | 3 |  | · | Kiểm thử đợt 3 (opts một nguồn X1, config file-first X2, ghi nguyên tử + khoá S13). Chạy t |
| [check_cookies](../modules/check_cookies.md) | 172 | 5 |  |  |  | · | check_cookies.py — Soi file cookie: còn hạn không, đã ĐĂNG NHẬP chưa, và có lấy được HD kh |
| [scripts.gen_sample_assets](../modules/scripts.gen_sample_assets.md) | 108 | 4 |  |  |  | · | Tạo sample assets cho Pineline (grain / LUT / BGM). Chạy:  python scripts/gen_sample_asset |
| [scripts.test_deepseek_plan](../modules/scripts.test_deepseek_plan.md) | 103 | 3 |  |  |  | · | Thử lập plan cả phim (A7) bằng DeepSeek cho 1 job — KHÔNG đụng job (chạy trên bản sao asr. |
| [vram](../modules/vram.md) | 89 | 4 |  | 1 |  | · | vram.py — Nhả VRAM trước MỖI bước dùng GPU. Ollama (Gemma ctx 128k), FunASR, Demucs, TTS,  |
| [scripts.brain_export](../modules/scripts.brain_export.md) | 67 | 2 |  |  |  | · | brain_export.py — Xuất dữ liệu Second Brain ra JSON gọn cho trang workflow (docs/brain/wor |
| [scripts.build_workflow_html](../modules/scripts.build_workflow_html.md) | 47 | 1 |  |  |  | · | build_workflow_html.py — Dựng docs/brain/workflow.html (trang workflow động) từ brain.json |
| [scripts.check_sidecar_lock](../modules/scripts.check_sidecar_lock.md) | 29 | 0 |  |  |  | · |  |
| [scripts.download_firered_models](../modules/scripts.download_firered_models.md) | 29 | 1 |  |  |  | · | Download FireRedASR2S models into FIRERED_MODELS (default D:/AI_CACHE/firered). |

## misc (9)

| Module | Dòng | Hàm | Routes | Fix | Test | Manual | Tóm tắt |
|---|---:|---:|---:|---:|---:|:-:|---|
| [source_preflight](../modules/source_preflight.md) | 551 | 22 |  | 2 | 1 | · | Preflight + chuẩn hoá video nguồn TRƯỚC asr/separate/ocr/render (2026-11-12, agentK). Vì s |
| [cloud_retry](../modules/cloud_retry.md) | 520 | 16 |  | 2 | 8 | · | cloud_retry.py — fix 2026-11-11 translate-b2 (Việc A): THỬ LẠI model cloud (Aurora/GPT…) k |
| [hs_ocr_fast](../modules/hs_ocr_fast.md) | 407 | 14 |  |  | 2 | · | hs_ocr_fast.py — OCR hardsub NHANH cho luồng simple (SIMPLE_ZH_SOURCE) — fix 2026-11-13. V |
| [lib_normalize](../modules/lib_normalize.md) | 303 | 17 |  |  | 1 | · | Chuẩn hóa video thư viện (D:\Lib\<mùa>) — hàng đợi NỀN trong sidecar :8802 (2026-11-17/18) |
| [machine](../modules/machine.md) | 255 | 24 |  | 4 |  | · | machine.py — Cấu hình PHỤ THUỘC MÁY (cổng dịch vụ ngoài, thư mục model/thư viện, lệnh đổi  |
| [tools.collect_manual_edits](../modules/tools.collect_manual_edits.md) | 192 | 8 |  | 1 |  | · | Gom câu NGƯỜI SỬA TAY (manual) trong work dir thành ỨNG VIÊN golden (định dạng golden V6)  |
| [tools.simple_stats](../modules/tools.simple_stats.md) | 116 | 4 |  | 1 |  | · | Thống kê luồng dịch simple THEO JOB — CHỈ ĐỌC work dir (2026-11-12 next, Bước 8c). Mỗi job |
| [tools.preflight_scan](../modules/tools.preflight_scan.md) | 87 | 2 |  | 2 |  | · | Quét CHỈ-ĐỌC các job trong work dir: nguồn video nào có vấn đề (preflight). Không ghi mani |
| [text_junk](../modules/text_junk.md) | 26 | 1 |  | 2 | 1 | · | Nhận diện câu ASR «rác» (fix 2026-11-13 agentM, sự cố 60892cc63cb7_p01 i=1039 zh="None."). |

## test

| Test | Kiểm module |
|---|---|
| `tests/__init__.py` | — |
| `tests/test_agent_brain_events.py` | [agent_brain](../modules/agent_brain.md), [agent_brain_context](../modules/agent_brain_context.md), [agent_heal](../modules/agent_heal.md) |
| `tests/test_agent_brain_notify.py` | [agent_brain](../modules/agent_brain.md), [agent_brain_notify](../modules/agent_brain_notify.md), [agent_heal](../modules/agent_heal.md), [agent_hold](../modules/agent_hold.md), [agent_watch](../modules/agent_watch.md), [manifest](../modules/manifest.md) |
| `tests/test_agent_core_smoke.py` | [agent_core](../modules/agent_core.md), [manifest](../modules/manifest.md) |
| `tests/test_agent_hold_telegram.py` | [agent_autopilot](../modules/agent_autopilot.md), [agent_hold](../modules/agent_hold.md), [agent_tele_cmd](../modules/agent_tele_cmd.md), [manifest](../modules/manifest.md) |
| `tests/test_agent_parser.py` | [agent_core](../modules/agent_core.md) |
| `tests/test_agent_quality.py` | [agent_quality](../modules/agent_quality.md) |
| `tests/test_agent_tool_loop.py` | [agent_tool_loop](../modules/agent_tool_loop.md) |
| `tests/test_asr_demucs.py` | [asr](../modules/asr.md), [manifest](../modules/manifest.md) |
| `tests/test_auto_publisher_dedup.py` | [auto_publisher](../modules/auto_publisher.md), [film_db](../modules/film_db.md) |
| `tests/test_autosplit_conflict_guards.py` | — |
| `tests/test_brain_finished_hold.py` | [agent_brain](../modules/agent_brain.md), [agent_brain_notify](../modules/agent_brain_notify.md), [agent_heal](../modules/agent_heal.md), [agent_hold](../modules/agent_hold.md) |
| `tests/test_brain_qa_ask.py` | [agent_brain](../modules/agent_brain.md), [agent_core](../modules/agent_core.md), [agent_qa_ask](../modules/agent_qa_ask.md), [agent_quality](../modules/agent_quality.md) |
| `tests/test_brain_qa_fix_retry.py` | [agent_qa_fix](../modules/agent_qa_fix.md), [agent_quality](../modules/agent_quality.md), [agent_retry](../modules/agent_retry.md) |
| `tests/test_brain_qa_hold_timeout.py` | [agent_brain](../modules/agent_brain.md) |
| `tests/test_chatgpt_route.py` | [config](../modules/config.md), [llm](../modules/llm.md), [meta_studio](../modules/meta_studio.md) |
| `tests/test_deepseek_empty_and_brain_idle.py` | [agent_brain](../modules/agent_brain.md), [cloud_retry](../modules/cloud_retry.md), [llm](../modules/llm.md), [translate_simple.stage_draft](../modules/translate_simple.stage_draft.md) |
| `tests/test_extract_pcm_robust.py` | [media_ts](../modules/media_ts.md) |
| `tests/test_extract_pcm_timing.py` | [media_ts](../modules/media_ts.md) |
| `tests/test_firered_slice_silence.py` | [firered_asr](../modules/firered_asr.md), [separate](../modules/separate.md) |
| `tests/test_hardsub_blur_toggle.py` | [batch_config](../modules/batch_config.md), [server](../modules/server.md) |
| `tests/test_hardsub_detection.py` | [render](../modules/render.md) |
| `tests/test_hg_merge_check.py` | [hg_merge_check](../modules/hg_merge_check.md) |
| `tests/test_hg_merge_queue.py` | [hongguo_bridge](../modules/hongguo_bridge.md) |
| `tests/test_job_queue.py` | [job_queue](../modules/job_queue.md) |
| `tests/test_job_queue_worker.py` | [job_queue](../modules/job_queue.md) |
| `tests/test_lib_normalize.py` | [hongguo_bridge](../modules/hongguo_bridge.md), [lib_normalize](../modules/lib_normalize.md) |
| `tests/test_meta_and_thumb.py` | [auto_publisher](../modules/auto_publisher.md), [meta_studio](../modules/meta_studio.md) |
| `tests/test_optimize_b5_b6.py` | [server](../modules/server.md), [translate](../modules/translate.md) |
| `tests/test_parent_rerun_after_done.py` | [agent_heal](../modules/agent_heal.md), [job_queue](../modules/job_queue.md), [render](../modules/render.md), [split_parts](../modules/split_parts.md) |
| `tests/test_park_review_retry.py` | [server](../modules/server.md) |
| `tests/test_pronoun_consistency.py` | [pronoun_consistency](../modules/pronoun_consistency.md) |
| `tests/test_pronoun_postpass.py` | [translate](../modules/translate.md) |
| `tests/test_pronoun_qa_slim_plan.py` | [translate](../modules/translate.md) |
| `tests/test_queue_jobs_api.py` | [server](../modules/server.md) |
| `tests/test_queue_run_one.py` | [server](../modules/server.md) |
| `tests/test_render_expr.py` | [render](../modules/render.md) |
| `tests/test_restart_guard.py` | [migrate_work](../modules/migrate_work.md) |
| `tests/test_review_batches.py` | — |
| `tests/test_review_fail_not_rv.py` | [translate](../modules/translate.md) |
| `tests/test_review_parallel_workers.py` | [translate](../modules/translate.md) |
| `tests/test_review_pass1_upload.py` | [translate](../modules/translate.md) |
| `tests/test_seat_lock_heal.py` | [agent_heal](../modules/agent_heal.md) |
| `tests/test_separate_demucs_chunks.py` | [asr](../modules/asr.md), [manifest](../modules/manifest.md), [separate](../modules/separate.md), [split_parts](../modules/split_parts.md) |
| `tests/test_server_split.py` | [routes_agent](../modules/routes_agent.md), [routes_hg](../modules/routes_hg.md), [server](../modules/server.md) |
| `tests/test_setup_machine.py` | — |
| `tests/test_sfx_lib.py` | [render](../modules/render.md), [sfx_lib](../modules/sfx_lib.md) |
| `tests/test_simple_junk_park.py` | [clone_tts](../modules/clone_tts.md), [firered_asr](../modules/firered_asr.md), [llm](../modules/llm.md), [separate](../modules/separate.md), [split_parts](../modules/split_parts.md), [tests.test_translate_simple](../modules/tests.test_translate_simple.md), [text_junk](../modules/text_junk.md), [translate](../modules/translate.md), [translate_simple.cfg](../modules/translate_simple.cfg.md), [translate_simple.pipeline](../modules/translate_simple.pipeline.md), [translate_simple.plan_view](../modules/translate_simple.plan_view.md), [translate_simple.script_store](../modules/translate_simple.script_store.md), [translate_simple.stage_review](../modules/translate_simple.stage_review.md), [translate_simple.validate](../modules/translate_simple.validate.md) |
| `tests/test_simple_r1_bugs.py` | [core.timeutil](../modules/core.timeutil.md), [translate](../modules/translate.md), [translate_simple.gate](../modules/translate_simple.gate.md), [translate_simple.pipeline](../modules/translate_simple.pipeline.md), [translate_simple.plan_view](../modules/translate_simple.plan_view.md), [translate_simple.script_store](../modules/translate_simple.script_store.md), [translate_simple.stage_draft](../modules/translate_simple.stage_draft.md), [translate_simple.stage_review](../modules/translate_simple.stage_review.md), [translate_simple.validate](../modules/translate_simple.validate.md) |
| `tests/test_source_link.py` | [server](../modules/server.md) |
| `tests/test_split_enospc_guard.py` | [split_parts](../modules/split_parts.md) |
| `tests/test_translate_b1.py` | [agent_hang_fix](../modules/agent_hang_fix.md), [agent_name_pass](../modules/agent_name_pass.md), [agent_pronoun_pass](../modules/agent_pronoun_pass.md), [llm](../modules/llm.md), [mt_zh_vi](../modules/mt_zh_vi.md), [preset_switcher](../modules/preset_switcher.md), [pronoun_consistency](../modules/pronoun_consistency.md), [pronoun_register_policy](../modules/pronoun_register_policy.md), [series_glossary](../modules/series_glossary.md), [translate](../modules/translate.md) |
| `tests/test_translate_b1_scenarios.py` | [agent_hang_fix](../modules/agent_hang_fix.md), [llm](../modules/llm.md), [mt_zh_vi](../modules/mt_zh_vi.md), [preset_switcher](../modules/preset_switcher.md), [pronoun_consistency](../modules/pronoun_consistency.md), [pronoun_register_policy](../modules/pronoun_register_policy.md), [series_glossary](../modules/series_glossary.md), [translate](../modules/translate.md) |
| `tests/test_translate_b2.py` | [agent_hang_fix](../modules/agent_hang_fix.md), [cloud_retry](../modules/cloud_retry.md), [llm](../modules/llm.md), [mt_zh_vi](../modules/mt_zh_vi.md), [preset_switcher](../modules/preset_switcher.md), [pronoun_consistency](../modules/pronoun_consistency.md), [series_glossary](../modules/series_glossary.md), [translate](../modules/translate.md) |
| `tests/test_translate_b2_review.py` | [agent_hang_fix](../modules/agent_hang_fix.md), [cloud_retry](../modules/cloud_retry.md), [llm](../modules/llm.md), [mt_zh_vi](../modules/mt_zh_vi.md), [preset_switcher](../modules/preset_switcher.md), [pronoun_consistency](../modules/pronoun_consistency.md), [tests.test_translate_b2](../modules/tests.test_translate_b2.md), [translate](../modules/translate.md) |
| `tests/test_translate_b3.py` | [cloud_retry](../modules/cloud_retry.md), [mt_zh_vi](../modules/mt_zh_vi.md), [tests.test_translate_b2](../modules/tests.test_translate_b2.md), [tests.test_translate_b2_review](../modules/tests.test_translate_b2_review.md), [translate](../modules/translate.md) |
| `tests/test_translate_missing.py` | [translate](../modules/translate.md) |
| `tests/test_translate_simple.py` | [agent_name_pass](../modules/agent_name_pass.md), [agent_pronoun_pass](../modules/agent_pronoun_pass.md), [cloud_retry](../modules/cloud_retry.md), [config](../modules/config.md), [llm](../modules/llm.md), [mt_zh_vi](../modules/mt_zh_vi.md), [preset_switcher](../modules/preset_switcher.md), [series_glossary](../modules/series_glossary.md), [translate](../modules/translate.md), [translate_simple.cfg](../modules/translate_simple.cfg.md), [translate_simple.gate](../modules/translate_simple.gate.md), [translate_simple.lexicon](../modules/translate_simple.lexicon.md), [translate_simple.pipeline](../modules/translate_simple.pipeline.md), [translate_simple.plan_view](../modules/translate_simple.plan_view.md), [translate_simple.script_store](../modules/translate_simple.script_store.md), [translate_simple.stage_draft](../modules/translate_simple.stage_draft.md), [translate_simple.stage_review](../modules/translate_simple.stage_review.md), [translate_simple.validate](../modules/translate_simple.validate.md) |
| `tests/test_translate_simple_a7_a8.py` | [translate_simple.cfg](../modules/translate_simple.cfg.md), [translate_simple.plan_view](../modules/translate_simple.plan_view.md), [translate_simple.script_store](../modules/translate_simple.script_store.md), [translate_simple.stage_draft](../modules/translate_simple.stage_draft.md), [translate_simple.stage_review](../modules/translate_simple.stage_review.md) |
| `tests/test_translate_simple_next.py` | [cloud_retry](../modules/cloud_retry.md), [hardsub_asr](../modules/hardsub_asr.md), [hs_ocr_fast](../modules/hs_ocr_fast.md), [llm](../modules/llm.md), [series_glossary](../modules/series_glossary.md), [tests.test_translate_simple](../modules/tests.test_translate_simple.md), [translate](../modules/translate.md), [translate_simple.cfg](../modules/translate_simple.cfg.md), [translate_simple.lexicon](../modules/translate_simple.lexicon.md), [translate_simple.pair_fill](../modules/translate_simple.pair_fill.md), [translate_simple.pair_rules](../modules/translate_simple.pair_rules.md), [translate_simple.pipeline](../modules/translate_simple.pipeline.md), [translate_simple.plan_view](../modules/translate_simple.plan_view.md), [translate_simple.stage_review](../modules/translate_simple.stage_review.md), [translate_simple.zh_source](../modules/translate_simple.zh_source.md) |
| `tests/test_translate_simple_next_review.py` | [cloud_retry](../modules/cloud_retry.md), [film_db](../modules/film_db.md), [hardsub_asr](../modules/hardsub_asr.md), [hs_ocr_fast](../modules/hs_ocr_fast.md), [llm](../modules/llm.md), [series_glossary](../modules/series_glossary.md), [tests](../modules/tests.md), [tests.test_translate_simple](../modules/tests.test_translate_simple.md), [tests.test_translate_simple_next](../modules/tests.test_translate_simple_next.md), [translate](../modules/translate.md), [translate_simple.pair_rules](../modules/translate_simple.pair_rules.md), [translate_simple.pipeline](../modules/translate_simple.pipeline.md), [translate_simple.plan_view](../modules/translate_simple.plan_view.md), [translate_simple.post](../modules/translate_simple.post.md), [translate_simple.script_store](../modules/translate_simple.script_store.md), [translate_simple.zh_source](../modules/translate_simple.zh_source.md) |
| `tests/test_translate_simple_scenarios.py` | [cloud_retry](../modules/cloud_retry.md), [film_db](../modules/film_db.md), [llm](../modules/llm.md), [series_glossary](../modules/series_glossary.md), [tests.test_translate_simple](../modules/tests.test_translate_simple.md), [translate](../modules/translate.md), [translate_simple.lexicon](../modules/translate_simple.lexicon.md), [translate_simple.pipeline](../modules/translate_simple.pipeline.md), [translate_simple.plan_view](../modules/translate_simple.plan_view.md), [translate_simple.script_store](../modules/translate_simple.script_store.md), [translate_simple.stage_review](../modules/translate_simple.stage_review.md), [translate_simple.validate](../modules/translate_simple.validate.md) |
| `tests/test_upload_limit_stop.py` | [auto_publisher](../modules/auto_publisher.md) |
| `tests/test_video_preflight.py` | [asr](../modules/asr.md), [manifest](../modules/manifest.md), [media_ts](../modules/media_ts.md), [mux](../modules/mux.md), [render](../modules/render.md), [separate](../modules/separate.md), [server](../modules/server.md), [source_preflight](../modules/source_preflight.md) |
