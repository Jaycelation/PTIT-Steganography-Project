# Labtainer Conversion Checklist

Date: 2026-05-11

## Scope

First Labtainer-ready lab: `dc-ac-drift-extract`

Topic: coefficient-domain video steganography using DC/AC coefficient modification, with drift-compensation context and a TODO for the full `drift-compensation-basic` conversion.

## Repository Review

- [x] Inspected repository tree.
- [x] Identified six standalone challenges and narrowed the main scope to four core challenges.
- [x] Read root `README.md`.
- [x] Read `LABTAINER_READINESS.md`.
- [x] Read `DEMO.md`.
- [x] Read `EVALUATION.md`.
- [x] Verified `dc-ac-combined` has `README.md`, `generate.py`, `solve.py`, `checker.py`, `src/`, `requirements.txt`, and public `output/`.
- [x] Verified `drift-compensation-basic` has the same challenge structure.

## Student/Instructor Separation

- [x] Student package includes root docs, challenge `README.md`, `solve.py`, `src/`, and public artifacts.
- [x] Student package excludes `generate.py`.
- [x] Student package excludes `checker.py`.
- [x] Student package excludes `private/`.
- [x] Student package excludes `private_config.json`.
- [x] Student package excludes `answer.txt`.
- [x] Student package excludes Python cache files.

## First Lab Implementation

- [x] Created Labtainer template for `dc-ac-drift-extract`.
- [x] Added single-container `start.config` using container `steg` and user `student`.
- [x] Added Dockerfile based on `labtainer.base`.
- [x] Added OS package dependencies: `python3`, `python3-pip`, `ffmpeg`, `libgl1`, `libglib2.0-0`.
- [x] Added Python dependencies: `numpy`, `opencv-python-headless`, `pytest`.
- [x] Added student instructions.
- [x] Added instructor notes.
- [x] Added reusable package script: `scripts/prepare_labtainer_public.py`.
- [x] Added local verification script: `scripts/run_all_lab_checks.py`.

## Additional Labtainer Labs

- [x] Created `dc-ac-combined-extract` from `dc-ac-combined`.
- [x] Created `ac-midband-extract` from `ac-coeff-midband`.
- [x] Reused file-based marker/checkwork pattern from `dc-ac-drift-extract`.
- [x] Kept each lab independent with its own config, Dockerfile, instructions, tools, and instructor notes.

## Checkwork Items

- [x] `video_metadata_checked`: checks `work/video_metadata.txt` for `VIDEO_METADATA_OK`.
- [x] `dc_ac_extractor_ran`: checks `work/extract.log` for `DC_AC_EXTRACT_OK`.
- [x] `answer_file_created`: checks `work/answer_status.txt` for `ANSWER_FILE_CREATED`.
- [x] `flag_recovered`: checks `work/answer.sha256` for the instructor-only expected hash.
- [x] `metrics_reported`: checks `work/metrics.json` for `METRICS_OK`.

## New Lab Checkwork

`dc-ac-combined-extract`:

- [x] `video_metadata_checked`
- [x] `dc_header_checked`
- [x] `ac_payload_extracted`
- [x] `answer_file_created`
- [x] `flag_recovered`

`ac-midband-extract`:

- [x] `video_metadata_checked`
- [x] `ac_config_checked`
- [x] `ac_extractor_ran`
- [x] `answer_file_created`
- [x] `flag_recovered`

## Verification

- [x] Existing challenge pytest verified where present.
- [x] Student solve path verified from generated package.
- [x] Checkwork helper path verified from generated package.
- [x] Confirmed generated student package does not include private files.
- [ ] Build with real Labtainers `rebuild dc-ac-drift-extract`.
- [ ] Run inside a Labtainers VM/container.

## Remaining TODOs

- [ ] Convert `drift-compensation-basic` into a full second lab with actual drift comparison goals.
- [ ] Convert `dc-coeff-warmup` as an introductory lab.
- [ ] Convert `ac-coeff-midband` as the midband AC lab.
- [x] Move advanced modules out of main scope.
- [x] Keep archived advanced challenges out of Labtainer student packages.
- [ ] Fix mojibake in existing Vietnamese Markdown files.
- [ ] Remove already tracked generated outputs and private artifacts from git index in a cleanup commit.
