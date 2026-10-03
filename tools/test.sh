#!/usr/bin/env bash
set -euo pipefail
HWABUN_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ -z "${DISPLAY:-}" && -S /tmp/.X11-unix/X0 ]]; then export DISPLAY=:0; fi
HWABUN_TEST_SAVES="$(mktemp -d -t hwabun-tests-XXXXXX)"
trap 'rm -rf -- "$HWABUN_TEST_SAVES"' EXIT
python "$HWABUN_ROOT/sample/tests/test_integrity.py"
for HWABUN_SUITE in garden voice_routing miran_voice voice_tail; do
  SDL_AUDIODRIVER=dummy "$HWABUN_ROOT/tools/renpy.sh" test "$HWABUN_SUITE" --savedir "$HWABUN_TEST_SAVES" --report-detailed --overwrite-screenshots
 done
