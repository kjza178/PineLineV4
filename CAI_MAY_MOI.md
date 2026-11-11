# Máy mới — cài GÌ ngoài code (git / zip)

## CÁCH NHANH (máy mới — 3 bước)

1) **git clone** code về ổ nhiều chỗ trống:
   ```bat
   git clone https://github.com/kjza178/PineLineV4.git D:\PinelineV4
   ```
   (chưa có git: tải https://git-scm.com hoặc `winget install -e --id Git.Git`)
2) **Nháy đúp `SETUP_MAY_MOI.bat`** (gốc thư mục V4). Nó tự: tìm Python 3.12/3.11 (không có → hỏi cài bằng winget) →
   detect máy (Windows, CPU, RAM, ổ trống, GPU + driver/CUDA qua `nvidia-smi`, ffmpeg/git/winget/llama-server) →
   in **Kế hoạch** (build torch, hồ sơ hiệu năng, nơi đặt venv) → hỏi **Y/N** → cài ffmpeg/git thiếu (winget),
   tạo/cập nhật `pineline_env` + `vieneu_env` (torch đúng build) → GỘP `pineline.config.json` (không xoá key cũ,
   không đặt bí mật) → tạo `work/ voices/ voice_samples/ cookies/ models/`, TEMP riêng → chạy doctor
   `scripts\check_env.py --offline`. Log: `scratch\setup_<thời gian>.log`.
3) **Làm các VIỆC TAY in ra cuối** (chép voices/, voice_samples/, models/, cookies/, key API; cài llama.cpp + presets
   hoặc đặt `LLM_BASE_URL`; Aurora/Hongguo tuỳ chọn…) → chạy `run_v4.bat`.

Cờ (thêm sau tên file trong CMD): `--dry-run` (chỉ xem kế hoạch, không cài) · `--yes` (không hỏi) · `--cpu` / `--gpu` ·
`--cuda cu128|cu124|cu121` · `--envs-dir E:\envs` · `--skip-vieneu` · `--with-funasr` · `--with-ollama` · `--online-check`.
Chạy lại nhiều lần an toàn (venv có rồi → chỉ cập nhật; torch sai build → cài lại đúng build).

| GPU / driver (nvidia-smi) | torch build |
|---|---|
| compute_cap ≥ 12.0 (RTX 50 / Blackwell, vd 5060 Ti) hoặc driver CUDA ≥ 12.8 | `cu128` (Blackwell + driver cũ → cảnh báo cập nhật driver ≥ 570) |
| driver CUDA 12.4–12.7 | `cu124` |
| driver CUDA 12.1–12.3 (vd 3060 + driver 537, CUDA 12.2) | `cu121` |
| GPU cũ compute < 7.0 (Pascal/Maxwell) + driver ≥ 12.8 | `cu124` |
| driver CUDA < 12.1 | cảnh báo cập nhật driver, cài `cpu` (trừ khi `--gpu`) |
| không có GPU NVIDIA | `cpu` (VIENEU/OMNI_DEVICE=cpu, RENDER_ENCODER=x264) |

Hồ sơ hiệu năng: tên GPU chứa 5060 → `pineline.config.rtx5060ti.json`, 3060 → `rtx3060.json`; khác thì theo VRAM
(≥16GB → như 5060 Ti, ~12GB → như 3060, <12GB → nhẹ). Chỉ lấy key hiệu năng (VIENEU_BATCH, VIENEU_CPU_THREADS,
TRANSLATE_BATCH, LLM_NUM_CTX, RENDER_ENCODER…), không lấy đường dẫn của máy gốc; key bạn đã có thì GIỮ.

`run_v4.bat` dùng python của `pineline_env` (đọc `.pineline_env_path` do setup ghi — venv có thể ở thư mục cha/ổ khác)
trước `C:\Python312`; TEMP lấy từ `PINELINE_TEMP` / `.pineline_tmp_path` (fallback `scratch\tmp`).

---

Code (git `kjza178/PineLineV4` hoặc zip) **chỉ có code**. Hướng dẫn đầy đủ + bảng key: **`docs/SETUP_MAY_MOI.md`**.
Kiểm tra máy: **`python scripts\check_env.py`** (doctor: OK / THIẾU / TUỲ CHỌN + cách sửa).

Cập nhật 2026-11-11: bỏ "Ollama bắt buộc" (sai so với code). Mọi cổng/thư mục phụ thuộc máy là key trong
`pineline.config.json` (mẫu: `pineline.config.example.json`, mục `_machine_keys_help`).

---

Chi tiết / làm tay từng bước (nếu không dùng SETUP_MAY_MOI.bat) — xem các mục dưới.

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
python install.py --gpu --cuda cu128   (Ollama pull mặc định TẮT; --dry-run để xem trước)
```

**5060 Ti = Blackwell → `--cuda cu128`**. `install.py` tạo `pineline_env` (app) + `vieneu_env` (TTS) rồi ghi
`pineline.config.json`. (Chỉ thêm `--with-ollama` khi bạn thật sự dùng Ollama.)

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
| **Fun-ASR / Paraformer** | engine ASR | `pip install funasr modelscope tiktoken jieba librosa soundfile` vào `pineline_env`, rồi `install_funasr_safe.bat <python venv> <cu128|cu124|cu121>` (khoá torch CUDA) — hoặc `SETUP_MAY_MOI.bat --with-funasr` |
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
