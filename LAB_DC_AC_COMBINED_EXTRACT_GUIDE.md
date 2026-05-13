# Hướng Dẫn Lab: DC/AC Combined Extract

## 1. Giới Thiệu Chung

Bài lab `dc-ac-combined-extract` hướng dẫn sinh viên khôi phục thông điệp ẩn từ một video stego MP4 công khai bằng kỹ thuật kết hợp hệ số DC và AC.

Trong bài lab này:

- Hệ số DC mang phần header đồng bộ dễ nhận biết.
- Các hệ số AC trung tần mang payload chính.

Đây là bài lab mô phỏng trên miền hệ số DCT của từng frame video. Bài lab không chỉnh sửa trực tiếp bitstream codec MPEG/H.265/H.264.

## 2. Mục Tiêu

Sau khi hoàn thành bài lab, sinh viên có thể:

- Kiểm tra metadata cơ bản của video stego.
- Hiểu vai trò của header trong hệ số DC.
- Trích xuất payload từ các hệ số AC trung tần.
- Chạy pipeline trích xuất kết hợp DC/AC.
- Tạo đầy đủ file kết quả để Labtainer `checkwork` đánh giá.

## 3. Khởi Động Lab

Trong máy ảo Labtainer, mở terminal và chuyển vào thư mục Labtainer student:

```bash
cd ~/labtainer/labtainer-student
```

Tải lab:

```bash
imodule https://github.com/Jaycelation/PTIT-Steganography-Project/raw/refs/heads/master/labtainer/dc-ac-combined-extract.tar
```

Khởi động lab:

```bash
labtainer -r dc-ac-combined-extract
```

Sau khi lab mở, terminal sẽ ở workspace:

```text
/home/student/dc-ac-combined-extract
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

### Task 2: Kiểm Tra Header Trong Hệ Số DC

Chạy lệnh:

```bash
python3 tools/check_dc_header.py
```

Lệnh này đọc video stego và cấu hình public, sau đó trích phần header được giấu trong hệ số DC.

Kết quả được ghi vào:

```text
work/header.log
```

Xem kết quả:

```bash
cat work/header.log
```

Kết quả hợp lệ cần có dòng:

```text
DC_HEADER_OK
```

Header kỳ vọng:

```text
magic=STEG
```

Ý nghĩa: header `STEG` cho biết bộ trích xuất đã đồng bộ đúng vị trí trước khi đọc payload chính.

### Task 3: Chạy Bộ Trích Xuất DC/AC

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
AC_PAYLOAD_OK
```

Trong log cũng có thể có marker:

```text
DC_AC_EXTRACT_OK
```

### Task 4: Xem Metrics Tùy Chọn

Task này không bắt buộc cho checkwork chính, nhưng nên chạy để hiểu thêm về tham số trích xuất.

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

File metrics có các thông tin như kích thước video, số frame, `dc_step`, `ac_step`, độ dài header, độ dài flag và ước lượng dung lượng nhúng trên miền AC.

## 6. Kiểm Tra Bài Làm

Sau khi hoàn thành các task bắt buộc, quay lại terminal Labtainer bên ngoài và chạy:

```bash
checkwork dc-ac-combined-extract
```

Labtainer sẽ kiểm tra các mục:

| Mục kiểm tra | File kết quả | Dấu hiệu hợp lệ |
|---|---|---|
| Metadata video | `work/video_metadata.txt` | `VIDEO_METADATA_OK` |
| Header DC | `work/header.log` | `DC_HEADER_OK` |
| Payload AC | `work/extract.log` | `AC_PAYLOAD_OK` |
| File answer | `work/answer_status.txt` | `ANSWER_FILE_CREATED` |
| Hash flag | `work/answer.sha256` | Hash khớp đáp án |

## 7. Kết Thúc Lab

Kết thúc lab:

```bash
stoplab dc-ac-combined-extract
```

Chạy lại lab từ đầu:

```bash
labtainer -r dc-ac-combined-extract
```

Lưu ý: tùy chọn `-r` sẽ reset trạng thái làm bài hiện tại.

## 8. Ghi Chú

- Không chỉnh sửa file `output/stego.mp4`.
- Header DC chỉ dùng để đồng bộ và xác nhận đường trích xuất.
- Payload chính nằm ở hệ số AC trung tần.
- Nếu thiếu file trong `work/`, chạy lại các script trong `tools/` theo đúng thứ tự.
