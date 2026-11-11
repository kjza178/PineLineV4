# `context_studio.app_streamlit`

[← Index](../generated/module-index.md) · [Brain home](../README.md)

<!-- AUTO:START — sinh bởi scripts/brain_build.py 2026-11-11 02:37. Đừng sửa tay khối này. -->
**File:** `context_studio/app_streamlit.py` · **Lớp:** `context` · **108 dòng** (95 code) · **0 hàm**, **0 class** · sha1 `a99bcc1ff3`

> Streamlit UI stub — Context Detection trước khi dịch Pineline. Chạy: pip install streamlit

### Phụ thuộc

- **Gọi tới (import nội bộ):** [context_studio.analyzer](./context_studio.analyzer.md), [context_studio.character_mapper](./context_studio.character_mapper.md), [context_studio.exporter](./context_studio.exporter.md), [context_studio.schema](./context_studio.schema.md), [context_studio.srt_io](./context_studio.srt_io.md)
- **Được dùng bởi:** —
- **Test:** ❌ chưa có test import trực tiếp
- **Thư viện ngoài:** `streamlit`

```mermaid
flowchart LR
  context_studio_app_streamlit[[context_studio.app_streamlit]]
  context_studio_app_streamlit --> context_studio_analyzer[context_studio.analyzer]
  context_studio_app_streamlit --> context_studio_character_mapper[context_studio.character_mapper]
  context_studio_app_streamlit --> context_studio_exporter[context_studio.exporter]
  context_studio_app_streamlit --> context_studio_schema[context_studio.schema]
  context_studio_app_streamlit --> context_studio_srt_io[context_studio.srt_io]
```

**File/artifact nhắc tới:** `glossary.json`

### Lịch sử (từ docs/)

- Fix logs: —
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
