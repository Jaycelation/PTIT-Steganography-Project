from __future__ import annotations

import numpy as np

from .dct_utils import block_dct, extract_parity
from .embed import DEFAULT_COEFFS, ac_positions, bits_to_bytes


def extract_bits_ac(
    frames: list[np.ndarray],
    seed: int,
    bit_count: int,
    coeffs: list[tuple[int, int]] = DEFAULT_COEFFS,
    step: float = 64.0,
) -> list[int]:
    bits = []
    for fi, y, x, cy, cx in ac_positions(frames, seed, bit_count, coeffs):
        coefs = block_dct(frames[fi][y : y + 8, x : x + 8])
        bits.append(extract_parity(float(coefs[cy, cx]), step))
    return bits


def extract_message_ac(
    frames: list[np.ndarray],
    seed: int,
    byte_length: int,
    coeffs: list[tuple[int, int]] = DEFAULT_COEFFS,
    step: float = 64.0,
) -> str:
    bits = extract_bits_ac(frames, seed, byte_length * 8, coeffs, step)
    return bits_to_bytes(bits).decode("utf-8", errors="replace")

