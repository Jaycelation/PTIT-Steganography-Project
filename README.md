# Coefficient-Domain Video Steganography Challenges

Bộ local CTF challenge về giấu tin trong video miền hệ số bằng sửa đổi hệ số DC/AC và mô phỏng cân bằng độ lệch.

Lưu ý quan trọng:
- Tất cả challenge trong repo này là mô phỏng frame-DCT local bằng Python.
- Đây không phải triển khai codec-level MPEG thật trên bitstream VLD/RLD/RLC/VLC.
- Không có payload tự thực thi, exploit media player, autorun hoặc hành vi độc hại.

## Challenge

| Challenge | Độ khó | Trọng tâm |
|---|---:|---|
| `dc-coeff-warmup` | Easy | Sửa hệ số DC |
| `ac-coeff-midband` | Easy/Medium | Sửa hệ số AC trung tần |
| `dc-ac-combined` | Medium | Header ở DC, payload ở AC |
| `drift-compensation-basic` | Medium/Hard | Mô phỏng drift và bù drift |
| `vlc-size-aware-embedding` | Hard | Ràng buộc kích thước VLC giả lập |
| `robust-dc-ac-after-reencode` | Hard | Repetition, majority vote sau re-encode |

## Chạy nhanh

```powershell
cd dc-coeff-warmup
python generate.py --flag "PTIT{dc_coeff_test}" --seed 1337 --output output/
python solve.py --input output/stego.mp4 --seed 1337 --length 19 --output output/answer.txt
python checker.py --answer-file output/answer.txt
```

Kỳ vọng: `PASS`.

## Demo Với Video Thật

Repo có thể dùng `videos/Video_Demo1.mp4` làm nguồn demo. Xem [DEMO.md](DEMO.md) để chạy lại toàn bộ demo bằng video này.
