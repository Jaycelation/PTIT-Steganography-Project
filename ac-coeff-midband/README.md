# ac-coeff-midband

## TL;DR

Challenge giấu flag trong các hệ số AC trung tần của block DCT 8x8. Đây là mô phỏng frame-DCT local, không phải can thiệp bitstream MPEG thật.

## Mục tiêu học tập

- Phân biệt DC và AC trong block DCT.
- Dùng AC trung tần để giảm ảnh hưởng thị giác so với sửa DC.
- Extract payload khi biết seed, độ dài flag và danh sách coefficient candidate.

## Public

- `output/stego.mp4`
- `output/hint.txt`
- `output/public_config.json`

## Private

- `output/private/flag.txt`
- `output/private_config.json`

## Lệnh chạy

```powershell
python generate.py --flag "PTIT{midband_ac_hidden}" --seed 2026 --output output/
python solve.py --input output/stego.mp4 --config output/public_config.json --output output/answer.txt
python checker.py --answer-file output/answer.txt
```

PSNR synthetic mặc định nên lớn hơn 30 dB trước bước encode MP4.

