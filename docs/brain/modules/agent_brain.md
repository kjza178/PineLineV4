# `agent_brain`

[← Index](../generated/module-index.md) · [Brain home](../README.md)

<!-- AUTO:START — sinh bởi scripts/brain_build.py 2026-11-11 02:37. Đừng sửa tay khối này. -->
**File:** `agent_brain.py` · **Lớp:** `agent` · **1230 dòng** (1097 code) · **35 hàm**, **0 class** · sha1 `a949f2447b`

> Second Brain — daemon nền full-silent. Sensors → incidents → policy → actuators. Bật: AGENT_BRAIN=1 (hoặc pineline.config.json).

### Phụ thuộc

- **Gọi tới (import nội bộ):** [agent_brain_context](./agent_brain_context.md), [agent_core](./agent_core.md), [agent_hang_fix](./agent_hang_fix.md), [agent_heal](./agent_heal.md), [agent_quality](./agent_quality.md), [agent_watch](./agent_watch.md), [config](./config.md), [job_queue](./job_queue.md), [manifest](./manifest.md), [preset_switcher](./preset_switcher.md)
- **Được dùng bởi:** [server](./server.md)
- **Test:** ❌ chưa có test import trực tiếp

```mermaid
flowchart LR
  agent_brain[[agent_brain]]
  server[server] --> agent_brain
  agent_brain --> agent_brain_context[agent_brain_context]
  agent_brain --> agent_core[agent_core]
  agent_brain --> agent_hang_fix[agent_hang_fix]
  agent_brain --> agent_heal[agent_heal]
  agent_brain --> agent_quality[agent_quality]
  agent_brain --> agent_watch[agent_watch]
  agent_brain --> config[config]
  agent_brain --> job_queue[job_queue]
  agent_brain --> manifest[manifest]
  agent_brain --> preset_switcher[preset_switcher]
```

### Hàm & class top-level

| Tên | Dòng | Dài | Tham số | Docstring |
|---|---:|---:|---|---|
| `_self_base` | 21 | 7 | `` | URL server Pineline đang chạy brain (fix 2026-11-11: trước cứng :8801 → V4/V5 điều khiển nhầm V2). |
| `_cfg` | 37 | 9 | `key, default` |  |
| `_truthy` | 48 | 2 | `v` |  |
| `brain_enabled` | 52 | 6 | `` |  |
| `_interval_sec` | 60 | 5 | `` |  |
| `_tg_mode` | 67 | 2 | `` |  |
| `_log_dir` | 71 | 4 | `root` |  |
| `log_line` | 77 | 9 | `root, msg` |  |
| `_state_path` | 88 | 2 | `root` |  |
| `_load_state` | 92 | 8 | `root` |  |
| `_save_state` | 102 | 7 | `root, state` |  |
| `_cooldown_ok` | 111 | 4 | `state, fp, sec` |  |
| `_mark_fp` | 117 | 3 | `state, fp, note` |  |
| `_telegram` | 122 | 16 | `msg, level` |  |
| `_ping` | 140 | 12 | `url, timeout` |  |
| `sense_infra` | 154 | 21 | `` |  |
| `sense_jobs` | 177 | 49 | `work_root, max_jobs` | Quét job có script / failed / stale cho quality + ops hints. |
| `_qa_pipeline_phase` | 228 | 63 | `work_dir` | Perceive: job đang ở đâu — mid_review / pre_tts / post_tts / idle. |
| `_gpu_or_queue_busy` | 293 | 12 | `work_root` |  |
| `decide` | 307 | 39 | `incidents, state` | Policy full-silent → list actions. |
| `apply_actions` | 348 | 191 ⚠️ | `work_root, actions, state, hooks` |  |
| `_llm_enabled` | 541 | 7 | `` |  |
| `_llm_interval_sec` | 550 | 5 | `` |  |
| `_http_json` | 557 | 11 | `method, url, body, timeout` |  |
| `_ensure_brain_runtime` | 570 | 177 ⚠️ | `work_root` | Bind agent_core Runtime nếu chưa có — FS + HTTP proxy (không cần restart :8801). |
| `_run_agent_llm` | 749 | 71 | `message, work_root, max_steps, force_first_tool, force_first_args` | Gọi agent_core tool-loop in-process (bind FS/HTTP nếu cần) hoặc fallback HTTP chat. |
| `llm_tick` | 822 | 185 ⚠️ | `work_root` | LLM Second Brain: đọc snapshot toàn hệ → tool-loop quyết định. |
| `_tg_report_sec` | 1010 | 5 | `` |  |
| `_progress_digest` | 1017 | 72 | `work_root` | Tóm tắt ngắn running/queue cho Telegram. |
| `_maybe_tg_progress` | 1091 | 11 | `work_root, state` |  |
| `tick` | 1104 | 73 | `work_root, hooks, list_jobs` |  |
| `_loop` | 1179 | 14 | `work_root, hooks, list_jobs, interval` |  |
| `start_brain` | 1195 | 22 | `work_root, hooks, list_jobs` |  |
| `stop_brain` | 1219 | 2 | `` |  |
| `brain_once` | 1223 | 8 | `work_root, hooks, list_jobs` | API/ops: chạy 1 tick thủ công. |

**Hàm dài ≥120 dòng:** `apply_actions` (191, L348), `llm_tick` (185, L822), `_ensure_brain_runtime` (177, L570)

### Config / env keys (12)

`AGENT_BRAIN`, `AGENT_BRAIN_LLM`, `AGENT_BRAIN_LLM_SEC`, `AGENT_BRAIN_LLM_STEPS`, `AGENT_BRAIN_MODE`, `AGENT_BRAIN_SEC`, `AGENT_BRAIN_TELEGRAM`, `AGENT_BRAIN_TG_SEC`, `PINELINE_BASE`, `PINELINE_PORT`, `REVIEW_PRESET`, `TRANSLATE_PRESET`

**Cổng nhắc tới:** 3377, 8083, 8802

**File/artifact nhắc tới:** `agent_brain.log`, `agent_brain_last_snapshot.json`, `agent_brain_state.json`, `brain_pending_decisions.json`, `manifest.json`, `script.json`

**Tín hiệu rủi ro (đếm tĩnh):** broad_except=36 · file_writes=5 · global_stmt=1 · swallow_except=8 · threads=1

### Lịch sử (từ docs/)

- **Fix logs (3):**
  - [REVIEW CLI song song + heal làm UI mất/soát % tụt](../../fixes/2026-11-10-review-heal-parallel.md)
  - [Brain thật: perceive → ACT → CLEAR/HOLD cửa TTS](../../fixes/2026-11-10-brain-real-loop.md)
  - [Brain LLM tick trả tools=[] (không gọi tool)](../../fixes/2026-11-09-brain-llm-tool-loop.md)
- Nhắc trong CHANGELOG: **1** lần · DECISIONS: **1** lần

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
