#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
export MPLBACKEND=Agg
if [[ -x bin/u12_lab/u12_lab ]]; then
  exec bin/u12_lab/u12_lab "${@:-todo}"
elif [[ -x .venv/bin/python ]]; then
  exec .venv/bin/python src/lab_runner.py "${@:-todo}"
else
  echo 'Primero: bash instalar.sh'; exit 1
fi
