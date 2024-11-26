#!/usr/bin/env pwsh

$ErrorActionPreference = "Stop"
$VerbosePreference = "Continue"

New-Item -ItemType Directory -Force -Path "var"

python3 -m venv .venv
& .\.venv\Scripts\Activate.ps1
python3 -m pip install -r requirements.txt
python3 src/librairie.py
