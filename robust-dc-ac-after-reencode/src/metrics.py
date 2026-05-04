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
    avg_mse = float(np.mean([mse(x, y) for x, y in zip(a, b)]))
    avg_psnr = float("inf") if avg_mse == 0 else 20.0 * math.log10(255.0 / math.sqrt(avg_mse))
    return {"mse": avg_mse, "psnr": avg_psnr}


def bit_error_rate(expected: list[int], actual: list[int]) -> float:
    if not expected:
        return 0.0
    return sum(int(a != b) for a, b in zip(expected, actual)) / len(expected)
