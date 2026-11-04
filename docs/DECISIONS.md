# Quyết định của user

Mới nhất trên cùng. Mỗi mục: quyết định — bối cảnh/lý do. Đổi quyết định → thêm mục mới, không xoá mục cũ.

## 2026-11

- **11-02 (review lock)** 31B chỉ mượt văn; CẤM đổi self/call khi pronouns_locked (prompt + filter).

- **11-02 (pronoun A–C)** User: làm hết V2+V4+V5 — analyze full ZH (lô+memory) → lock → ledger → QA/GPT vá. Không đợi diarization. Backup Z:\PinelineV2_codebak\2026-11-02_pronoun-consistency-abc\.

- **11-02 (pipeline LLM 3 tầng)** User chốt: local dịch thô → GPT name/pronoun → **31B rà văn phong**.
  - `TRANSLATE_MODEL=local`; `NAME`/`PRONOUN=chatgpt/gpt-5-6-mini`; `REVIEW_MODEL=ollama/gemma4:31b-cloud`.
  - `llm.chat`: model `ollama/*` / `*-cloud` → `CLOUD_LLM_*` (9router), không nuốt vào `:8083`.
  - Backup `Z:\PinelineV2_codebak\2026-11-02_review-31b\`.
- **11-02 (Aurora GPT pass ngắn)** User: pool ~100 Free → thử dùng thật. **Không** đổ TRANSLATE bulk lên Free.
  - `llm.chat` nhận tiền tố `chatgpt/` / `aurora/` → Aurora `:5005` (pool Free).
  - `NAME_MODEL` / `PRONOUN_MODEL` = `chatgpt/gpt-5-6-mini`; TRANSLATE giữ local.
  - Backup `Z:\PinelineV2_codebak\2026-11-02_aurora-name-pronoun\`.
- **11-02 (xưng hô translate)** User: improve translate vì lệch xưng hô nhiều — làm **cả V4 + V5**.
  - Post-pass deterministic `apply_pronoun_postpass` (tẩy Ta–Ngươi đô thị/mixed + ép self/call khi đủ tên who/to).
  - Inject mạnh xưng hô theo phân cảnh trong `_resolve_scene_context` + siết prompt batch.
  - `agent_pronoun_pass.run_pronoun_pass` (LLM) chạy sau name-pass khi Agent yêu cầu rà soát.
  - Không đổi model mặc định; không hard-lock mọi đại từ khi thiếu diarization.
- **11-02 (khung)** V5 có package `pineline/` (routes/services/pipeline/…) — chi tiết ghi trên **`Z:\PinelineV5\docs\DECISIONS.md`**. V4 không đổi cấu trúc runtime. V5 đã có queue LIVE + jobs registry LIVE.
- **11-02** Refactor cấu trúc codebase (dễ đọc / ổn định) — **không sửa inplace trên V4**.
  - Tạo tree riêng **`Z:\PinelineV5`** (copy từ V4). V4 = bản ổn định / restore; production ops vẫn theo V4 (:8804) cho đến khi user chuyển.
  - V5 dùng cổng **:8805**, temp `D:\PinelineV5_tmp`, work mặc định `D:\PinelineV5_work` (tránh đụng process/data V4).
  - Phương án kỹ thuật: **A** — tách dần `server.py` theo cụm `routes_*` (queue → jobs → assets), giữ `import server as S` như đợt 7; không big-bang package.
  - Mọi thay đổi refactor **bắt buộc** ghi thêm mục vào `DECISIONS.md` (V5) + CHANGELOG/worklog; trước mỗi đợt sửa: zip snapshot + codebak.
  - Nếu V5 fail: xóa/đổi tên `Z:\PinelineV5`, giữ nguyên V4; khôi phục từ zip trong `Z:\PinelineV2_codebak\2026-11-02_v4-to-v5\` / snapshot log.

## 2026-10

- **10-08** V3: nhiều key LLM xoay vòng (429/401/403) — **chỉ V3**, V2 giữ 1 key. UI3 + Hongguo hiển thị **trong launcher** bằng WebView2 (tkinter không render được web hiện đại; viết lại UI3 bằng tkinter quá lớn) — bỏ UI4 khỏi V3.
- **10-08** Tạo **V3 portable** ở `Z:\PinelineV3` (V2 giữ nguyên, vẫn là bản chạy chính). Launcher tkinter + exe; gói code + Python, model tải lần đầu; mang cả Hongguo + llama-server; GPU tự dò (cu128 để chạy được RTX 50xx); LLM mặc định **Ollama Cloud** bằng key người dùng nhập, 9router chỉ dùng qua preset Custom. Kích thước thực ~10,8 GB (torch cu128 riêng 6,9 GB) thay vì ~6 GB user ước.
- **10-07** Hàng đợi gộp Hongguo **lưu ra file** và restart server phải tôn trọng nó như queue render (chặn restart khi đang gộp). Xếp hàng chỉ ghi tên; việc nặng (ffprobe, chuẩn hoá 1080p, dọn tập lẻ) làm trong worker để UI không bị treo.
- **10-07** Video nguồn lấy **trực tiếp từ `D:\Lib`** (user chọn thay cho hard link): job không giữ bản sao/link, chỉ ghi đường dẫn thư viện trong manifest. Không viết lại pipeline (user: không cần test lại toàn bộ) — chỉ đổi chỗ chọn đường dẫn lúc import. File ngoài thư viện vẫn hard link/copy. Job cũ (0281, dccc bản sao; 5 job hard link) **giữ nguyên** — chỉ áp dụng từ job tiếp theo.
- **10-07** User duyệt mẫu `sfx_lib` → CONFIG BATCH dùng `sfx_lib`. Yêu cầu chỉnh: nhạc kho nhỏ hơn, tiếng động gốc to hơn nhưng vừa phải, giọng Việt to hơn (đặt 0,25 / 0,62 / ×1,25, có limiter). Bản tách CDX23 giữ bản nhanh (user chưa chọn khác).
- **10-07** Bỏ hẳn nhạc nền gốc vì claim Content ID (vd "Latin Zumba Dance Workout – Liberektro"). User không muốn dò từng bài sau khi bị claim (phức tạp với video dài) → chọn công thức **giọng Việt + tiếng động gốc + nhạc mới sạch bản quyền**: tách tiếng động bằng CDX23 (MIT), nhạc lấy từ **YouTube Audio Library** (Attribution not required, Ambient/Cinematic), chọn theo mức êm/vừa/dồn dập đo từ nhạc gốc. Mặc định CDX23 1 checkpoint (đo: sót nhạc không hơn bản 3 checkpoint, nhanh ~3×). Chế độ `sfx_lib` có trong UI/CONFIG BATCH nhưng **chưa đổi CONFIG BATCH** (vẫn `duck`) tới khi user duyệt mẫu. Không dùng MusicGen (license cấm thương mại), không dùng Pixabay (nhiều bài dính Content ID).
- **10-06** (đợt 7) Gỡ UI cũ `index1/2.html` + route `/ui1`, `/ui2` (user chọn). Tách `server.py` theo nhóm route bằng `APIRouter`; code chuyển đi gọi server qua `S.<tên>` (không `from server import …`) để patch trong test vẫn ăn và không nạp server 2 lần. Phần jobs/queue/pipeline giữ trong `server.py` vì check đợt 1–4 đọc mã nguồn của nó. Code mới chỉ có hiệu lực khi restart, restart chỉ khi hàng đợi rảnh hoặc user đồng ý.
- **10-06** (đợt 6) Có git local (không remote, không push). Secret và dữ liệu job không vào git. Script một lần ở gốc chuyển ra `codebak\…\attic` (không xoá). UI cũ `index1/2.html` giữ nguyên tới khi user quyết. Không tách file lớn khi đang có job chạy.
- **10-06** (đợt 5, theo review user chọn làm) Telegram:
  - Lệnh đổi trạng thái **phải có `/`**. Chữ trơn chỉ nhận gợi ý; câu dài thì chuyển cho agent.
  - Agent muốn dừng hàng chờ/job, gộp/dọn tập, chạy A-Z, chạy lại `force`, reset config, heal hàng loạt → **gửi nút ✅/❌**, bấm ✅ mới chạy (hết hạn 15 phút).
  - Panel Agent trên UI giữ như cũ (đã tick cho phép thì chạy thẳng).
  - `hg_auto_flow` từ agent chạy nền, mỗi bộ một flow.
  - Xoá `agent_v2/`.
- **10-06** Làm tiếp **đợt 2–6** review. Restart server: **hẹn sau khi f9fe xong** — rút 3a2e khỏi hàng đợi tạm, restart, xếp lại 3a2e.
- **10-06** (đợt 4, theo review user chọn làm) Auto-pilot **không tự xếp lại job failed** và job HOLD / QA chặn — job lỗi phải xem rồi xếp tay, HOLD chờ duyệt. Bấm Tạo giọng / Render / Dịch lại / Ghép khi job đang chạy (hàng đợi hoặc stage running) → từ chối 409 thay vì chạy song song. Server và sidecar chỉ chạy 1 bản (khoá file).
- **10-06** (đợt 3) Opts job một nguồn: config batch → `queue_opts` của job → tham số truyền thêm. Agent `mux_run` render lại theo đúng opts job đã chạy (không còn ép motion/LUT/4M/tắt logo). Giọng **không** lấy từ config batch khi xếp hàng qua API/queue (giữ luật cũ: job thiếu giọng → báo lỗi).
- **10-06** (đợt 2) API key **chỉ đặt trong `pineline.config.json`**; `.bat`/`config.json`/code không chứa key. Backup zip tự che secret. Server/sidecar chỉ nhận Host/Origin local. LLM sập → dừng stage dịch (pending, bấm Tiếp tục), không để trống câu.
- **10-06** Luôn **backup trước khi sửa** (zip toàn project + bản gốc từng file vào `Z:\PinelineV2_codebak\<ngày>_<đợt>\`) và ghi md đủ để biết đã sửa gì. Làm đợt 1 review trước; restart server **để sau**.
- **10-06** Tập lẻ sau gộp: **chuyển vào thùng rác, giữ 7 ngày** rồi mới xoá hẳn (không xoá ngay). Thùng rác đặt `D:\Lib_trash\<bộ>\<thời điểm>\` (ngoài `D:\Lib` để không bị quét như tập/bộ mới).
- **10-06** Docs: mọi thay đổi phải có markdown trong `docs/` (rule `docs-on-change.mdc`). Huỷ các câu hỏi đang treo (restart server, tắt llama-server).
- **10-06** Che hardsub stretch: **đệm 15/13 px** giữ nguyên — mọi mức mỏng hơn (12/11, 10/9, 6/4, 3/2) lọt nét ở ký tự cao (job 2ef87, t=2688,5 s).
- **10-06** Che hardsub stretch: **không làm mềm (sigma 0/0)** — user so 0/0, 0,6/1, 0,8/1 và chọn 0/0.
- **10-06** Che hardsub: chuyển từ blur sang **vệt kéo giãn giữ màu cảnh** (`HARDSUB_STYLE=stretch`), 1 lớp, gộp nhiều vị trí cùng lúc thành 1 dải. Giữ font sub. **Không render lại 2ef87.**
- **10-06** Mùa 1 chạy trước mùa 2 (kế thừa glossary/xưng hô đã duyệt).
- **10-05** Job 2ef87: để nguyên 21/93 lô review lỗi. Giữ `openclaw` làm fallback agent dù combo đang hỏng.
- **10-05** Model LLM lấy theo file config (file-first) cho dịch/review/agent: `ollama/gemma4:31b-cloud` qua 9router.
- **10-05** Render chia khúc: khúc 300 s, 3 song song (thay chia đôi), sau test 5 phút × 3 đạt.
- **10-04** Bỏ lớp đen hardsub; chỉ che đúng toạ độ chữ dò được theo đoạn (`HARDSUB_MODE=track`), bám zoom.
- **10-04** Video >12 h: cắt copy thành part cho YouTube (0281 → part1/part2).
- **10-04** LUT: giữ `lutrgb` trên CPU, không chuyển libplacebo (chậm hơn + lệch màu). Dùng ffmpeg 8.1.2 full_build.
- **10-03** Tăng tốc render: làm chia đoạn song song (đo 4,1×); LUT dùng lutrgb.
- **10-03** Hongguo preview/rank/catalog đưa vào Telegram + agent.

## 2026-09

- **09-30** Bản dịch: user tự sửa `sub.vi.srt` của cc52 → ghép ngược vào `script.json` rồi TTS lại; đổi "anh tôi/cô tôi" (他/她) thành "anh ta/cô ta".
- **09-30** Preset gemma4-26b-qat-mtp dùng `--fit` 131k (thay `-ngl 99 --n-cpu-moe 16`).
- **09-29** Agent: rà tên + văn phong trước TTS (sau khi dịch 100%); feeder tự thêm job khi hàng chờ trống, mặc định OFF tới khi có yêu cầu.
- **09-29** Database phim SQLite `data/films.db` + `/films/ui`; thư viện `/lib` qua Telegram.
- **09-29** YT uploader: mỗi tài khoản khoá 1 IP proxy, kiểm IP trước mọi request; proxy chết thì không upload (không rơi về mạng thẳng). Token Google không gửi bên thứ ba.
- **09-28** YT uploader tách ra `Z:\yt_uploader`, đa tài khoản đặt tên, sửa hàng loạt, thumbnail nhiều file.
- **09-28** Agent dùng 9router `gemma4:31b-cloud` mặc định.
- **09-27** Chuyển `work` sang `D:\PinelineV2_work` (junction từ Z) để không tranh ổ với Windows.
- **09-27** Config batch dùng chung (`batch_config.json`) cho UI3/UI4/Agent/Telegram/Auto-pilot; đổi config thì job chưa chạy theo luôn, job đang chạy giữ config cũ.
- **09-27** Mỗi job bị ép snapshot opts khi đến lượt (không kế thừa leftover). STOP = dừng hết + tắt Auto-pilot.
- **09-27** Tách 2 LLM: Agent → 9router, job → local (phương án 1, env tách). Sau đó (10-05) job cũng chuyển 9router.
- **09-27** YT uploader là app desktop (không web UI).
- **09-26** Auto-pilot: nút + lệnh, điều khiển qua Telegram; không restart server khi đang chạy.
- **09-26** Chỉ làm trên V2 (`Z:\PinelineV2`), không đụng V1 (`Z:\Pineline`, :8800).
- **09-26** UI4 Ops: layout danh sách dự án trên-trái, preview trên-phải, pipeline dưới-trái, kịch bản dưới-phải; form + Job trên UI4; chọn nhiều folder bằng hộp thoại Windows.
