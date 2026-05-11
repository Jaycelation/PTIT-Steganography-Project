# Coefficient-Domain Video Steganography Challenges

Bộ bài lab/CTF local cho đề tài:

> Giấu tin trong video miền hệ số bằng kỹ thuật sửa đổi hệ số DC và AC với hệ số cân bằng độ lệch (4.3).

Lưu ý an toàn:

- Tất cả challenge trong scope chính là mô phỏng frame-DCT local bằng Python.
- Đây không phải triển khai codec-level MPEG thật trên bitstream nén của codec.
- Không có payload tự thực thi, exploit media player, autorun MP4 hoặc hành vi độc hại.

## Scope Chính

| Challenge | Độ khó | Trọng tâm |
|---|---:|---|
| `dc-coeff-warmup` | Easy | Sửa hệ số DC |
| `ac-coeff-midband` | Easy/Medium | Sửa hệ số AC trung tần |
| `dc-ac-combined` | Medium | Header ở DC, payload ở AC |
| `drift-compensation-basic` | Medium/Hard | Mô phỏng drift và cân bằng độ lệch |

Labtainer-ready lab hiện tại:

| Lab | Nền tảng | Trạng thái |
|---|---|---|
| `dc-ac-drift-extract` | `dc-ac-combined` + ngữ cảnh drift compensation | Ready first pass |

## Chạy Nhanh

```powershell
cd dc-coeff-warmup
python generate.py --flag "PTIT{dc_coeff_test}" --seed 1337 --output output/
python solve.py --input output/stego.mp4 --seed 1337 --length 19 --output output/answer.txt
python checker.py --answer-file output/answer.txt
```

Kỳ vọng: `PASS`.

## Labtainer

Build student package cho lab chính:

```powershell
python scripts\prepare_labtainer_public.py
python scripts\run_all_lab_checks.py
```

Package được tạo tại:

```text
labtainer/build/dc-ac-drift-extract/
```

Student package không chứa `generate.py`, `checker.py`, `private/`, `private_config.json`, hoặc answer key.

## Demo Với Video Thật

Repo có thể dùng `videos/Video_Demo1.mp4` làm nguồn demo cho 4 challenge core. Xem [DEMO.md](DEMO.md).
