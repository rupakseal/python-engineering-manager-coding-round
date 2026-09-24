$ErrorActionPreference = "Stop"
$RepoDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = Join-Path $RepoDir "src"
python -m unittest discover -s (Join-Path $RepoDir "tests") -v
