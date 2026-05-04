from __future__ import annotations

import random

import numpy as np

from .dct_utils import block_dct, block_idct, embed_parity, iter_block_coords

DEFAULT_COEFFS = [(2, 3), (3, 2), (4, 1)]


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


def ac_positions(
    frames: list[np.ndarray],
    seed: int,
    count: int,
    coeffs: list[tuple[int, int]] = DEFAULT_COEFFS,
) -> list[tuple[int, int, int, int, int]]:
    coords: list[tuple[int, int, int, int, int]] = []
    for fi, frame in enumerate(frames):
        for y, x in iter_block_coords(*frame.shape):
            for cy, cx in coeffs:
                coords.append((fi, y, x, cy, cx))
    rng = random.Random(seed)
    rng.shuffle(coords)
    if count > len(coords):
        raise ValueError(f"Payload needs {count} coefficients, capacity is {len(coords)}")
    return coords[:count]


def embed_bits_ac(
    frames: list[np.ndarray],
    bits: list[int],
    seed: int,
    coeffs: list[tuple[int, int]] = DEFAULT_COEFFS,
    step: float = 64.0,
) -> list[np.ndarray]:
    stego = [f.copy() for f in frames]
    for bit, (fi, y, x, cy, cx) in zip(bits, ac_positions(frames, seed, len(bits), coeffs)):
        coefs = block_dct(stego[fi][y : y + 8, x : x + 8])
        coefs[cy, cx] = embed_parity(float(coefs[cy, cx]), bit, step)
        stego[fi][y : y + 8, x : x + 8] = block_idct(coefs)
    return stego

