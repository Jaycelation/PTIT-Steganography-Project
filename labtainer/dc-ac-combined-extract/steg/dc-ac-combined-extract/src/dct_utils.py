from __future__ import annotations

import cv2
import numpy as np

BLOCK = 8


def crop_to_blocks(frame: np.ndarray) -> np.ndarray:
    h, w = frame.shape[:2]
    return frame[: h - (h % BLOCK), : w - (w % BLOCK)]


def block_dct(block: np.ndarray) -> np.ndarray:
    return cv2.dct(block.astype(np.float32) - 128.0)


def block_idct(coefs: np.ndarray) -> np.ndarray:
    return np.clip(np.rint(cv2.idct(coefs) + 128.0), 0, 255).astype(np.uint8)


def iter_block_coords(height: int, width: int):
    for y in range(0, height - (height % BLOCK), BLOCK):
        for x in range(0, width - (width % BLOCK), BLOCK):
            yield y, x


def embed_parity(coef: float, bit: int, step: float) -> float:
    q = int(np.rint(coef / step))
    if (q & 1) == bit:
        return float(q * step)
    up = q + 1
    down = q - 1
    chosen = up if abs(up * step - coef) <= abs(down * step - coef) else down
    return float(chosen * step)


def extract_parity(coef: float, step: float) -> int:
    return int(np.rint(coef / step)) & 1

