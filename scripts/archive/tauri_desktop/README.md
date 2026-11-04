# Tauri desktop (không dùng trên V4)

Đưa khỏi root 2026-11-02. Desktop chính = WebView2 (`app_desktop.py` + `build_desktop.bat` + `run_v4.bat` chọn 1).

| Mục | Ghi chú |
|---|---|
| `src-tauri/` | Skeleton Rust/Tauri |
| `node_modules/` | `@tauri-apps/cli` (~16MB) |
| `package.json` / `package-lock.json` | npm meta |
| `run_tauri.bat` / `build_tauri.bat` / `install_rust.bat` | Launcher/build Tauri |

Khôi phục: chép lại root rồi `npm i` nếu thiếu `node_modules`.
