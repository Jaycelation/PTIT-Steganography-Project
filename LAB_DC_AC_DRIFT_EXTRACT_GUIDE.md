# Hướng Dẫn Lab: DC/AC Drift Extract

## 1. Giới Thiệu Chung

Bài lab `dc-ac-drift-extract` hướng dẫn sinh viên khôi phục thông điệp ẩn từ một video stego MP4 công khai, đồng thời ghi lại các metrics phục vụ phân tích độ ổn định và drift trong quá trình trích xuất.

Bài lab sử dụng pipeline trích xuất DC/AC:

- Hệ số DC cung cấp dữ liệu đồng bộ/header.
- Các hệ số AC trung tần mang payload chính.
- Metrics giúp sinh viên quan sát các tham số liên quan đến dung lượng và độ tin cậy của quá trình trích xuất.

Đây là bài lab mô phỏng trên miền hệ số DCT của từng frame video. Bài lab không chỉnh sửa trực tiếp bitstream codec MPEG/H.265/H.264.

## 2. Mục Tiêu

Sau khi hoàn thành bài lab, sinh viên có thể:

- Kiểm tra metadata cơ bản của video stego.
- Chạy pipeline trích xuất thông điệp theo hướng DC/AC.
- Tạo file answer và hash để Labtainer kiểm tra.
- Ghi lại metrics công khai của video và cấu hình trích xuất.
- Hiểu vai trò của metrics khi đánh giá drift và độ tin cậy trong video steganography.

## 3. Khởi Động Lab

Trong máy ảo Labtainer, mở terminal và chuyển vào thư mục Labtainer student:

```bash
cd ~/labtainer/labtainer-student
```

Tải lab:

```bash
imodule https://github.com/Jaycelation/PTIT-Steganography-Project/raw/refs/heads/master/labtainer/dc-ac-drift-extract.tar
```

Khởi động lab:

```bash
labtainer -r dc-ac-drift-extract
```

Sau khi lab mở, terminal sẽ ở workspace:

```text
/home/student/dc-ac-drift-extract
```

Nếu cần kiểm tra lại vị trí hiện tại:

```bash
pwd
```

## 4. Cấu Trúc File

Các file chính trong lab:

```text
output/stego.mp4
output/public_config.json
solve.py
src/
tools/
work/
```

Ý nghĩa:

- `output/stego.mp4`: video đã được nhúng thông điệp.
- `output/public_config.json`: tham số public dùng cho quá trình trích xuất.
- `solve.py`: chương trình trích xuất chính.
- `src/`: mã nguồn hỗ trợ DCT, đọc video, trích xuất và tính toán.
- `tools/`: các script phục vụ từng bước làm lab.
- `work/`: thư mục sinh ra kết quả sau khi chạy lệnh.

## 5. Thực Hành

### Task 1: Kiểm Tra Metadata Video

Chạy lệnh:

```bash
python3 tools/check_video_metadata.py
```

Lệnh này đọc `output/stego.mp4` và ghi thông tin video vào:

```text
work/video_metadata.txt
```

Xem kết quả:

```bash
cat work/video_metadata.txt
```

Kết quả hợp lệ cần có dòng:

```text
VIDEO_METADATA_OK
```

Các thông tin cần quan sát:

- `width`: chiều rộng video.
- `height`: chiều cao video.
- `frames`: số frame.
- `fps`: tốc độ khung hình.

### Task 2: Chạy Bộ Trích Xuất DC/AC

Chạy lệnh:

```bash
python3 tools/run_dc_ac_extract.py
```

Lệnh này gọi `solve.py` với input mặc định:

```text
output/stego.mp4
output/public_config.json
```

Kết quả được ghi vào:

```text
work/answer.txt
work/extract.log
work/answer_status.txt
work/answer.sha256
```

Xem thông điệp khôi phục:

```bash
cat work/answer.txt
```

Xem log:

```bash
cat work/extract.log
```

Kết quả hợp lệ cần có dòng:

```text
DC_AC_EXTRACT_OK
```

### Task 3: Ghi Lại Metrics Trích Xuất

Chạy lệnh:

```bash
python3 tools/report_metrics.py
```

Kết quả được ghi vào:

```text
work/metrics.json
```

Xem kết quả:

```bash
cat work/metrics.json
```

Kết quả hợp lệ cần có marker:

```text
METRICS_OK
```

Các trường quan trọng trong file metrics:

- `challenge`: tên lab.
- `source_model`: mô hình xử lý video.
- `width`, `height`: độ phân giải video.
- `frames`: số frame.
- `fps`: tốc độ khung hình.
- `dc_step`: bước nhúng/trích xuất trên hệ số DC.
- `ac_step`: bước nhúng/trích xuất trên hệ số AC.
- `flag_length_bytes`: độ dài thông điệp.
- `estimated_ac_capacity_bits`: ước lượng dung lượng nhúng trên miền AC.
- `drift_compensation_note`: ghi chú về phạm vi drift compensation.

## 6. Kiểm Tra Bài Làm

Sau khi hoàn thành các task bắt buộc, quay lại terminal Labtainer bên ngoài và chạy:

```bash
checkwork dc-ac-drift-extract
```

Labtainer sẽ kiểm tra các mục:

| Mục kiểm tra | File kết quả | Dấu hiệu hợp lệ |
|---|---|---|
| Metadata video | `work/video_metadata.txt` | `VIDEO_METADATA_OK` |
| Bộ trích xuất DC/AC | `work/extract.log` | `DC_AC_EXTRACT_OK` |
| File answer | `work/answer_status.txt` | `ANSWER_FILE_CREATED` |
| Hash flag | `work/answer.sha256` | Hash khớp đáp án |
| Metrics | `work/metrics.json` | `METRICS_OK` |

## 7. Kết Thúc Lab

Kết thúc lab:

```bash
stoplab dc-ac-drift-extract
```

Chạy lại lab từ đầu:

```bash
labtainer -r dc-ac-drift-extract
```

Lưu ý: tùy chọn `-r` sẽ reset trạng thái làm bài hiện tại.

## 8. Ghi Chú

- Không chỉnh sửa file `output/stego.mp4`.
- Bài lab này bắt buộc chạy `tools/report_metrics.py`, vì metrics là một phần của checkwork.
- File `work/answer.sha256` được dùng để đối chiếu đáp án mà không cần hiển thị đáp án trong cấu hình chấm.
- Nếu thiếu marker `METRICS_OK`, chạy lại script metrics và kiểm tra lỗi hiển thị trên terminal.
