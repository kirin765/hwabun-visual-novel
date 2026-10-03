# 화분 · 제1화 플레이 샘플

S01–S04와 C01 선택지를 포함한 Ren’Py 샘플입니다. 원문 대사·속말 415블록을 수록하며, 한 경로에서는 409블록을 읽습니다. 미란에게 사용자 승인 Selly Han 감정 발성을 연결했습니다. 세란 Rosa Oh, 옥녀 Yoojin Kim, 단주 JooHwan, 현마 Shin도 연결했습니다. 영훈 HoCho는 이후 등장용으로 준비했습니다. 속말은 무음입니다. 설정에서 발성을 끌 수 있습니다. 메인 음악은 사용자 지정 「Gymnopedie No 1」입니다.

## 실행

```bash
./play.sh
```

제목 화면의 **새 장면 S03부터** 버튼으로 추가 부분을 바로 볼 수 있습니다.

- [Linux 배포본](dist/HwabunGarden-0.3.5-storm-weather-linux.tar.bz2): 압축 해제 후 `HwabunGarden.sh` 실행.
- [Windows 배포본](dist/HwabunGarden-0.3.5-storm-weather-win.zip): 압축 해제 후 `HwabunGarden.exe` 실행. Windows 직접 실행 검증은 아직 없습니다.

## 이번 추가

손님 방문, 거리, 식당, 영화관, 폭풍우 속 아파트, 촛불 대화와 새벽까지 이어집니다. 단주·현마 스탠딩, 미란 외출용 겉옷, 장소 배경과 촛불 CG 등 이미지 11장을 추가했습니다. 비·천둥·영사기·전차 종 등 합성 효과음 7개도 추가했습니다. 저장·불러오기, 자동 진행, 기록과 읽은 대사 스킵을 지원합니다.

기존 승인 그림체와 복장을 유지한 플레이용 시안입니다. 한국적 복장과 시대 고증의 전체 개편은 [미술 방향](docs/korean-art-direction.md)과 [역사 배경](docs/historical-setting.md)을 기준으로 별도 진행합니다. 식당·축음기·라디오 음악은 현재 메인 곡으로 임시 연결했습니다.

## 검증·출처

[추가 장면 검증](docs/s03-s04/verification.md), [화면 캡처](sample/tests/screenshots), [자산 출처](sample/ASSETS.md), [새 이미지 원본 기록](docs/s03-s04/image-sources.json).

```bash
python tools/generate_script.py
./tools/test.sh
./tools/build.sh
python tools/check_packages.py
```

엔진은 Ren’Py 8.5.4.26092102+nightly입니다. Linux 화면 멈춤에 대한 기존 VSync 우회를 유지했습니다. [기존 조사 기록](docs/freeze-diagnosis/README.md). 게임 실행에는 인터넷이나 API 키가 필요 없습니다.

인물은 호흡에 따른 미세한 움직임과 발화 반응, 등장·퇴장, 놀람 동작을 사용합니다. 설정의 인물 움직임 버튼으로 끌 수 있습니다. 기존 스탠딩을 움직이는 연출이며 눈·입의 별도 애니메이션은 아직 없습니다.

0.3.4에서는 발성 기회를 기존의 50%로 줄였습니다. 자연스러운 글자 표시 완료 시 재생 중인 발성을 중간에 자르던 처리를 수정했습니다. 미란의 평상·망설임·궁금함·불만, 단주의 걱정 파일을 같은 선택 목소리로 다시 생성했습니다. [교체 발성 확인](docs/miran-audio-check/index.html), [미란 전체 대사 샘플](docs/miran-full-line/index.html).

0.3.5: S3 후반 바람 → S4 실외 강풍/폭우 → 극장·아파트 실내의 작고 먹먹한 비바람 → 새벽 잦아드는 비로 전환합니다. 환경음 볼륨 설정을 따릅니다.

[비바람 실외·실내 비교](docs/s03-s04/weather-preview.html)
