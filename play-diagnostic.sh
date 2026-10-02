#!/usr/bin/env bash
set -euo pipefail
HWABUN_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
HWABUN_TRACE_DIR="$(mktemp -d "$HWABUN_ROOT/docs/freeze-diagnosis/session-$(date +%Y%m%d-%H%M%S)-XXXXXX")"
export HWABUN_FREEZE_PROBE="$HWABUN_TRACE_DIR/stacks.log"
printf '%s\n' "진단 기록: $HWABUN_TRACE_DIR" "멈추면 창을 그대로 두고 알려주세요."
exec "$HWABUN_ROOT/play.sh" "$@" >"$HWABUN_TRACE_DIR/console.log" 2>&1
