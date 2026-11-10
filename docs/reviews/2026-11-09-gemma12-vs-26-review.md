# Gemma4 12B vs 26B — độ chuẩn khi làm REVIEW

- **Date:** 2026-11-09 ~22:12
- **Context:** Job `05670cbf7c1c` đang soát bằng `llama/gemma4-12b-qat-mtp-fast` (:8083). User nghi 12B yếu hơn 26B.

## Kết luận ngắn

**Nghi đúng.** 12B đang đóng vai “cổng nhanh”, không phải biên tập viên tin cậy cho thành ngữ/calque. Repo **chưa có** bench A/B review head-to-head 12↔26 trên cùng lô cue; phán dựa trên (1) lỗi live đã chứng minh, (2) lịch sử chọn model, (3) bench tốc độ/VRAM.

| | **12B QAT MTP fast** (đang dùng) | **26B QAT / uncen MTP** |
|---|---|---|
| Vai trò hiện tại | TRANSLATE + REVIEW | Có preset, không gắn REVIEW |
| Điểm mạnh | Nhanh, nhẹ VRAM, ổn cho polish nhẹ | Khỏe hơn idiom / instruction / “thấy câu vô nghĩa” |
| Điểm yếu REVIEW | Dễ no-op; bỏ sót calque/ASR stutter | Chậm hơn; nạp lại :8083 cắt job đang chạy |
| Máy này (3060 12GB) | Active `gemma4-12b-qat-mtp-fast` | Bench ~36–74 tg tok/s tùy quant/offload (vẫn chạy được) |

## Bằng chứng (không đoán)

1. **Live miss hôm nay — `05670` i=8**  
   ZH `你还没大没小了。` → VI `Cậu còn chưa lớn không nhỏ.` với `mt=1` **`rv=1`**.  
   Pass1 (GPT mini upload) cũng **không** flag. 12B review coi như OK.  
   → Fix log `docs/fixes/2026-11-09-meidameixiao-calque.md`.

2. **ASR stutter (cùng ngày)**  
   Smoke duty E trên Gemma4 12B: hay **no-op** / bỏ sót lặp `不对不对`; phải dựa **deterministic heal**.  
   → `docs/fixes/2026-11-09-review-asr-merge.md` follow-up.

3. **Lịch sử chọn REVIEW khi cần chất lượng**  
   - 11-02: REVIEW = `gemma4:31b-cloud` (tầng 3).  
   - 11-09 sáng: GPT mini / qwen36 rồi **đổi sang 12B vì tốc độ** (DECISIONS), không vì 12B thắng chất lượng.

4. **Tốc độ (preset benches, không phải điểm dịch)**  
   - 26B Q6_K tg128 ~36 t/s; QAT MTP có config ~50–74 t/s.  
   - 12B fast đang giữ throughput cho ~3900 cue — đúng trade-off tốc độ.

## Việc đang làm thay cho “đọc hết tay”

Watcher kỹ: `D:\PinelineV2_tmp\_qa_watch_05670.py`  
Report: `D:\PinelineV2_tmp\qa_watch_05670\REPORT.md`  

Quét deterministic: calque đã biết, CJK leak, đuôi treo, stutter (trừ reduplicate hợp lệ), heal lại `没大没小` mỗi vòng (vì worker còn ghi đè memory).

## Khuyến nghị vận hành

1. **Giữ NMT primary** — không giao dịch chính cho 12B/26B.  
2. **REVIEW:** nếu ưu tiên chuẩn > tốc độ → `gemma4-26b-qat-uncen-mtp` (hoặc qwen36 / 31b-cloud như trước). Đổi **sau** khi job `05670` xong (đổi giữa chừng = unload 12B, review đứt).  
3. **Luôn giữ lưới deterministic** (polish/heuristic) — 26B cũng sẽ sót; chỉ ít hơn.  
4. Muốn số liệu cứng 12↔26: sandbox A/B 50–100 cue “khó” (thành ngữ + ASR cắt) trên cùng NMT draft — chưa chạy trong phiên này.

## Liên quan

- Config: `REVIEW_MODEL=llama/gemma4-12b-qat-mtp-fast`
- Presets: `E:\models\presets\models.json` (`gemma4-12b-*`, `gemma4-26b-*`)
