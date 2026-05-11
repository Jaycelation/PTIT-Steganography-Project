# Labtainer Build Prep

This directory contains Labtainer scaffolds for packaging the steganography challenges as safe, single-container educational labs.

The current primary first-pass lab is:

```text
dc-ac-drift-extract
```

It is based on `dc-ac-combined`, adds drift-compensation context, and has five deterministic checkwork items.

## Build `dc-ac-drift-extract`

Run from the repository root:

```bash
python scripts/prepare_labtainer_public.py
python scripts/run_all_lab_checks.py
```

The script creates:

```text
labtainer/build/dc-ac-drift-extract/
```

Copy that generated `dc-ac-drift-extract` directory into the Labtainers `labs/` directory, then rebuild from `scripts/labtainers-student`:

```bash
rebuild dc-ac-drift-extract
labtainer dc-ac-drift-extract
```

Student work happens from:

```text
/home/student/dc-ac-drift-extract
```

## Legacy All-Challenge Scaffold

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
