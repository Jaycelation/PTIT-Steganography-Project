# Labtainer Readiness Review

Date: 2026-05-12

## Scope Chính

Đề tài được thu hẹp theo đúng hướng:

> Giấu tin trong video miền hệ số bằng kỹ thuật sửa đổi hệ số DC và AC với hệ số cân bằng độ lệch (4.3).

Chỉ giữ các challenge liên quan trực tiếp đến DC, AC, DC+AC và drift compensation:

| Challenge | Status | Notes |
|---|---|---|
| `dc-coeff-warmup` | Ready with cleanup | Warmup cho sửa hệ số DC. |
| `ac-coeff-midband` | Ready with cleanup | Nhúng payload vào hệ số AC trung tần. |
| `dc-ac-combined` | Ready with cleanup | Header ở DC, payload ở AC. |
| `drift-compensation-basic` | Ready with cleanup | Mô phỏng drift và cân bằng độ lệch. |
| `dc-ac-drift-extract` | Labtainer-ready first pass | Lab chính dựa trên `dc-ac-combined`, có context drift và checkwork ổn định. |

## Verification Performed

- Existing pytest inside `ac-coeff-midband`: passed.
- `dc-ac-drift-extract` package path verified with:
  - `tools/check_video_metadata.py`
  - `tools/run_dc_ac_extract.py`
  - `tools/report_metrics.py`
- Student package scan confirms no private/generate/checker/source answer files.

## Main Risks Before Final Release

1. Generated artifacts are tracked in git history.
   `output/`, `demo_color/`, `.pyc`, and private flags/answers should not be included in the final student release.

2. Some original generated demo artifacts are large.
   Labtainer student package should keep only the small public artifacts needed for the lab.

3. Lab execution assumes per-challenge working directory.
   Keep wrapper scripts so students run from `/home/student/dc-ac-drift-extract`.

4. Full drift lab is not yet converted.
   The first Labtainer lab includes drift context. A full `drift-compensation-basic` Labtainer conversion remains a TODO.

## Build Recommendation

Use one single-container Labtainer first:

- Lab name: `dc-ac-drift-extract`
- Container: `steg`
- User: `student`
- Base image: `labtainer.base`
- Packages: `python3`, `python3-pip`, `ffmpeg`, `libgl1`, `libglib2.0-0`
- Python packages: `numpy`, `opencv-python-headless`, `pytest`

The legacy all-core package `steg-video-labs` may still be built for internal testing, but it must include only:

- `dc-coeff-warmup`
- `ac-coeff-midband`
- `dc-ac-combined`
- `drift-compensation-basic`

## Student/Instructor Separation

Student-facing content may include:

- root docs
- each core challenge `README.md`
- each core challenge `src/`
- each core challenge `solve.py`
- generated public artifacts:
  - `stego*.mp4`
  - `public_config.json`
  - `hint.txt`
  - `public/README.md` when present

Instructor-only content must not be shipped:

- `generate.py`
- `checker.py`
- `private/`
- `private_config.json`
- `answer.txt`
- expected flags or expected-file data

## Next Cleanup Items

- Remove tracked generated artifacts from git index in a separate cleanup commit.
- Convert `drift-compensation-basic` into a full Labtainer lab if the course needs a separate drift-focused exercise.
- Keep archived advanced challenges out of student-facing docs and packages.
