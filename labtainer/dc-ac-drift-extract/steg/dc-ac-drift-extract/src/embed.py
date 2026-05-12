from __future__ import annotations

import random

import numpy as np

from .dct_utils import block_dct, block_idct, embed_parity, iter_block_coords

MAGIC = "STEG"
AC_COEFFS = [(2, 3), (3, 2), (4, 1)]


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


def positions(frames: list[np.ndarray], seed: int, count: int, stream: str, coeffs: list[tuple[int, int]] = AC_COEFFS):
    coords = []
    for fi, frame in enumerate(frames):
        for y, x in iter_block_coords(*frame.shape):
            if stream == "dc":
                coords.append((fi, y, x, 0, 0))
            else:
                for cy, cx in coeffs:
                    coords.append((fi, y, x, cy, cx))
    rng = random.Random(f"{seed}:{stream}")
    rng.shuffle(coords)
    if count > len(coords):
        raise ValueError(f"{stream} payload needs {count}, capacity is {len(coords)}")
    return coords[:count]


def embed_stream(frames: list[np.ndarray], bits: list[int], seed: int, stream: str, step: float, coeffs: list[tuple[int, int]] = AC_COEFFS) -> list[np.ndarray]:
    stego = [f.copy() for f in frames]
    for bit, (fi, y, x, cy, cx) in zip(bits, positions(frames, seed, len(bits), stream, coeffs)):
        coefs = block_dct(stego[fi][y : y + 8, x : x + 8])
        coefs[cy, cx] = embed_parity(float(coefs[cy, cx]), bit, step)
        stego[fi][y : y + 8, x : x + 8] = block_idct(coefs)
    return stego


def embed_combined(frames: list[np.ndarray], flag: str, seed: int, dc_step: float = 96.0, ac_step: float = 64.0) -> list[np.ndarray]:
    stego = embed_stream(frames, bytes_to_bits(MAGIC.encode()), seed, "dc", dc_step)
    return embed_stream(stego, bytes_to_bits(flag.encode()), seed, "ac", ac_step, AC_COEFFS)

