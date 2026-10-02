# 화분 · 제1화 플레이 샘플

S01–S04와 C01 선택지를 포함한 Ren’Py 샘플입니다. 원문 대사·속말 415블록을 수록하며, 한 경로에서는 409블록을 읽습니다. 사람 목소리는 넣지 않았습니다. 메인 음악은 사용자 지정 「Gymnopedie No 1」입니다.

## 실행

```bash
./play.sh
```

제목 화면의 **새 장면 S03부터** 버튼으로 추가 부분을 바로 볼 수 있습니다.

- [Linux 배포본](dist/HwabunGarden-0.3.0-episode1-linux.tar.bz2): 압축 해제 후 `HwabunGarden.sh` 실행.
- [Windows 배포본](dist/HwabunGarden-0.3.0-episode1-win.zip): 압축 해제 후 `HwabunGarden.exe` 실행. Windows 직접 실행 검증은 아직 없습니다.

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
