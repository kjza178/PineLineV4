# `translate_simple.plan_view`

[← Index](../generated/module-index.md) · [Brain home](../README.md)

<!-- AUTO:START — sinh bởi scripts/brain_build.py 2026-11-17 19:05. Đừng sửa tay khối này. -->
**File:** `translate_simple/plan_view.py` · **Lớp:** `translate` · **215 dòng** (188 code) · **5 hàm**, **1 class** · sha1 `9b224bb27f`

> Đọc plan (glossary.json) cho luồng simple: nhân vật, cặp xưng hô, cảnh, thuật ngữ — và khối plan thu gọn THEO LÔ (chỉ nhân vật có mặt / cặp liên quan / cảnh phủ lô / thuật ngữ xuất hiện).

### Phụ thuộc

- **Gọi tới (import nội bộ):** —
- **Được dùng bởi:** [translate_simple.pair_fill](./translate_simple.pair_fill.md), [translate_simple.pair_rules](./translate_simple.pair_rules.md), [translate_simple.pipeline](./translate_simple.pipeline.md), [translate_simple.repair](./translate_simple.repair.md), [translate_simple.stage_review](./translate_simple.stage_review.md), [translate_simple.suggest](./translate_simple.suggest.md), [translate_simple.validate](./translate_simple.validate.md)
- **Test:** `tests/test_simple_junk_park.py`, `tests/test_simple_r1_bugs.py`, `tests/test_translate_simple.py`, `tests/test_translate_simple_a7_a8.py`, `tests/test_translate_simple_next.py`, `tests/test_translate_simple_next_review.py`, `tests/test_translate_simple_scenarios.py`

```mermaid
flowchart LR
  translate_simple_plan_view[[translate_simple.plan_view]]
  translate_simple_pair_fill[translate_simple.pair_fill] --> translate_simple_plan_view
  translate_simple_pair_rules[translate_simple.pair_rules] --> translate_simple_plan_view
  translate_simple_pipeline[translate_simple.pipeline] --> translate_simple_plan_view
  translate_simple_repair[translate_simple.repair] --> translate_simple_plan_view
  translate_simple_stage_review[translate_simple.stage_review] --> translate_simple_plan_view
  translate_simple_suggest[translate_simple.suggest] --> translate_simple_plan_view
  translate_simple_validate[translate_simple.validate] --> translate_simple_plan_view
```

### Hàm & class top-level

| Tên | Dòng | Dài | Tham số | Docstring |
|---|---:|---:|---|---|
| **class `PlanView`** | 54 | 11 method | |  |
| `nfc` | 12 | 2 | `s` |  |
| `norm_name` | 16 | 4 | `s` |  |
| `forms` | 22 | 16 | `v` | «anh / học trưởng» → ['anh', 'học trưởng'] (giữ thứ tự, bỏ trùng). |
| `_alts` | 40 | 2 | `xs` |  |
| `pair_line` | 44 | 8 | `p` | 1 dòng cặp xưng hô cho prompt — review 2026-11-12: tách rõ tự xưng / gọi (trước đây |

### Lịch sử (từ docs/)

- **Fix logs (2):**
  - [translate-simple: luồng dịch mới (plan ∥ NMT → review 1 lần/lô → vá câu bị cờ → cổng), sau cờ TRANSLATE_PIPELI](../../fixes/2026-11-12-translate-simple.md)
  - [translate-simple «next»: lexicon src · bảng quy tắc xưng hô · bổ sung cặp thiếu · học lại · nguồn ZH · gỡ lặp ](../../fixes/2026-11-12-translate-simple-next.md)
- Nhắc trong CHANGELOG: **0** lần · DECISIONS: **0** lần

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
