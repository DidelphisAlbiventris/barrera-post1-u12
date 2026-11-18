#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."
.venv/bin/python -m pip install pyinstaller==6.13.0 pyinstaller-hooks-contrib==2025.4
.venv/bin/python -m PyInstaller --noconfirm --clean --onedir --name u12_lab --distpath bin --collect-all qiskit --collect-all qiskit_aer src/lab_runner.py
