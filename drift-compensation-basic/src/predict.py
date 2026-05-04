from __future__ import annotations

import numpy as np


def predict_from_previous(frames: list[np.ndarray]) -> list[np.ndarray]:
    predicted = [frames[0].copy()]
    for i in range(1, len(frames)):
        predicted.append(frames[i - 1].copy())
    return predicted

