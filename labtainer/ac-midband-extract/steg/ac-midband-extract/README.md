# AC Midband Extract

Recover a hidden message from a public stego MP4. The payload is embedded in selected midband AC coefficients from 8x8 DCT blocks. This is a local frame-DCT teaching lab, not codec bitstream editing.

## Files

- `output/stego.mp4`: public stego video.
- `output/public_config.json`: public extraction parameters.
- `output/hint.txt`: public hint.
- `solve.py`: reference extractor entry point.
- `src/`: DCT, video I/O, extraction, and metrics helpers.
- `tools/`: commands used by Labtainer checkwork.

## Required Commands

Run from this directory:

```bash
python3 tools/check_video_metadata.py
python3 tools/check_ac_config.py
python3 tools/run_ac_extract.py
```

Optional metrics:

```bash
python3 tools/report_metrics.py
```

The recovered answer is written under `work/` when you run the commands. Labtainer checkwork validates the answer hash.
