# Pineline V4 — cài trên MÁY MỚI / máy khác cấu hình

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

Cập nhật 2026-11-11 (machine-config). Mọi thứ phụ thuộc máy (cổng llama/Aurora/Hongguo, thư mục presets/model/thư viện,
lệnh đổi preset) giờ là **key trong `pineline.config.json`** — không phải sửa code. Mặc định = cấu hình máy gốc.

Kiểm tra nhanh mọi thứ: **`python scripts\check_env.py`** (doctor; xem mục 8).

Chi tiết / làm tay từng bước (nếu không dùng SETUP_MAY_MOI.bat) — xem các mục dưới.

## 0. Lấy code (V4 — từ git)

```bat
git clone https://github.com/kjza178/PineLineV4.git D:\PinelineV4
cd /d D:\PinelineV4
```

Git **không** chứa: `pineline.config.json` (có key), `voices/`, `voice_samples/`, `cookies/`, `data/`, `work/`,
model, backup. Phần 5 liệt kê thứ phải chép tay.

> Nếu lỡ commit thư mục backup trước đây: `git rm -r --cached .backup_edit_*` rồi commit (file trên đĩa vẫn giữ).
> `.gitignore` đã bỏ qua `.backup_*/`, `_to_delete/`, `scratch/`, `work` (junction).

## 1. Bắt buộc

| Cái | Ghi chú |
|-----|---------|
| **Driver NVIDIA** mới | `nvidia-smi` phải ra GPU. RTX 50-series (Blackwell) cần driver mới + `--cuda cu128`. |
| **Python 3.11 hoặc 3.12** (64-bit, Add to PATH) | Không dùng 3.13 Store. |
| **FFmpeg** (ffmpeg + ffprobe trong PATH) | `winget install Gyan.FFmpeg`, mở lại CMD, `ffmpeg -version`. |
| **install.py** | `python install.py --gpu --cuda cu128   (Ollama pull mặc định TẮT; --dry-run để xem trước)` — tạo `pineline_env` + `vieneu_env`, ghi `pineline.config.json`. |

**Ollama KHÔNG còn bắt buộc** (bản cũ ghi vậy là sai): code dịch/review gọi LLM OpenAI-compatible qua `LLM_BASE_URL`
(máy gốc: llama-server :8083 + 9router). Ollama chỉ dùng nếu bạn chọn model `local/...`.

## 2. LLM dịch/review — chọn 1 trong 2

**A. Giống máy gốc: llama.cpp `llama-server` + presets GGUF**

- Cài llama.cpp (bản CUDA), tải GGUF.
- Thư mục presets (máy gốc `E:\models\presets`) gồm `models.json`, `active.json`, script đổi model `start-model.ps1`
  (kill llama-server cũ → mở preset mới ở cổng 8083). Pineline gọi script này khi cần `TRANSLATE_PRESET`/`REVIEW_PRESET`.
- Khác máy gốc thì sửa: `LLAMA_BASE_URL` (vd `http://127.0.0.1:8090/v1`), `MODEL_PRESETS_DIR`, `MODEL_START_SCRIPT`.
  Không dùng PowerShell → `MODEL_START_CMD`, vd `"bash /opt/llama/switch.sh {preset} --port {port}"`
  (placeholder: `{script} {preset} {presets_dir} {host} {port} {base_url}`).

**B. LLM khác (không llama.cpp / không presets)**

- `LLM_BASE_URL` = endpoint OpenAI-compatible (Ollama `http://127.0.0.1:11434/v1`, 9router, OpenAI, LM Studio…),
  `LLM_API_KEY`, `LLM_MODEL`, `TRANSLATE_MODEL`.
- `AUTO_SWITCH_PRESETS=0` (hoặc để thư mục presets không tồn tại): Pineline **bỏ qua đổi preset, không lỗi**,
  dùng model đang chạy.
- `LLAMA_BASE_URL` để trống: nếu `LLM_BASE_URL` trỏ localhost thì llama = LLM_BASE_URL, không thì `127.0.0.1:8083`.

Model `ollama/...-cloud` đi qua 9router: `CLOUD_LLM_BASE_URL` + `CLOUD_LLM_API_KEY`.

## 3. Aurora / ChatGPT proxy (tuỳ chọn)

Model `chatgpt/...` (plan, review, pass1, agent…) gọi Aurora: `AURORA_BASE_URL` → `CHATGPT_BASE_URL`
(máy gốc `http://127.0.0.1:3377/v1`) → `AURORA_FALLBACK_URLS` (Aurora LAN; `off` = tắt).

**Máy không có Aurora**: đổi các key đang là `chatgpt/...` sang model khác (vd `local` = llama-server, hoặc model của
`LLM_BASE_URL`): `PLAN_MODEL`, `REVIEW_MODEL`, `REVIEW_PASS1_MODEL`, `AURORA_REVIEW_MODEL`, `AGENT_MODEL`,
`NAME_MODEL`, `PRONOUN_MODEL`, `CHATGPT_MODEL`. Không đổi thì bước đó báo lỗi rõ
("Không tới được Aurora/ChatGPT … đổi PLAN_MODEL/…") — Pineline không tự đổi model ngầm.
Doctor liệt kê key nào đang dùng `chatgpt/...`.

## 4. Hongguo (tuỳ chọn — chỉ khi dùng tải Hongguo)

Hongguo Downloader HTTP API: `HONGGUO_BASE_URL` (mặc định `http://127.0.0.1:8000`). Thư viện phim: `LIBRARY_DIR`
(mặc định `D:\Lib`). Không mở Hongguo → mục tải Hongguo báo không kết nối; pipeline job thường vẫn chạy.

## 5. Chép tay từ máy cũ (KHÔNG có trong git/zip)

| Thứ | Đặt ở | Key liên quan |
|-----|-------|---------------|
| `pineline.config.json` (có API key) | gốc dự án | — (hoặc chép `pineline.config.example.json` rồi điền) |
| `voices/`, `voice_samples/` | gốc dự án | — |
| `models/` (cdx23 tách nhạc nền…) | gốc dự án | — |
| `cookies/` | gốc dự án | — |
| Model MT zh→vi (HachimiMT ct2) | `E:\models\mt\…` hoặc tuỳ | `MT_MODEL_DIR`, `MT_ZH_VI_LOCAL` (không có → tự tải HF lần đầu) |
| FireRedASR2S + model | tuỳ | `FIRERED_ROOT`, `FIRERED_MODELS` (chỉ khi dùng ASR FireRed) |
| `yt_uploader` + `client_secret.json` | `Z:\yt_uploader` hoặc tuỳ | `YT_UPLOADER_DIR` (chỉ khi upload YouTube) |
| GGUF + presets llama | tuỳ | `MODEL_PRESETS_DIR`… (mục 2A) |
| venv VieNeu / OmniVoice | install.py tạo | `VIENEU_PY`, `OMNI_PY`, `OMNI_CWD` |

## 6. Thư mục work

```bat
mkdir work
rem hoặc junction sang ổ lớn:
mklink /J work E:\pineline_work
```

## 7. Bảng key phụ thuộc máy

Đặt trong `pineline.config.json` (ưu tiên: biến môi trường > file > mặc định; riêng `LLM_*`, `AGENT_*`,
`CHATGPT_*`, `AURORA_BASE_URL`, `CLOUD_LLM_*`: file > env). Mẫu đầy đủ: `pineline.config.example.json` (mục `_machine_keys_help`).

| Key | Mặc định | Ý nghĩa |
|-----|----------|---------|
| `LLM_BASE_URL` | `http://192.168.31.247:20128/v1` | LLM chính (OpenAI-compatible) cho dịch/review: llama-server, 9router, Ollama /v1, OpenAI... |
| `LLAMA_BASE_URL` | `(trống)` | llama-server /v1 (GGUF local). Trống = LLM_BASE_URL nếu trỏ localhost, không thì http://127.0.0.1:8083/v1 |
| `AUTO_SWITCH_PRESETS` | `1` | 1 = tự đổi preset llama (TRANSLATE_PRESET/REVIEW_PRESET) bằng script; 0 = không bao giờ đổi, dùng model đang chạy |
| `MODEL_PRESETS_DIR` | `E:\models\presets` | Thư mục presets llama.cpp (active.json, models.json, script khởi động). Không tồn tại = bỏ qua đổi preset |
| `MODEL_START_SCRIPT` | `start-model.ps1` | Script đổi preset (tương đối theo MODEL_PRESETS_DIR hoặc đường dẫn tuyệt đối) |
| `MODEL_START_CMD` | `(trống)` | Lệnh đổi preset tuỳ ý; placeholder {script} {preset} {presets_dir} {host} {port} {base_url}. Trống = powershell -ExecutionPolicy Bypass -File {script} {preset} |
| `AURORA_BASE_URL` | `(trống)` | Aurora/ChatGPT proxy cho model chatgpt/... (ưu tiên trước CHATGPT_BASE_URL) |
| `CHATGPT_BASE_URL` | `http://127.0.0.1:3377/v1` | Proxy ChatGPT local (plan/review/agent dùng model chatgpt/...) |
| `AURORA_FALLBACK_URLS` | `http://192.168.31.247:5005/v1,http://192.168.31.244:5005/v1` | Aurora dự phòng (phân cách dấu phẩy). 'off' = không dùng |
| `AGENT_BASE_URL` | `(trống)` | LLM cho agent chat/feeder; trống = LLM_BASE_URL |
| `CLOUD_LLM_BASE_URL` | `http://192.168.31.247:20128/v1` | 9router cho model ollama/...-cloud (cần CLOUD_LLM_API_KEY) |
| `HONGGUO_BASE_URL` | `http://127.0.0.1:8000` | Hongguo Downloader HTTP API — chỉ cần khi dùng tải Hongguo |
| `MT_MODEL_DIR` | `E:\models\mt` | Thư mục model MT zh→vi (HachimiMT ct2); MT_ZH_VI_LOCAL = trỏ thẳng 1 model |
| `LIBRARY_DIR` | `D:\Lib` | Thư viện phim tải về (Hongguo output / nguồn job) |
| `YT_UPLOADER_DIR` | `Z:\yt_uploader` | Thư mục tool yt_uploader (accounts, client_secret.json, queue_state.json) |
| `LIB_SAMPLE_DIR` | `(trống)` | Thư mục mẫu cắt thử bản quyền (lib_check); trống = mặc định cũ ghi trong lib_check.py |
| `VIENEU_PY` | `(trống)` | python.exe của venv VieNeu-TTS (install.py tự ghi) |
| `FIRERED_ROOT` | `(trống)` | Mã nguồn FireRedASR2S; trống = vendor/FireRedASR2S |
| `FIRERED_MODELS` | `(trống)` | Model FireRed; trống = FIRERED_ROOT/pretrained_models |
| `HF_HOME` | `(trống)` | Cache HuggingFace |

## 8. Doctor

```bat
python scripts\check_env.py              rem đầy đủ, gọi thử LLM/Aurora/Hongguo (timeout ngắn)
python scripts\check_env.py --offline    rem không gọi mạng
python scripts\check_env.py --show       rem in giá trị hiệu lực các key máy
```

Bảng `OK / THIẾU / TUỲ CHỌN / CẢNH BÁO` + cách sửa. Chạy bằng python của venv app (`pineline_env`) để kiểm cả torch+CUDA.
Không còn THIẾU → chạy `run_v4.bat`.
