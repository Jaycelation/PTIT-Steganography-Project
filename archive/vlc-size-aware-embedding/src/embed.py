from __future__ import annotations

import random

import numpy as np

from .dct_utils import block_dct, block_idct, extract_parity, iter_block_coords, parity_candidate
from .vlc_model import estimated_vlc_size


def bytes_to_bits(data: bytes) -> list[int]:
    return [(byte >> shift) & 1 for byte in data for shift in range(7, -1, -1)]


def bits_to_bytes(bits: list[int]) -> bytes:
    out = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for bit in bits[i : i + 8]:
            byte = (byte << 1) | int(bit)
        out.append(byte)
    return bytes(out)


def positions(frames: list[np.ndarray], seed: int):
    coords = []
    for fi, frame in enumerate(frames):
        for y, x in iter_block_coords(*frame.shape):
            coords.append((fi, y, x, 0, 0))
    rng = random.Random(seed)
    rng.shuffle(coords)
    return coords


def embed_size_aware(frames: list[np.ndarray], bits: list[int], seed: int, step: float = 160.0) -> tuple[list[np.ndarray], list[int]]:
    stego = [f.copy() for f in frames]
    used_indices: list[int] = []
    all_positions = positions(frames, seed)
    bit_index = 0
    for pos_index, (fi, y, x, cy, cx) in enumerate(all_positions):
        if bit_index == len(bits):
            return stego, used_indices
        bit = bits[bit_index]
        coefs = block_dct(stego[fi][y : y + 8, x : x + 8])
        old = float(coefs[cy, cx])
        new = parity_candidate(old, bit, step)
        if estimated_vlc_size(new) > estimated_vlc_size(old):
            new = old if extract_parity(old, step) == bit else -old
            if extract_parity(new, step) != bit or estimated_vlc_size(new) > estimated_vlc_size(old):
                continue
        coefs[cy, cx] = new
        stego[fi][y : y + 8, x : x + 8] = block_idct(coefs)
        used_indices.append(pos_index)
        bit_index += 1
    raise ValueError("Not enough size-aware coefficients for payload")
