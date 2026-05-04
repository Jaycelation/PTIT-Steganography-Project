# drift-compensation-basic

## TL;DR

Challenge mô phỏng drift trong video có dự đoán liên khung và nhúng DC/AC có bù drift. Đây là mô phỏng frame-DCT local, không phải sửa bitstream MPEG codec-level.

## Mục tiêu học tập

- Hiểu vì sao sửa hệ số trong video dự đoán liên khung có thể gây drift.
- Mô phỏng frame dự đoán từ frame trước.
- Tính `drift = frame_that - frame_du_doan`.
- So sánh `stego_no_comp.mp4` và `stego_comp.mp4`.
- Extract flag từ bản có compensation.

## Lệnh chạy

```powershell
python generate.py --flag "PTIT{drift_compensated}" --seed 404 --output output/
python solve.py --input output/stego_comp.mp4 --seed 404 --output output/answer.txt
python checker.py --answer-file output/answer.txt
```

