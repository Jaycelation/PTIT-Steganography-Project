# Demo với `videos/Video_Demo1.mp4`

## TL;DR

Demo dùng video thật trong `videos/Video_Demo1.mp4`. Pipeline xử lý theo YCrCb:

- Chỉ nhúng/extract trên kênh Y.
- Giữ lại Cr/Cb để video stego vẫn có màu.
- Mặc định code không downscale; `--max-width 0` nghĩa là giữ kích thước gốc.
- Demo mặc định bên dưới dùng `--max-width 0` để giữ nguyên `1920x1080` như video gốc.

Lưu ý: full HD sẽ chạy lâu hơn và dung lượng file có thể tăng vì môi trường hiện tại đang encode bằng OpenCV `mp4v`, không phải H.264/CRF.

## Scope Demo

Chỉ giữ demo cho các challenge core liên quan trực tiếp đến DC, AC, DC+AC và cân bằng độ lệch:

- `dc-coeff-warmup`
- `ac-coeff-midband`
- `dc-ac-combined`
- `drift-compensation-basic`

## Lệnh Demo HQ

### dc-coeff-warmup

```powershell
cd dc-coeff-warmup
python -B generate.py --input ../videos/Video_Demo1.mp4 --max-width 0 --flag "PTIT{dc_demo_video}" --seed 1337 --output demo_color/
python -B solve.py --input demo_color/stego.mp4 --seed 1337 --length 19 --output demo_color/answer.txt
python -B checker.py --answer-file demo_color/answer.txt --expected-file demo_color/private/flag.txt
```

### ac-coeff-midband

```powershell
cd ac-coeff-midband
python -B generate.py --input ../videos/Video_Demo1.mp4 --max-width 0 --flag "PTIT{ac_demo_video}" --seed 2026 --output demo_color/
python -B solve.py --input demo_color/stego.mp4 --config demo_color/public_config.json --output demo_color/answer.txt
python -B checker.py --answer-file demo_color/answer.txt --expected-file demo_color/private/flag.txt
```

### dc-ac-combined

```powershell
cd dc-ac-combined
python -B generate.py --input ../videos/Video_Demo1.mp4 --max-width 0 --flag "PTIT{combo_demo}" --seed 2026 --output demo_color/
python -B solve.py --input demo_color/stego.mp4 --config demo_color/public_config.json --output demo_color/answer.txt
python -B checker.py --answer-file demo_color/answer.txt --expected-file demo_color/private/flag.txt
```

### drift-compensation-basic

```powershell
cd drift-compensation-basic
python -B generate.py --input ../videos/Video_Demo1.mp4 --max-width 0 --flag "PTIT{drift_demo_video}" --seed 404 --output demo_color/
python -B solve.py --input demo_color/stego_comp.mp4 --seed 404 --output demo_color/answer.txt
python -B checker.py --answer-file demo_color/answer.txt --expected-file demo_color/private/flag.txt
```

## Ghi Chú

- Đây vẫn là mô phỏng frame-DCT local, không phải sửa bitstream MPEG codec-level.
- Output demo nằm trong thư mục `demo_color/` của từng challenge.
- Các hướng mở rộng ngoài DC/AC và cân bằng độ lệch không thuộc scope chính của đề tài 4.3.
