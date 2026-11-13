# firered-slice-silence: FireRed ASR chia slice tại khoảng lặng + đệm chồng lấn (hết cắt đôi/lặp/mất chữ ở biên 20')

- **Date:** 2026-11-13
- **Nguồn:** agent L. Bằng chứng trong `D:\PinelineV2_work\*\asr.json` (vd `2d3316593ea9` @1200 «您已成为天。|命之子。», `60892cc63cb7_p01` @1200 «我想学这个。|个猫咪后空翻。»).
- **Khu vực:** `firered_asr.py` (mới `slice_cfg`, `find_cut_frame`, `plan_slices`, `describe_plan`, `transcribe_sliced`; khối slice trong `run_asr_firered` viết lại). Mới `tests/test_firered_slice_silence.py` (9 ca), `tools/asr_boundary_scan.py` (chỉ đọc).
- **Status:** trên đĩa V2. **Có hiệu lực NGAY cho lần ASR FireRed kế tiếp** (engine chạy tiến trình con, nạp `firered_asr.py` mới mỗi lần) — không cần restart. asr.json đã có KHÔNG tự sửa: phải chạy lại ASR (force) cho job cần.
- **Backup:** `Z:\PinelineV2\.backup_edit_20261113_agentL\` (`firered_asr.py`, docs đã sửa).

## Nguyên nhân

`run_asr_firered` cắt audio thành slice cứng `FIRERED_SLICE_SEC`=1200 s bằng `ffmpeg -ss/-to` tại đúng k×1200 s, không nhìn nội dung, không chồng lấn. FireRed VAD trong mỗi slice bị chặn ở mép → câu vắt biên thành 2 mảnh (`end`=1200.0 | `start`=1200.0), lặp chữ ở 2 bên hoặc mất chữ.

## Sửa

1. **Điểm cắt = khoảng lặng gần mốc**: cửa sổ ±`FIRERED_CUT_SEARCH_SEC` (60, tối đa 0.4×slice) quanh k×slice trên CHÍNH wav ASR (`audio.wav` 16k mono — từ vocals Demucs). RMS khung 20 ms bằng numpy, chỉ đọc đúng cửa sổ (seek, không nạp cả file). Ngưỡng lặng: `FIRERED_SILENCE_DB` (-40 dBFS); nền ồn cao → nền(p5)+6 dB, nhưng luôn ≤ trung vị−10 dB và ≤ -25 dBFS. Khoảng lặng ≥ `FIRERED_MIN_SILENCE_SEC` (0.3 s); điểm số = khoảng cách/bán kính − 0.25×min(dài,2 s) (gần + dài); cắt ở GIỮA khoảng lặng.
2. **Không có khoảng lặng** → điểm năng lượng thấp nhất (trung bình trượt 0.2 s, ưu tiên gần mốc) + đệm lớn `FIRERED_SLICE_PAD_NOSIL_SEC` (10 s) cho biên đó.
3. **Chồng lấn an toàn**: slice = lõi [c_k, c_k+1) + đệm `FIRERED_SLICE_PAD_SEC` (2 s) hai đầu; sau ASR chỉ giữ câu có TÂM (start+end)/2 trong lõi → không trùng, câu vắt biên nằm trọn trong đệm của ít nhất 1 slice. Mốc thời gian = giây trong slice + start_frame/rate (start gồm đệm).
4. **Cắt theo mẫu**: `separate.write_wav_slice` chép byte PCM (không re-encode) → clip == src[start:end] từng mẫu (test kiểm). wav không phải PCM s16 mono 16k → đổi 1 lần bằng ffmpeg rồi mới cắt.
5. `FIRERED_SLICE_SEC=0` → không chia (một lượt cả file, đưa thẳng `audio.wav`) để thử khi đủ VRAM/RAM; mặc định vẫn 1200 (OOM). Đuôi < bán kính tìm → gộp vào slice cuối.
6. Log: `[firered] N slice, cắt tại khoảng lặng: 1199.42s (lặng 0.86s), …` (biên không lặng ghi «KHÔNG lặng -> chồng lấn đệm lớn»).
7. Các biến đọc env trước, rồi `pineline.config.json`.

## Kiểm chứng

- `tests/test_firered_slice_silence.py` (9): FireRed giả đọc chính file slice (mỗi câu = sóng vuông biên độ riêng → tách câu chính xác tới mẫu, câu cụt mép → «S{j}~»). Đối chứng cắt cứng → có câu cụt; bản mới: đúng thứ tự, không cụt/lặp/mất, start/end ±1.5 ms; biên không lặng; `FIRERED_SLICE_SEC=0` (1 lượt, đúng file gốc); ưu tiên lặng gần mốc; input 44.1k stereo; end-to-end `run_asr_firered` với package `fireredasr2s` giả; tool quét. Thêm 120 tổ hợp seed/khe (0.35–1.5 s) × 6 biên: 0 lỗi.
- Toàn bộ `tests/` (bản sao cloud, thiếu fastapi/google → 12 module không collect, như trước): trước 25 failed/437 passed, sau 25 failed/445 passed — cùng danh sách fail (môi trường: thiếu `data/`, lexicon…).

## Quét job cũ (`tools/asr_boundary_scan.py`, 2026-11-13)

`python tools/asr_boundary_scan.py D:/PinelineV2_work --all`: 10 job có asr.json (đều firered) · **10/10 nghi lỗi · 53/71 biên · 106 câu nghi** (34 biên «cắt đôi» chắc chắn; «đầu/đuôi bị chặn» có thể là dương tính giả khi câu tình cờ kết ở biên). Nên chạy lại ASR (+ dịch/TTS/mux): `2493d3c7cb29_p01..p04`, `2d3316593ea9`, `32da3d8f225b`, `365baf19df54`, `60892cc63cb7_p01`, `60892cc63cb7_p02`, `9dedde16e35b`.

## Engine ASR khác

- `fun_asr_nano.py`: VAD theo cửa sổ 480 s chồng 2 s, rồi ASR trên đoạn VAD đã gộp + pad → không cắt cứng giữa câu (rủi ro nhỏ: đoạn VAD bị chặn ở mép cửa sổ rồi gộp lại). Không sửa.
- `paraformer_zh.py --slice`: slice theo VAD + pad/overlap → không cùng kiểu. `sensevoice_asr.py`: FunASR VAD 1 lượt → không cắt cứng.
- `asr.py::_cut_wav_from` (resume ASR giữa chừng, `-ss` 1 điểm): chỉ khi resume — không cùng kiểu, không sửa.

## Port (CHƯA sửa)

V4 `Z:\PinelineV4\firered_asr.py`; V5 `Z:\PinelineV5\engines\asr\firered_asr.py`; V6 `Z:\PinelineV6\engines\asr\firered_asr.py` (+ hàm `wav_info`/`write_wav_slice` của `separate.py` bản agent E chưa có ở V4/V5/V6 — port cùng). Tool `tools/asr_boundary_scan.py` + test.

## Còn treo

- [ ] Chạy lại ASR (force) cho 10 job trên khi queue rảnh (asr.json mới → cần dịch/TTS lại).
- [ ] Thử `FIRERED_SLICE_SEC=0` trên 1 job dài nếu VRAM/RAM đủ.
