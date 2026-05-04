# Demo voi `videos/Video_Demo1.mp4`

## TL;DR

Demo dung video that trong `videos/Video_Demo1.mp4`. Pipeline xu ly theo YCrCb:

- Chi nhung/extract tren kenh Y.
- Giu lai Cr/Cb de video stego van co mau.
- Mac dinh code khong downscale; `--max-width 0` nghia la giu kich thuoc goc.
- Demo mac dinh ben duoi dung `--max-width 1280` de can bang chat luong va RAM.

Neu muon giu nguyen 1920x1080, bo `--max-width 1280` hoac truyen `--max-width 0`. Luu y cac bai drift/robust co the ton RAM va chay lau hon.

## Lenh Demo HQ

### dc-coeff-warmup

```powershell
cd dc-coeff-warmup
python -B generate.py --input ../videos/Video_Demo1.mp4 --max-width 1280 --flag "PTIT{dc_demo_video}" --seed 1337 --output demo_color/
python -B solve.py --input demo_color/stego.mp4 --seed 1337 --length 19 --output demo_color/answer.txt
python -B checker.py --answer-file demo_color/answer.txt --expected-file demo_color/private/flag.txt
```

### ac-coeff-midband

```powershell
cd ac-coeff-midband
python -B generate.py --input ../videos/Video_Demo1.mp4 --max-width 1280 --flag "PTIT{ac_demo_video}" --seed 2026 --output demo_color/
python -B solve.py --input demo_color/stego.mp4 --config demo_color/public_config.json --output demo_color/answer.txt
python -B checker.py --answer-file demo_color/answer.txt --expected-file demo_color/private/flag.txt
```

### dc-ac-combined

```powershell
cd dc-ac-combined
python -B generate.py --input ../videos/Video_Demo1.mp4 --max-width 1280 --flag "PTIT{combo_demo}" --seed 2026 --output demo_color/
python -B solve.py --input demo_color/stego.mp4 --config demo_color/public_config.json --output demo_color/answer.txt
python -B checker.py --answer-file demo_color/answer.txt --expected-file demo_color/private/flag.txt
```

### drift-compensation-basic

```powershell
cd drift-compensation-basic
python -B generate.py --input ../videos/Video_Demo1.mp4 --max-width 1280 --flag "PTIT{drift_demo_video}" --seed 404 --output demo_color/
python -B solve.py --input demo_color/stego_comp.mp4 --seed 404 --output demo_color/answer.txt
python -B checker.py --answer-file demo_color/answer.txt --expected-file demo_color/private/flag.txt
```

### vlc-size-aware-embedding

```powershell
cd vlc-size-aware-embedding
python -B generate.py --input ../videos/Video_Demo1.mp4 --max-width 1280 --flag "PTIT{vlc_demo}" --seed 1337 --output demo_color/
python -B solve.py --input demo_color/stego.mp4 --seed 1337 --output demo_color/answer.txt
python -B checker.py --answer-file demo_color/answer.txt --expected-file demo_color/private/flag.txt
```

### robust-dc-ac-after-reencode

```powershell
cd robust-dc-ac-after-reencode
python -B generate.py --input ../videos/Video_Demo1.mp4 --max-width 1280 --flag "PTIT{robust_demo}" --seed 9001 --repeat 5 --output demo_color/
python -B solve.py --input demo_color/stego_reencoded.mp4 --seed 9001 --repeat 5 --output demo_color/answer.txt
python -B checker.py --answer-file demo_color/answer.txt --expected-file demo_color/private/flag.txt
```

## Ghi chu

- Day van la mo phong frame-DCT local, khong phai sua bitstream MPEG codec-level.
- Neu may co `ffmpeg`, bai robust se re-encode bang libx264 CRF 18; neu khong co, script dung copy fallback de demo van chay.
- Output demo nam trong thu muc `demo_color/` cua tung challenge.
