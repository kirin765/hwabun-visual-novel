#!/usr/bin/env bash
set -euo pipefail
HWABUN_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
HWABUN_SDK="${RENPY_SDK:-/home/giwan/.local/share/renpy/renpy-8.5.4.26092102+nightly-sdk}"
if [[ ! -x "$HWABUN_SDK/renpy.sh" ]]; then
  echo 'Ren’Py SDK를 찾지 못했습니다. RENPY_SDK를 지정하거나 dist의 배포본을 실행하세요.' >&2
  exit 1
fi
exec "$HWABUN_SDK/renpy.sh" "$HWABUN_ROOT/sample" "$@"
