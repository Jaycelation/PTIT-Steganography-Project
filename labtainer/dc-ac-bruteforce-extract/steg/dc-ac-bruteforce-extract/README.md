# DC/AC Brute Force Extract

This Labtainer lab asks you to recover a hidden message from a stego video when
the public config intentionally omits the true embedding seed and active AC
coefficient profile.

The lab is a frame-DCT steganography simulation. It is not a codec exploit and
does not require changing MPEG/H.264/H.265 bitstreams.

## Files

- `output/stego.mp4`: public stego video.
- `output/public_config.json`: bounded search ranges and public extraction data.
- `tools/`: helper commands used by Labtainer checkwork.
- `work/`: output files created while solving the lab.

## Required Commands

```bash
python3 tools/check_video_metadata.py
python3 tools/audit_public_config.py
python3 tools/build_candidate_space.py
python3 tools/probe_dc_sync.py
python3 tools/run_bruteforce.py
python3 tools/run_bruteforce_extract.py
```

Optional:

```bash
python3 tools/report_metrics.py
```

Labtainer checkwork validates the seven required artifacts under `work/`.
