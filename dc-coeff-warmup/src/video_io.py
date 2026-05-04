from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from .dct_utils import crop_to_blocks


MAX_READ_WIDTH = 320


def normalize_bgr(frame: np.ndarray, max_width: int = MAX_READ_WIDTH) -> np.ndarray:
    h, w = frame.shape[:2]
    if w > max_width:
        new_h = max(8, int(round(h * (max_width / w))))
        frame = cv2.resize(frame, (max_width, new_h), interpolation=cv2.INTER_AREA)
    return crop_to_blocks(frame)


def split_y_chroma(frame: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    ycrcb = cv2.cvtColor(normalize_bgr(frame), cv2.COLOR_BGR2YCrCb)
    return ycrcb[:, :, 0].copy(), ycrcb[:, :, 1:3].copy()


def normalize_gray(frame: np.ndarray, max_width: int = MAX_READ_WIDTH) -> np.ndarray:
    y, _ = split_y_chroma(frame)
    return y


def synthetic_video(width: int = 128, height: int = 96, frames: int = 36) -> list[np.ndarray]:
    out = []
    yy, xx = np.mgrid[0:height, 0:width]
    base = ((xx * 1.7 + yy * 1.1) % 80 + 70).astype(np.float32)
    for i in range(frames):
        frame = base.copy()
        x0 = 8 + (i * 3) % (width - 40)
        y0 = 12 + (i * 2) % (height - 36)
        frame[y0 : y0 + 24, x0 : x0 + 32] += 62
        frame[(yy - (30 + i % 18)) ** 2 + (xx - (80 - i % 30)) ** 2 < 13**2] -= 35
        out.append(crop_to_blocks(np.clip(frame, 0, 255).astype(np.uint8)))
    return out


def read_gray_video(path: str | Path) -> tuple[list[np.ndarray], float]:
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise ValueError(f"Cannot open video: {path}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 12.0
    frames: list[np.ndarray] = []
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        y, _ = split_y_chroma(frame)
        frames.append(y)
    cap.release()
    if not frames:
        raise ValueError(f"No frames read from: {path}")
    return frames, float(fps)


def read_y_video(path: str | Path) -> tuple[list[np.ndarray], float, list[np.ndarray]]:
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise ValueError(f"Cannot open video: {path}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 12.0
    frames: list[np.ndarray] = []
    chroma: list[np.ndarray] = []
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        y, crcb = split_y_chroma(frame)
        frames.append(y)
        chroma.append(crcb)
    cap.release()
    if not frames:
        raise ValueError(f"No frames read from: {path}")
    return frames, float(fps), chroma


def write_y_video(
    path: str | Path,
    frames: list[np.ndarray],
    fps: float = 12.0,
    chroma_frames: list[np.ndarray] | None = None,
) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    h, w = frames[0].shape
    writer = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h), True)
    if not writer.isOpened():
        raise ValueError(f"Cannot create video: {path}")
    for i, y in enumerate(frames):
        if chroma_frames is None:
            bgr = cv2.cvtColor(y, cv2.COLOR_GRAY2BGR)
        else:
            ycrcb = np.dstack([y, chroma_frames[i]])
            bgr = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)
        writer.write(bgr)
    writer.release()


def write_gray_video(path: str | Path, frames: list[np.ndarray], fps: float = 12.0) -> None:
    write_y_video(path, frames, fps)
