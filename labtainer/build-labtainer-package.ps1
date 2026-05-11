param(
    [string]$OutputRoot = "labtainer/build/steg-video-labs"
)

$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$outRoot = Join-Path $repoRoot $OutputRoot
$studentHome = Join-Path $outRoot "steg"
$workspace = Join-Path $studentHome "steg-video-labs"

$challenges = @(
    "dc-coeff-warmup",
    "ac-coeff-midband",
    "dc-ac-combined",
    "drift-compensation-basic"
)

if (Test-Path $outRoot) {
    Remove-Item -LiteralPath $outRoot -Recurse -Force
}

New-Item -ItemType Directory -Force -Path $workspace | Out-Null

foreach ($path in @("bin", "config", "dockerfiles", "instr_config", "steg/_bin")) {
    New-Item -ItemType Directory -Force -Path (Join-Path $outRoot $path) | Out-Null
}

Copy-Item -LiteralPath (Join-Path $PSScriptRoot "templates/config/start.config") -Destination (Join-Path $outRoot "config/start.config")
Copy-Item -LiteralPath (Join-Path $PSScriptRoot "templates/config/about.txt") -Destination (Join-Path $outRoot "config/about.txt")
Copy-Item -LiteralPath (Join-Path $PSScriptRoot "templates/config/keywords.txt") -Destination (Join-Path $outRoot "config/keywords.txt")
Copy-Item -LiteralPath (Join-Path $PSScriptRoot "templates/config/parameter.config") -Destination (Join-Path $outRoot "config/parameter.config")
Copy-Item -LiteralPath (Join-Path $PSScriptRoot "templates/dockerfiles/Dockerfile.steg-video-labs.steg.student") -Destination (Join-Path $outRoot "dockerfiles/Dockerfile.steg-video-labs.steg.student")
Copy-Item -LiteralPath (Join-Path $PSScriptRoot "templates/instr_config/results.config") -Destination (Join-Path $outRoot "instr_config/results.config")
Copy-Item -LiteralPath (Join-Path $PSScriptRoot "templates/instr_config/goals.config") -Destination (Join-Path $outRoot "instr_config/goals.config")
Copy-Item -LiteralPath (Join-Path $PSScriptRoot "templates/steg/_bin/fixlocal") -Destination (Join-Path $studentHome "_bin/fixlocal")
Copy-Item -LiteralPath (Join-Path $PSScriptRoot "templates/steg/instructions.txt") -Destination (Join-Path $studentHome "instructions.txt")
Copy-Item -LiteralPath (Join-Path $PSScriptRoot "templates/steg/run_all_checks.sh") -Destination (Join-Path $workspace "run_all_checks.sh")

foreach ($doc in @("README.md", "DEMO.md", "EVALUATION.md", "LABTAINER_READINESS.md")) {
    $src = Join-Path $repoRoot $doc
    if (Test-Path $src) {
        Copy-Item -LiteralPath $src -Destination (Join-Path $workspace $doc)
    }
}

foreach ($challenge in $challenges) {
    $srcDir = Join-Path $repoRoot $challenge
    $dstDir = Join-Path $workspace $challenge
    New-Item -ItemType Directory -Force -Path $dstDir | Out-Null

    foreach ($item in @("README.md", "requirements.txt", "solve.py")) {
        $src = Join-Path $srcDir $item
        if (Test-Path $src) {
            Copy-Item -LiteralPath $src -Destination (Join-Path $dstDir $item)
        }
    }

    Copy-Item -LiteralPath (Join-Path $srcDir "src") -Destination (Join-Path $dstDir "src") -Recurse

    $outDir = Join-Path $srcDir "output"
    if (Test-Path $outDir) {
        New-Item -ItemType Directory -Force -Path (Join-Path $dstDir "output") | Out-Null
        foreach ($pattern in @("stego*.mp4", "public_config.json", "hint.txt")) {
            Get-ChildItem -LiteralPath $outDir -Filter $pattern -File -ErrorAction SilentlyContinue |
                Copy-Item -Destination (Join-Path $dstDir "output")
        }
        $publicDir = Join-Path $outDir "public"
        if (Test-Path $publicDir) {
            Copy-Item -LiteralPath $publicDir -Destination (Join-Path $dstDir "output/public") -Recurse
        }
    }
}

Get-ChildItem -LiteralPath $outRoot -Recurse -Directory -Force |
    Where-Object { $_.Name -eq "__pycache__" } |
    Remove-Item -Recurse -Force

Get-ChildItem -LiteralPath $outRoot -Recurse -File -Force |
    Where-Object { $_.Name -like "*.pyc" } |
    Remove-Item -Force

Write-Host "Created Labtainer package at $outRoot"
