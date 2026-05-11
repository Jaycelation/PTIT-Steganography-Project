# Labtainer Build Prep

This directory contains a first-pass Labtainer scaffold for packaging the steganography challenges as a single-container lab.

The scaffold follows the common Labtainers layout:

```text
steg-video-labs/
  bin/
  config/
  dockerfiles/
  instr_config/
  steg/
    _bin/
```

Run the package script from the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File labtainer\build-labtainer-package.ps1
```

The script creates:

```text
labtainer/build/steg-video-labs/
```

Copy that generated `steg-video-labs` directory into the Labtainers `labs/` directory, then rebuild from `scripts/labtainers-student`:

```bash
rebuild steg-video-labs
labtainer steg-video-labs
```

Notes:

- The package intentionally excludes `private/`, `private_config.json`, `answer.txt`, `demo_color/`, `__pycache__/`, and generated build output.
- The Dockerfile installs `ffmpeg` so `robust-dc-ac-after-reencode` can exercise the intended re-encode path.
- Student work should happen from `/home/student/steg-video-labs`.
