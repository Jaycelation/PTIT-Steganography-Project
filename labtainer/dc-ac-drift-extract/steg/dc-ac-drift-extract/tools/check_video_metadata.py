#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import cv2


def inspect_video(path: Path) -> dict[str, float | int]:
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise SystemExit(f"Cannot open video: {path}")
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = float(cap.get(cv2.CAP_PROP_FPS) or 0.0)
    cap.release()
    if width <= 0 or height <= 0 or frames <= 0:
        raise SystemExit(f"Invalid video metadata read from: {path}")
    return {"width": width, "height": height, "frames": frames, "fps": fps}


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect the public stego video and write a stable checkwork marker.")
    parser.add_argument("--input", default="output/stego.mp4")
    parser.add_argument("--output", default="work/video_metadata.txt")
    args = parser.parse_args()

    metadata = inspect_video(Path(args.input))
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "VIDEO_METADATA_OK",
        f"width={metadata['width']}",
        f"height={metadata['height']}",
        f"frames={metadata['frames']}",
        f"fps={metadata['fps']:.3f}",
    ]
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("VIDEO_METADATA_OK")


if __name__ == "__main__":
    main()
