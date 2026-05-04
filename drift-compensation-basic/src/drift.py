from __future__ import annotations

import numpy as np

from .predict import predict_from_previous


def drift_residuals(frames: list[np.ndarray]) -> list[np.ndarray]:
    predicted = predict_from_previous(frames)
    return [a.astype(np.float32) - p.astype(np.float32) for a, p in zip(frames, predicted)]


def apply_compensation_base(frames: list[np.ndarray], strength: float = 0.05) -> list[np.ndarray]:
    residuals = drift_residuals(frames)
    compensated = []
    for frame, residual in zip(frames, residuals):
        comp = frame.astype(np.float32) + strength * residual
        compensated.append(np.clip(np.rint(comp), 0, 255).astype(np.uint8))
    return compensated


def simulate_uncompensated_drift(original: list[np.ndarray], stego: list[np.ndarray], strength: float = 1.50) -> list[np.ndarray]:
    out = [stego[0].copy()]
    for i in range(1, len(stego)):
        drift = out[i - 1].astype(np.float32) - original[i - 1].astype(np.float32)
        frame = stego[i].astype(np.float32) + strength * drift
        out.append(np.clip(np.rint(frame), 0, 255).astype(np.uint8))
    return out
