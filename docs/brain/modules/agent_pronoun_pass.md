# `agent_pronoun_pass`

[← Index](../generated/module-index.md) · [Brain home](../README.md)

<!-- AUTO:START — sinh bởi scripts/brain_build.py 2026-11-11 02:37. Đừng sửa tay khối này. -->
**File:** `agent_pronoun_pass.py` · **Lớp:** `agent` · **256 dòng** (231 code) · **4 hàm**, **0 class** · sha1 `a45e71ea8d`

> Rà XƯNG HÔ trong bản dịch theo glossary.pronouns + genre. 1. Quét deterministic (cùng apply_pronoun_postpass) rồi 2. Các câu còn nghi (Ta/Ngươi lệch genre, hoặc cặp who+to có mặt mà self/call lệch)

### Phụ thuộc

- **Gọi tới (import nội bộ):** [config](./config.md), [llm](./llm.md), [manifest](./manifest.md), [pronoun_register_policy](./pronoun_register_policy.md), [subs](./subs.md), [translate](./translate.md)
- **Được dùng bởi:** [pronoun_consistency](./pronoun_consistency.md), [server](./server.md)
- **Test:** ❌ chưa có test import trực tiếp

```mermaid
flowchart LR
  agent_pronoun_pass[[agent_pronoun_pass]]
  pronoun_consistency[pronoun_consistency] --> agent_pronoun_pass
  server[server] --> agent_pronoun_pass
  agent_pronoun_pass --> config[config]
  agent_pronoun_pass --> llm[llm]
  agent_pronoun_pass --> manifest[manifest]
  agent_pronoun_pass --> pronoun_register_policy[pronoun_register_policy]
  agent_pronoun_pass --> subs[subs]
  agent_pronoun_pass --> translate[translate]
```

### Hàm & class top-level

| Tên | Dòng | Dài | Tham số | Docstring |
|---|---:|---:|---|---|
| `_fold` | 22 | 3 | `s` |  |
| `find_pronoun_issues` | 27 | 63 | `rows, plan` |  |
| `_fix_batch` | 92 | 36 | `chunk, plan_block, model, system` |  |
| `run_pronoun_pass` | 130 | 127 ⚠️ | `work_dir, model` |  |

**Hàm dài ≥120 dòng:** `run_pronoun_pass` (127, L130)

### Config / env keys (1)

`PRONOUN_TITLE_POLICY`

**File/artifact nhắc tới:** `glossary.json`, `script.json`, `sub.vi.srt`

**Tín hiệu rủi ro (đếm tĩnh):** broad_except=8 · file_writes=3 · swallow_except=3

### Lịch sử (từ docs/)

- **Fix logs (3):**
  - [Mix #1+#3 + title→ngươi vào production](../../fixes/2026-11-10-mix13-title-nguoi.md)
  - [Pronoun-QA GPT vá đỏ → Aurora 413 (payload quá lớn)](../../fixes/2026-11-06-pronoun-qa-413-slim.md)
  - [Lệch xưng hô sau dịch (Ta–Ngươi / sai self–call)](../../fixes/2026-11-02-pronoun-xung-ho.md)
- Nhắc trong CHANGELOG: **3** lần · DECISIONS: **1** lần

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
