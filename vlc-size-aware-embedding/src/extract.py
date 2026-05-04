from __future__ import annotations

from .dct_utils import block_dct, extract_parity
from .embed import bits_to_bytes, positions


def extract_message(frames, seed: int, byte_length: int, step: float = 160.0, used_indices: list[int] | None = None) -> str:
    bits = []
    all_positions = positions(frames, seed)
    selected = [all_positions[i] for i in used_indices] if used_indices is not None else all_positions
    for fi, y, x, cy, cx in selected:
        coefs = block_dct(frames[fi][y : y + 8, x : x + 8])
        bits.append(extract_parity(float(coefs[cy, cx]), step))
        if len(bits) == byte_length * 8:
            break
    return bits_to_bytes(bits).decode("utf-8", errors="replace")
