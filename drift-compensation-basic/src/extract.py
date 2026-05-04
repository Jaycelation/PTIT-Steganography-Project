from __future__ import annotations

from .dct_utils import block_dct, extract_parity
from .embed import bits_to_bytes, positions


def extract_message(frames, seed: int, byte_length: int, step: float = 80.0) -> str:
    bits = []
    for fi, y, x, cy, cx in positions(frames, seed, byte_length * 8):
        coefs = block_dct(frames[fi][y : y + 8, x : x + 8])
        local_step = step + 24.0 if (cy, cx) == (0, 0) else step
        bits.append(extract_parity(float(coefs[cy, cx]), local_step))
    return bits_to_bytes(bits).decode("utf-8", errors="replace")

