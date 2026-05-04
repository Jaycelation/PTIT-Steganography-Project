from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from .dct_utils import crop_to_blocks


def synthetic_video(width: int = 128, height: int = 96, frames: int = 40) -> list[np.ndarray]:
    yy, xx = np.mgrid[0:height, 0:width]
    out = []
    for i in range(frames):
        frame = 98 + 42 * np.sin((xx + i * 2) / 12.0) + 35 * np.cos((yy - i) / 10.0)
        frame[:, 48:80] += 20
        frame[16 + i % 16 : 42 + i % 16, 12 + i : 44 + i] += 38
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
        frames.append(crop_to_blocks(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)))
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

