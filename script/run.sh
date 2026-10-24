#!/bin/bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
exec python3 collector.py "${1:-start}"
