# DC/AC Combined Extract

Recover a hidden message from a public stego MP4. DC coefficients carry a recognizable header, and selected midband AC coefficients carry the payload. This is a local frame-DCT teaching lab, not codec bitstream editing.

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
python3 tools/check_dc_header.py
python3 tools/run_dc_ac_extract.py
```

Optional metrics:

```bash
python3 tools/report_metrics.py
```

The recovered answer is written under `work/` when you run the commands. Labtainer checkwork validates the answer hash.
