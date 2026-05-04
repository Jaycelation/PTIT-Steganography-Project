from __future__ import annotations

import math

import numpy as np


def mse(a: np.ndarray, b: np.ndarray) -> float:
    d = a.astype(np.float32) - b.astype(np.float32)
    return float(np.mean(d * d))


def psnr(a: np.ndarray, b: np.ndarray) -> float:
    err = mse(a, b)
    return float("inf") if err == 0 else 20.0 * math.log10(255.0 / math.sqrt(err))


def average_metrics(a: list[np.ndarray], b: list[np.ndarray]) -> dict[str, float]:
    return {"mse": float(np.mean([mse(x, y) for x, y in zip(a, b)])), "psnr": float(np.mean([psnr(x, y) for x, y in zip(a, b)]))}

