# Demo Với `videos/Video_Demo1.mp4`

## TL;DR

Các challenge có thể nhận video thật qua `--input`. Khi đọc video đầu vào, code normalize frame về YCrCb, chỉ nhúng trên kênh sáng Y, giữ lại Cr/Cb để video stego demo vẫn có màu, rồi crop về bội số 8 để DCT block 8x8 ổn định.

Video demo hiện dùng:

```powershell
videos/Video_Demo1.mp4
```

## Lệnh Demo

### dc-coeff-warmup

```powershell
cd dc-coeff-warmup
python -B generate.py --input ../videos/Video_Demo1.mp4 --flag "PTIT{dc_demo_video}" --seed 1337 --output demo_video/
python -B solve.py --input demo_video/stego.mp4 --seed 1337 --length 19 --output demo_video/answer.txt
python -B checker.py --answer-file demo_video/answer.txt --expected-file demo_video/private/flag.txt
```

### ac-coeff-midband

```powershell
cd ac-coeff-midband
python -B generate.py --input ../videos/Video_Demo1.mp4 --flag "PTIT{ac_demo_video}" --seed 2026 --output demo_video/
python -B solve.py --input demo_video/stego.mp4 --config demo_video/public_config.json --output demo_video/answer.txt
python -B checker.py --answer-file demo_video/answer.txt --expected-file demo_video/private/flag.txt
```

### dc-ac-combined

```powershell
cd dc-ac-combined
python -B generate.py --input ../videos/Video_Demo1.mp4 --flag "PTIT{combo_demo}" --seed 2026 --output demo_video/
python -B solve.py --input demo_video/stego.mp4 --config demo_video/public_config.json --output demo_video/answer.txt
python -B checker.py --answer-file demo_video/answer.txt --expected-file demo_video/private/flag.txt
```

### drift-compensation-basic

```powershell
cd drift-compensation-basic
python -B generate.py --input ../videos/Video_Demo1.mp4 --flag "PTIT{drift_demo_video}" --seed 404 --output demo_video/
python -B solve.py --input demo_video/stego_comp.mp4 --seed 404 --output demo_video/answer.txt
python -B checker.py --answer-file demo_video/answer.txt --expected-file demo_video/private/flag.txt
```

### vlc-size-aware-embedding

```powershell
cd vlc-size-aware-embedding
python -B generate.py --input ../videos/Video_Demo1.mp4 --flag "PTIT{vlc_demo}" --seed 1337 --output demo_video/
python -B solve.py --input demo_video/stego.mp4 --seed 1337 --output demo_video/answer.txt
python -B checker.py --answer-file demo_video/answer.txt --expected-file demo_video/private/flag.txt
```

### robust-dc-ac-after-reencode

```powershell
cd robust-dc-ac-after-reencode
python -B generate.py --input ../videos/Video_Demo1.mp4 --flag "PTIT{robust_demo}" --seed 9001 --repeat 5 --output demo_video/
python -B solve.py --input demo_video/stego_reencoded.mp4 --seed 9001 --repeat 5 --output demo_video/answer.txt
python -B checker.py --answer-file demo_video/answer.txt --expected-file demo_video/private/flag.txt
```

## Ghi Chú

- Đây vẫn là mô phỏng frame-DCT local, không phải sửa bitstream MPEG codec-level.
- Nếu máy có `ffmpeg`, bài robust sẽ re-encode bằng libx264 CRF 18; nếu không có, script dùng copy fallback để demo vẫn chạy.
- Output demo nằm trong thư mục `demo_video/` của từng challenge.
