from __future__ import annotations

import numpy as np

from .dct_utils import block_dct, extract_parity
from .embed import AC_COEFFS, bits_to_bytes, positions


def extract_stream(frames: list[np.ndarray], seed: int, byte_length: int, stream: str, step: float, coeffs: list[tuple[int, int]] = AC_COEFFS) -> str:
    bits = []
    for fi, y, x, cy, cx in positions(frames, seed, byte_length * 8, stream, coeffs):
        coefs = block_dct(frames[fi][y : y + 8, x : x + 8])
        bits.append(extract_parity(float(coefs[cy, cx]), step))
    return bits_to_bytes(bits).decode("utf-8", errors="replace")


def extract_flag(frames: list[np.ndarray], seed: int, flag_length: int, dc_step: float, ac_step: float, coeffs: list[tuple[int, int]] = AC_COEFFS) -> tuple[str, str]:
    magic = extract_stream(frames, seed, 4, "dc", dc_step)
    flag = extract_stream(frames, seed, flag_length, "ac", ac_step, coeffs)
    return magic, flag

