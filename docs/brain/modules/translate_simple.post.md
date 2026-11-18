# `translate_simple.post`

[← Index](../generated/module-index.md) · [Brain home](../README.md)

<!-- AUTO:START — sinh bởi scripts/brain_build.py 2026-11-17 19:05. Đừng sửa tay khối này. -->
**File:** `translate_simple/post.py` · **Lớp:** `translate` · **76 dòng** (63 code) · **3 hàm**, **0 class** · sha1 `d5a6e9d3f1`

> Hậu kỳ tất định của luồng simple — KHÔNG regex đổi đại từ: 1) chuẩn dấu nghìn (translate.normalize_vi_thousands) 2) gỡ lặp ASR/VI tất định (translate.heal_obvious_internal_stutter — CÙNG hàm luồng cũ dùng trong

### Phụ thuộc

- **Gọi tới (import nội bộ):** [translate](./translate.md), [translate_simple.script_store](./translate_simple.script_store.md)
- **Được dùng bởi:** [translate_simple.pipeline](./translate_simple.pipeline.md), [translate_simple.repair](./translate_simple.repair.md)
- **Test:** `tests/test_translate_simple_next_review.py`

```mermaid
flowchart LR
  translate_simple_post[[translate_simple.post]]
  translate_simple_pipeline[translate_simple.pipeline] --> translate_simple_post
  translate_simple_repair[translate_simple.repair] --> translate_simple_post
  translate_simple_post --> translate[translate]
  translate_simple_post --> translate_simple_script_store[translate_simple.script_store]
```

### Hàm & class top-level

| Tên | Dòng | Dài | Tham số | Docstring |
|---|---:|---:|---|---|
| `_zh_stutter` | 23 | 9 | `T, r, stutter_i` | ZH của câu có lặp ASR: còn lặp (câu rv giữ zh) hoặc ASR gốc lặp (pipeline đã gỡ ở bước dựng script). |
| `heal_vi` | 34 | 10 | `T, vi` | translate.heal_obvious_internal_stutter + dọn dấu phẩy treo («Giết đi,!» → «Giết đi!», «,,» → «,»). |
| `apply` | 46 | 31 | `store, plan, rows` |  |

**Tín hiệu rủi ro (đếm tĩnh):** broad_except=1

### Lịch sử (từ docs/)

- **Fix logs (1):**
  - [translate-simple «next»: lexicon src · bảng quy tắc xưng hô · bổ sung cặp thiếu · học lại · nguồn ZH · gỡ lặp ](../../fixes/2026-11-12-translate-simple-next.md)
- **Reviews:** [2026-11-12-translate-simple-next-review](../../reviews/2026-11-12-translate-simple-next-review.md)
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
