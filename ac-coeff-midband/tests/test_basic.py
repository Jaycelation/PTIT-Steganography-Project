from src.embed import bits_to_bytes, bytes_to_bits
from src.metrics import psnr
from src.video_io import synthetic_video


def test_bit_roundtrip():
    payload = b"PTIT{unit}"
    assert bits_to_bytes(bytes_to_bits(payload)) == payload


def test_synthetic_video_shape_and_psnr():
    frames = synthetic_video()
    assert frames[0].shape == (96, 128)
    assert psnr(frames[0], frames[0]) == float("inf")

