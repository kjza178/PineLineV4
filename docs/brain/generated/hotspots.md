# Hotspots — nơi nên soi bug/refactor trước

_Sinh tự động bởi `scripts/brain_build.py` lúc 2026-11-17 19:05. Đừng sửa tay — chạy lại script._


Điểm = LOC/500 + 2×fix log + 0.15×nhắc CHANGELOG + 1×hàm dài + 0.1×`except Exception` + 1×bare except + 0.5×nuốt lỗi (`except: pass`) + 0.5×Thread + 0.3×`global` + 3 nếu >800 dòng mà không test.
Đây là **heuristic để ưu tiên**, không phải kết luận có bug.

| # | Module | Điểm | Dòng | Fix | Hàm dài | broad/bare/swallow except | Thread | Test |
|---:|---|---:|---:|---:|---:|---|---:|---|
| 1 | [server](../modules/server.md) | 172.2 | 7322 | 43 | 6 | 235/0/74 | 0 | ✅ |
| 2 | [translate](../modules/translate.md) | 87.4 | 5167 | 27 | 7 | 71/0/14 | 0 | ✅ |
| 3 | [hongguo_bridge](../modules/hongguo_bridge.md) | 65.1 | 3676 | 16 | 4 | 66/0/23 | 1 | ✅ |
| 4 | [render](../modules/render.md) | 61.2 | 3143 | 17 | 7 | 34/0/15 | 1 | ✅ |
| 5 | [agent_tele_cmd](../modules/agent_tele_cmd.md) | 56.7 | 2464 | 14 | 4 | 61/0/10 | 12 | ✅ |
| 6 | [agent_feeder](../modules/agent_feeder.md) | 42.5 | 2066 | 8 | 4 | 40/0/20 | 0 | ❌ |
| 7 | [agent_brain](../modules/agent_brain.md) | 40.1 | 2201 | 9 | 3 | 65/0/13 | 1 | ✅ |
| 8 | [hongguo_rpc](../modules/hongguo_rpc.md) | 36.9 | 1435 | 10 | 0 | 21/0/8 | 5 | ❌ |
| 9 | [auto_publisher](../modules/auto_publisher.md) | 33.4 | 1567 | 5 | 1 | 44/0/25 | 2 | ✅ |
| 10 | [meta_studio](../modules/meta_studio.md) | 30.8 | 2084 | 4 | 5 | 39/0/18 | 0 | ✅ |
| 11 | [split_parts](../modules/split_parts.md) | 30.0 | 1100 | 11 | 3 | 14/0/2 | 0 | ✅ |
| 12 | [test_channel](../modules/test_channel.md) | 27.9 | 1444 | 4 | 0 | 35/0/16 | 2 | ❌ |
| 13 | [job_queue](../modules/job_queue.md) | 27.7 | 667 | 10 | 0 | 10/0/2 | 1 | ✅ |
| 14 | [llm](../modules/llm.md) | 26.7 | 1167 | 8 | 1 | 31/0/5 | 0 | ✅ |
| 15 | [asr](../modules/asr.md) | 26.6 | 488 | 10 | 1 | 11/0/4 | 1 | ✅ |
| 16 | [agent_hongguo](../modules/agent_hongguo.md) | 26.4 | 1570 | 4 | 1 | 33/0/12 | 1 | ❌ |
| 17 | [agent_heal](../modules/agent_heal.md) | 24.8 | 830 | 6 | 3 | 22/0/11 | 0 | ✅ |
| 18 | [routes_hg](../modules/routes_hg.md) | 23.9 | 1107 | 7 | 0 | 56/0/3 | 0 | ✅ |
| 19 | [routes_agent](../modules/routes_agent.md) | 21.8 | 815 | 7 | 0 | 33/0/4 | 0 | ✅ |
| 20 | [agent_core](../modules/agent_core.md) | 20.6 | 2115 | 6 | 1 | 6/0/1 | 0 | ✅ |
| 21 | [film_db](../modules/film_db.md) | 20.0 | 1091 | 5 | 0 | 19/0/11 | 0 | ✅ |
| 22 | [restart_server](../modules/restart_server.md) | 19.4 | 250 | 8 | 0 | 6/0/0 | 0 | ❌ |
| 23 | [media_ts](../modules/media_ts.md) | 18.7 | 1014 | 7 | 2 | 1/0/0 | 0 | ✅ |
| 24 | [agent_autopilot](../modules/agent_autopilot.md) | 16.6 | 348 | 7 | 0 | 6/0/0 | 0 | ✅ |
| 25 | [series_glossary](../modules/series_glossary.md) | 15.3 | 199 | 6 | 0 | 8/0/4 | 0 | ✅ |
| 26 | [firered_asr](../modules/firered_asr.md) | 14.9 | 565 | 6 | 1 | 5/0/0 | 0 | ✅ |
| 27 | [separate](../modules/separate.md) | 14.6 | 570 | 5 | 1 | 7/0/2 | 0 | ✅ |
| 28 | [clone_tts](../modules/clone_tts.md) | 14.2 | 1115 | 1 | 2 | 19/0/10 | 1 | ✅ |
| 29 | [agent_av_sync](../modules/agent_av_sync.md) | 14.1 | 569 | 5 | 1 | 9/0/1 | 0 | ❌ |
| 30 | [routes_uploader_settings](../modules/routes_uploader_settings.md) | 13.3 | 611 | 3 | 0 | 18/0/8 | 0 | ❌ |
| 31 | [translate_simple.cfg](../modules/translate_simple.cfg.md) | 13.3 | 372 | 6 | 0 | 4/0/0 | 0 | ✅ |
| 32 | [uploader_settings_api](../modules/uploader_settings_api.md) | 13.2 | 675 | 3 | 0 | 22/0/7 | 0 | ❌ |
| 33 | [mux](../modules/mux.md) | 12.9 | 132 | 6 | 0 | 2/0/0 | 0 | ✅ |
| 34 | [download](../modules/download.md) | 12.3 | 706 | 4 | 1 | 11/0/0 | 1 | ❌ |
| 35 | [translate_simple.pipeline](../modules/translate_simple.pipeline.md) | 12.2 | 497 | 4 | 1 | 17/0/1 | 0 | ✅ |
| 36 | [agent_watch](../modules/agent_watch.md) | 11.9 | 408 | 3 | 0 | 16/0/5 | 1 | ✅ |
| 37 | [config](../modules/config.md) | 11.6 | 194 | 5 | 0 | 2/0/0 | 0 | ✅ |
| 38 | [agent_brain_context](../modules/agent_brain_context.md) | 11.3 | 287 | 4 | 0 | 9/0/3 | 0 | ✅ |
| 39 | [fun_asr_nano](../modules/fun_asr_nano.md) | 10.9 | 597 | 3 | 1 | 12/0/3 | 0 | ❌ |
| 40 | [manifest](../modules/manifest.md) | 10.9 | 262 | 5 | 0 | 2/0/0 | 0 | ✅ |
