# robust-dc-ac-after-reencode

## TL;DR

Challenge giấu flag bằng DC+AC có repetition, sau đó video bị re-encode nhẹ. Solver extract nhiều candidate và majority vote để khôi phục flag.

## Mục tiêu học tập

- Dùng DC làm sync/header.
- Dùng AC làm payload.
- Lặp mỗi bit `N` lần để tăng bền vững.
- Extract sau re-encode bằng majority vote.

## Lệnh chạy

```powershell
python generate.py --flag "PTIT{robust_dc_ac}" --seed 9001 --repeat 5 --output output/
python solve.py --input output/stego_reencoded.mp4 --seed 9001 --repeat 5 --output output/answer.txt
python checker.py --answer-file output/answer.txt
```

