# Index module

_Sinh tự động bởi `scripts/brain_build.py` lúc 2026-11-11 02:37. Đừng sửa tay — chạy lại script._


Tổng: **108 module** (+27 test), **67,021 dòng**. Cột *Manual* = thẻ đã có phần viết tay (✅) hay chưa (·).

## control (13)

| Module | Dòng | Hàm | Routes | Fix | Test | Manual | Tóm tắt |
|---|---:|---:|---:|---:|---:|:-:|---|
| [server](../modules/server.md) | 6644 | 176 | 68 | 31 | 6 | · | server.py — Backend web Phase 1 (FastAPI). Bọc engine (download -> asr -> translate) thành |
| [routes_hg](../modules/routes_hg.md) | 1018 | 56 | 58 | 6 | 1 | · | Cầu nối Hongguo Downloader (local :8000): /api/hg/*. Tách từ server.py (đợt 7). Chỉ được n |
| [job_queue](../modules/job_queue.md) | 658 | 32 |  | 9 | 2 | ✅ |  |
| [routes_agent](../modules/routes_agent.md) | 645 | 40 | 16 | 4 | 1 | · | AI Agent nhúng (agent_core): hook cho Runtime + /api/agent/*. Tách từ server.py (đợt 7). C |
| [routes_uploader_settings](../modules/routes_uploader_settings.md) | 607 | 23 | 31 | 2 | ❌ | · | routes_uploader_settings.py — API Router cho Quản lý Cài đặt (Settings) & YouTube Uploader |
| [routes_films](../modules/routes_films.md) | 370 | 31 | 31 | 1 | ❌ | · | FastAPI Router cho Thư viện Phim & Database (đồng bộ trực tiếp trong Pineline V4). Thay vì |
| [batch_config](../modules/batch_config.md) | 295 | 14 |  | 4 | 1 | · | Cấu hình batch dùng chung — 1 nguồn duy nhất cho Auto-pilot, Agent (queue_add), Telegram ( |
| [manifest](../modules/manifest.md) | 242 | 4 |  | 2 | 2 | ✅ | manifest.py — Trạng thái/checkpoint cho pipeline. Mỗi job (mỗi video) có một thư mục làm v |
| [restart_server](../modules/restart_server.md) | 237 | 8 |  | 7 |  | · | Restart server Pineline (giữ sidecar), khôi phục hàng đợi + Auto-pilot. Port mặc định V4:  |
| [config](../modules/config.md) | 188 | 8 |  | 3 | 1 | ✅ | config.py — Cấu hình/đường dẫn PORTABLE cho Pineline. Thứ tự ưu tiên khi lấy 1 giá trị: bi |
| [app_desktop](../modules/app_desktop.md) | 147 | 4 |  |  |  | · | app_desktop.py — Desktop App Studio cho Pineline V4. Sử dụng Microsoft Edge WebView2 (nati |
| [routes_ui](../modules/routes_ui.md) | 107 | 10 | 14 | 2 |  | · | Trang UI: /, /ui3, /ui4, /hongguo, /hongguo2, /films/ui, /studio, /v5-map. /hongguo2 = ski |
| [fileio](../modules/fileio.md) | 104 | 4 |  | 2 |  | · | Ghi file an toàn giữa nhiều tiến trình (server :8801, sidecar :8802, script). atomic_write |

## agent (15)

| Module | Dòng | Hàm | Routes | Fix | Test | Manual | Tóm tắt |
|---|---:|---:|---:|---:|---:|:-:|---|
| [agent_core](../modules/agent_core.md) | 2072 | 30 |  | 6 | 2 | · | agent_core.py — AI Agent nhúng trong Pineline V2. Không gọi HTTP self. Tools gọi runtime đ |
| [agent_hongguo](../modules/agent_hongguo.md) | 1570 | 36 |  | 3 | ❌ | · | agent_hongguo.py — Tích hợp bộ tool Hongguo Downloader & Auto-chain cho Pineline AI Agent. |
| [agent_brain](../modules/agent_brain.md) | 1230 | 35 |  | 3 | ❌ | · | Second Brain — daemon nền full-silent. Sensors → incidents → policy → actuators. Bật: AGEN |
| [agent_heal](../modules/agent_heal.md) | 665 | 10 |  | 1 | ❌ | · | agent_heal.py — Chẩn đoán + heal job lỗi (an toàn theo cấp). safe: heal stale running, vá  |
| [agent_av_sync](../modules/agent_av_sync.md) | 567 | 11 |  | 3 | ❌ | · | AV sync diagnose + heal — phát hiện lệch sub/audio / audio cụt sau mux. Các class chính: a |
| [agent_tool_loop](../modules/agent_tool_loop.md) | 475 | 11 |  |  | ❌ | · | Tool loop — điều khiển pipeline theo bước, chờ kết quả thật. Khác `pineline_run_stage` (fi |
| [agent_watch](../modules/agent_watch.md) | 375 | 19 |  | 1 | ❌ | · | Watcher A: định kỳ scan → heal safe + log + Telegram (tuỳ chọn). Env: AGENT_WATCH=1 |
| [agent_hang_fix](../modules/agent_hang_fix.md) | 368 | 9 |  | 2 | ❌ | · | Second Brain — pass LLM trace + xử lý high `hang` (đuôi treo / nửa câu). Không chỉ merge m |
| [agent_quality](../modules/agent_quality.md) | 356 | 6 |  | 1 | 1 | · | Deterministic VI quality scan + safe heals (Second Brain L2). Port từ D:\PinelineV2_tmp\_q |
| [agent_stage_io](../modules/agent_stage_io.md) | 286 | 14 |  |  |  | · | Peek / tóm tắt từng stage — chỉ đọc disk (an toàn). |
| [agent_brain_context](../modules/agent_brain_context.md) | 266 | 6 |  |  |  | · | System snapshot cho Second Brain LLM — toàn hệ, không chỉ 1 job. |
| [agent_pronoun_pass](../modules/agent_pronoun_pass.md) | 256 | 4 |  | 3 |  | · | Rà XƯNG HÔ trong bản dịch theo glossary.pronouns + genre. 1. Quét deterministic (cùng appl |
| [agent_qa_gate](../modules/agent_qa_gate.md) | 226 | 8 |  |  |  | · | Gate QA: translate → review → diff → mới cho TTS. |
| [agent_name_pass](../modules/agent_name_pass.md) | 134 | 5 |  | 1 |  | · | Rà TÊN NHÂN VẬT trong bản dịch theo bảng nhân vật (glossary.json). 1. Quét: câu nào zh có  |
| [agent_error_class](../modules/agent_error_class.md) | 121 | 3 |  |  |  | · | Phân loại lỗi theo log / cur_text / error (ASR · TTS · mux · …). |

## sidecar (3)

| Module | Dòng | Hàm | Routes | Fix | Test | Manual | Tóm tắt |
|---|---:|---:|---:|---:|---:|:-:|---|
| [agent_tele_cmd](../modules/agent_tele_cmd.md) | 2333 | 37 |  | 11 | ❌ | · | Sidecar: Telegram lệnh + Auto-pilot + HTTP :8802 KHÔNG restart Pineline server — chỉ gọi A |
| [agent_feeder](../modules/agent_feeder.md) | 2065 | 68 |  | 7 | ❌ | · | Feeder + Run-watch cho Auto-pilot (chạy trong sidecar :8802, chỉ gọi API :8801). Feeder —  |
| [agent_autopilot](../modules/agent_autopilot.md) | 331 | 16 |  | 4 | ❌ | · | Auto-pilot — queue need_queue + heal safe qua HTTP Pineline (PORT / PINELINE_BASE). Chạy t |

## source (6)

| Module | Dòng | Hàm | Routes | Fix | Test | Manual | Tóm tắt |
|---|---:|---:|---:|---:|---:|:-:|---|
| [hongguo_bridge](../modules/hongguo_bridge.md) | 4216 | 118 |  | 15 | 1 | · | hongguo_bridge.py — client mỏng gọi Hongguo Downloader local API (:8000). App Hongguo phải |
| [hongguo_rpc](../modules/hongguo_rpc.md) | 1449 | 57 |  | 10 | ❌ | · | hongguo_rpc.py — JSON-RPC stdio client cho Hongguo WinUI 2.x helper.jar. Không dùng HTTP : |
| [download](../modules/download.md) | 692 | 20 |  | 2 | ❌ | · | download.py — STAGE 1: Tải video (Douyin / Bilibili / TikTok / ...). Engine: yt-dlp. Tự re |
| [hongguo_license_ensure](../modules/hongguo_license_ensure.md) | 285 | 11 |  |  |  | · | Ensure Hongguo 2.x helper is license-proved (same process as hongguo_rpc). Uses DPAPI key  |
| [playlist](../modules/playlist.md) | 214 | 5 |  |  |  | · | playlist.py — Bóc 1 link thành DANH SÁCH video rồi tải hàng loạt. Vì sao tách riêng: Pinel |
| [hg_ui_ctx](../modules/hg_ui_ctx.md) | 46 | 4 |  | 2 |  | · | Per-request Hongguo UI backend context (không reload — tránh mất override). Hongguo1 vs Ho |

## asr (16)

| Module | Dòng | Hàm | Routes | Fix | Test | Manual | Tóm tắt |
|---|---:|---:|---:|---:|---:|:-:|---|
| [fun_asr_nano](../modules/fun_asr_nano.md) | 597 | 11 |  | 1 | ❌ | · | fun_asr_nano.py — STAGE ASR bằng Fun-ASR-Nano (chất lượng tiếng Trung cao nhất). Model : F |
| [asr_repair](../modules/asr_repair.md) | 546 | 16 |  |  | ❌ | · | asr_repair.py — Hậu kỳ Hybrid: A lấp lỗ + B sửa nghe sai + FA. A) Gap: Para có thoại, bản  |
| [asr_spam](../modules/asr_spam.md) | 464 | 14 |  |  | ❌ | · | asr_spam.py — Chặn ASR nuốt tiếng nền (cười/rên 哈·啊·呃 lặp). Không dựa vào check tay: sau m |
| [hardsub_asr](../modules/hardsub_asr.md) | 452 | 12 |  |  | ❌ | · | hardsub_asr.py — OCR hardsub chỉ để RÀ SOÁT / SỬA sub ZH (asr · srt). Một nhiệm vụ: RapidO |
| [asr](../modules/asr.md) | 442 | 13 |  | 2 | 1 | · | asr.py — STAGE 2 (phần đầu): tách audio + nhận diện lời (Whisper). Đầu vào : work/<job>/so |
| [asr_align_nano_para](../modules/asr_align_nano_para.md) | 384 | 10 |  |  | ❌ | · | asr_align_nano_para.py — Hybrid A: chữ Fun-ASR-Nano + timestamp Paraformer (char-ts). Đầu  |
| [separate](../modules/separate.md) | 370 | 8 |  |  | ❌ | · | separate.py — STAGE 6 (Tách nền): dùng Demucs bỏ GIỌNG NÓI (tiếng Trung) khỏi audio gốc, G |
| [firered_asr](../modules/firered_asr.md) | 340 | 5 |  | 2 | ❌ | · | firered_asr.py — STAGE ASR bằng FireRedASR2-AED (system VAD+LID+ASR+Punc). Cần clone repo  |
| [nano_fa_asr](../modules/nano_fa_asr.md) | 337 | 5 |  |  | ❌ | · | nano_fa_asr.py — SOTA ASR: Fun-ASR-Nano (Chữ chuẩn nhất) + Direct Qwen3-ForcedAligner (Mốc |
| [asr_fix_align](../modules/asr_fix_align.md) | 330 | 7 |  |  | ❌ | · | asr_fix_align.py — Phương án 3: fix monotonic_fix Bước 1 (fallback): chỗ timing bịa/đảo →  |
| [paraformer_zh](../modules/paraformer_zh.md) | 309 | 2 |  | 1 | ❌ | · | paraformer_zh.py — STAGE ASR bằng FunASR Paraformer-zh (timestamp tốt cho phụ đề/TTS). Mod |
| [ocr](../modules/ocr.md) | 273 | 8 |  |  |  | · | ocr.py — STAGE OCR: đọc chữ TRÊN HÌNH (tên nhân vật / địa danh / caption / thẻ) mà KHÔNG n |
| [sensevoice_asr](../modules/sensevoice_asr.md) | 255 | 4 |  | 1 |  | · | sensevoice_asr.py — STAGE ASR bằng FunASR SenseVoiceSmall (nhanh, đa ngôn ngữ). Model : ii |
| [hybrid_asr](../modules/hybrid_asr.md) | 202 | 3 |  |  |  | · | hybrid_asr.py — ASR chốt: Nano chữ + Para timing + ForcedAlign + Repair. Pipeline (sidecar |
| [asr_vad_utils](../modules/asr_vad_utils.md) | 158 | 5 |  |  |  | · | asr_vad_utils.py — VAD kwargs FunASR thật + pad/overlap khi cắt đoạn. FunASR fsmn-vad (1.4 |
| [asr_hybrid_progress](../modules/asr_hybrid_progress.md) | 144 | 5 |  |  |  | · | asr_hybrid_progress.py — Đưa tiến độ sidecar (Nano/Para) vào stages.asr cho UI Hybrid. UI  |

## translate (10)

| Module | Dòng | Hàm | Routes | Fix | Test | Manual | Tóm tắt |
|---|---:|---:|---:|---:|---:|:-:|---|
| [translate](../modules/translate.md) | 4128 | 74 |  | 21 | 5 | · | translate.py — STAGE dịch: "lập phương án" (hồ sơ nhân vật + XƯNG HÔ) rồi dịch CÓ NGỮ CẢNH |
| [llm](../modules/llm.md) | 894 | 23 |  | 5 | 1 | · | llm.py — Gọi LLM qua 9router API (tương thích chuẩn OpenAI). Cấu hình qua config.json / pi |
| [pronoun_consistency](../modules/pronoun_consistency.md) | 870 | 30 |  | 2 | 1 | · | Đồng nhất xưng hô không cần diarization (A–C + vá câu đỏ). A) analyze_full_zh: quét TOÀN B |
| [hv_auditor](../modules/hv_auditor.md) | 475 | 15 |  | 1 | ❌ | · | Hán-Việt auditor — chống glossary khóa sai âm (vd 逆→Nghị thay vì Nghịch). 1) Unihan kVietn |
| [translate_alts](../modules/translate_alts.md) | 377 | 5 |  | 1 | ❌ | · | Phương án dịch tối ưu — ngữ cảnh + văn phong (trọng tâm Pineline). Quét câu dễ lệch / đa n |
| [mt_zh_vi](../modules/mt_zh_vi.md) | 302 | 14 |  | 1 | ❌ | · | NMT ZH→VI (HachimiMT) — DỊCH CHÍNH; LLM chỉ rà soát (run_review). Config: MT_ZH_VI=1       |
| [pronoun_register_policy](../modules/pronoun_register_policy.md) | 243 | 8 |  | 1 |  | · | Policy xưng hô tổng quát cho mix #1+#3 — không gắn 1 job/phim. Mục tiêu: - Phát hiện cửa s |
| [series_glossary](../modules/series_glossary.md) | 199 | 11 |  | 4 |  | · | Bảng nhân vật / thuật ngữ / xưng hô dùng chung cho CẢ BỘ (mọi mùa). - apply(work_dir, plan |
| [title_mt](../modules/title_mt.md) | 172 | 6 |  | 1 |  | · | Dịch thô tiêu đề Trung → Việt (Google gtx, không cần API key). Chỉ để duyệt Hongguo cho bi |
| [script_lint](../modules/script_lint.md) | 170 | 10 |  |  |  | · | Soát lỗi máy móc bản dịch VI (script.json) — chạy SAU review/polish, trước TTS. autofix_ro |

## tts (3)

| Module | Dòng | Hàm | Routes | Fix | Test | Manual | Tóm tắt |
|---|---:|---:|---:|---:|---:|:-:|---|
| [clone_tts](../modules/clone_tts.md) | 1115 | 38 |  | 1 | ❌ | · | clone_tts.py — STAGE Lồng tiếng bằng TTS zero-shot clone tiếng Việt. Hai engine, cùng regi |
| [rvc_bridge.vieneu_batch](../modules/rvc_bridge.vieneu_batch.md) | 183 | 5 |  | 1 |  | · | Worker VieNeu-TTS v3-Turbo (chạy trong D:/vieneu_env). Đọc job json: {out_dir, ref, text,  |
| [rvc_bridge.omnivoice_batch](../modules/rvc_bridge.omnivoice_batch.md) | 47 | 1 |  | 1 |  | · | Worker omnivoice-vietnamese (chạy trong D:/OmniVoiceStudio-v2/.venv). Đọc job json: {out_d |

## render (8)

| Module | Dòng | Hàm | Routes | Fix | Test | Manual | Tóm tắt |
|---|---:|---:|---:|---:|---:|:-:|---|
| [render](../modules/render.md) | 3061 | 72 |  | 15 | 2 | · | render.py — STAGE 7 (Ghép + xuất): ráp video lồng tiếng "sạch như bản localize". Video (1  |
| [subs](../modules/subs.md) | 1106 | 34 |  |  | ❌ | · | subs.py — Sinh phụ đề .srt từ danh sách câu có timestamp. Dùng chung: asr.json (tiếng Trun |
| [split_parts](../modules/split_parts.md) | 828 | 17 |  | 6 | ❌ | · | split_parts.py — Tự động tính toán và chia video dài (3h-12h+) thành các Part 2-2.5h để ch |
| [render_fx](../modules/render_fx.md) | 564 | 32 |  |  | ❌ | · | Helpers: uniqueness filters + library BGM paths (copyright-safe audio). |
| [sfx_lib](../modules/sfx_lib.md) | 438 | 21 |  | 1 | 1 | · | sfx_lib.py — chế độ audio `sfx_lib`: giọng Việt + TIẾNG ĐỘNG gốc + NHẠC KHO SẠCH theo mức. |
| [assemble](../modules/assemble.md) | 417 | 16 |  | 2 | ❌ | · | assemble.py — Ghép clip TTS thành MỘT track + kiểm khớp SRT. Hai chế độ: - assemble()      |
| [media_ts](../modules/media_ts.md) | 304 | 14 |  | 3 | ❌ | · | Mốc thời gian tiếng của file nguồn — sửa tiếng "dồn mẫu" ở file ghép nhiều tập. File ghép  |
| [mux](../modules/mux.md) | 135 | 5 |  | 3 |  | · | mux.py — STAGE cuối: ghép track lồng tiếng vào video -> output.mp4 (thuyết minh). Kiểu thu |

## publish (7)

| Module | Dòng | Hàm | Routes | Fix | Test | Manual | Tóm tắt |
|---|---:|---:|---:|---:|---:|:-:|---|
| [meta_studio](../modules/meta_studio.md) | 1918 | 32 |  | 2 | 1 | · | meta_studio.py — Module sinh Metadata YouTube (Title / Description / Tags / AI Image Promp |
| [auto_publisher](../modules/auto_publisher.md) | 1567 | 36 |  | 4 | 2 | · | auto_publisher.py — Tự động hoá toàn trình: Sau khi render xong → Tự tạo Metadata SEO & Th |
| [test_channel](../modules/test_channel.md) | 1435 | 38 |  | 3 | ❌ | · | test_channel.py — Quản lý Kênh Phụ Test (Burner Channel) độc lập trong Pineline. Chức năng |
| [film_db](../modules/film_db.md) | 1091 | 42 |  | 4 | 1 | · | Database phim đã làm (SQLite) — nguồn sự thật lâu dài, không mất khi xoá thư mục job. film |
| [uploader_settings_api](../modules/uploader_settings_api.md) | 670 | 31 |  | 2 | ❌ | · | Settings + YouTube Uploader API — dùng được từ sidecar :8802 (stdlib) và FastAPI. Trả về ( |
| [canva_client](../modules/canva_client.md) | 406 | 12 |  |  | ❌ | · | canva_client.py — Tích hợp Canva Connect API chính thức cho Pineline. Quản lý OAuth2 (PKCE |
| [films_merge_api](../modules/films_merge_api.md) | 174 | 10 |  | 1 |  | · | Gộp parts (split jobs) + scan job đã làm sẵn sàng merge — dùng từ sidecar :8802. |

## context (9)

| Module | Dòng | Hàm | Routes | Fix | Test | Manual | Tóm tắt |
|---|---:|---:|---:|---:|---:|:-:|---|
| [context_studio.character_mapper](../modules/context_studio.character_mapper.md) | 353 | 10 |  |  | ❌ | · | 02 — Character + relation map: ai tự xưng gì khi nói với ai. |
| [context_studio.address_lexicon](../modules/context_studio.address_lexicon.md) | 338 | 4 |  |  | ❌ | · | Kho xưng hô cổ trang / võ hiệp / tu tiên (VN dịch Trung). Nguồn tham chiếu (quy ước văn họ |
| [context_studio.analyzer](../modules/context_studio.analyzer.md) | 264 | 5 |  |  |  | · | 01 — Context analyzer: SRT Trung → glossary draft (+ style_lock). |
| [context_studio.schema](../modules/context_studio.schema.md) | 129 | 3 |  |  |  | · | Heuristic number / name flags — không sửa transcript. |
| [context_studio.app_streamlit](../modules/context_studio.app_streamlit.md) | 108 | 0 |  |  |  | · | Streamlit UI stub — Context Detection trước khi dịch Pineline. Chạy: pip install streamlit |
| [context_studio.srt_io](../modules/context_studio.srt_io.md) | 99 | 4 |  |  |  | · | Parse SRT / asr.json → list[{i, start, end, text}]. |
| [context_studio.exporter](../modules/context_studio.exporter.md) | 73 | 1 |  |  |  | · | 05 — Export context pack vào thư mục job Pineline (hoặc out/). |
| [context_studio.__main__](../modules/context_studio.__main__.md) | 67 | 1 |  |  |  | · | CLI: python -m context_studio analyze <srt/asr.json> -o work/<job> Chỉ PRE-SCAN — không dị |
| [context_studio.__init__](../modules/context_studio.__init__.md) | 6 | 0 |  |  |  | · | Context Studio — PRE-SCAN SRT Trung → context pack cho Pineline dịch. Không dịch. Chỉ phân |

## ops (18)

| Module | Dòng | Hàm | Routes | Fix | Test | Manual | Tóm tắt |
|---|---:|---:|---:|---:|---:|:-:|---|
| [scripts.brain_build](../modules/scripts.brain_build.md) | 857 | 23 |  |  | ❌ | · | brain_build.py — Sinh/làm mới phần TỰ ĐỘNG của Second Brain (docs/brain/). Đọc mã nguồn bằ |
| [scripts.check_batch4](../modules/scripts.check_batch4.md) | 452 | 6 |  | 2 | ❌ | · | Kiểm thử đợt 4 (tranh chấp ghi manifest, claim endpoint, single-instance, worker khởi động |
| [lib_check](../modules/lib_check.md) | 411 | 9 |  |  | ❌ | · | lib_check.py — Kiểm tra bản quyền / Block YouTube cho Phim trong Thư viện gốc (D:\Lib) trư |
| [check_block](../modules/check_block.md) | 350 | 4 |  |  | ❌ | · | check_block.py — Module kiểm tra trạng thái Bản quyền / Block YouTube (Cơ chế 1: Không cần |
| [scripts.check_batch5](../modules/scripts.check_batch5.md) | 347 | 6 |  | 1 | ❌ | · | Kiểm thử đợt 5 (agent an toàn): lệnh / bắt buộc, phân tầng tool + xác nhận ✅/❌, hg_auto_fl |
| [scripts.check_batch2](../modules/scripts.check_batch2.md) | 305 | 9 | 2 | 2 | ❌ | · | Kiểm thử đợt 2 (bảo mật + config 1 nguồn + LLM lỗi dừng stage). KHÔNG chạm server/sidecar  |
| [migrate_work](../modules/migrate_work.md) | 296 | 12 |  | 1 | 1 | · | Chuyển Z:\PinelineV4\work sang ổ khác (mặc định D:\PinelineV4_work) giữa 2 job, không mất  |
| [scripts.check_batch1](../modules/scripts.check_batch1.md) | 294 | 11 |  | 2 |  | · | Test đợt 1 (chặn mất dữ liệu) — chỉ dùng thư mục tạm, không đụng job/queue/thư viện thật. |
| [install](../modules/install.md) | 241 | 11 |  |  |  | · | install.py — Bộ cài Pineline TỰ DETECT máy + dựng môi trường trên BẤT KỲ máy nào. Chạy:  p |
| [scripts.tree_audit](../modules/scripts.tree_audit.md) | 226 | 9 |  |  |  | · | tree_audit.py — Kiểm tra sức khoẻ cây code Pineline (V2/V4/V5) sau mỗi lần sync/port. Chỉ  |
| [preset_switcher](../modules/preset_switcher.md) | 225 | 5 |  |  |  | · | preset_switcher.py — Tự động chuyển đổi Preset Model trên llama-server (:8083) Quản lý bộ  |
| [pick_dirs_dialog](../modules/pick_dirs_dialog.md) | 204 | 4 |  |  |  | · | Hộp thoại chọn NHIỀU folder cùng lúc (Listbox multi-select). Chạy: python pick_dirs_dialog |
| [scripts.check_batch3](../modules/scripts.check_batch3.md) | 197 | 1 |  | 3 |  | · | Kiểm thử đợt 3 (opts một nguồn X1, config file-first X2, ghi nguyên tử + khoá S13). Chạy t |
| [check_cookies](../modules/check_cookies.md) | 172 | 5 |  |  |  | · | check_cookies.py — Soi file cookie: còn hạn không, đã ĐĂNG NHẬP chưa, và có lấy được HD kh |
| [scripts.gen_sample_assets](../modules/scripts.gen_sample_assets.md) | 108 | 4 |  |  |  | · | Tạo sample assets cho Pineline (grain / LUT / BGM). Chạy:  python scripts/gen_sample_asset |
| [vram](../modules/vram.md) | 89 | 4 |  |  |  | · | vram.py — Nhả VRAM trước MỖI bước dùng GPU. Ollama (Gemma ctx 128k), FunASR, Demucs, TTS,  |
| [scripts.check_sidecar_lock](../modules/scripts.check_sidecar_lock.md) | 29 | 0 |  |  |  | · |  |
| [scripts.download_firered_models](../modules/scripts.download_firered_models.md) | 29 | 1 |  |  |  | · | Download FireRedASR2S models into FIRERED_MODELS (default D:/AI_CACHE/firered). |

## test

| Test | Kiểm module |
|---|---|
| `tests/__init__.py` | — |
| `tests/test_agent_core_smoke.py` | [agent_core](../modules/agent_core.md), [manifest](../modules/manifest.md) |
| `tests/test_agent_parser.py` | [agent_core](../modules/agent_core.md) |
| `tests/test_agent_quality.py` | [agent_quality](../modules/agent_quality.md) |
| `tests/test_asr_demucs.py` | [asr](../modules/asr.md), [manifest](../modules/manifest.md) |
| `tests/test_auto_publisher_dedup.py` | [auto_publisher](../modules/auto_publisher.md), [film_db](../modules/film_db.md) |
| `tests/test_chatgpt_route.py` | [config](../modules/config.md), [llm](../modules/llm.md) |
| `tests/test_hardsub_blur_toggle.py` | [batch_config](../modules/batch_config.md), [server](../modules/server.md) |
| `tests/test_hg_merge_queue.py` | [hongguo_bridge](../modules/hongguo_bridge.md) |
| `tests/test_job_queue.py` | [job_queue](../modules/job_queue.md) |
| `tests/test_job_queue_worker.py` | [job_queue](../modules/job_queue.md) |
| `tests/test_meta_and_thumb.py` | [auto_publisher](../modules/auto_publisher.md), [meta_studio](../modules/meta_studio.md) |
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
| `tests/test_server_split.py` | [routes_agent](../modules/routes_agent.md), [routes_hg](../modules/routes_hg.md), [server](../modules/server.md) |
| `tests/test_sfx_lib.py` | [render](../modules/render.md), [sfx_lib](../modules/sfx_lib.md) |
| `tests/test_source_link.py` | [server](../modules/server.md) |
