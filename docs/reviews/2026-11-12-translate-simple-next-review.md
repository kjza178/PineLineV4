> **Bản sao từ V2** (`Z:\PinelineV2\docs\reviews\2026-11-12-translate-simple-next-review.md`) — tham chiếu cho port V4 2026-11-12 (agent F4, xem `docs/fixes/2026-11-12-port-simple-demucs.md`). Cổng/đường dẫn trong bài là của V2 (:8801); V4 = :8804. Khác biệt V4: mặc định `TRANSLATE_PIPELINE`=simple, rollback `legacy`.

# Review độc lập — translate-simple «next» (agent D)

- **Date:** 2026-11-12 (~khuya, sau agent B). Người review: agent D (không thấy quá trình làm của B).
- **Phạm vi:** `docs/fixes/2026-11-12-translate-simple-next.md`; `translate_simple/{cfg,lexicon,pipeline,plan_view,post,suggest,pair_rules,pair_fill,zh_source}.py`; `data/lexicon/{idioms_zh_vi,pronoun_rules_zh_vi}.json`; `tools/{collect_manual_edits,simple_stats}.py`; `tests/test_translate_simple_next.py`; V6 `scripts/{golden_ab.py,golden_ab_simple.bat,test_v2_translate_simple.bat}`. So với `.backup_edit_20261112_agentB\`.
- **Cách làm:** bản sao V2 (tar từ đĩa, md5 khớp bảng «md5 sau ghi» của B) → đọc diff + code mới → viết ca test tái hiện lỗi (FAIL trên bản B) → sửa → chạy lại bộ simple/next, nhóm dịch cũ 15 file, toàn bộ `tests/`. Không LLM/GPU/HTTP/git, không restart. Không đọc `Z:\PinelineV6\data\golden_heldout\`.
- **Backup trước khi ghi:** `Z:\PinelineV2\.backup_edit_20261112_agentD\` (giữ cấu trúc), V6: `Z:\PinelineV6\.backup_edit_20261112_agentD\scripts\`.

## Kết luận

**An toàn để chạy A/B `golden_ab_simple.bat next`** sau khi ghi các sửa dưới đây (cờ mặc định vẫn TẮT; luồng cũ và simple-cờ-tắt không đổi — `translate.py`/`server.py` KHÔNG sửa). Hai lỗi nặng nhất chỉ chạm khi bật `SIMPLE_ZH_SOURCE=1` (không thuộc biến thể `next`); lỗi gỡ lặp VI (D1) chạm luồng simple mặc định nên đã sửa trước A/B.

## Phát hiện và xử lý

| # | Mức | Vùng | Lỗi (có ca tái hiện) | Xử lý |
|---|---|---|---|---|
| D1 | **Trung bình–cao** | `post.py` (simple, KHÔNG cờ) | Gỡ lặp VI ở hậu kỳ chạy trên MỌI câu, là bước CUỐI (không còn LLM soát sau): «Đi mau, đi mau!» (快走，快走！ — nhấn giọng có chủ ý) → **«Đi mau,!»**; «Cứu tôi với, cứu tôi với!» → «Cứu tôi với,!»; «Tốt lắm, tốt lắm, tốt lắm!» → «Tốt lắm,, tốt lắm!». Luồng cũ cũng gọi hàm này trong `apply_style_polish` (lỗi có sẵn, xem đề xuất P1). | VI chỉ được gỡ lặp khi ZH của câu có lặp ASR (ZH hiện tại còn lặp — câu rv giữ zh — hoặc ASR gốc lặp: `store.stutter_i` do pipeline tính từ `asr.json`); dọn dấu phẩy treo («Giết đi,!» → «Giết đi!»). Ca của agent A (杀吧杀吧， → «Giết đi,») giữ nguyên. |
| D2 | Trung bình (cờ `SIMPLE_ZH_SOURCE`) | `pipeline.py` | `_heal_zh_stutter` chạy TRƯỚC `zh_source.sync_rows` ⇒ sync so zh đã gỡ với chữ OCR/namefix (còn lặp) và **ghi đè lại chữ lặp** (OCR «不对不对» → zh cuối «不对不对»), `zh_asr` ghi sai. | Gỡ lặp chạy SAU sync. Cờ tắt: `zh_rep is None` ⇒ thứ tự không ảnh hưởng (byte-identical đã kiểm). |
| D3 | **Cao** (cờ `SIMPLE_ZH_SOURCE`) | `zh_source.prepare` ← `hardsub_asr.merge_hardsub_into_asr` | Merge chọn cue OCR cho TỪNG câu ASR độc lập. ASR tách 1 dòng hardsub thành 2 câu (rất thường gặp) ⇒ **cả hai câu nhận nguyên dòng OCR** («我今天一定要把他抓回来» ×2 — lồng tiếng đọc 2 lần, câu 1 vỡ độ dài) hoặc câu 1 nhận cả dòng còn câu 2 giữ nửa sau (đọc lặp nửa sau). Bảo vệ «dính câu kế» có sẵn chỉ bắt khi cover < 0,35. | `_guard_ocr` trong `zh_source` (không sửa `hardsub_asr.py` vì nơi khác dùng): trả lại chữ ASR khi chữ OCR dài hơn rõ (> max(ASR+3, ASR×1,4) ký tự) hoặc cùng một chữ OCR thay cho ≥2 câu có chữ ASR khác nhau. Timing/i không đổi; `zh_source.json.merge.guard_reverted` đếm. |
| D4 | **Cao** (cờ `SIMPLE_ZH_SOURCE`, `SIMPLE_ZH_NAMEFIX` mặc định 1) | `zh_source.fix_names` | Không có `pypinyin` (V2 hiện CHƯA cài) ⇒ tên/**thuật ngữ** ≥4 chữ lệch 1 chữ BẤT KỲ bị thay (điểm 3/4 = 0,75 ≥ ngưỡng): «天下第二» → «天下第一», «九阳神剑» → «九阳神功» — đổi nghĩa. | Không có pypinyin ⇒ không sửa gì (log rỗng). Test của B (`test_fix_names_guarded`) đổi kỳ vọng tương ứng. Muốn bật: `pip install pypinyin` trong venv V2. |
| D5 | Trung bình (cờ `SIMPLE_PAIR_RULES`) | `pronoun_rules_zh_vi.json` | `兄弟` / «huynh đệ» thuộc «bạn bè» ⇒ anh em RUỘT («亲兄弟», «Huynh đệ ruột thịt») ra cặp **tôi/tao — cậu/mày** thay vì anh–em. Bạn bè hiện đại thiếu «tớ» (tớ–cậu rất phổ biến ⇒ cờ pronoun sai → vá kéo về «tôi»). | siblings `pair_kw` + «anh em trai ruột», «huynh đệ ruột», 亲兄弟, 亲姐妹, 兄弟俩 (mơ hồ vai ⇒ KHÔNG đoán, không rơi sang bạn bè); friends bỏ 兄弟/«huynh đệ», thêm 好兄弟, 结拜, «huynh đệ tốt», «hảo huynh đệ»; friends modern self + «tớ». Nới thêm (ít cờ sai): cha tự xưng «bố / ba»; nhân viên gọi sếp + «chủ tịch», «anh»/«chị» theo giới sếp. |
| D6 | Trung bình | `tools/collect_manual_edits.py` | Chỉ chặn `--out` NẰM TRONG `--work`. `--work <work>\job1 --out <work>` ⇒ `od = <work>\job1` ⇒ **ghi `lines.gold.jsonl`… vào thư mục job** (công cụ «chỉ đọc» ghi vào work). | Chặn cả hai chiều lồng nhau + chặn `--out` trong `golden_heldout`. |

Kiểm khác — **không thấy lỗi**:
1. **Cờ tắt = byte-identical:** chạy lại test của B (8 kịch bản × 2) = trùng; thêm ca bảng bộ THẬT 2 tập (tập 2 thừa kế cặp, done → `save_from` ghi bảng bộ) + job **park rồi chạy lại → done**: prompt, script, display, srt, glossary, trace, manifest, plan_suggestions, bảng bộ — trùng từng byte với bản gốc (kiểm chứng ngược: bật `SIMPLE_PAIR_RULES` ⇒ test báo khác). Lưu ý: khác biệt cố ý chỉ ở câu có lặp ASR (sửa lỗi của A + D1).
2. **pair_rules:** không bao giờ đè cặp plan (`add_pair` kiểm khoá; plan dict không bị chèn); hướng A→B/B→A đúng (vai đảo khi đọc ma trận ngược, `self` theo giới người nói / `call` theo giới người nghe); giới «?» ⇒ nhận mọi dạng hoặc bỏ (người yêu cần giới; vợ chồng cùng giới ⇒ bỏ); «Sư phụ» đơn lẻ không đoán; «vợ» trong «vợ chồng» được che. Dạng xưng hô theo modern/cổ trang/tiên hiệp (vợ chồng anh–em / ta–nàng–thiếp–chàng; sư đồ vi sư–đồ nhi; vua tôi trẫm–khanh / thần–bệ hạ; ông cháu; anh chị em huynh/tỷ–đệ/muội) hợp quy ước lồng tiếng.
3. **pair_fill:** `retries=0` ⇒ không `wait_turn`, không backoff, lỗi/429/timeout/JSON hỏng ⇒ `info.error`, KHÔNG park, không treo (tối đa 1 timeout); chạy lại dùng `plan_inferred.json` (llm_fill) — không hỏi lại cặp đã nhận; không ghi `glossary.json` khi `SIMPLE_LEARN_INFERRED=0` (không module nào khác đọc `plan_inferred.json`/`inferred_pairs`); chi phí ≤ 1 lời gọi/job (≤8 cặp × ≤12 câu, ≤2048 token ra).
4. **zh_source:** không ghi `asr.json`; ffmpeg thiếu ⇒ 0 khung ⇒ không hardsub; RapidOCR thiếu ⇒ `no_ocr`; mọi ngoại lệ trong `prepare` ⇒ giữ ASR; merge giữ 1-1 câu, i/start/end.
5. **Gỡ lặp ZH:** chỉ đổi `zh`, không đổi i/timing/số câu; 哈哈哈哈 giữ, 不不不 (lẻ) giữ, 不不不不 → 不不 / 对对对对 → 对对 — GIỐNG luồng cũ (`apply_asr_stutter_heal`).
6. **golden_ab:** biến thể mới đúng env; `_MANAGED` gồm mọi khoá `SIMPLE_*` mới (env người dùng không lọt); `.bat` CRLF, `next`/`dry next`/`score next` rẽ đúng nhánh, `heldout` không đổi.
7. **tools:** `simple_stats.py` chỉ ghi `--json` ngoài work (đã chặn); `collect_manual_edits.py` xem D6.
8. **Ghi file/khoá:** manifest chỉ qua `_manifest_update`/`_set_stage` có sẵn; trace xoay trước mọi `note` mới (`prepare` không ghi trace); `plan_inferred.json`/`zh_source.json`/`asr.zhsource.json` ghi atomic.

## Đề xuất (thấp / thiết kế — chưa làm)

- **P1** Luồng cũ có cùng lỗi D1 (`translate.apply_style_polish` → `apply_asr_stutter_heal` cuối luồng: «Đi mau,!»). Sửa trong `translate.py` (cần đợt riêng + đối chiếu golden).
- **P2** `hardsub_asr.merge_hardsub_into_asr` (dùng ngoài simple) có cùng lỗi nhân đôi D3 — nên chuyển `_guard_ocr` vào đó sau khi kiểm nơi gọi.
- **P3** `golden_ab.py`: biến thể `simple*` nên đặt tường minh `"0"` cho các cờ «next» không dùng — hiện `_MANAGED` chỉ xoá ENV; nếu `pineline.config.json` có `SIMPLE_PAIR_RULES=1` thì biến thể `simple` bị nhiễm (hiện file không có khoá `SIMPLE_*` ⇒ chưa ảnh hưởng).
- **P4** pair_rules: cặp rule B→A có thể mâu thuẫn cặp plan A→B (plan «ta/ngươi», rule «em/anh»); khi plan đã có một chiều, nên suy chiều kia theo chiều plan hoặc bỏ.
- **P5** pair_fill: cặp bị model trả conf thấp được hỏi lại mỗi lần chạy lại (tốn 1 lời gọi); nên nhớ «đã hỏi» trong `plan_inferred.json`.
- **P6** `_learn_inferred` đọc-sửa-ghi `glossary.json` không khoá (đua với sửa plan trên UI) — như `series_glossary.save_from` hiện có.
- **P7** `zh_source`: `extract_hardsub_cues` OCR cả phim không có `stop_check`/giới hạn thời gian; chạy trước `try` của pipeline (lỗi đã được nuốt, nhưng dừng job phải chờ OCR xong).
- **P8** Bảng quy tắc vẫn là quy ước chung: nên đo `simple_rules` trên held-out KHÁC 2 job B đã xem (khai báo của B).

## Test (cloud, Python 3.13, không fastapi)

| Bộ | Trước (bản B) | Sau |
|---|---|---|
| simple + scenarios + next (+ next_review mới) | 70 pass, 4 skip | **78 pass, 4 skip** (+8 ca mới; 7 ca tái hiện lỗi FAIL trên bản B) |
| nhóm dịch cũ (15 file của bat) | 231 pass / 8 fail / 11 skip / 2 lỗi collect | giống hệt (cùng danh sách fail có sẵn/môi trường) |
| toàn bộ `tests/` | 367 pass / 16 fail / 15 skip / 12 lỗi collect | **375 pass** / 16 fail (cùng danh sách) / 15 skip / 12 lỗi collect |

Windows: `Z:\PinelineV6\scripts\test_v2_translate_simple.bat` — kỳ vọng mới **82 pass** (74 + 8 ca `tests\test_translate_simple_next_review.py`).

## File đã ghi (md5 sau ghi)

`server.py`, `translate.py`, `hardsub_asr.py`, V6 `golden_ab.py`/`golden_ab_simple.bat` KHÔNG đổi.

| File | md5 |
|---|---|
| `translate_simple/post.py` | `0b9f99f6d867985592d0c014cff6b309` |
| `translate_simple/pipeline.py` | `5e0e2ca8fce548bbce868569614a2330` |
| `translate_simple/zh_source.py` | `b40ab0fb97ef02a776e06a662414a756` |
| `data/lexicon/pronoun_rules_zh_vi.json` | `0276cb0eb8a405eb723ccabee789839d` |
| `tools/collect_manual_edits.py` | `ace02d6e2119f1d1d47277e0d444d544` |
| `tests/test_translate_simple_next.py` | `4d9c7ca0897b1dbdd32e1b570f55fe06` |
| `tests/test_translate_simple_next_review.py` | `17257bc0b40424e8d06cb5e0ccf4da1d` |
| `docs/CHANGELOG.md` | `818ff9bb7867029e3ef1afdb39aece34` |
| `docs/worklog/2026-11-12.md` | `c7c7edf2377e12d0154d05cc356eba37` |
| V6 `scripts/test_v2_translate_simple.bat` | `e2b32459d02b3d64d0de612741ee3cba` |
