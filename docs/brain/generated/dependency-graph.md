# Phụ thuộc giữa các lớp

_Sinh tự động bởi `scripts/brain_build.py` lúc 2026-11-11 02:37. Đừng sửa tay — chạy lại script._


Cạnh A → B = module lớp A import module lớp B (số = số cặp module).

```mermaid
flowchart LR
  agent -->|18| control
  agent -->|1| ops
  agent -->|1| publish
  agent -->|3| render
  agent -->|1| source
  agent -->|8| translate
  agent -->|1| tts
  asr -->|13| control
  asr -->|11| ops
  asr -->|14| render
  asr -->|3| translate
  context -->|1| translate
  control -->|12| agent
  control -->|6| asr
  control -->|5| context
  control -->|5| ops
  control -->|9| publish
  control -->|6| render
  control -->|2| sidecar
  control -->|8| source
  control -->|6| translate
  control -->|1| tts
  ops -->|4| agent
  ops -->|1| asr
  ops -->|10| control
  ops -->|2| publish
  ops -->|4| render
  ops -->|5| sidecar
  ops -->|3| source
  ops -->|3| translate
  ops -->|1| tts
  publish -->|6| control
  publish -->|4| ops
  publish -->|1| render
  publish -->|1| sidecar
  publish -->|2| source
  publish -->|2| translate
  render -->|1| asr
  render -->|7| control
  render -->|1| ops
  render -->|1| publish
  sidecar -->|2| agent
  sidecar -->|4| control
  sidecar -->|2| ops
  sidecar -->|9| publish
  sidecar -->|2| source
  sidecar -->|2| translate
  source -->|2| control
  source -->|1| publish
  translate -->|3| agent
  translate -->|1| context
  translate -->|9| control
  translate -->|3| ops
  translate -->|1| publish
  translate -->|2| render
  translate -->|1| source
  tts -->|2| control
  tts -->|1| ops
  tts -->|1| render
```

## Ngược chiều đáng chú ý

Lớp pipeline/media (`source/asr/translate/tts/render`) import ngược `control`/`agent` là dấu hiệu coupling cần xem.

- [pronoun_consistency](../modules/pronoun_consistency.md) → [agent_pronoun_pass](../modules/agent_pronoun_pass.md)
- [script_lint](../modules/script_lint.md) → [agent_name_pass](../modules/agent_name_pass.md)
- [translate](../modules/translate.md) → [agent_hang_fix](../modules/agent_hang_fix.md)
- [translate](../modules/translate.md) → [batch_config](../modules/batch_config.md)

## Fan-in / fan-out

| Module | Fan-in (được import) | Fan-out (import) | Hot-reload |
|---|---:|---:|---|
| [server](../modules/server.md) | 5 | 40 |  |
| [manifest](../modules/manifest.md) | 28 | 1 |  |
| [translate](../modules/translate.md) | 9 | 15 |  |
| [config](../modules/config.md) | 25 | 0 |  |
| [agent_tele_cmd](../modules/agent_tele_cmd.md) | 3 | 17 | canva_client, check_block, lib_check, meta_studio, test_channel |
| [film_db](../modules/film_db.md) | 15 | 2 | check_block |
| [subs](../modules/subs.md) | 17 | 1 |  |
| [llm](../modules/llm.md) | 14 | 2 |  |
| [agent_core](../modules/agent_core.md) | 4 | 10 |  |
| [hongguo_bridge](../modules/hongguo_bridge.md) | 11 | 4 |  |
| [vram](../modules/vram.md) | 16 | 0 |  |
| [render](../modules/render.md) | 4 | 9 |  |
| [asr](../modules/asr.md) | 7 | 6 |  |
| [fun_asr_nano](../modules/fun_asr_nano.md) | 7 | 7 |  |
| [auto_publisher](../modules/auto_publisher.md) | 4 | 6 |  |
| [agent_brain](../modules/agent_brain.md) | 1 | 10 |  |
| [routes_agent](../modules/routes_agent.md) | 1 | 9 |  |
| [agent_hang_fix](../modules/agent_hang_fix.md) | 4 | 6 |  |
| [agent_watch](../modules/agent_watch.md) | 7 | 3 |  |
| [batch_config](../modules/batch_config.md) | 8 | 1 |  |
| [job_queue](../modules/job_queue.md) | 8 | 0 |  |
| [meta_studio](../modules/meta_studio.md) | 4 | 5 |  |
| [paraformer_zh](../modules/paraformer_zh.md) | 1 | 9 |  |
| [asr_spam](../modules/asr_spam.md) | 7 | 2 |  |
| [hybrid_asr](../modules/hybrid_asr.md) | 0 | 9 |  |
| [routes_hg](../modules/routes_hg.md) | 1 | 7 |  |
| [scripts.check_batch4](../modules/scripts.check_batch4.md) | 0 | 9 |  |
| [agent_autopilot](../modules/agent_autopilot.md) | 6 | 2 |  |
| [agent_hongguo](../modules/agent_hongguo.md) | 3 | 5 |  |
| [agent_pronoun_pass](../modules/agent_pronoun_pass.md) | 2 | 6 |  |
| [assemble](../modules/assemble.md) | 8 | 0 |  |
| [fileio](../modules/fileio.md) | 8 | 0 |  |
| [lib_check](../modules/lib_check.md) | 5 | 3 |  |
| [media_ts](../modules/media_ts.md) | 7 | 1 |  |
| [routes_uploader_settings](../modules/routes_uploader_settings.md) | 0 | 8 |  |
| [agent_feeder](../modules/agent_feeder.md) | 2 | 5 |  |
| [agent_quality](../modules/agent_quality.md) | 4 | 2 |  |
| [clone_tts](../modules/clone_tts.md) | 3 | 4 |  |
| [firered_asr](../modules/firered_asr.md) | 0 | 7 |  |
| [pronoun_consistency](../modules/pronoun_consistency.md) | 1 | 5 |  |

## Không ai import và không ai nhắc tên file (ứng viên code chết — kiểm .bat/UI trước khi xoá)

[app_desktop](../modules/app_desktop.md), [context_studio.__init__](../modules/context_studio.__init__.md), [context_studio.app_streamlit](../modules/context_studio.app_streamlit.md), [mux](../modules/mux.md)
