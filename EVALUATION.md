# Đánh Giá Demo Video

Nguồn gốc:

- File: `videos/Video_Demo1.mp4`
- Resolution: `1920x1080`
- Frames: `341`
- FPS: `25`
- Size: `13.16 MiB`

Demo hiện tại trong scope chính nằm trong thư mục `demo_color/` của 4 challenge core và đã được regenerate ở đúng resolution gốc `1920x1080`.

## Tiêu Chí 1: Chất Lượng Video Tương Đương Video Gốc

Kết luận: **Đạt về resolution, màu sắc và độ nét tương đối.**

- Resolution: đạt, các demo core là `1920x1080`.
- Màu sắc: đạt, pipeline chỉ nhúng trên kênh Y và giữ Cr/Cb.
- Độ nét: khá tốt.
- PSNR màu lấy mẫu theo frame: khoảng `34.87` đến `34.89 dB`.

## Tiêu Chí 2: Dung Lượng Video Tương Đương Video Gốc

Kết luận: **Chưa đạt nếu bắt buộc dung lượng gần source.**

- Video gốc: `13.16 MiB`.
- Demo full HD hiện tại: khoảng `30.45` đến `30.68 MiB`.
- Tỷ lệ size: khoảng `2.31x` đến `2.33x` video gốc.

Nguyên nhân: môi trường hiện tại không có `ffmpeg` CLI, và OpenCV H.264 trên máy này lỗi `openh264`, nên code đang ghi MP4 bằng `mp4v`. Codec này giữ full HD khá ổn nhưng nén kém hơn H.264 của video gốc.

## Bảng Đo Nhanh Trong Scope Chính

| Challenge | Resolution | Size vs source | PSNR màu | Saturation delta | Sharpness ratio |
|---|---:|---:|---:|---:|---:|
| `dc-coeff-warmup` | 1920x1080 | 231.46% | 34.89 dB | 1.68 | 0.975 |
| `ac-coeff-midband` | 1920x1080 | 231.45% | 34.89 dB | 1.68 | 0.975 |
| `dc-ac-combined` | 1920x1080 | 231.45% | 34.89 dB | 1.68 | 0.975 |
| `drift-compensation-basic` | 1920x1080 | 233.22% | 34.87 dB | 1.70 | 0.976 |

## Kết Luận Hiện Tại

- Nếu ưu tiên độ nét/resolution: bản `demo_color/` hiện tại của các challenge core là bản nên dùng.
- Nếu ưu tiên dung lượng gần source: cần bổ sung `ffmpeg` hoặc sửa H.264/OpenH264 để encode full HD bằng H.264/H.265 với CRF/bitrate phù hợp.
- Thư mục `output/` chỉ là synthetic acceptance output nhỏ, không phải demo chất lượng cao.
- Các hướng mở rộng ngoài DC/AC và cân bằng độ lệch đã được đưa ra khỏi scope chính.
