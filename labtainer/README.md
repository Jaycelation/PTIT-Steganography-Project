# Labtainer Build Prep

This directory contains Labtainer scaffolds for packaging the core DC/AC and drift-compensation steganography challenges as safe, single-container educational labs.

The current primary first-pass lab is:

```text
dc-ac-drift-extract
```

It is based on `dc-ac-combined`, adds drift-compensation context, and has five deterministic checkwork items.

Additional independent Labtainer-ready labs:

- `dc-ac-combined-extract`: Tách tin trong video miền hệ số bằng kết hợp hệ số DC và AC.
- `ac-midband-extract`: Tách tin trong video miền hệ số bằng hệ số AC.
- `dc-ac-bruteforce-extract`: Brute-force seed và profile hệ số AC bị ẩn để khôi phục payload DC/AC.

## Build `dc-ac-drift-extract`

Run from the repository root:

```bash
python scripts/prepare_labtainer_public.py
python scripts/run_all_lab_checks.py
```

See `../README_LABTAINER_VM.md` for Labtainer VM import commands and DockerHub image build commands for the extract labs.

The script creates:

```text
labtainer/build/dc-ac-drift-extract/
labtainer/build/dc-ac-combined-extract/
labtainer/build/ac-midband-extract/
labtainer/build/dc-ac-bruteforce-extract/
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

## Legacy Core-Challenge Scaffold

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

This package includes only the four core challenges:

- `dc-coeff-warmup`
- `ac-coeff-midband`
- `dc-ac-combined`
- `drift-compensation-basic`

Copy that generated `steg-video-labs` directory into the Labtainers `labs/` directory, then rebuild from `scripts/labtainers-student`:

```bash
rebuild steg-video-labs
labtainer steg-video-labs
```

Notes:

- The package intentionally excludes `private/`, `private_config.json`, `answer.txt`, `demo_color/`, `__pycache__/`, and generated build output.
- Archived advanced modules are not copied into student packages.
- Student work should happen from `/home/student/steg-video-labs`.
