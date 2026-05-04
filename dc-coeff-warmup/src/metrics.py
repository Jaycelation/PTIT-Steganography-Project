from __future__ import annotations

import math

import numpy as np


def mse(a: np.ndarray, b: np.ndarray) -> float:
    diff = a.astype(np.float32) - b.astype(np.float32)
    return float(np.mean(diff * diff))


def psnr(a: np.ndarray, b: np.ndarray) -> float:
    err = mse(a, b)
    if err == 0:
        return float("inf")
    return 20.0 * math.log10(255.0 / math.sqrt(err))


def average_metrics(original: list[np.ndarray], stego: list[np.ndarray]) -> dict[str, float]:
    mses = [mse(a, b) for a, b in zip(original, stego)]
    psnrs = [psnr(a, b) for a, b in zip(original, stego)]
    return {"mse": float(np.mean(mses)), "psnr": float(np.mean(psnrs))}

