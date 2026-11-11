# Máy mới — cài GÌ ngoài code (git / zip)

Code (git `kjza178/PineLineV4` hoặc zip) **chỉ có code**. Hướng dẫn đầy đủ + bảng key: **`docs/SETUP_MAY_MOI.md`**.
Kiểm tra máy: **`python scripts\check_env.py`** (doctor: OK / THIẾU / TUỲ CHỌN + cách sửa).

Cập nhật 2026-11-11: bỏ "Ollama bắt buộc" (sai so với code). Mọi cổng/thư mục phụ thuộc máy là key trong
`pineline.config.json` (mẫu: `pineline.config.example.json`, mục `_machine_keys_help`).

---

## Bắt buộc

| Cái | Để làm gì | Ghi chú |
|-----|-----------|---------|
| **NVIDIA Driver** mới | CUDA / NVENC | `nvidia-smi` ra GPU. 50-series (Blackwell) cần driver mới. |
| **Python 3.11 hoặc 3.12** | 64-bit, tick **Add to PATH** | https://python.org — không dùng Store 3.13. |
| **FFmpeg** | tách audio, render | `winget install Gyan.FFmpeg` rồi **mở lại** CMD. `ffmpeg -version`, `ffprobe -version`. |
| **install.py** | tạo venv + `pineline.config.json` | xem dưới |
| **Một LLM OpenAI-compatible** | bước **Dịch** / review | xem "LLM" dưới — KHÔNG nhất thiết Ollama |

**Ổ trống:** ~25–40 GB (2 venv torch CUDA + model HF + GGUF).

```bat
cd /d D:\PinelineV4
python install.py --gpu --cuda cu128 --skip-ollama-pull
```

**5060 Ti = Blackwell → `--cuda cu128`**. `install.py` tạo `pineline_env` (app) + `vieneu_env` (TTS) rồi ghi
`pineline.config.json`. (Bỏ `--skip-ollama-pull` chỉ khi bạn thật sự dùng Ollama.)

---

## LLM (dịch / review) — chọn 1

**A. Như máy gốc — llama.cpp `llama-server` + presets**

- Code gọi `llama-server` ở `LLAMA_BASE_URL` (mặc định `http://127.0.0.1:8083/v1`).
- Đổi model theo `TRANSLATE_PRESET` / `REVIEW_PRESET` bằng script `E:\models\presets\start-model.ps1`
  (cùng `models.json`, `active.json`). Máy mới cần: llama.cpp (CUDA) + thư mục presets + file GGUF.
- Khác đường dẫn/cổng: `LLAMA_BASE_URL`, `MODEL_PRESETS_DIR`, `MODEL_START_SCRIPT`; không dùng PowerShell:
  `MODEL_START_CMD` (vd `"bash switch.sh {preset} --port {port}"`).

**B. LLM khác qua `LLM_BASE_URL`** (Ollama `/v1`, 9router, OpenAI, LM Studio…)

- Điền `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL`, `TRANSLATE_MODEL`.
- Đặt `AUTO_SWITCH_PRESETS=0` (hoặc không có thư mục presets) → **bỏ qua đổi preset, không lỗi**.

Model `ollama/...-cloud` (9router): `CLOUD_LLM_BASE_URL` + `CLOUD_LLM_API_KEY`.

---

## Tuỳ chọn

| Cái | Khi nào cần | Key |
|-----|-------------|-----|
| **Aurora / ChatGPT proxy** `:3377` | plan / review / pass1 / agent dùng model `chatgpt/...` | `CHATGPT_BASE_URL`, `AURORA_BASE_URL`, `AURORA_FALLBACK_URLS` (`off` = tắt LAN) |
| ↳ không có Aurora | đổi `PLAN_MODEL`, `REVIEW_MODEL`, `REVIEW_PASS1_MODEL`, `AURORA_REVIEW_MODEL`, `AGENT_MODEL`, `NAME_MODEL`, `PRONOUN_MODEL` sang model khác (vd `local`) | — không đổi thì bước đó báo lỗi rõ, không tự đổi ngầm |
| **Hongguo Downloader** `:8000` | chỉ khi tải phim Hongguo | `HONGGUO_BASE_URL`, `LIBRARY_DIR` (mặc định `D:\Lib`) |
| **OmniVoiceStudio** + venv | engine TTS phụ | `OMNI_PY`, `OMNI_CWD` |
| **Fun-ASR / Paraformer** | engine ASR | `pip install funasr modelscope tiktoken jieba librosa soundfile` vào `pineline_env`, rồi `install_funasr_safe.bat` (khoá torch CUDA) |
| **FireRed ASR** | engine ASR | `FIRERED_ROOT`, `FIRERED_MODELS` |

---

## Chép tay (không có trong git)

- `pineline.config.json` (chứa key — **không** commit)
- `voices/`, `voice_samples/`, `models/` (cdx23…), `cookies/`
- Model MT zh→vi (HachimiMT, máy gốc `E:\models\mt`) → `MT_MODEL_DIR` / `MT_ZH_VI_LOCAL` (không có thì tự tải HF lần đầu)
- FireRed (nếu dùng), `yt_uploader` + `client_secret.json` → `YT_UPLOADER_DIR` (nếu upload YouTube)
- `work/` job cũ (nếu cần resume) — hoặc tạo mới: `mkdir work` / `mklink /J work E:\pineline_work`

---

## Không cần cài tay (tự có khi chạy)

- VieNeu-TTS v3-Turbo (HF, lần TTS đầu) · faster-whisper / RapidOCR / Demucs · yt-dlp (requirements)

---

## Checklist

```bat
nvidia-smi
python --version
ffmpeg -version
python scripts\check_env.py --offline
python scripts\check_env.py
```

Doctor không còn **THIẾU** → `run_v4.bat`.
