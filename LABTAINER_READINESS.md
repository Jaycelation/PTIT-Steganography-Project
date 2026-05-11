# Labtainer Readiness Review

Date: 2026-05-11

## Current State

The project contains six standalone video steganography challenges:

| Challenge | Status | Notes |
|---|---|---|
| `dc-coeff-warmup` | Ready with cleanup | Single-container friendly; public config includes seed and length. |
| `ac-coeff-midband` | Ready with cleanup | Has the only existing pytest tests. |
| `dc-ac-combined` | Ready with cleanup | Uses public config for solve path. |
| `drift-compensation-basic` | Ready with cleanup | Demonstrates compensated vs uncompensated embedding. |
| `vlc-size-aware-embedding` | Ready with cleanup | Conceptually the hardest; still a local model, not codec-level VLC editing. |
| `robust-dc-ac-after-reencode` | Environment-sensitive | Uses `ffmpeg` + `libx264` when available, otherwise copy fallback. Labtainer image should install `ffmpeg`. |

Verification performed:

- `python -m pytest tests -q` inside `ac-coeff-midband`: passed.
- Existing `output/answer.txt` passed each challenge checker.
- Root-level pytest currently fails because imports assume the working directory is the challenge directory.

## Main Risks Before Build

1. Generated artifacts are tracked in git.
   `output/`, `demo_color/`, `.pyc`, and private flags/answers are currently part of the repository history. These should not be included in the student Labtainer package.

2. Documentation encoding is inconsistent.
   Several Markdown files display Vietnamese text as mojibake. This does not block execution, but it should be fixed before release to students.

3. Lab execution assumes per-challenge working directory.
   `solve.py` and tests import `src` locally. Lab instructions and helper scripts should `cd` into each challenge before running commands.

4. Codec behavior depends on environment.
   The current host does not expose `ffmpeg` on PATH. For Labtainer, install `ffmpeg` in the image so the robust re-encode challenge runs as intended.

5. Challenge secrets need release separation.
   Student package should contain challenge code, public config, and stego media only. Instructor/private package should retain flags, checkers, and answer keys.

## Build Recommendation

Use one single-container Labtainer first:

- Lab name: `steg-video-labs`
- Container: `steg`
- User: `student`
- Base image: `labtainer.base`
- Packages: `python3`, `python3-pip`, `ffmpeg`, `libgl1`, `libglib2.0-0`
- Python packages: `numpy`, `opencv-python-headless`, `pytest`

This keeps the first build simple and avoids unnecessary network topology. Multi-container design is not needed unless the course later wants separate attacker/victim/media-server roles.

## Release Layout

Student-facing content:

- `README.md`
- `DEMO.md`
- `EVALUATION.md`
- each challenge `README.md`
- each challenge `src/`
- each challenge `solve.py`
- each challenge generated public artifacts:
  - `stego*.mp4`
  - `public_config.json`
  - `hint.txt` when present
  - `public/README.md` when present

Instructor-only content:

- `generate.py`
- `checker.py`
- `private/`
- `private_config.json`
- `answer.txt`
- demo flags and generated answer files

## Next Cleanup Items

- Remove tracked generated artifacts from git index in a separate cleanup commit.
- Regenerate Markdown files as UTF-8.
- Add root-level test runner that loops through challenges with the correct cwd.
- Decide whether Labtainer will include all six challenges or only the first three for an introductory lab.
