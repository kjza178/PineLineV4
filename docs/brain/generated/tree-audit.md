# Tree audit — PinelineV4

_Sinh bởi `scripts/tree_audit.py` lúc 2026-11-10 19:38. ERROR = sẽ hỏng khi chạy; WARN = nên xem._

**ERROR: 0** · import lỗi 6 · cổng lạ 3 · module trùng tên 0

## Import không resolve

| Mức | File | Dòng | Module |
|---|---|---:|---|
| WARN | `film_db.py` | 893 | `agents.hongguo_bridge` |
| WARN | `film_db.py` | 1012 | `agents.hongguo_bridge` |
| WARN | `hongguo_bridge.py` | 53 | `core.config` |
| WARN | `hongguo_bridge.py` | 69 | `agents.hongguo_rpc` |
| WARN | `hongguo_bridge.py` | 975 | `core.config` |
| WARN | `hongguo_bridge.py` | 2949 | `core` |

## Cổng của cây khác

| Mức | File | Dòng | Chi tiết |
|---|---|---:|---|
| WARN | `agent_tele_cmd.py` | 69 | :8801 (cây này 8804) — BASE = (os.getenv("PINELINE_BASE") or "http://127.0.0.1:8801").strip().rstrip("/") |
| WARN | `agent_tool_loop.py` | 10 | :8801 (cây này 8804) — python agent_tool_loop.py --base http://127.0.0.1:8801 --job ID --stages translate --dry |
| WARN | `agent_tool_loop.py` | 443 | :8801 (cây này 8804) — p.add_argument("--base", default=os.getenv("PINELINE_BASE") or "http://127.0.0.1:8801") |

## Module trùng tên

| Mức | Tên | Bản [md5] |
|---|---|---|
| — | | |

## So với cây khác

- **WARN** `docs/STATE.md` GIỐNG HỆT PinelineV2 — có thể bị sync đè (file này nên riêng từng cây)
- **WARN** `docs/ARCHITECTURE.md` GIỐNG HỆT PinelineV2 — có thể bị sync đè (file này nên riêng từng cây)
- **INFO** so PinelineV2: root .py giống 56, khác 28 (agent_autopilot.py, agent_brain.py, agent_brain_context.py, agent_heal.py, agent_hongguo.py, agent_name_pass.py, agent_tele_cmd.py, agent_tool_loop.py, agent_watch.py, canva_client.py, fileio.py, films_merge_api.py, hg_ui_ctx.py, hongguo_license_ensure.py, hongguo_rpc.py, hv_auditor.py, lib_check.py, llm.py, manifest.py, meta_studio.py, migrate_work.py, mt_zh_vi.py, preset_switcher.py, pronoun_consistency.py, restart_server.py…)
- **WARN** `docs/STATE.md` GIỐNG HỆT PinelineV5 — có thể bị sync đè (file này nên riêng từng cây)
- **WARN** `docs/ARCHITECTURE.md` GIỐNG HỆT PinelineV5 — có thể bị sync đè (file này nên riêng từng cây)
- **INFO** so PinelineV5: root .py giống 28, khác 10 (agent_brain.py, agent_brain_context.py, agent_tele_cmd.py, agent_tool_loop.py, app_desktop.py, meta_studio.py, render.py, restart_server.py, server.py, translate.py)
