#!/usr/bin/env bash
set -euo pipefail
HWABUN_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# The desktop session has XWayland on :0; use it only if no display was inherited.
if [[ -z "${DISPLAY:-}" && -S /tmp/.X11-unix/X0 ]]; then export DISPLAY=:0; fi
exec "$HWABUN_ROOT/tools/renpy.sh" "$@"
