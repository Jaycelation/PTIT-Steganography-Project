# Instructor Notes: dc-ac-drift-extract

This first-pass Labtainer lab is based on `dc-ac-combined`.

Expected recovered flag hash:

```text
sha256(answer.txt) = 0fa7e495d0fa26baaa53dc0510f5f395c7fae3d435545f243ed59ea6af2b9c97
```

The exact flag is intentionally not copied into the student home directory. The generated student package excludes:

- `generate.py`
- `checker.py`
- `private/`
- `private_config.json`
- source `answer.txt`
- Python bytecode/cache

Checkwork items:

- `video_metadata_checked`: student ran the metadata helper and wrote `VIDEO_METADATA_OK`.
- `dc_ac_extractor_ran`: student ran the DC/AC extraction wrapper and wrote `DC_AC_EXTRACT_OK`.
- `answer_file_created`: wrapper verified a non-empty answer and wrote `ANSWER_FILE_CREATED`.
- `flag_recovered`: wrapper wrote the SHA-256 of the recovered answer.
- `metrics_reported`: student ran the metrics helper and wrote `METRICS_OK`.

TODO: Convert `drift-compensation-basic` into a separate full lab that compares compensated and uncompensated extraction. This lab currently includes drift as concept guidance and metrics context only.
