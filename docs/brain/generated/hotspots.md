# Hotspots — nơi nên soi bug/refactor trước

_Sinh tự động bởi `scripts/brain_build.py` lúc 2026-11-11 02:37. Đừng sửa tay — chạy lại script._


Điểm = LOC/500 + 2×fix log + 0.15×nhắc CHANGELOG + 1×hàm dài + 0.1×`except Exception` + 1×bare except + 0.5×nuốt lỗi (`except: pass`) + 0.5×Thread + 0.3×`global` + 3 nếu >800 dòng mà không test.
Đây là **heuristic để ưu tiên**, không phải kết luận có bug.

| # | Module | Điểm | Dòng | Fix | Hàm dài | broad/bare/swallow except | Thread | Test |
|---:|---|---:|---:|---:|---:|---|---:|---|
| 1 | [server](../modules/server.md) | 140.6 | 6644 | 31 | 5 | 206/0/72 | 0 | ✅ |
| 2 | [translate](../modules/translate.md) | 69.8 | 4128 | 21 | 6 | 60/0/12 | 0 | ✅ |
| 3 | [hongguo_bridge](../modules/hongguo_bridge.md) | 68.2 | 4216 | 15 | 5 | 89/0/25 | 1 | ✅ |
| 4 | [render](../modules/render.md) | 56.8 | 3061 | 15 | 7 | 33/0/15 | 1 | ✅ |
| 5 | [agent_tele_cmd](../modules/agent_tele_cmd.md) | 52.2 | 2333 | 11 | 4 | 58/0/10 | 11 | ❌ |
| 6 | [agent_feeder](../modules/agent_feeder.md) | 40.5 | 2065 | 7 | 4 | 40/0/20 | 0 | ❌ |
| 7 | [hongguo_rpc](../modules/hongguo_rpc.md) | 37.3 | 1449 | 10 | 0 | 22/0/9 | 5 | ❌ |
| 8 | [auto_publisher](../modules/auto_publisher.md) | 31.4 | 1567 | 4 | 1 | 44/0/25 | 2 | ✅ |
| 9 | [job_queue](../modules/job_queue.md) | 25.7 | 658 | 9 | 0 | 10/0/2 | 1 | ✅ |
| 10 | [meta_studio](../modules/meta_studio.md) | 25.5 | 1918 | 2 | 5 | 36/0/17 | 0 | ✅ |
| 11 | [test_channel](../modules/test_channel.md) | 25.3 | 1435 | 3 | 0 | 34/0/15 | 2 | ❌ |
| 12 | [agent_hongguo](../modules/agent_hongguo.md) | 24.4 | 1570 | 3 | 1 | 33/0/12 | 1 | ❌ |
| 13 | [agent_brain](../modules/agent_brain.md) | 23.0 | 1230 | 3 | 3 | 36/0/8 | 1 | ❌ |
| 14 | [routes_hg](../modules/routes_hg.md) | 21.3 | 1018 | 6 | 0 | 53/0/3 | 0 | ✅ |
| 15 | [agent_core](../modules/agent_core.md) | 20.4 | 2072 | 6 | 1 | 5/0/1 | 0 | ✅ |
| 16 | [split_parts](../modules/split_parts.md) | 19.8 | 828 | 6 | 2 | 8/0/0 | 0 | ❌ |
| 17 | [llm](../modules/llm.md) | 18.8 | 894 | 5 | 1 | 22/0/5 | 0 | ✅ |
| 18 | [film_db](../modules/film_db.md) | 18.0 | 1091 | 4 | 0 | 19/0/11 | 0 | ✅ |
| 19 | [clone_tts](../modules/clone_tts.md) | 17.2 | 1115 | 1 | 2 | 19/0/10 | 1 | ❌ |
| 20 | [restart_server](../modules/restart_server.md) | 17.1 | 237 | 7 | 0 | 5/0/0 | 0 | ❌ |
| 21 | [routes_agent](../modules/routes_agent.md) | 11.8 | 645 | 4 | 0 | 24/0/0 | 0 | ✅ |
| 22 | [series_glossary](../modules/series_glossary.md) | 11.3 | 199 | 4 | 0 | 8/0/4 | 0 | ❌ |
| 23 | [routes_uploader_settings](../modules/routes_uploader_settings.md) | 11.2 | 607 | 2 | 0 | 18/0/8 | 0 | ❌ |
| 24 | [uploader_settings_api](../modules/uploader_settings_api.md) | 11.2 | 670 | 2 | 0 | 22/0/7 | 0 | ❌ |
| 25 | [agent_heal](../modules/agent_heal.md) | 11.1 | 665 | 1 | 2 | 16/0/8 | 0 | ❌ |
| 26 | [batch_config](../modules/batch_config.md) | 10.6 | 295 | 4 | 0 | 2/0/0 | 0 | ✅ |
| 27 | [agent_autopilot](../modules/agent_autopilot.md) | 10.5 | 331 | 4 | 0 | 6/0/0 | 0 | ❌ |
| 28 | [agent_pronoun_pass](../modules/agent_pronoun_pass.md) | 10.3 | 256 | 3 | 1 | 8/0/3 | 0 | ❌ |
| 29 | [agent_av_sync](../modules/agent_av_sync.md) | 10.0 | 567 | 3 | 1 | 9/0/1 | 0 | ❌ |
| 30 | [pronoun_consistency](../modules/pronoun_consistency.md) | 9.6 | 870 | 2 | 1 | 11/0/3 | 0 | ✅ |
| 31 | [asr](../modules/asr.md) | 8.8 | 442 | 2 | 1 | 8/0/2 | 1 | ✅ |
| 32 | [agent_hang_fix](../modules/agent_hang_fix.md) | 8.1 | 368 | 2 | 1 | 7/0/3 | 0 | ❌ |
| 33 | [scripts.brain_build](../modules/scripts.brain_build.md) | 8.1 | 857 | 0 | 2 | 4/0/2 | 0 | ❌ |
| 34 | [download](../modules/download.md) | 8.0 | 692 | 2 | 1 | 10/0/0 | 1 | ❌ |
| 35 | [scripts.check_batch3](../modules/scripts.check_batch3.md) | 7.8 | 197 | 3 | 0 | 0/0/0 | 2 | ❌ |
| 36 | [config](../modules/config.md) | 7.5 | 188 | 3 | 0 | 2/0/0 | 0 | ✅ |
| 37 | [agent_watch](../modules/agent_watch.md) | 7.2 | 375 | 1 | 0 | 12/0/5 | 1 | ❌ |
| 38 | [media_ts](../modules/media_ts.md) | 7.1 | 304 | 3 | 0 | 0/0/0 | 0 | ❌ |
| 39 | [fun_asr_nano](../modules/fun_asr_nano.md) | 6.9 | 597 | 1 | 1 | 12/0/3 | 0 | ❌ |
| 40 | [mux](../modules/mux.md) | 6.8 | 135 | 3 | 0 | 2/0/0 | 0 | ❌ |
