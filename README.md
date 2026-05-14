# PTIT Steganography Project

Repo này chứa các bài lab về giấu tin trong video trên miền hệ số DCT, tập trung vào kỹ thuật sửa đổi hệ số DC và AC. Phần triển khai chính phục vụ Labtainer gồm 3 bài lab trích xuất thông điệp từ video stego.

Lưu ý phạm vi:

- Các bài lab là mô phỏng giáo dục bằng Python trên frame/video và hệ số DCT.
- Project không triển khai tấn công media player, payload tự thực thi, autorun MP4 hoặc exploit codec.
- Các lab không yêu cầu sinh viên chỉnh sửa trực tiếp bitstream codec MPEG/H.265/H.264.

## 1. Các Bài Lab Chính

| Lab | Nội dung | Hướng dẫn |
|---|---|---|
| `ac-midband-extract` | Trích xuất thông điệp từ hệ số AC trung tần. | [LAB_AC_MIDBAND_EXTRACT_GUIDE.md](LAB_AC_MIDBAND_EXTRACT_GUIDE.md) |
| `dc-ac-combined-extract` | Trích xuất thông điệp bằng pipeline kết hợp header DC và payload AC. | [LAB_DC_AC_COMBINED_EXTRACT_GUIDE.md](LAB_DC_AC_COMBINED_EXTRACT_GUIDE.md) |
| `dc-ac-drift-extract` | Trích xuất DC/AC và ghi metrics phục vụ phân tích drift. | [LAB_DC_AC_DRIFT_EXTRACT_GUIDE.md](LAB_DC_AC_DRIFT_EXTRACT_GUIDE.md) |

Các gói Labtainer public đã có sẵn trong thư mục:

```text
labtainer/ac-midband-extract.tar
labtainer/dc-ac-combined-extract.tar
labtainer/dc-ac-drift-extract.tar
```

## 2. Tải Và Chạy Lab Trong Labtainer VM

Chạy các lệnh sau trong máy ảo Labtainer, từ thư mục student:

```bash
cd ~/labtainer/labtainer-student
```

### Lab 1: AC Midband Extract

```bash
imodule https://github.com/Jaycelation/PTIT-Steganography-Project/raw/refs/heads/master/labtainer/ac-midband-extract.tar
labtainer -r ac-midband-extract
```

Kiểm tra kết quả:

```bash
checkwork ac-midband-extract
```

### Lab 2: DC/AC Combined Extract

```bash
imodule https://github.com/Jaycelation/PTIT-Steganography-Project/raw/refs/heads/master/labtainer/dc-ac-combined-extract.tar
labtainer -r dc-ac-combined-extract
```

Kiểm tra kết quả:

```bash
checkwork dc-ac-combined-extract
```

### Lab 3: DC/AC Drift Extract

```bash
imodule https://github.com/Jaycelation/PTIT-Steganography-Project/raw/refs/heads/master/labtainer/dc-ac-drift-extract.tar
labtainer -r dc-ac-drift-extract
```

Kiểm tra kết quả:

```bash
checkwork dc-ac-drift-extract
```

Xem thêm hướng dẫn chạy trong VM tại [README_LABTAINER_VM.md](README_LABTAINER_VM.md).

## 3. Cấu Trúc Repo

```text
ac-coeff-midband/             Challenge nền cho lab AC.
dc-ac-combined/               Challenge nền cho lab DC/AC.
dc-coeff-warmup/              Challenge warmup về hệ số DC.
drift-compensation-basic/     Challenge mô phỏng drift compensation.
labtainer/                    Template, gói build và file .tar cho Labtainer.
scripts/                      Script build và kiểm tra package Labtainer.
videos/                       Video demo dùng cho phát triển/thử nghiệm.
```

Các file hướng dẫn chính:

```text
LAB_AC_MIDBAND_EXTRACT_GUIDE.md
LAB_DC_AC_COMBINED_EXTRACT_GUIDE.md
LAB_DC_AC_DRIFT_EXTRACT_GUIDE.md
README_LABTAINER_VM.md
LABTAINER_READINESS.md
LABTAINER_PROGRESS.md
```

## 4. Build Lại Package Labtainer

Chạy từ thư mục gốc của repo:

```powershell
python scripts\prepare_labtainer_public.py
python scripts\run_all_lab_checks.py
```

Script `prepare_labtainer_public.py` sẽ tạo lại:

```text
labtainer/build/ac-midband-extract/
labtainer/build/dc-ac-combined-extract/
labtainer/build/dc-ac-drift-extract/
labtainer/ac-midband-extract.tar
labtainer/dc-ac-combined-extract.tar
labtainer/dc-ac-drift-extract.tar
```

Script `run_all_lab_checks.py` chạy các helper script trong từng package và kiểm tra các file cần cho `checkwork`.

Có thể build hoặc kiểm tra từng lab riêng:

```powershell
python scripts\prepare_labtainer_public.py --lab ac-midband-extract
python scripts\run_all_lab_checks.py --lab ac-midband-extract
```

Các tên lab hợp lệ:

```text
ac-midband-extract
dc-ac-combined-extract
dc-ac-drift-extract
```

## 5. Challenge Nền

Ngoài 3 Labtainer lab chính, repo vẫn giữ các challenge nền để phát triển và kiểm thử thuật toán:

| Challenge | Trọng tâm |
|---|---|
| `dc-coeff-warmup` | Sửa hệ số DC. |
| `ac-coeff-midband` | Nhúng/trích xuất payload bằng hệ số AC trung tần. |
| `dc-ac-combined` | Header ở DC, payload ở AC. |
| `drift-compensation-basic` | Mô phỏng drift và cân bằng độ lệch. |

Ví dụ chạy nhanh một challenge nền:

```powershell
cd ac-coeff-midband
python generate.py --flag "PTIT{ac_midband_test}" --seed 1337 --output output
python solve.py --input output/stego.mp4 --config output/public_config.json --output output/answer.txt
python checker.py --answer-file output/answer.txt
```

## 6. Tách Nội Dung Student Và Instructor

Package student chỉ nên chứa:

- `solve.py`
- thư mục `src/`
- thư mục `tools/`
- video stego công khai trong `output/stego.mp4`
- cấu hình public như `output/public_config.json` và `output/hint.txt` nếu có

Package student không được chứa:

- `generate.py`
- `checker.py`
- `private/`
- `private_config.json`
- flag, answer key hoặc file đáp án mẫu
- cache Python như `__pycache__/` hoặc `.pyc`

Các script build hiện tại đã có bước loại bỏ những file này khỏi package public.

## 7. Ghi Chú

- Nếu cần hướng dẫn chi tiết cho sinh viên, dùng 3 file guide riêng ở mục 1.
- Nếu cần kiểm tra trạng thái đóng gói Labtainer, xem [LABTAINER_READINESS.md](LABTAINER_READINESS.md).
- Nếu cần ghi nhận tiến độ hoặc thay đổi gần đây, xem [LABTAINER_PROGRESS.md](LABTAINER_PROGRESS.md).
