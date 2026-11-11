# File/artifact & cổng — ai đụng tới

_Sinh tự động bởi `scripts/brain_build.py` lúc 2026-11-11 02:37. Đừng sửa tay — chạy lại script._


Dùng để trả lời: *file `X.json` do ai ghi/đọc?* (chỉ là chuỗi literal xuất hiện trong code). Artifact dùng bởi ≥2 module là điểm có thể race khi ghi.

## Cổng

| Cổng | Module |
|---|---|
| 3377 | [agent_brain](../modules/agent_brain.md), [agent_brain_context](../modules/agent_brain_context.md), [llm](../modules/llm.md), [meta_studio](../modules/meta_studio.md) |
| 8000 | [agent_brain_context](../modules/agent_brain_context.md), [agent_tele_cmd](../modules/agent_tele_cmd.md), [hongguo_bridge](../modules/hongguo_bridge.md), [server](../modules/server.md) |
| 8083 | [agent_brain](../modules/agent_brain.md), [agent_brain_context](../modules/agent_brain_context.md), [config](../modules/config.md), [llm](../modules/llm.md), [routes_uploader_settings](../modules/routes_uploader_settings.md), [uploader_settings_api](../modules/uploader_settings_api.md) |
| 8801 | [agent_tele_cmd](../modules/agent_tele_cmd.md), [agent_tool_loop](../modules/agent_tool_loop.md), [scripts.check_batch2](../modules/scripts.check_batch2.md), [scripts.check_batch3](../modules/scripts.check_batch3.md), [scripts.check_batch5](../modules/scripts.check_batch5.md) |
| 8802 | [agent_brain](../modules/agent_brain.md), [agent_brain_context](../modules/agent_brain_context.md), [agent_core](../modules/agent_core.md), [agent_feeder](../modules/agent_feeder.md), [agent_tele_cmd](../modules/agent_tele_cmd.md), [migrate_work](../modules/migrate_work.md), [restart_server](../modules/restart_server.md), [scripts.check_batch2](../modules/scripts.check_batch2.md) |
| 8804 | [routes_films](../modules/routes_films.md) |
| 11434 | [llm](../modules/llm.md), [scripts.check_batch2](../modules/scripts.check_batch2.md) |

## Artifact

| File | Số module | Module |
|---|---:|---|
| `manifest.json` | 25 | [agent_autopilot](../modules/agent_autopilot.md), [agent_av_sync](../modules/agent_av_sync.md), [agent_brain](../modules/agent_brain.md), [agent_brain_context](../modules/agent_brain_context.md), [agent_core](../modules/agent_core.md), [agent_feeder](../modules/agent_feeder.md), [agent_heal](../modules/agent_heal.md), [agent_stage_io](../modules/agent_stage_io.md), [agent_tool_loop](../modules/agent_tool_loop.md), [agent_watch](../modules/agent_watch.md), [auto_publisher](../modules/auto_publisher.md), [film_db](../modules/film_db.md), [films_merge_api](../modules/films_merge_api.md), [job_queue](../modules/job_queue.md), [manifest](../modules/manifest.md), [media_ts](../modules/media_ts.md), [meta_studio](../modules/meta_studio.md), [migrate_work](../modules/migrate_work.md), [restart_server](../modules/restart_server.md), [routes_agent](../modules/routes_agent.md), [scripts.check_batch1](../modules/scripts.check_batch1.md), [scripts.check_batch3](../modules/scripts.check_batch3.md), [scripts.check_batch4](../modules/scripts.check_batch4.md), [series_glossary](../modules/series_glossary.md), [server](../modules/server.md) |
| `script.json` | 25 | [agent_brain](../modules/agent_brain.md), [agent_brain_context](../modules/agent_brain_context.md), [agent_core](../modules/agent_core.md), [agent_feeder](../modules/agent_feeder.md), [agent_hang_fix](../modules/agent_hang_fix.md), [agent_heal](../modules/agent_heal.md), [agent_name_pass](../modules/agent_name_pass.md), [agent_pronoun_pass](../modules/agent_pronoun_pass.md), [agent_qa_gate](../modules/agent_qa_gate.md), [agent_quality](../modules/agent_quality.md), [agent_stage_io](../modules/agent_stage_io.md), [clone_tts](../modules/clone_tts.md), [hardsub_asr](../modules/hardsub_asr.md), [job_queue](../modules/job_queue.md), [media_ts](../modules/media_ts.md), [meta_studio](../modules/meta_studio.md), [pronoun_consistency](../modules/pronoun_consistency.md), [render](../modules/render.md), [routes_agent](../modules/routes_agent.md), [script_lint](../modules/script_lint.md), [scripts.check_batch1](../modules/scripts.check_batch1.md), [scripts.check_batch4](../modules/scripts.check_batch4.md), [server](../modules/server.md), [translate](../modules/translate.md), [translate_alts](../modules/translate_alts.md) |
| `asr.json` | 18 | [agent_heal](../modules/agent_heal.md), [agent_stage_io](../modules/agent_stage_io.md), [asr](../modules/asr.md), [asr_repair](../modules/asr_repair.md), [asr_spam](../modules/asr_spam.md), [firered_asr](../modules/firered_asr.md), [fun_asr_nano](../modules/fun_asr_nano.md), [hardsub_asr](../modules/hardsub_asr.md), [hybrid_asr](../modules/hybrid_asr.md), [media_ts](../modules/media_ts.md), [nano_fa_asr](../modules/nano_fa_asr.md), [ocr](../modules/ocr.md), [paraformer_zh](../modules/paraformer_zh.md), [pronoun_consistency](../modules/pronoun_consistency.md), [sensevoice_asr](../modules/sensevoice_asr.md), [server](../modules/server.md), [split_parts](../modules/split_parts.md), [translate](../modules/translate.md) |
| `output.mp4` | 15 | [agent_av_sync](../modules/agent_av_sync.md), [agent_brain_context](../modules/agent_brain_context.md), [agent_core](../modules/agent_core.md), [agent_feeder](../modules/agent_feeder.md), [agent_heal](../modules/agent_heal.md), [agent_stage_io](../modules/agent_stage_io.md), [auto_publisher](../modules/auto_publisher.md), [films_merge_api](../modules/films_merge_api.md), [job_queue](../modules/job_queue.md), [meta_studio](../modules/meta_studio.md), [mux](../modules/mux.md), [render](../modules/render.md), [scripts.check_batch1](../modules/scripts.check_batch1.md), [server](../modules/server.md), [split_parts](../modules/split_parts.md) |
| `audio.wav` | 14 | [agent_heal](../modules/agent_heal.md), [asr](../modules/asr.md), [asr_fix_align](../modules/asr_fix_align.md), [asr_repair](../modules/asr_repair.md), [firered_asr](../modules/firered_asr.md), [fun_asr_nano](../modules/fun_asr_nano.md), [hybrid_asr](../modules/hybrid_asr.md), [media_ts](../modules/media_ts.md), [nano_fa_asr](../modules/nano_fa_asr.md), [paraformer_zh](../modules/paraformer_zh.md), [scripts.check_batch1](../modules/scripts.check_batch1.md), [scripts.check_batch4](../modules/scripts.check_batch4.md), [sensevoice_asr](../modules/sensevoice_asr.md), [separate](../modules/separate.md) |
| `sub.zh.srt` | 13 | [agent_heal](../modules/agent_heal.md), [asr](../modules/asr.md), [asr_spam](../modules/asr_spam.md), [firered_asr](../modules/firered_asr.md), [fun_asr_nano](../modules/fun_asr_nano.md), [hybrid_asr](../modules/hybrid_asr.md), [media_ts](../modules/media_ts.md), [nano_fa_asr](../modules/nano_fa_asr.md), [paraformer_zh](../modules/paraformer_zh.md), [pronoun_consistency](../modules/pronoun_consistency.md), [sensevoice_asr](../modules/sensevoice_asr.md), [server](../modules/server.md), [split_parts](../modules/split_parts.md) |
| `glossary.json` | 12 | [agent_name_pass](../modules/agent_name_pass.md), [agent_pronoun_pass](../modules/agent_pronoun_pass.md), [agent_qa_gate](../modules/agent_qa_gate.md), [agent_stage_io](../modules/agent_stage_io.md), [context_studio.app_streamlit](../modules/context_studio.app_streamlit.md), [context_studio.exporter](../modules/context_studio.exporter.md), [pronoun_consistency](../modules/pronoun_consistency.md), [script_lint](../modules/script_lint.md), [series_glossary](../modules/series_glossary.md), [server](../modules/server.md), [translate](../modules/translate.md), [translate_alts](../modules/translate_alts.md) |
| `sub.vi.srt` | 11 | [agent_av_sync](../modules/agent_av_sync.md), [agent_feeder](../modules/agent_feeder.md), [agent_hang_fix](../modules/agent_hang_fix.md), [agent_heal](../modules/agent_heal.md), [agent_pronoun_pass](../modules/agent_pronoun_pass.md), [media_ts](../modules/media_ts.md), [meta_studio](../modules/meta_studio.md), [render](../modules/render.md), [script_lint](../modules/script_lint.md), [server](../modules/server.md), [translate](../modules/translate.md) |
| `tts.json` | 11 | [agent_heal](../modules/agent_heal.md), [agent_stage_io](../modules/agent_stage_io.md), [assemble](../modules/assemble.md), [clone_tts](../modules/clone_tts.md), [media_ts](../modules/media_ts.md), [mux](../modules/mux.md), [render](../modules/render.md), [routes_agent](../modules/routes_agent.md), [scripts.check_batch1](../modules/scripts.check_batch1.md), [scripts.check_batch4](../modules/scripts.check_batch4.md), [server](../modules/server.md) |
| `dub_fit.wav` | 8 | [agent_av_sync](../modules/agent_av_sync.md), [agent_heal](../modules/agent_heal.md), [agent_stage_io](../modules/agent_stage_io.md), [assemble](../modules/assemble.md), [mux](../modules/mux.md), [render](../modules/render.md), [scripts.check_batch4](../modules/scripts.check_batch4.md), [server](../modules/server.md) |
| `script.display.json` | 7 | [agent_heal](../modules/agent_heal.md), [media_ts](../modules/media_ts.md), [render](../modules/render.md), [script_lint](../modules/script_lint.md), [scripts.check_batch1](../modules/scripts.check_batch1.md), [server](../modules/server.md), [translate](../modules/translate.md) |
| `tts_config.json` | 7 | [agent_heal](../modules/agent_heal.md), [agent_hongguo](../modules/agent_hongguo.md), [agent_stage_io](../modules/agent_stage_io.md), [clone_tts](../modules/clone_tts.md), [scripts.check_batch4](../modules/scripts.check_batch4.md), [server](../modules/server.md), [split_parts](../modules/split_parts.md) |
| `asr.fun_nano.json` | 6 | [asr_align_nano_para](../modules/asr_align_nano_para.md), [asr_fix_align](../modules/asr_fix_align.md), [asr_spam](../modules/asr_spam.md), [hybrid_asr](../modules/hybrid_asr.md), [nano_fa_asr](../modules/nano_fa_asr.md), [server](../modules/server.md) |
| `vocals.wav` | 6 | [asr](../modules/asr.md), [media_ts](../modules/media_ts.md), [render](../modules/render.md), [scripts.check_batch4](../modules/scripts.check_batch4.md), [separate](../modules/separate.md), [server](../modules/server.md) |
| `asr.paraformer_zh.json` | 5 | [asr_align_nano_para](../modules/asr_align_nano_para.md), [asr_repair](../modules/asr_repair.md), [asr_spam](../modules/asr_spam.md), [hybrid_asr](../modules/hybrid_asr.md), [server](../modules/server.md) |
| `context_pack.json` | 5 | [agent_stage_io](../modules/agent_stage_io.md), [context_studio.exporter](../modules/context_studio.exporter.md), [server](../modules/server.md), [translate](../modules/translate.md), [translate_alts](../modules/translate_alts.md) |
| `no_vocals.wav` | 5 | [media_ts](../modules/media_ts.md), [render](../modules/render.md), [scripts.check_batch4](../modules/scripts.check_batch4.md), [separate](../modules/separate.md), [server](../modules/server.md) |
| `ocr.json` | 5 | [agent_stage_io](../modules/agent_stage_io.md), [ocr](../modules/ocr.md), [render](../modules/render.md), [server](../modules/server.md), [translate](../modules/translate.md) |
| `sub.vi.burn.srt` | 5 | [agent_av_sync](../modules/agent_av_sync.md), [agent_heal](../modules/agent_heal.md), [media_ts](../modules/media_ts.md), [meta_studio](../modules/meta_studio.md), [render](../modules/render.md) |
| `tts_fit.json` | 5 | [agent_av_sync](../modules/agent_av_sync.md), [agent_heal](../modules/agent_heal.md), [assemble](../modules/assemble.md), [render](../modules/render.md), [scripts.check_batch1](../modules/scripts.check_batch1.md) |
| `.progress.json` | 4 | [asr_hybrid_progress](../modules/asr_hybrid_progress.md), [fun_asr_nano](../modules/fun_asr_nano.md), [paraformer_zh](../modules/paraformer_zh.md), [sensevoice_asr](../modules/sensevoice_asr.md) |
| `asr.aligned.json` | 4 | [asr_fix_align](../modules/asr_fix_align.md), [asr_repair](../modules/asr_repair.md), [asr_spam](../modules/asr_spam.md), [server](../modules/server.md) |
| `asr.aligned_fa.json` | 4 | [asr_repair](../modules/asr_repair.md), [asr_spam](../modules/asr_spam.md), [hybrid_asr](../modules/hybrid_asr.md), [server](../modules/server.md) |
| `asr.aligned_fix.json` | 4 | [asr_fix_align](../modules/asr_fix_align.md), [asr_repair](../modules/asr_repair.md), [hybrid_asr](../modules/hybrid_asr.md), [server](../modules/server.md) |
| `output.partial.mp4` | 4 | [agent_av_sync](../modules/agent_av_sync.md), [agent_heal](../modules/agent_heal.md), [agent_stage_io](../modules/agent_stage_io.md), [server](../modules/server.md) |
| `pineline.config.json` | 4 | [config](../modules/config.md), [install](../modules/install.md), [scripts.check_batch3](../modules/scripts.check_batch3.md), [uploader_settings_api](../modules/uploader_settings_api.md) |
| `qa_flags.json` | 4 | [agent_qa_gate](../modules/agent_qa_gate.md), [agent_stage_io](../modules/agent_stage_io.md), [context_studio.exporter](../modules/context_studio.exporter.md), [server](../modules/server.md) |
| `queue_state.json` | 4 | [film_db](../modules/film_db.md), [lib_check](../modules/lib_check.md), [routes_uploader_settings](../modules/routes_uploader_settings.md), [uploader_settings_api](../modules/uploader_settings_api.md) |
| `source.mp4` | 4 | [agent_av_sync](../modules/agent_av_sync.md), [agent_stage_io](../modules/agent_stage_io.md), [download](../modules/download.md), [server](../modules/server.md) |
| `style_lock.json` | 4 | [agent_qa_gate](../modules/agent_qa_gate.md), [agent_stage_io](../modules/agent_stage_io.md), [context_studio.exporter](../modules/context_studio.exporter.md), [translate](../modules/translate.md) |
| `upload_history.jsonl` | 4 | [auto_publisher](../modules/auto_publisher.md), [film_db](../modules/film_db.md), [routes_uploader_settings](../modules/routes_uploader_settings.md), [uploader_settings_api](../modules/uploader_settings_api.md) |
| `.series.json` | 3 | [agent_feeder](../modules/agent_feeder.md), [hongguo_bridge](../modules/hongguo_bridge.md), [meta_studio](../modules/meta_studio.md) |
| `asr.aligned_repaired.json` | 3 | [asr_spam](../modules/asr_spam.md), [hybrid_asr](../modules/hybrid_asr.md), [server](../modules/server.md) |
| `asr.hardsub.json` | 3 | [asr_spam](../modules/asr_spam.md), [hardsub_asr](../modules/hardsub_asr.md), [server](../modules/server.md) |
| `asr.paraformer_zh.chars.json` | 3 | [asr_align_nano_para](../modules/asr_align_nano_para.md), [asr_repair](../modules/asr_repair.md), [hybrid_asr](../modules/hybrid_asr.md) |
| `config.json` | 3 | [config](../modules/config.md), [mt_zh_vi](../modules/mt_zh_vi.md), [scripts.check_batch2](../modules/scripts.check_batch2.md) |
| `dub_tts.wav` | 3 | [assemble](../modules/assemble.md), [render](../modules/render.md), [server](../modules/server.md) |
| `meta.json` | 3 | [download](../modules/download.md), [render](../modules/render.md), [server](../modules/server.md) |
| `mixed_audio.partial.wav` | 3 | [agent_av_sync](../modules/agent_av_sync.md), [media_ts](../modules/media_ts.md), [render](../modules/render.md) |
| `mixed_audio.wav` | 3 | [agent_av_sync](../modules/agent_av_sync.md), [media_ts](../modules/media_ts.md), [render](../modules/render.md) |
| `output_full.mp4` | 3 | [films_merge_api](../modules/films_merge_api.md), [server](../modules/server.md), [split_parts](../modules/split_parts.md) |
| `script.pre_review.json` | 3 | [agent_heal](../modules/agent_heal.md), [agent_qa_gate](../modules/agent_qa_gate.md), [media_ts](../modules/media_ts.md) |
| `.meta.json` | 2 | [asr_align_nano_para](../modules/asr_align_nano_para.md), [asr_repair](../modules/asr_repair.md) |
| `.partial.mp4` | 2 | [agent_feeder](../modules/agent_feeder.md), [render](../modules/render.md) |
| `.upload.lock` | 2 | [auto_publisher](../modules/auto_publisher.md), [film_db](../modules/film_db.md) |
| `_filter_complex.txt` | 2 | [agent_heal](../modules/agent_heal.md), [render](../modules/render.md) |
| `_job_queue.json` | 2 | [job_queue](../modules/job_queue.md), [scripts.check_batch1](../modules/scripts.check_batch1.md) |
| `_keys.json` | 2 | [clone_tts](../modules/clone_tts.md), [scripts.check_batch4](../modules/scripts.check_batch4.md) |
| `asr.consensus.json` | 2 | [asr_spam](../modules/asr_spam.md), [server](../modules/server.md) |
| `asr.firered.json` | 2 | [asr_spam](../modules/asr_spam.md), [server](../modules/server.md) |
| `asr.nano_fa.json` | 2 | [nano_fa_asr](../modules/nano_fa_asr.md), [server](../modules/server.md) |
| `asr.sensevoice.json` | 2 | [asr_spam](../modules/asr_spam.md), [server](../modules/server.md) |
| `audio.ts.wav` | 2 | [media_ts](../modules/media_ts.md), [scripts.check_batch1](../modules/scripts.check_batch1.md) |
| `audio.wav.json` | 2 | [agent_heal](../modules/agent_heal.md), [scripts.check_batch4](../modules/scripts.check_batch4.md) |
| `autopilot_state.json` | 2 | [agent_autopilot](../modules/agent_autopilot.md), [scripts.check_batch3](../modules/scripts.check_batch3.md) |
| `batch_config.json` | 2 | [batch_config](../modules/batch_config.md), [scripts.check_batch3](../modules/scripts.check_batch3.md) |
| `chatgpt_token.txt` | 2 | [llm](../modules/llm.md), [meta_studio](../modules/meta_studio.md) |
| `client_secret.json` | 2 | [auto_publisher](../modules/auto_publisher.md), [test_channel](../modules/test_channel.md) |
| `feeder_state.json` | 2 | [agent_feeder](../modules/agent_feeder.md), [lib_check](../modules/lib_check.md) |
| `hardsub_band.json` | 2 | [hardsub_asr](../modules/hardsub_asr.md), [render](../modules/render.md) |
| `hardsub_cues.json` | 2 | [hardsub_asr](../modules/hardsub_asr.md), [server](../modules/server.md) |
| `mixed_audio.json` | 2 | [render](../modules/render.md), [scripts.check_batch4](../modules/scripts.check_batch4.md) |
| `orig_audio.wav` | 2 | [media_ts](../modules/media_ts.md), [separate](../modules/separate.md) |
| `qa_brain.json` | 2 | [agent_brain_context](../modules/agent_brain_context.md), [agent_quality](../modules/agent_quality.md) |
| `relation_matrix.json` | 2 | [agent_stage_io](../modules/agent_stage_io.md), [context_studio.exporter](../modules/context_studio.exporter.md) |
| `script.pre_agent_review.json` | 2 | [agent_heal](../modules/agent_heal.md), [server](../modules/server.md) |
| `seg_0000.wav` | 2 | [clone_tts](../modules/clone_tts.md), [scripts.check_batch4](../modules/scripts.check_batch4.md) |
| `settings.json` | 2 | [routes_uploader_settings](../modules/routes_uploader_settings.md), [uploader_settings_api](../modules/uploader_settings_api.md) |
| `token.json` | 2 | [auto_publisher](../modules/auto_publisher.md), [test_channel](../modules/test_channel.md) |
| `vi_alts.json` | 2 | [server](../modules/server.md), [translate_alts](../modules/translate_alts.md) |
| `.audio_ts_fixed.json` | 1 | [media_ts](../modules/media_ts.md) |
| `.audio_ts_pending.json` | 1 | [media_ts](../modules/media_ts.md) |
| `.auto_publish_global.lock` | 1 | [auto_publisher](../modules/auto_publisher.md) |
| `.bak.json` | 1 | [server](../modules/server.md) |
| `.chars.json` | 1 | [paraformer_zh](../modules/paraformer_zh.md) |
| `.cl.wav` | 1 | [clone_tts](../modules/clone_tts.md) |
| `.follow.ass` | 1 | [render](../modules/render.md) |
| `.norm.partial.mp4` | 1 | [hongguo_bridge](../modules/hongguo_bridge.md) |
| `.norm.tmp.mp4` | 1 | [hongguo_bridge](../modules/hongguo_bridge.md) |
| `.nvenc_state.json` | 1 | [render](../modules/render.md) |
| `.partial.wav` | 1 | [separate](../modules/separate.md) |
| `.server_test.lock` | 1 | [scripts.check_batch4](../modules/scripts.check_batch4.md) |
| `.sidecar_18902.lock` | 1 | [scripts.check_batch4](../modules/scripts.check_batch4.md) |
| `.sp.wav` | 1 | [clone_tts](../modules/clone_tts.md) |
| `.tmp.mp4` | 1 | [hongguo_bridge](../modules/hongguo_bridge.md) |
| `.tmp.txt` | 1 | [hongguo_license_ensure](../modules/hongguo_license_ensure.md) |
| `_audio.m4a` | 1 | [render](../modules/render.md) |
| `_chunks.txt` | 1 | [render](../modules/render.md) |
| `_cookies.txt` | 1 | [server](../modules/server.md) |
| `_f5.wav` | 1 | [server](../modules/server.md) |
| `_hg_title_cache.json` | 1 | [title_mt](../modules/title_mt.md) |
| `_job.json` | 1 | [clone_tts](../modules/clone_tts.md) |
| `_meta.json` | 1 | [scripts.brain_build](../modules/scripts.brain_build.md) |
| `_sample90s.mp4` | 1 | [agent_feeder](../modules/agent_feeder.md) |
| `_vieneu_job.json` | 1 | [scripts.check_batch4](../modules/scripts.check_batch4.md) |
| `a.json` | 1 | [scripts.check_batch3](../modules/scripts.check_batch3.md) |
| `a.wav` | 1 | [scripts.check_batch1](../modules/scripts.check_batch1.md) |
| `active.json` | 1 | [preset_switcher](../modules/preset_switcher.md) |
| `agent_brain.log` | 1 | [agent_brain](../modules/agent_brain.md) |
| `agent_brain_last_snapshot.json` | 1 | [agent_brain](../modules/agent_brain.md) |
| `agent_brain_state.json` | 1 | [agent_brain](../modules/agent_brain.md) |
| `agent_watch.log` | 1 | [agent_watch](../modules/agent_watch.md) |
| `agent_watch_state.json` | 1 | [agent_watch](../modules/agent_watch.md) |
| `asr.aligned_fa.meta.json` | 1 | [asr_fix_align](../modules/asr_fix_align.md) |
| `asr.aligned_fix.meta.json` | 1 | [asr_fix_align](../modules/asr_fix_align.md) |
| `asr.aligned_n1.json` | 1 | [server](../modules/server.md) |
| `asr.chars.json` | 1 | [paraformer_zh](../modules/paraformer_zh.md) |
| `asr.fun_nano_retry.json` | 1 | [server](../modules/server.md) |
| `audio.partial.wav` | 1 | [scripts.check_batch4](../modules/scripts.check_batch4.md) |
| `audio_resume.wav` | 1 | [asr](../modules/asr.md) |
| `auto_publish_config.json` | 1 | [auto_publisher](../modules/auto_publisher.md) |
| `auto_publish_queue.json` | 1 | [auto_publisher](../modules/auto_publisher.md) |
| `auto_publish_state.json` | 1 | [auto_publisher](../modules/auto_publisher.md) |
| `b.wav` | 1 | [scripts.check_batch1](../modules/scripts.check_batch1.md) |
| `batch_config2.json` | 1 | [scripts.check_batch3](../modules/scripts.check_batch3.md) |
| `bgm.wav` | 1 | [server](../modules/server.md) |
| `brain_pending_decisions.json` | 1 | [agent_brain](../modules/agent_brain.md) |
| `c.wav` | 1 | [scripts.check_batch1](../modules/scripts.check_batch1.md) |
| `canva_config.json` | 1 | [canva_client](../modules/canva_client.md) |
| `canva_pkce.json` | 1 | [canva_client](../modules/canva_client.md) |
| `canva_token.json` | 1 | [canva_client](../modules/canva_client.md) |
| `censor.json` | 1 | [render](../modules/render.md) |
| `channel.json` | 1 | [test_channel](../modules/test_channel.md) |
| `channel_limit.json` | 1 | [test_channel](../modules/test_channel.md) |
| `chunks_meta.json` | 1 | [separate](../modules/separate.md) |
| `cnt.txt` | 1 | [scripts.check_batch3](../modules/scripts.check_batch3.md) |
| `code_verifier.txt` | 1 | [test_channel](../modules/test_channel.md) |
| `concat.txt` | 1 | [scripts.check_batch1](../modules/scripts.check_batch1.md) |
| `current_oauth_project.txt` | 1 | [test_channel](../modules/test_channel.md) |
| `dub.wav` | 1 | [scripts.check_batch4](../modules/scripts.check_batch4.md) |
| `dub_fit.partial.wav` | 1 | [scripts.check_batch4](../modules/scripts.check_batch4.md) |
| `exhausted.json` | 1 | [test_channel](../modules/test_channel.md) |
| `f5_voices.json` | 1 | [clone_tts](../modules/clone_tts.md) |
| `films.db` | 1 | [film_db](../modules/film_db.md) |
| `final.mp4` | 1 | [auto_publisher](../modules/auto_publisher.md) |
| `full_merged.mp4` | 1 | [scripts.check_batch1](../modules/scripts.check_batch1.md) |
| `generation_config.json` | 1 | [mt_zh_vi](../modules/mt_zh_vi.md) |
| `hardsub_track.json` | 1 | [render](../modules/render.md) |
| `hg_merge_state.json` | 1 | [hongguo_bridge](../modules/hongguo_bridge.md) |
| `hg_title_cache.json` | 1 | [hongguo_bridge](../modules/hongguo_bridge.md) |
| `hongguo_feed_labels.json` | 1 | [hongguo_bridge](../modules/hongguo_bridge.md) |
| `hongguo_play_cache.json` | 1 | [hongguo_rpc](../modules/hongguo_rpc.md) |
| `input.mp4` | 1 | [meta_studio](../modules/meta_studio.md) |
| `kVietnamese.json` | 1 | [hv_auditor](../modules/hv_auditor.md) |
| `list.txt` | 1 | [hongguo_bridge](../modules/hongguo_bridge.md) |
| `list_mp4.txt` | 1 | [agent_feeder](../modules/agent_feeder.md) |
| `list_ts.txt` | 1 | [agent_feeder](../modules/agent_feeder.md) |
| `migrate_work.log` | 1 | [migrate_work](../modules/migrate_work.md) |
| `migrate_work.prev.log` | 1 | [migrate_work](../modules/migrate_work.md) |
| `migrate_work_plan.json` | 1 | [migrate_work](../modules/migrate_work.md) |
| `models.json` | 1 | [preset_switcher](../modules/preset_switcher.md) |
| `nope.mp4` | 1 | [scripts.check_batch1](../modules/scripts.check_batch1.md) |
| `projects.json` | 1 | [test_channel](../modules/test_channel.md) |
| `projects_health.json` | 1 | [test_channel](../modules/test_channel.md) |
| `pronoun_lock.json` | 1 | [pronoun_consistency](../modules/pronoun_consistency.md) |
| `pronoun_qa.json` | 1 | [pronoun_consistency](../modules/pronoun_consistency.md) |
| `qa_hang_trace.json` | 1 | [agent_hang_fix](../modules/agent_hang_fix.md) |
| `ref.wav` | 1 | [scripts.check_batch4](../modules/scripts.check_batch4.md) |
| `requirements-main.txt` | 1 | [install](../modules/install.md) |
| `requirements-vieneu.txt` | 1 | [install](../modules/install.md) |
| `restart_pending.json` | 1 | [restart_server](../modules/restart_server.md) |
| `review_pass1.json` | 1 | [translate](../modules/translate.md) |
| `s.json` | 1 | [scripts.check_batch3](../modules/scripts.check_batch3.md) |
| `s.mp4` | 1 | [lib_check](../modules/lib_check.md) |
| `seg_0001.wav` | 1 | [scripts.check_batch4](../modules/scripts.check_batch4.md) |
| `sfx_levels.json` | 1 | [sfx_lib](../modules/sfx_lib.md) |
| `sfx_lib.json` | 1 | [sfx_lib](../modules/sfx_lib.md) |
| `source.info.json` | 1 | [download](../modules/download.md) |
| `source.m4a` | 1 | [scripts.check_batch4](../modules/scripts.check_batch4.md) |
| `split_manifest.json` | 1 | [split_parts](../modules/split_parts.md) |
| `sub.review_pair.srt` | 1 | [translate](../modules/translate.md) |
| `sub.vi.aligned.srt` | 1 | [meta_studio](../modules/meta_studio.md) |
| `sub.vi.burn.follow.ass` | 1 | [agent_heal](../modules/agent_heal.md) |
| `sub.zh.aligned_fa.srt` | 1 | [hybrid_asr](../modules/hybrid_asr.md) |
| `sub.zh.aligned_fix.srt` | 1 | [hybrid_asr](../modules/hybrid_asr.md) |
| `sub.zh.aligned_repaired.srt` | 1 | [hybrid_asr](../modules/hybrid_asr.md) |
| `sub.zh.analyze.txt` | 1 | [pronoun_consistency](../modules/pronoun_consistency.md) |
| `sub.zh.hardsub.srt` | 1 | [hardsub_asr](../modules/hardsub_asr.md) |
| `sub.zh.nano_fa.srt` | 1 | [nano_fa_asr](../modules/nano_fa_asr.md) |
| `tele_chat_history.json` | 1 | [agent_tele_cmd](../modules/agent_tele_cmd.md) |
| `tokenizer_config.json` | 1 | [mt_zh_vi](../modules/mt_zh_vi.md) |
| `trailer.mp4` | 1 | [scripts.check_batch1](../modules/scripts.check_batch1.md) |
| `v.mp4` | 1 | [scripts.check_batch4](../modules/scripts.check_batch4.md) |
| `video.mp4` | 1 | [meta_studio](../modules/meta_studio.md) |
| `vocab.json` | 1 | [mt_zh_vi](../modules/mt_zh_vi.md) |
| `x.json` | 1 | [scripts.check_batch1](../modules/scripts.check_batch1.md) |
| `zh_full_for_pronoun.txt` | 1 | [pronoun_consistency](../modules/pronoun_consistency.md) |
| `第001集.mp4` | 1 | [scripts.check_batch1](../modules/scripts.check_batch1.md) |
| `第002集.mp4` | 1 | [scripts.check_batch1](../modules/scripts.check_batch1.md) |
