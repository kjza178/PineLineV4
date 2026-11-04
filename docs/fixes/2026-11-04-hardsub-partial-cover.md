# Che hardsub chỗ có chỗ không — chữ Trung lộ 2 mép

- **Date:** 2026-11-04
- **Job / khu vực:** `render.py` hardsub track/stretch/blur (V2/V4/V5)
- **Status:** fixed
- **Backup:** `Z:\PinelineV2_codebak\2026-11-04_hardsub-fullw\`

## Triệu chứng

Frame có phụ đề Việt đè giữa; chữ Trung hardsub vẫn thấy rõ **hai bên** (chỉ vùng giữa bị che/mờ).

## Root cause

`hardsub_track.json` OCR ghi `x0≈0.24…x1≈0.76` (~52% ngang). Che dùng đúng OCR x → dải hẹp giữa khung. Comment code đã nói «không tin x0/x1» nhưng `_hardsub_track_boxes` vẫn lấy OCR. Ba bản `render.py` hash giống nhau.

## Evidence

- Track job mẫu: `x0=0.24 x1=0.76` → box `(468,888,984,90)` trên 1920.
- Screenshot: 还真 / 大幸啊 lộ, giữa mới bị che.

## Fix

- `_hardsub_cover_fullw` + `_hardsub_track_boxes`: mặc định `x0=0,x1=1`; pad dọc tăng.
- Stretch **và** blur đều ép full ngang; band fallback `HARDSUB_BLUR_W=1.0`.
- Gộp khoảng thời gian OCR rộng hơn (tránh hở giữa mẫu).
- Config V2/V4/V5: `HARDSUB_COVER_FULLW=1`, `HARDSUB_BLUR_W=1.0`, pad top/bottom.

## Recheck

1. Remux 1 job có hardsub đáy (xoá `hardsub_track.json` nếu muốn detect lại).
2. Frame có chữ Trung dài: **Pass** nếu cả dòng bị che hết ngang; **Fail** nếu còn chữ rõ 2 mép.
