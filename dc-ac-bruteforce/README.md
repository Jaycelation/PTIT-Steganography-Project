# dc-ac-bruteforce

Recover a message hidden across DC and AC DCT coefficients when the public
configuration intentionally omits the embedding seed and the active AC
coefficient profile.

This is an educational frame-DCT simulation. It is not a codec exploit and does
not modify MPEG/H.264/H.265 bitstreams directly.

## Generate

```powershell
python generate.py --flag "PTIT{dc_ac_bruteforce}" --seed 1769 --coefficient-profile 3,2 --output output
```

## Intended solve path

```powershell
python tools/build_candidate_space.py
python tools/probe_dc_sync.py
python tools/run_bruteforce.py
python solve.py --input output/stego.mp4 --config work/recovered_config.json --output work/answer.txt
```

## Public files

- `output/stego.mp4`
- `output/public_config.json`

The public config exposes bounded candidate ranges, but not the true `seed` or
active coefficient profile.
