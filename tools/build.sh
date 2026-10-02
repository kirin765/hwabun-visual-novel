#!/usr/bin/env bash
set -euo pipefail
HWABUN_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
HWABUN_SDK="${RENPY_SDK:-/home/giwan/.local/share/renpy/renpy-8.5.4.26092102+nightly-sdk}"
python "$HWABUN_ROOT/tools/generate_script.py"
python "$HWABUN_ROOT/tools/asset_manifest.py"
python "$HWABUN_ROOT/sample/tests/test_integrity.py"
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy "$HWABUN_SDK/renpy.sh" "$HWABUN_ROOT/sample" lint
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy "$HWABUN_SDK/renpy.sh" "$HWABUN_SDK/launcher" distribute "$HWABUN_ROOT/sample" --package linux --package win --destination "$HWABUN_ROOT/dist"
