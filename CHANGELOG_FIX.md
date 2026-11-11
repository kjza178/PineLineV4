# Pineline — tổng hợp fix (mang sang máy 5060 Ti)

## 1. Khớp hình + lời (A/V)

- Burn sub theo `tts_fit.json` (mốc sau `assemble_fit`), không theo SRT gốc.
- Assemble: ghép cạnh, không cắt câu; mặc định không nén tốc độ.
- TTS `_dur` lỗi `NameError` — đo độ dài wav đúng chỗ.
- Câu ASR/dịch quá dài: tách **sau dịch** (max ~4s/dòng, wrap 2 dòng × 42 ký tự).
- Không cắt cứng chữ Trung giữa từ (`好养活` → `活，`) — tránh **lệch hàng Trung/Việt**.
- Gộp mảnh vụn ASR (chỉ dấu `，`, clip < 0.45s).
- Tách bilingual: cắt liền mạch cùng câu, không zip 2 cột độc lập.

## 2. ASR (Fun-ASR-Nano / Paraformer / Whisper)

- Engine chọn được trên UI: Fun-ASR-Nano · Paraformer-zh · Whisper.
- File riêng: `fun_asr_nano.py`, `paraformer_zh.py`.
- Fun-ASR-Nano: VAD cắt đoạn + ASR từng clip (model HF không có CTC timestamp).
- Paraformer: `merge_vad=False` — timestamp câu mịn hơn (chữ hơi kém Nano).
- `install_funasr_safe.bat`: cài FunASR **không** kéo torch CPU (khóa `torch==2.11.0+cu128`).
- Timestamp FunASR luôn ms → giây.

## 3. Dịch (Ollama / Gemma)

- Timeout 300s lô 100 câu: ctx Gemma mặc định **128k** → tràn VRAM 12GB, offload CPU.
- Ép `num_ctx=8192`, `num_predict` trần 8k, `think=False`.
- Lô local **50** (40–60); >60 mới hạ. Timeout **không** retry 4 lần — chia đôi lô.
- **Nhả VRAM trước mọi bước GPU**: ASR, dịch, TTS, Demucs, OCR, render (`vram.py` → `ollama stop` + `empty_cache`).

## 4. Render

- NVENC: ép `yuv420p`; nhớ fail → fallback libx264 (`RENDER_ENCODER=auto|nvenc|x264`).
- Che watermark (delogo) + blur hardsub + burn sub Việt + OCR overlay.
- Hardsub blur: **dài ngang** hơn (≥~88%), cao theo OCR (không ép cao); khi kẹp giữ mép dưới chữ Trung.
- **Lật video** lúc render: không / ngang (`h`) / dọc (`v`, úp ngược) / cả hai. Sub Việt không bị chữ gương.
- Zoom+crop, xuất source hoặc 1080p.

## 5. TTS clone

- Mặc định **VieNeu-TTS v3-Turbo** (`mode=v3turbo`) — neural codec + speaker encoder, enroll 1 lần từ wav mẫu.
- OmniVoice là engine phụ (UI đổi được).
- Worker venv riêng; stall/kill/resume.
- **Recheck runaway**: sau TTS, nếu `dur` bất thường so với slot/chữ (vd “Ừm.” 16s) → xóa wav → đọc lại tối đa 2 lần (`TTS_RUNAWAY_RETRIES`) → vẫn lỗi thì silence đúng slot. Resume cũng bỏ clip runaway khỏi “đã xong” (bấm TTS lại là đủ, không cần tool riêng).
- Assemble: cắt trần runaway còn lại (lưới an toàn khi ghép `dub_fit`).
- **Giọng Bắc VieNeu preset** (HF 20 voices / 9 Bắc): `VieNeu_MinhDuc`, `PhamTuyen`, `ThanhBinh`, `TrucLy`, `NgocLinh`, `DoanTrang`, `MaiAnh`, `QuynhAnh`, `NgocHuyen_VieNeu` trong `voices/f5_voices.json` + `voices/vieneu_bac/`.

## 6. Launcher / máy

- `Pineline.bat`: fallback Python hệ thống nếu thiếu `pineline_env`.
- Profile 5060 Ti: CPU threads=2, low priority, batch VieNeu=8.

## Máy 5060 Ti — xem file **CAI_MAY_MOI.md**

Zip không chứa Python/CUDA/Ollama/FFmpeg/model.

Tóm tắt: Driver NVIDIA mới + Python 3.12 + FFmpeg + Ollama (`pull gemma4` + `gemma3:12b`)  
→ `python install.py --gpu --cuda cu128`  
→ FunASR: `install_funasr_safe.bat` (nếu dùng Fun/Paraformer)  
→ `dung-may-5060ti.bat`

## 2026-11-11 — Cấu hình phụ thuộc máy (machine-config)

- Mới `machine.py`: mọi cổng/thư mục phụ thuộc máy thành key `pineline.config.json` (mặc định = máy gốc):
  `LLAMA_BASE_URL`, `AUTO_SWITCH_PRESETS`, `MODEL_PRESETS_DIR`, `MODEL_START_SCRIPT`, `MODEL_START_CMD`,
  `CHATGPT_BASE_URL`/`AURORA_BASE_URL`, `AURORA_FALLBACK_URLS`, `CLOUD_LLM_BASE_URL`, `HONGGUO_BASE_URL`,
  `MT_MODEL_DIR`, `LIBRARY_DIR`, `YT_UPLOADER_DIR`, `LIB_SAMPLE_DIR`.
- preset_switcher: không có presets / `AUTO_SWITCH_PRESETS=0` → bỏ qua đổi preset, không lỗi.
- Aurora không tới được → lỗi rõ, gợi ý đổi `PLAN_MODEL`/`REVIEW_MODEL`/`REVIEW_PASS1_MODEL`.
- Doctor `python scripts\check_env.py [--offline]`; `docs/SETUP_MAY_MOI.md`; `CAI_MAY_MOI.md` viết lại (bỏ Ollama bắt buộc).
- `.gitignore`: `.backup_*/`, `_to_delete/`, `scratch/`, `/work`. Chi tiết: docs/fixes/2026-11-11-machine-config.md

## 2026-11-11 — Bộ cài máy mới 1 file (installer)

- Mới `SETUP_MAY_MOI.bat` (ASCII+CRLF): tìm Python 3.12/3.11 (py launcher, đường dẫn thường gặp, `where python`,
  bỏ stub WindowsApps); không có → hỏi `winget install Python.Python.3.12` (`--yes` bỏ hỏi) → `scripts\setup_machine.py`.
- Mới `scripts/setup_machine.py` (stdlib): detect OS/CPU/RAM/ổ/GPU (`nvidia-smi` query + CUDA header)/công cụ/presets →
  kế hoạch (torch cu128/cu124/cu121/cpu, hồ sơ rtx5060ti/rtx3060/small/cpu, ổ đặt venv, TEMP riêng) → cài (winget
  ffmpeg/git, install.py) → GỘP config → doctor `check_env.py --offline` (`--online-check` mới gọi mạng) → việc tay.
  Cờ `--dry-run --yes --cpu --gpu --cuda --envs-dir --skip-vieneu --with-funasr --with-ollama --online-check
  --scan-requirements`. Log `scratch/setup_<ts>.log`.
- `install.py`: GỘP `pineline.config.json` (không ghi đè; backup `scratch/config_backup/`), launcher `start.bat`/`start.sh`
  trỏ `app_desktop.py`/`server.py` (trước trỏ `app.py` không tồn tại), Ollama pull mặc định TẮT (`--with-ollama`),
  `--cuda` mặc định tự chọn theo GPU (trước cứng cu121), `--dry-run`, `--hf-home`, `--skip-tools`; torch sai build →
  cài lại; ghi `.pineline_env_path`; pip tạm đặt ở `<envs>/.pip_tmp` (trước ở gốc code).
- `run_v4.bat`, `run_tele_cmd.bat`: python `pineline_env` (`.pineline_env_path`) trước `C:\Python312`; TEMP không cứng
  `D:\` (PINELINE_TEMP > `.pineline_tmp_path` > `D:\PinelineV4_tmp` nếu đã có > `scratch\tmp`); ASCII.
- `install_funasr_safe.bat [PY] [BUILD]`, `install_ort_gpu.bat [VPY]`: nhận python từ tham số/biến, bỏ đường dẫn cứng.
- `install/requirements-main.txt` + psutil, huggingface_hub; mới `install/requirements-optional.txt` (funasr, modelscope,
  qwen-asr, transformers/sentencepiece, google-api, pythonnet).
- Test `tests/test_setup_machine.py`. Backup: `.backup_edit_20261111_installer/`.
