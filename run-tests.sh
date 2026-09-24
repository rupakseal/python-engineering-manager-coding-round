#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "$0")" && pwd)"
PYTHONPATH="$repo_dir/src" python3 -m unittest discover -s "$repo_dir/tests" -v
