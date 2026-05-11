#!/bin/bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"

run_challenge() {
    local name="$1"
    shift
    echo "== $name =="
    (cd "$ROOT/$name" && "$@")
}

run_challenge dc-coeff-warmup python3 solve.py --input output/stego.mp4 --seed 1337 --length 19 --output /tmp/dc-answer.txt
run_challenge ac-coeff-midband python3 solve.py --input output/stego.mp4 --config output/public_config.json --output /tmp/ac-answer.txt
run_challenge dc-ac-combined python3 solve.py --input output/stego.mp4 --config output/public_config.json --output /tmp/combo-answer.txt
run_challenge drift-compensation-basic python3 solve.py --input output/stego_comp.mp4 --seed 404 --output /tmp/drift-answer.txt
run_challenge vlc-size-aware-embedding python3 solve.py --input output/stego.mp4 --seed 1337 --output /tmp/vlc-answer.txt
run_challenge robust-dc-ac-after-reencode python3 solve.py --input output/stego_reencoded.mp4 --seed 9001 --repeat 5 --output /tmp/robust-answer.txt

echo "All solve scripts completed."
