# Danh gia demo video

Nguon goc:

- File: `videos/Video_Demo1.mp4`
- Resolution: `1920x1080`
- Frames: `341`
- FPS: `25`
- Size: `13.16 MiB`

Demo hien tai duoc sinh trong thu muc `demo_color/` cua tung challenge voi `--max-width 1280`.

## Tieu chi 1: Chat luong video tuong duong video goc

Ket luan: **Dat mot phan, chua dat neu yeu cau giu nguyen do net 1920x1080.**

Ly do:

- Mau sac: dat. Demo giu Cr/Cb va chi nhung tren kenh Y, sai khac saturation trung binh chi khoang `1.83`.
- Do net noi bo o ban 1280x720: kha tot. Sharpness ratio so voi source resize ve 1280x720 khoang `0.974`.
- Do net so voi video goc 1920x1080: chua dat nghiem ngat, vi demo hien tai la `1280x720`, chi bang `44.44%` so pixel cua source.

## Tieu chi 2: Dung luong video tuong duong video goc

Ket luan: **Dat.**

Dung luong cac file stego nam trong khoang `90.99%` den `91.67%` so voi file goc.

## Bang do nhanh

| Challenge | Resolution | Size vs source | PSNR mau | Saturation delta | Sharpness ratio |
|---|---:|---:|---:|---:|---:|
| `dc-coeff-warmup` | 1280x720 | 90.997% | 34.55 dB | 1.83 | 0.974 |
| `ac-coeff-midband` | 1280x720 | 90.997% | 34.55 dB | 1.83 | 0.974 |
| `dc-ac-combined` | 1280x720 | 90.997% | 34.55 dB | 1.83 | 0.974 |
| `drift-compensation-basic` | 1280x720 | 91.668% | 34.53 dB | 1.85 | 0.975 |
| `vlc-size-aware-embedding` | 1280x720 | 90.997% | 34.55 dB | 1.83 | 0.974 |
| `robust-dc-ac-after-reencode` | 1280x720 | 91.029% | 34.55 dB | 1.83 | 0.974 |

## Nhan xet ky thuat

Neu giu full resolution 1920x1080 bang OpenCV `mp4v`, chat luong hinh anh tot hon nhung dung luong tang manh. Test nhanh voi `dc-coeff-warmup` cho file khoang `31.9 MiB`, bang hon `2.3x` source, nen khong dat tieu chi dung luong tuong duong.

De dat dong thoi 2 tieu chi:

- Can encoder H.264/H.265 co dieu khien CRF/bitrate, uu tien `ffmpeg`.
- Moi truong hien tai khong co `ffmpeg` CLI.
- OpenCV H.264 tren may nay bao loi `openh264`, nen chua dung duoc cho encode full HD dung luong gan goc.

## Ket luan hien tai

- Ban demo `demo_color/` la ban tot nhat hien tai voi tool san co: mau tot, dung luong gan goc, extract PASS.
- Neu bat buoc chat luong/size deu gan video goc 1920x1080, can bo sung `ffmpeg` hoac sua moi truong H.264.
