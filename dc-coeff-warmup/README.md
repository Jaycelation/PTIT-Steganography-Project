# dc-coeff-warmup

## TL;DR

Bài nhập môn về giấu tin trong miền hệ số video bằng cách sửa hệ số DC của block DCT 8x8. Challenge dùng mô phỏng frame-DCT local, không thao tác trực tiếp bitstream MPEG.

## Mục tiêu học tập

- Tách video thành frame grayscale.
- Chia frame thành block 8x8.
- Tính DCT và đọc/sửa hệ số DC.
- Extract flag khi biết seed, số byte flag và quy tắc nhúng.
- Đánh giá MSE/PSNR ở mức cơ bản.

## Public

Sau khi generate:
- `output/stego.mp4`
- `output/public/README.md`

Public hint:
- Seed được cung cấp.
- Số byte flag được cung cấp.
- Mỗi bit được nhúng vào hệ số DC của một block 8x8.

## Private

- `output/private/flag.txt`
- `output/private/config.json`
- `generate.py`
- `solve.py`

## Lệnh chạy

```powershell
python generate.py --flag "PTIT{dc_coeff_test}" --seed 1337 --output output/
python solve.py --input output/stego.mp4 --seed 1337 --length 19 --output output/answer.txt
python checker.py --answer-file output/answer.txt
```

## Ghi chú kỹ thuật

Embedding dùng QIM parity:

```text
q = round(DC / step)
bit = q mod 2
```

Khi nhúng, `q` được điều chỉnh để parity khớp bit cần giấu. Đây là mô phỏng frame-DCT local, không phải sửa hệ số DC trong bitstream MPEG thật.

