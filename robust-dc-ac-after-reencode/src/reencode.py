from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def reencode_light(src: Path, dst: Path) -> str:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        shutil.copyfile(src, dst)
        return "copy-fallback-no-ffmpeg"
    cmd = [
        ffmpeg,
        "-y",
        "-i",
        str(src),
        "-c:v",
        "libx264",
        "-crf",
        "18",
        "-preset",
        "veryfast",
        "-pix_fmt",
        "yuv420p",
        str(dst),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return "ffmpeg-libx264-crf18"

