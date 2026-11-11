# Config & env keys

_Sinh tự động bởi `scripts/brain_build.py` lúc 2026-11-11 02:37. Đừng sửa tay — chạy lại script._


Thứ tự ưu tiên xem `config.py` (LLM keys: file thắng env; còn lại env → file → default) và `docs/ARCHITECTURE.md#config`. Bảng này chỉ cho biết **key được đọc ở đâu**.

**252 key.**

| Key | Đọc ở (số lần) |
|---|---|
| `AGENT_API_KEY` | [config](../modules/config.md) (1), [routes_uploader_settings](../modules/routes_uploader_settings.md) (1) |
| `AGENT_BASE_URL` | [config](../modules/config.md) (1), [routes_uploader_settings](../modules/routes_uploader_settings.md) (1) |
| `AGENT_BRAIN` | [agent_brain](../modules/agent_brain.md) (1) |
| `AGENT_BRAIN_LLM` | [agent_brain](../modules/agent_brain.md) (1) |
| `AGENT_BRAIN_LLM_SEC` | [agent_brain](../modules/agent_brain.md) (1) |
| `AGENT_BRAIN_LLM_STEPS` | [agent_brain](../modules/agent_brain.md) (1) |
| `AGENT_BRAIN_MODE` | [agent_brain](../modules/agent_brain.md) (2) |
| `AGENT_BRAIN_SEC` | [agent_brain](../modules/agent_brain.md) (1) |
| `AGENT_BRAIN_TELEGRAM` | [agent_brain](../modules/agent_brain.md) (1) |
| `AGENT_BRAIN_TG_SEC` | [agent_brain](../modules/agent_brain.md) (1) |
| `AGENT_FALLBACK_MODEL` | [config](../modules/config.md) (1), [routes_uploader_settings](../modules/routes_uploader_settings.md) (1) |
| `AGENT_MODEL` | [config](../modules/config.md) (1), [routes_uploader_settings](../modules/routes_uploader_settings.md) (1) |
| `AGENT_QA_GATE` | [server](../modules/server.md) (1) |
| `AGENT_TELEGRAM` | [agent_tele_cmd](../modules/agent_tele_cmd.md) (2), [agent_watch](../modules/agent_watch.md) (1), [migrate_work](../modules/migrate_work.md) (1), [restart_server](../modules/restart_server.md) (1), [routes_uploader_settings](../modules/routes_uploader_settings.md) (2) |
| `AGENT_TELEGRAM_STARTUP` | [agent_watch](../modules/agent_watch.md) (1) |
| `AGENT_TOOL_RESULT_MAX` | [agent_core](../modules/agent_core.md) (1) |
| `AGENT_WATCH` | [agent_watch](../modules/agent_watch.md) (1) |
| `AGENT_WATCH_COOLDOWN` | [agent_watch](../modules/agent_watch.md) (1) |
| `AGENT_WATCH_MAX_JOBS` | [agent_core](../modules/agent_core.md) (1), [agent_watch](../modules/agent_watch.md) (1), [routes_agent](../modules/routes_agent.md) (1) |
| `AGENT_WATCH_SEC` | [agent_watch](../modules/agent_watch.md) (1) |
| `AGENT_WATCH_SKIP_PREFIX` | [agent_watch](../modules/agent_watch.md) (1) |
| `ASR_FA_PAD_S` | [asr_fix_align](../modules/asr_fix_align.md) (1), [nano_fa_asr](../modules/nano_fa_asr.md) (1) |
| `ASR_VAD_CHUNK_S` | [fun_asr_nano](../modules/fun_asr_nano.md) (1) |
| `ASR_VAD_MAX_SEGMENT_S` | [asr_vad_utils](../modules/asr_vad_utils.md) (1) |
| `ASR_VAD_MAX_SINGLE_SEGMENT_MS` | [sensevoice_asr](../modules/sensevoice_asr.md) (1) |
| `ASR_VAD_MERGE_GAP_S` | [asr_vad_utils](../modules/asr_vad_utils.md) (1) |
| `ASR_VAD_OVERLAP_S` | [asr_vad_utils](../modules/asr_vad_utils.md) (1) |
| `ASR_VAD_PAD_S` | [asr_vad_utils](../modules/asr_vad_utils.md) (1) |
| `ASSEMBLE_FIT_MODE` | [assemble](../modules/assemble.md) (1) |
| `ASSEMBLE_MAX_SPEED` | [assemble](../modules/assemble.md) (1) |
| `AURORA_BASE_URL` | [config](../modules/config.md) (1) |
| `AURORA_REVIEW_MODEL` | [translate](../modules/translate.md) (1) |
| `AUTOPILOT_HOST` | [agent_tele_cmd](../modules/agent_tele_cmd.md) (1) |
| `AUTOPILOT_PORT` | [agent_hongguo](../modules/agent_hongguo.md) (1), [agent_tele_cmd](../modules/agent_tele_cmd.md) (1), [scripts.check_sidecar_lock](../modules/scripts.check_sidecar_lock.md) (1) |
| `AUTOPILOT_TICK_SEC` | [agent_tele_cmd](../modules/agent_tele_cmd.md) (1) |
| `AUTOPILOT_URL` | [agent_core](../modules/agent_core.md) (1) |
| `AUTO_REVIEW` | [server](../modules/server.md) (1), [translate](../modules/translate.md) (1) |
| `AUTO_SWITCH_PRESETS` | [translate](../modules/translate.md) (2) |
| `BRAIN_HANG_FIX` | [agent_hang_fix](../modules/agent_hang_fix.md) (1) |
| `BYPASS_SPEED` | [render](../modules/render.md) (1) |
| `CANVA_CLIENT_ID` | [canva_client](../modules/canva_client.md) (1) |
| `CANVA_CLIENT_SECRET` | [canva_client](../modules/canva_client.md) (1) |
| `CANVA_REDIRECT_URI` | [canva_client](../modules/canva_client.md) (2) |
| `CENSOR_BLUR` | [render](../modules/render.md) (1) |
| `CENSOR_RANGES` | [render](../modules/render.md) (1) |
| `CHATGPT_ACCESS_TOKEN` | [llm](../modules/llm.md) (2) |
| `CHATGPT_API_KEY` | [llm](../modules/llm.md) (2) |
| `CHATGPT_BASE_URL` | [config](../modules/config.md) (1) |
| `CHATGPT_FORCE_TOKEN` | [llm](../modules/llm.md) (4) |
| `CHATGPT_MODEL` | [config](../modules/config.md) (2), [llm](../modules/llm.md) (2) |
| `CHATGPT_TIMEOUT` | [llm](../modules/llm.md) (3), [meta_studio](../modules/meta_studio.md) (1), [translate](../modules/translate.md) (2) |
| `CLONE_CLEANUP` | [clone_tts](../modules/clone_tts.md) (2) |
| `CLONE_HISHELF` | [clone_tts](../modules/clone_tts.md) (1) |
| `CLOUD_LLM_API_KEY` | [llm](../modules/llm.md) (1) |
| `CLOUD_LLM_BASE_URL` | [llm](../modules/llm.md) (1) |
| `DEMUCS_CHUNK_SEC` | [separate](../modules/separate.md) (1) |
| `DEMUCS_LONG_THRESHOLD_SEC` | [separate](../modules/separate.md) (1) |
| `DL_WORKERS` | [server](../modules/server.md) (1) |
| `DOWNLOAD_MAX_HEIGHT` | [download](../modules/download.md) (2) |
| `DOWNLOAD_PREFER_HEVC` | [download](../modules/download.md) (2) |
| `FALLBACK_MODEL` | [translate](../modules/translate.md) (1) |
| `FILMDB_SEC` | [agent_tele_cmd](../modules/agent_tele_cmd.md) (1) |
| `FILM_DB` | [film_db](../modules/film_db.md) (1) |
| `FIRERED_MODELS` | [firered_asr](../modules/firered_asr.md) (2), [scripts.download_firered_models](../modules/scripts.download_firered_models.md) (1) |
| `FIRERED_ROOT` | [firered_asr](../modules/firered_asr.md) (2) |
| `FIRERED_SLICE_SEC` | [firered_asr](../modules/firered_asr.md) (1) |
| `FIRERED_USE_HALF` | [firered_asr](../modules/firered_asr.md) (2) |
| `HANG_FIX_MODEL` | [agent_hang_fix](../modules/agent_hang_fix.md) (2) |
| `HARDSUB_BAR_ALPHA` | [render](../modules/render.md) (1) |
| `HARDSUB_BAR_RADIUS` | [render](../modules/render.md) (1) |
| `HARDSUB_BLUR` | [render](../modules/render.md) (1) |
| `HARDSUB_BLUR_MARGIN` | [render](../modules/render.md) (1) |
| `HARDSUB_BLUR_MAX_H` | [render](../modules/render.md) (1) |
| `HARDSUB_BLUR_R` | [render](../modules/render.md) (1) |
| `HARDSUB_BLUR_W` | [render](../modules/render.md) (1) |
| `HARDSUB_COVER_FULLW` | [render](../modules/render.md) (1) |
| `HARDSUB_FIXED_BOTTOM` | [render](../modules/render.md) (1) |
| `HARDSUB_FORCE_BLUR` | [render](../modules/render.md) (2) |
| `HARDSUB_FULL_COVER_RATIO` | [render](../modules/render.md) (1) |
| `HARDSUB_GAP_FILL_SEC` | [render](../modules/render.md) (1) |
| `HARDSUB_MODE` | [render](../modules/render.md) (2) |
| `HARDSUB_PAD_BOTTOM` | [render](../modules/render.md) (1) |
| `HARDSUB_PAD_TOP` | [render](../modules/render.md) (1) |
| `HARDSUB_REDETECT` | [render](../modules/render.md) (1) |
| `HARDSUB_STRETCH_FULLW` | [render](../modules/render.md) (2) |
| `HARDSUB_STRETCH_SIGMA` | [render](../modules/render.md) (1) |
| `HARDSUB_STRETCH_SIGMA_V` | [render](../modules/render.md) (1) |
| `HARDSUB_STYLE` | [render](../modules/render.md) (1) |
| `HARDSUB_TRACK_MAX_SAMPLES` | [render](../modules/render.md) (1) |
| `HF_HOME` | [config](../modules/config.md) (1) |
| `HF_HUB_DISABLE_SYMLINKS` | [asr_fix_align](../modules/asr_fix_align.md) (1), [asr_repair](../modules/asr_repair.md) (1), [config](../modules/config.md) (1), [firered_asr](../modules/firered_asr.md) (1), [fun_asr_nano](../modules/fun_asr_nano.md) (1), [hybrid_asr](../modules/hybrid_asr.md) (1), [nano_fa_asr](../modules/nano_fa_asr.md) (1), [paraformer_zh](../modules/paraformer_zh.md) (1), [sensevoice_asr](../modules/sensevoice_asr.md) (1), [server](../modules/server.md) (1) |
| `HF_HUB_DISABLE_SYMLINKS_WARNING` | [asr_fix_align](../modules/asr_fix_align.md) (1), [config](../modules/config.md) (1), [firered_asr](../modules/firered_asr.md) (1), [fun_asr_nano](../modules/fun_asr_nano.md) (1), [hybrid_asr](../modules/hybrid_asr.md) (1), [nano_fa_asr](../modules/nano_fa_asr.md) (1), [paraformer_zh](../modules/paraformer_zh.md) (1), [sensevoice_asr](../modules/sensevoice_asr.md) (1), [server](../modules/server.md) (1) |
| `HG_BACKEND` | [hongguo_bridge](../modules/hongguo_bridge.md) (1), [server](../modules/server.md) (1) |
| `HG_ENGINE_DIR` | [hongguo_rpc](../modules/hongguo_rpc.md) (1) |
| `HG_HELPER_PIDFILE` | [hongguo_rpc](../modules/hongguo_rpc.md) (1) |
| `HG_HELPER_SINGLETON` | [hongguo_rpc](../modules/hongguo_rpc.md) (1), [server](../modules/server.md) (1) |
| `HG_LIC_ACTIVATE_EXE` | [hongguo_license_ensure](../modules/hongguo_license_ensure.md) (1) |
| `HG_RPC_IDLE_SEC` | [hongguo_rpc](../modules/hongguo_rpc.md) (1) |
| `HG_RPC_TIMEOUT` | [hongguo_rpc](../modules/hongguo_rpc.md) (1) |
| `HG_UI_TOKEN` | [hongguo_bridge](../modules/hongguo_bridge.md) (1) |
| `HOST` | [server](../modules/server.md) (1) |
| `JOB_WORKERS` | [server](../modules/server.md) (1) |
| `LIBRARY_DIR` | [routes_uploader_settings](../modules/routes_uploader_settings.md) (1) |
| `LIB_ROOT` | [lib_check](../modules/lib_check.md) (1) |
| `LLAMA_BASE_URL` | [llm](../modules/llm.md) (3) |
| `LLM_API_KEY` | [config](../modules/config.md) (2), [llm](../modules/llm.md) (1), [routes_uploader_settings](../modules/routes_uploader_settings.md) (2) |
| `LLM_BASE_URL` | [config](../modules/config.md) (2), [llm](../modules/llm.md) (1), [routes_uploader_settings](../modules/routes_uploader_settings.md) (2) |
| `LLM_ENABLE_THINKING` | [agent_core](../modules/agent_core.md) (1), [llm](../modules/llm.md) (2) |
| `LLM_MODEL` | [config](../modules/config.md) (3), [context_studio.analyzer](../modules/context_studio.analyzer.md) (1), [llm](../modules/llm.md) (1), [routes_uploader_settings](../modules/routes_uploader_settings.md) (2), [scripts.check_batch3](../modules/scripts.check_batch3.md) (1), [translate](../modules/translate.md) (1) |
| `LLM_NUM_CTX` | [llm](../modules/llm.md) (1) |
| `LOCALAPPDATA` | [agent_hongguo](../modules/agent_hongguo.md) (1), [hongguo_license_ensure](../modules/hongguo_license_ensure.md) (2), [hongguo_rpc](../modules/hongguo_rpc.md) (3) |
| `LOCAL_LLM_BASE_URL` | [llm](../modules/llm.md) (1) |
| `MODEL_PRESETS_DIR` | [preset_switcher](../modules/preset_switcher.md) (1) |
| `MT_ZH_VI` | [mt_zh_vi](../modules/mt_zh_vi.md) (2) |
| `MT_ZH_VI_BATCH` | [mt_zh_vi](../modules/mt_zh_vi.md) (1) |
| `MT_ZH_VI_BEAM` | [mt_zh_vi](../modules/mt_zh_vi.md) (1) |
| `MT_ZH_VI_DEVICE` | [mt_zh_vi](../modules/mt_zh_vi.md) (1) |
| `MT_ZH_VI_LOCAL` | [mt_zh_vi](../modules/mt_zh_vi.md) (1) |
| `MT_ZH_VI_MAX_TOKENS` | [mt_zh_vi](../modules/mt_zh_vi.md) (1) |
| `MT_ZH_VI_MODEL` | [mt_zh_vi](../modules/mt_zh_vi.md) (1) |
| `MT_ZH_VI_MODEL_BASE` | [mt_zh_vi](../modules/mt_zh_vi.md) (1) |
| `MT_ZH_VI_MODEL_QT` | [mt_zh_vi](../modules/mt_zh_vi.md) (1) |
| `MT_ZH_VI_ONLY` | [mt_zh_vi](../modules/mt_zh_vi.md) (1) |
| `MT_ZH_VI_ROLE` | [mt_zh_vi](../modules/mt_zh_vi.md) (1) |
| `NAME_MODEL` | [config](../modules/config.md) (2) |
| `OAUTHLIB_RELAX_TOKEN_SCOPE` | [test_channel](../modules/test_channel.md) (1) |
| `OMNI_CWD` | [config](../modules/config.md) (1) |
| `OMNI_DEVICE` | [config](../modules/config.md) (1) |
| `OMNI_GUIDANCE` | [clone_tts](../modules/clone_tts.md) (1) |
| `OMNI_MODEL` | [config](../modules/config.md) (1), [routes_uploader_settings](../modules/routes_uploader_settings.md) (1) |
| `OMNI_NUM_STEP` | [clone_tts](../modules/clone_tts.md) (1) |
| `OMNI_PY` | [config](../modules/config.md) (1) |
| `PATH` | [firered_asr](../modules/firered_asr.md) (2) |
| `PINELINE_BASE` | [agent_autopilot](../modules/agent_autopilot.md) (1), [agent_brain](../modules/agent_brain.md) (1), [agent_brain_context](../modules/agent_brain_context.md) (1), [agent_tele_cmd](../modules/agent_tele_cmd.md) (1), [migrate_work](../modules/migrate_work.md) (1) |
| `PINELINE_OMNI_ENV` | [config](../modules/config.md) (1) |
| `PINELINE_PORT` | [agent_brain](../modules/agent_brain.md) (1), [agent_brain_context](../modules/agent_brain_context.md) (1), [meta_studio](../modules/meta_studio.md) (1), [server](../modules/server.md) (1) |
| `PINELINE_VIENEU_ENV` | [config](../modules/config.md) (1) |
| `PLAN_FILE_TIMEOUT` | [translate](../modules/translate.md) (1) |
| `PLAN_MODE` | [translate](../modules/translate.md) (1) |
| `PLAN_MODEL` | [translate](../modules/translate.md) (2) |
| `PORT` | [agent_autopilot](../modules/agent_autopilot.md) (1), [agent_hongguo](../modules/agent_hongguo.md) (4), [app_desktop](../modules/app_desktop.md) (1), [canva_client](../modules/canva_client.md) (2), [migrate_work](../modules/migrate_work.md) (1), [restart_server](../modules/restart_server.md) (1), [server](../modules/server.md) (1) |
| `PRONOUN_ANALYZE` | [pronoun_consistency](../modules/pronoun_consistency.md) (1) |
| `PRONOUN_ANALYZE_CHUNK` | [pronoun_consistency](../modules/pronoun_consistency.md) (1) |
| `PRONOUN_ANALYZE_EARLY_STOP` | [pronoun_consistency](../modules/pronoun_consistency.md) (1) |
| `PRONOUN_ANALYZE_MAX_CHUNKS` | [pronoun_consistency](../modules/pronoun_consistency.md) (1) |
| `PRONOUN_ANALYZE_MIN_CHUNKS` | [pronoun_consistency](../modules/pronoun_consistency.md) (1) |
| `PRONOUN_ANALYZE_MODE` | [pronoun_consistency](../modules/pronoun_consistency.md) (1) |
| `PRONOUN_ANALYZE_MODEL` | [pronoun_consistency](../modules/pronoun_consistency.md) (1) |
| `PRONOUN_MODEL` | [agent_hang_fix](../modules/agent_hang_fix.md) (2), [config](../modules/config.md) (2) |
| `PRONOUN_TITLE_POLICY` | [agent_pronoun_pass](../modules/agent_pronoun_pass.md) (1) |
| `PYTHONEXECUTABLE` | [rvc_bridge.vieneu_batch](../modules/rvc_bridge.vieneu_batch.md) (1) |
| `PYTHONIOENCODING` | [server](../modules/server.md) (1) |
| `QA_ASR_DEVICE` | [clone_tts](../modules/clone_tts.md) (1) |
| `QA_ASR_MODEL` | [clone_tts](../modules/clone_tts.md) (1) |
| `QUEUE_LIVE_CONFIG` | [agent_tele_cmd](../modules/agent_tele_cmd.md) (1) |
| `QUEUE_PARK_POLL_SEC` | [job_queue](../modules/job_queue.md) (1) |
| `QUEUE_REVIEW_RETRY_MAX` | [server](../modules/server.md) (1) |
| `QUEUE_REVIEW_RETRY_SEC` | [server](../modules/server.md) (1) |
| `QWEN3_FORCED_ALIGNER` | [asr_fix_align](../modules/asr_fix_align.md) (1), [nano_fa_asr](../modules/nano_fa_asr.md) (1) |
| `REF_ASR` | [server](../modules/server.md) (1) |
| `REF_ASR_DEVICE` | [server](../modules/server.md) (2) |
| `REF_ASR_MODEL` | [server](../modules/server.md) (3) |
| `RENDER_BGM_FILE` | [render_fx](../modules/render_fx.md) (2) |
| `RENDER_BGM_VOL` | [render_fx](../modules/render_fx.md) (2) |
| `RENDER_BRAND` | [render_fx](../modules/render_fx.md) (2) |
| `RENDER_BRAND_LOGO` | [render_fx](../modules/render_fx.md) (2) |
| `RENDER_BRAND_LOGO_FILE` | [render_fx](../modules/render_fx.md) (2) |
| `RENDER_BRAND_MODE` | [render_fx](../modules/render_fx.md) (2) |
| `RENDER_BRAND_OPACITY` | [render_fx](../modules/render_fx.md) (2) |
| `RENDER_BRAND_TEXT` | [render_fx](../modules/render_fx.md) (2) |
| `RENDER_DUB_VOL` | [render_fx](../modules/render_fx.md) (2) |
| `RENDER_ENCODER` | [render](../modules/render.md) (2), [routes_uploader_settings](../modules/routes_uploader_settings.md) (1) |
| `RENDER_EQ_BRIGHTNESS` | [render_fx](../modules/render_fx.md) (1) |
| `RENDER_EQ_CONTRAST` | [render_fx](../modules/render_fx.md) (1) |
| `RENDER_EQ_SATURATION` | [render_fx](../modules/render_fx.md) (1) |
| `RENDER_FRAME` | [render_fx](../modules/render_fx.md) (2) |
| `RENDER_FRAME_FILE` | [render_fx](../modules/render_fx.md) (2) |
| `RENDER_GRAIN_FILE` | [render_fx](../modules/render_fx.md) (2) |
| `RENDER_LIB_BGM_VOL` | [sfx_lib](../modules/sfx_lib.md) (1) |
| `RENDER_LUT_FILE` | [render_fx](../modules/render_fx.md) (2) |
| `RENDER_SFX_VOICE_BOOST` | [sfx_lib](../modules/sfx_lib.md) (1) |
| `RENDER_SFX_VOL` | [sfx_lib](../modules/sfx_lib.md) (1) |
| `RENDER_SPEED` | [render](../modules/render.md) (2) |
| `REVIEW_BACKUP` | [translate](../modules/translate.md) (1) |
| `REVIEW_MODEL` | [config](../modules/config.md) (2), [routes_uploader_settings](../modules/routes_uploader_settings.md) (1), [translate](../modules/translate.md) (3) |
| `REVIEW_PARALLEL` | [translate](../modules/translate.md) (1) |
| `REVIEW_PARALLEL_DEFAULT` | [translate](../modules/translate.md) (1) |
| `REVIEW_PARALLEL_MAX` | [translate](../modules/translate.md) (1) |
| `REVIEW_PASS1_ALLOW_CHAT_FALLBACK` | [translate](../modules/translate.md) (1) |
| `REVIEW_PASS1_CHUNK_CUES` | [translate](../modules/translate.md) (1) |
| `REVIEW_PASS1_FALLBACK_CUES` | [translate](../modules/translate.md) (1) |
| `REVIEW_PASS1_FULL_VI` | [translate](../modules/translate.md) (1) |
| `REVIEW_PASS1_MAX_UPLOAD_BYTES` | [translate](../modules/translate.md) (1) |
| `REVIEW_PASS1_MODEL` | [translate](../modules/translate.md) (1) |
| `REVIEW_PASS1_TIMEOUT` | [translate](../modules/translate.md) (1) |
| `REVIEW_PRESET` | [agent_brain](../modules/agent_brain.md) (1), [translate](../modules/translate.md) (2) |
| `REVIEW_PRONOUN_MASK` | [translate](../modules/translate.md) (1) |
| `REVIEW_RETRY_BACKOFF_SEC` | [translate](../modules/translate.md) (1) |
| `RUNWATCH_MAX_HEAL` | [agent_feeder](../modules/agent_feeder.md) (1) |
| `RUNWATCH_SEC` | [agent_tele_cmd](../modules/agent_tele_cmd.md) (1) |
| `RUNWATCH_STUCK_MIN` | [agent_feeder](../modules/agent_feeder.md) (1) |
| `SFX_CDX_HQ` | [sfx_lib](../modules/sfx_lib.md) (1) |
| `SFX_CDX_MODEL_DIR` | [sfx_lib](../modules/sfx_lib.md) (1) |
| `SFX_LIB_DIR` | [sfx_lib](../modules/sfx_lib.md) (1) |
| `SKIP_VRAM_FREE` | [vram](../modules/vram.md) (1) |
| `SOURCE_DIRECT_ROOTS` | [server](../modules/server.md) (1) |
| `SUB_ALIGN` | [render](../modules/render.md) (1) |
| `SUB_BOLD` | [render](../modules/render.md) (1) |
| `SUB_COLOR` | [render](../modules/render.md) (1) |
| `SUB_FOLLOW_HARDSUB` | [render](../modules/render.md) (1) |
| `SUB_FONT` | [render](../modules/render.md) (1) |
| `SUB_FONT_SIZE` | [render](../modules/render.md) (1) |
| `SUB_MARGIN_L` | [render](../modules/render.md) (1) |
| `SUB_MARGIN_R` | [render](../modules/render.md) (1) |
| `SUB_MARGIN_V` | [render](../modules/render.md) (1) |
| `SUB_MAX_DUR` | [subs](../modules/subs.md) (1) |
| `SUB_OUTLINE` | [render](../modules/render.md) (1) |
| `SUB_OUTLINE_COLOR` | [render](../modules/render.md) (1) |
| `SUB_SHADOW` | [render](../modules/render.md) (1) |
| `SUB_SPLIT_CHARS_VI` | [subs](../modules/subs.md) (1) |
| `SUB_SPLIT_CHARS_ZH` | [subs](../modules/subs.md) (1) |
| `SUB_WRAP_CHARS` | [subs](../modules/subs.md) (1) |
| `SUB_WRAP_LINES` | [subs](../modules/subs.md) (1) |
| `TELEGRAM_ALLOWED_USERS` | [agent_watch](../modules/agent_watch.md) (2), [routes_uploader_settings](../modules/routes_uploader_settings.md) (4) |
| `TELEGRAM_BOT_TOKEN` | [agent_watch](../modules/agent_watch.md) (2), [routes_uploader_settings](../modules/routes_uploader_settings.md) (4) |
| `TELEGRAM_POLL_SEC` | [agent_tele_cmd](../modules/agent_tele_cmd.md) (1) |
| `TEMP` | [agent_tele_cmd](../modules/agent_tele_cmd.md) (1), [app_desktop](../modules/app_desktop.md) (1), [hongguo_license_ensure](../modules/hongguo_license_ensure.md) (1), [hongguo_rpc](../modules/hongguo_rpc.md) (2), [routes_uploader_settings](../modules/routes_uploader_settings.md) (1), [uploader_settings_api](../modules/uploader_settings_api.md) (1) |
| `TEST_YT_SECRET` | [test_channel](../modules/test_channel.md) (1) |
| `TMP` | [agent_tele_cmd](../modules/agent_tele_cmd.md) (1), [hongguo_rpc](../modules/hongguo_rpc.md) (2) |
| `TRANSLATE_BATCH` | [server](../modules/server.md) (2), [translate](../modules/translate.md) (2) |
| `TRANSLATE_CTX_LINES` | [translate](../modules/translate.md) (1) |
| `TRANSLATE_FILL_ROUNDS` | [translate](../modules/translate.md) (1) |
| `TRANSLATE_MODE` | [translate](../modules/translate.md) (2) |
| `TRANSLATE_MODEL` | [config](../modules/config.md) (1), [context_studio.analyzer](../modules/context_studio.analyzer.md) (1), [routes_uploader_settings](../modules/routes_uploader_settings.md) (1), [server](../modules/server.md) (1), [translate](../modules/translate.md) (2) |
| `TRANSLATE_ONESHOT_MAX` | [translate](../modules/translate.md) (1) |
| `TRANSLATE_PRESET` | [agent_brain](../modules/agent_brain.md) (1), [translate](../modules/translate.md) (1) |
| `TTS_RUNAWAY_RETRIES` | [clone_tts](../modules/clone_tts.md) (1) |
| `VIENEU_BATCH` | [clone_tts](../modules/clone_tts.md) (2), [routes_uploader_settings](../modules/routes_uploader_settings.md) (1), [rvc_bridge.vieneu_batch](../modules/rvc_bridge.vieneu_batch.md) (1) |
| `VIENEU_BOOT_SEC` | [clone_tts](../modules/clone_tts.md) (1), [server](../modules/server.md) (1) |
| `VIENEU_CPU_THREADS` | [rvc_bridge.vieneu_batch](../modules/rvc_bridge.vieneu_batch.md) (1) |
| `VIENEU_DEVICE` | [config](../modules/config.md) (1), [routes_uploader_settings](../modules/routes_uploader_settings.md) (1) |
| `VIENEU_LOW_PRIORITY` | [rvc_bridge.vieneu_batch](../modules/rvc_bridge.vieneu_batch.md) (1) |
| `VIENEU_PY` | [config](../modules/config.md) (1) |
| `VIENEU_STALL_SEC` | [clone_tts](../modules/clone_tts.md) (1) |
| `WM_FORCE_CORNERS` | [render](../modules/render.md) (2) |
| `WM_MAX_SAMPLES` | [render](../modules/render.md) (1) |
| `WM_SAMPLE_SEC` | [render](../modules/render.md) (1) |
| `WORK_DIR` | [films_merge_api](../modules/films_merge_api.md) (1), [routes_uploader_settings](../modules/routes_uploader_settings.md) (1) |
| `WORK_ROOT` | [agent_hongguo](../modules/agent_hongguo.md) (1) |
| `YT_UPLOADER_DIR` | [auto_publisher](../modules/auto_publisher.md) (1), [film_db](../modules/film_db.md) (1), [lib_check](../modules/lib_check.md) (1), [routes_uploader_settings](../modules/routes_uploader_settings.md) (2), [uploader_settings_api](../modules/uploader_settings_api.md) (1) |
| `ZZ_ENVSET` | [scripts.check_batch3](../modules/scripts.check_batch3.md) (2) |
| `ZZ_FROMFILE` | [scripts.check_batch3](../modules/scripts.check_batch3.md) (2) |
