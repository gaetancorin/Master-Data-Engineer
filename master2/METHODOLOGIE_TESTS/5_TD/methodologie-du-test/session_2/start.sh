#!/usr/bin/env bash

set -euxo pipefail
mkdir -p var
python3 -m venv .venv
set +x
source .venv/bin/activate
set -x
python3 -m pip install -r requirements.txt
python3 src/librairie.py
