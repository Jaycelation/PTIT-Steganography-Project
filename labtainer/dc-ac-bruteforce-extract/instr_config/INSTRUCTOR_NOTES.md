# Instructor Notes: dc-ac-bruteforce-extract

Source challenge: `dc-ac-bruteforce`.

This lab is an educational brute-force extraction exercise. The public config
contains bounded candidate ranges, but intentionally omits the true `seed` and
active AC coefficient profile. Students recover those parameters by using the
DC `STEG` sync marker and then validating the AC payload format.

Expected recovered answer hash:

```text
sha256(answer.txt) = 4927ee5cc15b5b9af916ff7daa1555d13b353d8d540981f69bef8f4a0d604523
```

The seven checkwork items are:

- `video_metadata_checked`
- `config_audited`
- `candidate_space_built`
- `dc_sync_found`
- `bruteforce_config_recovered`
- `bruteforce_extract_ran`
- `flag_recovered`

Student package excludes `generate.py`, `checker.py`, `private/`,
`private_config.json`, source `answer.txt`, flags, and Python cache.
