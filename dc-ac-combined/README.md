# dc-ac-combined

## TL;DR

Challenge kết hợp DC và AC: DC chứa magic/header `STEG`, AC trung tần chứa flag. Đây là mô phỏng frame-DCT local.

## Mục tiêu học tập

- Dùng DC cho sync/header dễ phát hiện.
- Dùng AC trung tần cho payload chính.
- Hiểu cách seed quyết định thứ tự frame/block/coefficient.

## Public

- `output/stego.mp4`
- `output/public_config.json`

## Private

- `output/private_config.json`
- `output/private/flag.txt`

## Lệnh chạy

```powershell
python generate.py --flag "PTIT{dc_ac_combo}" --seed 2026 --output output/
python solve.py --input output/stego.mp4 --config output/public_config.json --output output/answer.txt
python checker.py --answer-file output/answer.txt
```

