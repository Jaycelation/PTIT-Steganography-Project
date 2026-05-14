# Hướng Dẫn Lab: AC Midband Extract

## 1. Giới Thiệu Chung

Bài lab `ac-midband-extract` hướng dẫn sinh viên khôi phục thông điệp ẩn từ một video stego MP4 công khai. Payload được nhúng vào các hệ số AC trung tần trong các khối DCT 8x8.

Đây là bài lab mô phỏng trên miền hệ số DCT của từng frame video. Bài lab không chỉnh sửa trực tiếp bitstream codec MPEG/H.265/H.264.

## 2. Mục Tiêu

Sau khi hoàn thành bài lab, sinh viên có thể:

- Kiểm tra metadata cơ bản của video stego.
- Đọc và hiểu file cấu hình public dùng cho quá trình trích xuất.
- Nhận biết vai trò của các hệ số AC trung tần trong giấu tin video.
- Chạy pipeline trích xuất thông điệp từ video stego.
- Tạo các file kết quả để Labtainer `checkwork` kiểm tra.

## 3. Yêu Cầu

Sinh viên cần chuẩn bị:

- Máy ảo Labtainer đã cài đặt và chạy được terminal.
- Kết nối Internet để tải lab bằng `imodule`.
- Kiến thức Linux cơ bản: `cd`, `pwd`, `cat`, chạy lệnh Python.
- Biết cách quan sát file output trong thư mục `work/`.
- Không chỉnh sửa file `output/stego.mp4` hoặc các file đáp án của Labtainer.

## 4. Tải Và Khởi Động Lab

Trong máy ảo Labtainer, mở terminal và chuyển vào thư mục Labtainer student:

```bash
cd ~/labtainer/labtainer-student
```

Tải lab:

```bash
imodule https://github.com/Jaycelation/PTIT-Steganography-Project/raw/refs/heads/master/labtainer/ac-midband-extract.tar
```

Khởi động lab:

```bash
labtainer -r ac-midband-extract
```

Sau khi lab mở, terminal sẽ ở workspace:

```text
/home/student/ac-midband-extract
```

Nếu cần kiểm tra lại vị trí hiện tại:

```bash
pwd
```

### Cấu Trúc File Trong Lab

Các file chính trong lab:

```text
output/stego.mp4
output/public_config.json
output/hint.txt
solve.py
src/
tools/
work/
```

Ý nghĩa:

- `output/stego.mp4`: video đã được nhúng thông điệp.
- `output/public_config.json`: tham số public dùng để trích xuất payload.
- `output/hint.txt`: gợi ý công khai cho sinh viên.
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

### Task 2: Kiểm Tra Cấu Hình AC

Chạy lệnh:

```bash
python3 tools/check_ac_config.py
```

Lệnh này đọc `output/public_config.json` và `output/hint.txt`, sau đó ghi kết quả vào:

```text
work/ac_config.txt
```

Xem kết quả:

```bash
cat work/ac_config.txt
```

Kết quả hợp lệ cần có dòng:

```text
AC_CONFIG_OK
```

Các trường quan trọng:

- `seed`: seed dùng để chọn vị trí trích xuất.
- `flag_length_bytes`: độ dài thông điệp cần khôi phục.
- `q_step`: bước lượng tử dùng cho nhúng/trích xuất.
- `coefficient_candidates`: danh sách hệ số AC trung tần được xét.
- `hint`: gợi ý công khai.

### Task 3: Chạy Bộ Trích Xuất AC Midband

Chạy lệnh:

```bash
python3 tools/run_ac_extract.py
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
AC_EXTRACT_OK
```

### Task 4: Xem Metrics Tùy Chọn

Task này không bắt buộc cho checkwork chính, nhưng nên chạy để hiểu thêm về dữ liệu video và dung lượng nhúng.

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

File metrics có các thông tin như kích thước video, số frame, `q_step`, độ dài flag và ước lượng dung lượng nhúng trên miền AC.

## 6. Kiểm Tra Kết Quả

Sau khi hoàn thành các task bắt buộc, quay lại terminal Labtainer bên ngoài và chạy:

```bash
checkwork ac-midband-extract
```

Labtainer sẽ kiểm tra các mục:

| Mục kiểm tra | File kết quả | Dấu hiệu hợp lệ |
|---|---|---|
| Metadata video | `work/video_metadata.txt` | `VIDEO_METADATA_OK` |
| Cấu hình AC | `work/ac_config.txt` | `AC_CONFIG_OK` |
| Bộ trích xuất AC | `work/extract.log` | `AC_EXTRACT_OK` |
| File answer | `work/answer_status.txt` | `ANSWER_FILE_CREATED` |
| Hash flag | `work/answer.sha256` | Hash khớp đáp án |

### Kết Thúc Lab

Kết thúc lab:

```bash
stoplab ac-midband-extract
```

Chạy lại lab từ đầu:

```bash
labtainer -r ac-midband-extract
```

Lưu ý: tùy chọn `-r` sẽ reset trạng thái làm bài hiện tại.

### Ghi Chú

- Không chỉnh sửa file `output/stego.mp4`.
- Không cần biết đáp án trước; `checkwork` dùng hash để xác minh.
- Nếu lệnh Python báo lỗi, kiểm tra lại thư mục hiện tại bằng `pwd`.
- Nếu thiếu file trong `work/`, chạy lại các script trong `tools/` theo đúng thứ tự.
