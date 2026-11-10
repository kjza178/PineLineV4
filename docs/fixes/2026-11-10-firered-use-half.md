# FireRedASR mặc định BF16 (use_half)

- **Date:** 2026-11-10
- **Job / khu vực:** `firered_asr.py` (V2/V4/V5)
- **Status:** fixed

## Triệu chứng

FireRedAED chạy FP32 mặc định — chậm hơn / nặng VRAM trên RTX 3060 so với half precision.

## Root cause

`FireRedAsr2Config(use_half=False)` và LID `use_half=False` hardcode trong `firered_asr.py`.

## Evidence

Bench tmp `D:\PinelineV2_tmp\firered_bf16_bench\BENCH.md`: zh_120 FP32 10.97s (RTF 0.27) vs BF16 7.83s (RTF 0.20), text identical, VRAM ~8.5→4.3 GB.

## Fix

- `use_half` mặc định bật khi GPU; tắt bằng `FIRERED_USE_HALF=0` / config.
- Backup: `Z:\PinelineV2_codebak\2026-11-10_firered-use-half\` + zip `Z:\PinelineV2_backup_2026-11-10_0827.zip`

## Recheck

1. Restart server (`run_v2.bat`) rồi chạy job `firered_asr` (hoặc `python firered_asr.py work/<id>`).
2. Log có `half=True`.
3. **Pass nếu:** ASR xong, log half=True, không OOM.
4. **Fail nếu:** half=False dù GPU, hoặc crash load model.

## Liên quan

- Config key: `FIRERED_USE_HALF`
