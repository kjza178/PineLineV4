# 2026-11-11 — machine-config: cổng/thư mục phụ thuộc máy thành setting (V4 — layout phẳng)

## Triệu chứng
- Hướng dẫn máy mới ghi Ollama bắt buộc, nhưng code gọi llama-server :8083 và đổi preset bằng
  `E:\models\presets\start-model.ps1` (PowerShell) — máy khác cấu hình không chạy/không biết sửa đâu.
- Cứng trong code: llama 127.0.0.1:8083 (preset_switcher, brain), presets `E:\models\presets` (active.json),
  Aurora :3377 + 2 IP LAN, 9router IP, Hongguo :8000, `E:\models\mt`, `D:\Lib`, `Z:\yt_uploader`.

## Nguyên nhân
Giá trị máy gốc viết thẳng vào code (một số có env nhưng không qua config.json).

## Sửa
- Mới `machine.py`: một chỗ đọc mọi key máy qua `config.get` (env > pineline.config.json > mặc định),
  đọc lúc gọi; `MACHINE_KEYS` (mặc định + mô tả), `llama_base_url/host_port`, `presets_dir`, `model_start_cmd`,
  `preset_switch_unavailable_reason`, `aurora_base_urls`, `aurora_missing_hint`, `hongguo_base_url`, `mt_model_dir`,
  `library_dir`, `in_library`, `yt_uploader_dir`.
- preset_switcher: host/cổng/presets/lệnh lấy từ machine; thiếu presets/script hoặc `AUTO_SWITCH_PRESETS=0` →
  **bỏ qua đổi preset, không lỗi** (dùng model đang chạy nếu llama sẵn sàng; không thì False + thông báo rõ).
- llm: llama base, danh sách Aurora, 9router mặc định qua machine; Aurora hỏng hết → LLMUnavailable kèm gợi ý đổi
  PLAN_MODEL/REVIEW_MODEL/REVIEW_PASS1_MODEL… (không tự đổi model ngầm).
- brain/brain_context ping theo URL cấu hình; hongguo_bridge `DEFAULT_BASE` = HONGGUO_BASE_URL; fallback `D:\Lib` →
  LIBRARY_DIR (feeder, hongguo_bridge, agent_hongguo, routes_hg, server, lib_check, film_db); `Z:\yt_uploader` →
  YT_UPLOADER_DIR (film_db, auto_publisher, uploader settings, lib_check, test_channel); mt_zh_vi → MT_MODEL_DIR;
  meta_studio Aurora theo machine; agent_tele_cmd poster dùng `hg.DEFAULT_BASE`.
- `pineline.config.example.json`: thêm key máy + `_machine_note` + `_machine_keys_help` (mô tả | mặc định). Không bí mật.
- Doctor `scripts/check_env.py` (stdlib): Python, ffmpeg/ffprobe, nvidia-smi, torch+CUDA, config đọc được, LLM/llama,
  presets, Aurora (+ key nào dùng chatgpt/), 9router, Hongguo, voices/models/cookies/work, MT, FireRed, VieNeu, HF, thư viện,
  yt_uploader. `--offline` (không gọi mạng), `--no-torch`, `--show`. Exit 1 nếu có THIẾU.
- `docs/SETUP_MAY_MOI.md`: cài máy mới (llama.cpp+presets HOẶC LLM khác; Aurora/Hongguo tuỳ chọn; thứ chép tay; work; bảng key).
- `CAI_MAY_MOI.md` viết lại (bỏ Ollama bắt buộc); `.gitignore` thêm `.backup_*/`, `_to_delete/`, `scratch/`, `/work` (junction).
  Nếu thư mục backup từng bị commit: `git rm -r --cached .backup_edit_*` (user tự làm; agent không chạy git).
Key mới (mặc định = giá trị cứng cũ → máy hiện tại không đổi hành vi):
`MODEL_START_SCRIPT` (start-model.ps1), `MODEL_START_CMD` (trống = PowerShell cũ), `AURORA_FALLBACK_URLS`
(2 Aurora LAN cũ; `off` tắt), `HONGGUO_BASE_URL` (http://127.0.0.1:8000), `MT_MODEL_DIR` (E:\models\mt),
`LIB_SAMPLE_DIR` (trống = mặc định cũ trong lib_check).
Key cũ nay được dùng ở mọi chỗ: `LLAMA_BASE_URL` (trống → LLM_BASE_URL nếu localhost → :8083), `MODEL_PRESETS_DIR`
(trước chỉ env), `AUTO_SWITCH_PRESETS` (nay cả brain + fallback review tôn trọng), `CHATGPT_BASE_URL`/`AURORA_BASE_URL`,
`CLOUD_LLM_BASE_URL`, `LIBRARY_DIR`, `YT_UPLOADER_DIR` (trước chỉ env).

File sửa: machine.py (mới), scripts/check_env.py (mới), docs/SETUP_MAY_MOI.md (mới), CAI_MAY_MOI.md (viết lại), .gitignore, preset_switcher.py, llm.py, mt_zh_vi.py, agent_brain.py, agent_brain_context.py, hongguo_bridge.py, agent_feeder.py, agent_hongguo.py, agent_tele_cmd.py, meta_studio.py, auto_publisher.py, uploader_settings_api.py, film_db.py, lib_check.py (SAMPLE_DIR V4 = data/samples của cây, nay LIB_SAMPLE_DIR ghi đè được), routes_hg.py, routes_uploader_settings.py, server.py, pineline.config.example.json, test_channel.py (client_secret theo YT_UPLOADER_DIR)

## Backup
`.backup_edit_20261111_machine_cfg/` (cp --parents bản gốc mọi file sửa).

## Recheck
- VM: ast.parse 20 file (.py sửa + mới): Pass; `python3 scripts/check_env.py --offline --no-torch` chạy hết bảng; import
  `machine` + `preset_switcher` trên VM: BASE_URL http://127.0.0.1:8083, START_SCRIPT E:\models\presets\start-model.ps1 (= cũ).
- Cloud (tar subset, script tạm trong scratch V6 — không commit vào cây): bản port của tests/test_machine_config.py → 13 passed;
  import smoke 18 module: 14 OK, 4 SKIP (thiếu fastapi/google.oauth2), 0 FAIL.
- CHỈ kiểm được trên Windows: doctor đầy đủ, đổi preset thật.
