#!/usr/bin/env pwsh

$ErrorActionPreference = "Stop"
$VerbosePreference = "Continue"

New-Item -ItemType Directory -Force -Path "var"

python -m venv .venv
& .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python src/librairie.py
