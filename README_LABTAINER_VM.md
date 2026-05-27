# Labtainer VM Usage

Run these commands inside the Labtainer VM from the Labtainer student directory.

## ac-midband-extract

```bash
cd ~/labtainer/labtainer-student
imodule https://github.com/Jaycelation/PTIT-Steganography-Project/raw/refs/heads/master/labtainer/ac-midband-extract.tar
labtainer -r ac-midband-extract
```

## dc-ac-combined-extract

```bash
cd ~/labtainer/labtainer-student
imodule https://github.com/Jaycelation/PTIT-Steganography-Project/raw/refs/heads/master/labtainer/dc-ac-combined-extract.tar
labtainer -r dc-ac-combined-extract
```

## dc-ac-drift-extract

```bash
cd ~/labtainer/labtainer-student
imodule https://github.com/Jaycelation/PTIT-Steganography-Project/raw/refs/heads/master/labtainer/dc-ac-drift-extract.tar
labtainer -r dc-ac-drift-extract
```

## dc-ac-bruteforce-extract

```bash
cd ~/labtainer/labtainer-student
imodule https://github.com/Jaycelation/PTIT-Steganography-Project/raw/refs/heads/master/labtainer/dc-ac-bruteforce-extract.tar
labtainer -r dc-ac-bruteforce-extract
```

## DockerHub Build Commands

Run from the repository root after regenerating Labtainer packages.

### ac-midband-extract

```bash
cd labtainer/build/ac-midband-extract
docker build \
  -f dockerfiles/Dockerfile.ac-midband-extract.steg.student \
  --build-arg registry=labtainers \
  --build-arg lab=ac-midband-extract.steg.student \
  --build-arg labdir=steg \
  --build-arg imagedir=steg \
  --build-arg user_name=student \
  --build-arg password=student \
  --build-arg apt_source= \
  -t jaycedang/ac-midband-extract.steg.student:latest \
  -t jaycedang/ac-midband-extract-steg-student:latest \
  .
```

### dc-ac-combined-extract

```bash
cd labtainer/build/dc-ac-combined-extract
docker build \
  -f dockerfiles/Dockerfile.dc-ac-combined-extract.steg.student \
  --build-arg registry=labtainers \
  --build-arg lab=dc-ac-combined-extract.steg.student \
  --build-arg labdir=steg \
  --build-arg imagedir=steg \
  --build-arg user_name=student \
  --build-arg password=student \
  --build-arg apt_source= \
  -t jaycedang/dc-ac-combined-extract.steg.student:latest \
  -t jaycedang/dc-ac-combined-extract-steg-student:latest \
  .
```

### dc-ac-drift-extract

```bash
cd labtainer/build/dc-ac-drift-extract
docker build \
  -f dockerfiles/Dockerfile.dc-ac-drift-extract.steg.student \
  --build-arg registry=labtainers \
  --build-arg lab=dc-ac-drift-extract.steg.student \
  --build-arg labdir=steg \
  --build-arg imagedir=steg \
  --build-arg user_name=student \
  --build-arg password=student \
  --build-arg apt_source= \
  -t jaycedang/dc-ac-drift-extract.steg.student:latest \
  -t jaycedang/dc-ac-drift-extract-steg-student:latest \
  .
```

### dc-ac-bruteforce-extract

```bash
cd labtainer/build/dc-ac-bruteforce-extract
docker build \
  -f dockerfiles/Dockerfile.dc-ac-bruteforce-extract.steg.student \
  --build-arg registry=labtainers \
  --build-arg lab=dc-ac-bruteforce-extract.steg.student \
  --build-arg labdir=steg \
  --build-arg imagedir=steg \
  --build-arg user_name=student \
  --build-arg password=student \
  --build-arg apt_source= \
  -t jaycedang/dc-ac-bruteforce-extract.steg.student:latest \
  -t jaycedang/dc-ac-bruteforce-extract-steg-student:latest \
  .
```

## Regenerate Packages

```bash
python scripts/prepare_labtainer_public.py
python scripts/run_all_lab_checks.py
```

The generated GitHub tar files are written to `labtainer/`.
