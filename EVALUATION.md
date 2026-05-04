# Danh gia demo video

Nguon goc:

- File: `videos/Video_Demo1.mp4`
- Resolution: `1920x1080`
- Frames: `341`
- FPS: `25`
- Size: `13.16 MiB`

Demo hien tai nam trong thu muc `demo_color/` cua tung challenge va da duoc regenerate o dung resolution goc `1920x1080`.

## Tieu chi 1: Chat luong video tuong duong video goc

Ket luan: **Dat ve resolution, mau sac va do net tuong doi.**

- Resolution: dat, tat ca demo la `1920x1080`.
- Mau sac: dat, pipeline chi nhung tren kenh Y va giu Cr/Cb. Saturation delta trung binh khoang `1.68`.
- Do net: kha tot. Sharpness ratio so voi source goc khoang `0.975`.
- PSNR mau lay mau theo frame: khoang `34.87` den `34.89 dB`.

## Tieu chi 2: Dung luong video tuong duong video goc

Ket luan: **Chua dat neu bat buoc dung luong gan source.**

- Video goc: `13.16 MiB`.
- Demo full HD hien tai: khoang `30.45` den `30.68 MiB`.
- Ty le size: khoang `2.31x` den `2.33x` video goc.

Nguyen nhan: moi truong hien tai khong co `ffmpeg` CLI, va OpenCV H.264 tren may nay loi `openh264`, nen code dang ghi MP4 bang `mp4v`. Codec nay giu full HD kha on nhung nen kem hon H.264 cua video goc.

## Bang do nhanh

| Challenge | Resolution | Size vs source | PSNR mau | Saturation delta | Sharpness ratio |
|---|---:|---:|---:|---:|---:|
| `dc-coeff-warmup` | 1920x1080 | 231.46% | 34.89 dB | 1.68 | 0.975 |
| `ac-coeff-midband` | 1920x1080 | 231.45% | 34.89 dB | 1.68 | 0.975 |
| `dc-ac-combined` | 1920x1080 | 231.45% | 34.89 dB | 1.68 | 0.975 |
| `drift-compensation-basic` | 1920x1080 | 233.22% | 34.87 dB | 1.70 | 0.976 |
| `vlc-size-aware-embedding` | 1920x1080 | 231.45% | 34.89 dB | 1.68 | 0.975 |
| `robust-dc-ac-after-reencode` | 1920x1080 | 231.48% | 34.89 dB | 1.68 | 0.975 |

## Ket luan hien tai

- Neu uu tien do net/resolution: ban `demo_color/` hien tai la ban nen dung.
- Neu uu tien dung luong gan source: can bo sung `ffmpeg` hoac sua H.264/OpenH264 de encode full HD bang H.264/H.265 voi CRF/bitrate phu hop.
- Thu muc `output/` chi la synthetic acceptance output nho, khong phai demo chat luong cao.
