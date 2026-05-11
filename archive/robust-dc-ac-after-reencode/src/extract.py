from __future__ import annotations

from .dct_utils import block_dct, extract_parity
from .embed import AC_COEFFS, bits_to_bytes, positions


def majority_vote(bits: list[int], repeat: int) -> list[int]:
    voted = []
    for i in range(0, len(bits), repeat):
        group = bits[i : i + repeat]
        voted.append(1 if sum(group) >= (len(group) / 2) else 0)
    return voted


def extract_repeated_bits(frames, seed: int, bit_count: int, repeat: int, stream: str, step: float) -> list[int]:
    raw = []
    for fi, y, x, cy, cx in positions(frames, seed, bit_count * repeat, stream):
        coefs = block_dct(frames[fi][y : y + 8, x : x + 8])
        raw.append(extract_parity(float(coefs[cy, cx]), step))
    return majority_vote(raw, repeat)


def extract_message(frames, seed: int, byte_length: int, repeat: int, ac_step: float) -> str:
    bits = extract_repeated_bits(frames, seed, byte_length * 8, repeat, "ac", ac_step)
    return bits_to_bytes(bits).decode("utf-8", errors="replace")

