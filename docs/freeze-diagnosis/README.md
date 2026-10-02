# 화면 정지 수정 — 0.1.1

2026-10-02~03, Linux / NVIDIA RTX 3060 / 610.57.04 / XWayland / Ren’Py 8.5.4.26092102+nightly.

사용자 증상: `play.sh`의 대사 화면에서 게임만 멈춤. Enter·Esc 무반응, 음악도 들리지 않음. 데스크톱과 다른 앱은 정상. 화면 크기를 바꾸지 않아도 발생.

## 확인한 원인과 수정 범위

실제 사용자 재현에서 **37번 대사의 화면 출력 호출이 11.3849초 이상 반환하지 않았다.** `reported-live-observations.json`에 5초 동안 반복 관찰한 멈춤 상태를 보관했다. `session-20261002-234909-wGm9Rn/stacks.log`의 메인 스레드는 `renpy/display/core.py:1287`의 `draw.draw_screen()` 안에 있었고 커널 대기 위치는 `drm_syncobj_array_wait_timeout`이었다. 이후 회복하기도 하는 간헐적 정지다.

VSync만 끈 비교 실행(`RENPY_GL_VSYNC=0`)에서 로그의 `swap interval: 0 frames`를 확인했다. 동일한 실제 오디오·이미지·대사 처리로 사용자 재시험을 진행했고 **“지금은 정상적으로 진행됨”** 답변을 받았다. 비교 실행 첫 수 분의 가장 긴 프레임 출력은 0.0898초 미만이었다. `session-20261002-235719-ORnq4d`에 해당 기록이 있다.

따라서 `sample/game/options.rpy`에서 Linux에서 렌더러 생성 전에 `RENPY_GL_VSYNC=0`을 기본 적용했다. 일반 `play.sh`와 새 Linux 배포본에 모두 적용된다. Windows와 다른 플랫폼의 기존 설정은 유지했다. 이 변경은 관찰된 GPU 동기화 대기를 피하는 **호환성 우회**이며, NVIDIA 드라이버 내부의 근본 결함까지 확정한 것은 아니다. 시스템·드라이버 설정은 변경하지 않았다.

공식 설정 근거: [Ren’Py VSync 환경 변수](https://www.renpy.org/doc/html/environment_variables.html#envvar-RENPY_GL_VSYNC). 필요하면 `RENPY_GL_VSYNC=1 ./play.sh`로 비교할 수 있지만 이 컴퓨터에서는 이전 정지가 재발할 수 있다.

## 검증과 한계

- 기존 테스트 엔진은 VSync를 자동으로 끈다. 이전 자동 검사 통과가 일반 실행의 정지를 검출하지 못했던 이유다.
- `reported-live-observations.json`: 사용자 재현 중 11.38초 이상의 실제 출력 지연.
- 비교 실행: 사용자 정상 진행 확인, 누적 최대 출력 시간 기록.
- `regression-tests.log`: 원문 대사·발성 정책, 완주, 저장/불러오기, 메뉴, 자동 진행·스킵, 발성 라우팅 회귀 검사.
- `fixed-source-native-repro.log`와 `packaged-native-repro.log`: 별도 VSync 환경 변수 없이 수정된 원본의 일반 실행 검사. 테스트 모드를 사용하지 않고 Enter·Esc·전체 화면·음악 시계·출력 지연을 검사한다.
- Windows는 패키지 검사만 한다. Windows 실기기 실행 결과는 없다.
- 모든 하드웨어와 장시간 플레이에서 재발하지 않는다는 보장은 아니다. 재발하면 아래 진단 실행으로 해당 상태를 기록한다.

## 재현 도구

`./play-diagnostic.sh`: 원래 저장 경로와 설정으로 실행하며 세션마다 `docs/freeze-diagnosis/session-*`에 콘솔·마지막 프레임 상태·1초 초과 프레임을 기록한다. 인터넷으로 보내지 않는다. 멈추면 창을 닫지 않고 그대로 둔 상태에서 알려주면 된다.

`uv run --with python-xlib python tools/repro_freeze.py`: 별도의 임시 저장 폴더를 쓰는 일반 실행 검사. `HWABUN_PROBE_STEPS=600`으로 120초까지 늘릴 수 있다. 입력 실패는 실제 정지와 구분해 해석해야 한다.

진단 기능은 `HWABUN_FREEZE_PROBE`가 설정된 경우에만 켜진다. 테스트 파일이므로 배포본에서는 제외한다. `diagnostic-development-*`와 초기 `repro`/`paced` 로그는 진단 도구 개발 중의 오류를 포함하며 사용자 정지의 근거가 아니다.

## 진단 도구 자체의 별도 오류

배포본 검사 중 추가했던 `faulthandler.dump_traceback_later` 타이머가 SIGSEGV를 일으켰다. 코어 덤프 354200의 크래시 스레드는 `_Py_DumpTracebackThreads` 내부였으며 게임 메인 스레드는 정상 계산 중이었다. `diagnostic-coredump-info.txt` 참조. 주기적 스택 출력 기능을 제거했고 프레임 시간 기록만 유지했다. 진단 코드는 원래 배포 압축 파일에서 제외되므로 배포 게임 코드의 오류로 분류하지 않는다. 제거 후 같은 배포본 일반 실행 검사를 재수행했다.
