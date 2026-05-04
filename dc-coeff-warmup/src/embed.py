from __future__ import annotations

import random

import numpy as np

from .dct_utils import block_dct, block_idct, embed_parity, iter_block_coords


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


def dc_positions(frames: list[np.ndarray], seed: int, count: int) -> list[tuple[int, int, int]]:
    coords: list[tuple[int, int, int]] = []
    for fi, frame in enumerate(frames):
        for y, x in iter_block_coords(*frame.shape):
            coords.append((fi, y, x))
    rng = random.Random(seed)
    rng.shuffle(coords)
    if count > len(coords):
        raise ValueError(f"Payload needs {count} blocks, capacity is {len(coords)}")
    return coords[:count]


def embed_bits_dc(frames: list[np.ndarray], bits: list[int], seed: int, step: float = 96.0) -> list[np.ndarray]:
    stego = [f.copy() for f in frames]
    for bit, (fi, y, x) in zip(bits, dc_positions(frames, seed, len(bits))):
        coefs = block_dct(stego[fi][y : y + 8, x : x + 8])
        coefs[0, 0] = embed_parity(float(coefs[0, 0]), bit, step)
        stego[fi][y : y + 8, x : x + 8] = block_idct(coefs)
    return stego

