from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from .dct_utils import crop_to_blocks


MAX_READ_WIDTH = 320


def normalize_gray(frame: np.ndarray, max_width: int = MAX_READ_WIDTH) -> np.ndarray:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    if w > max_width:
        new_h = max(8, int(round(h * (max_width / w))))
        gray = cv2.resize(gray, (max_width, new_h), interpolation=cv2.INTER_AREA)
    return crop_to_blocks(gray)


def synthetic_video(width: int = 160, height: int = 112, frames: int = 64) -> list[np.ndarray]:
    yy, xx = np.mgrid[0:height, 0:width]
    out = []
    for i in range(frames):
        frame = 115 + 28 * np.sin((xx + i * 3) / 15.0) + 24 * np.cos((yy - i * 2) / 12.0)
        x0 = 10 + (i * 2) % (width - 50)
        y0 = 18 + (i * 2) % (height - 42)
        frame[y0 : y0 + 30, x0 : x0 + 40] += 44
        out.append(crop_to_blocks(np.clip(frame, 0, 255).astype(np.uint8)))
    return out


def read_gray_video(path: str | Path) -> tuple[list[np.ndarray], float]:
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise ValueError(f"Cannot open video: {path}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 12.0
    frames = []
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        frames.append(normalize_gray(frame))
    cap.release()
    if not frames:
        raise ValueError(f"No frames read from: {path}")
    return frames, float(fps)


def write_gray_video(path: str | Path, frames: list[np.ndarray], fps: float = 12.0) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    h, w = frames[0].shape
    writer = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h), True)
    if not writer.isOpened():
        raise ValueError(f"Cannot create video: {path}")
    for frame in frames:
        writer.write(cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR))
    writer.release()
