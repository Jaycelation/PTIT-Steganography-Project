# vlc-size-aware-embedding

## TL;DR

Challenge mô phỏng nhúng hệ số DC/AC có ràng buộc kích thước VLC. Generator chỉ chấp nhận sửa hệ số nếu kích thước mã hóa giả lập sau sửa không lớn hơn trước sửa.

## Mục tiêu học tập

- Hiểu vì sao sửa hệ số trong miền hệ số có thể làm tăng kích thước VLC.
- Dùng mô hình `estimated_vlc_size(coef)` đơn giản theo magnitude.
- Extract flag từ các coefficient được chọn bằng seed.

## Lệnh chạy

```powershell
python generate.py --flag "PTIT{test_flag}" --seed 1337 --output output/
python solve.py --input output/stego.mp4 --seed 1337 --output output/answer.txt
python checker.py --answer-file output/answer.txt
```

