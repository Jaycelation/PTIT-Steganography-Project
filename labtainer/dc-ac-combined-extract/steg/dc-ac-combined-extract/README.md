# Tách tin trong video miền hệ số bằng kết hợp hệ số DC và AC

Lab này dựa trên challenge `dc-ac-combined`.

Bạn được cung cấp một stego video và public config. Header/sync/magic được nhúng trong hệ số DC, còn payload/flag được nhúng trong các hệ số AC trung tần của block DCT 8x8.

Đây là mô phỏng frame-DCT local bằng Python, không phải sửa bitstream codec-level.

## Files

- `output/stego.mp4`: video stego public.
- `output/public_config.json`: tham số public cho extractor.
- `solve.py`: extractor gốc.
- `src/`: code DCT, video I/O và extraction.
- `tools/`: helper tạo marker checkwork.
- `work/`: sinh ra khi chạy bài.

## Lệnh Chạy

```bash
cd ~/dc-ac-combined-extract
python3 tools/check_video_metadata.py
python3 tools/check_dc_header.py
python3 tools/run_dc_ac_extract.py
```

Tuỳ chọn:

```bash
python3 tools/report_metrics.py
```

## Output Mong Đợi

- `work/video_metadata.txt`
- `work/header.log`
- `work/extract.log`
- `work/answer.txt`
- `work/answer_status.txt`
- `work/answer.sha256`
- `work/metrics.json`

Flag đúng không được công bố trong README. Checkwork kiểm tra hash của answer.
