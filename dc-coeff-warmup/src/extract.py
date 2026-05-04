from __future__ import annotations

import numpy as np

from .dct_utils import block_dct, extract_parity
from .embed import bits_to_bytes, dc_positions


def extract_bits_dc(frames: list[np.ndarray], seed: int, bit_count: int, step: float = 96.0) -> list[int]:
    bits: list[int] = []
    for fi, y, x in dc_positions(frames, seed, bit_count):
        coefs = block_dct(frames[fi][y : y + 8, x : x + 8])
        bits.append(extract_parity(float(coefs[0, 0]), step))
    return bits


def extract_message_dc(frames: list[np.ndarray], seed: int, byte_length: int, step: float = 96.0) -> str:
    bits = extract_bits_dc(frames, seed, byte_length * 8, step)
    return bits_to_bytes(bits).decode("utf-8", errors="replace")

