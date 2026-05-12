# DC/AC Drift Extract

Recover a hidden message from a public stego MP4 while recording extraction metrics useful for reasoning about drift and reliability. This lab uses the same DC/AC extraction pipeline as the combined coefficient lab: DC coefficients provide synchronization/header data, and selected midband AC coefficients carry the payload.

## Files

- `output/stego.mp4`: public stego video.
- `output/public_config.json`: public extraction parameters.
- `solve.py`: reference extractor entry point.
- `src/`: DCT, video I/O, extraction, and metrics helpers.
- `tools/`: commands used by Labtainer checkwork.

## Required Commands

Run from this directory:

```bash
python3 tools/check_video_metadata.py
python3 tools/run_dc_ac_extract.py
python3 tools/report_metrics.py
```

The recovered answer and metrics are written under `work/` when you run the commands. Labtainer checkwork validates the answer hash and metrics marker.
