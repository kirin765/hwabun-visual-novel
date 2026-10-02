# 화분 정원 샘플 자산 기록

기록일: 2026-10-03. 버전: 0.3.3-character-voices. 개별 파일 해시는 `asset-manifest.json`을 따른다.

| 자산 | 수량 | 출처·제작 | 이용 근거 및 상태 |
|---|---:|---|---|
| 대사·속말 | 415블록 (각 경로 409) | 프로젝트의 `1화대본.md` S01–S04 및 C01 | 사용자 제공 기존 각색 대본. 본 샘플에서 문구·순서 유지. 최종 출시의 원작·각색 권리 검토를 대신하지 않음. |
| 정원·복도 | 2장 | OpenAI 내장 imagegen, 신규 생성 | 프로젝트 장소와 사용자 승인 미란 시안을 공통 화풍 기준으로 신규 생성. AI 제작·프롬프트·참조 경로 기록. |
| 미란·세란·옥녀 | 4+3+2장 | OpenAI 내장 imagegen | 사용자 승인 미란 및 새 세란·옥녀 기준 생성물에서 표정 수정. 얼굴·의상·포즈 유지. |
| CG01 | 1장 | OpenAI 내장 imagegen | 본 프로젝트의 자매 이미지와 정원을 참조해 생성. |
| M01 피아노풍 음악 | 1곡, 196초 | `tools/create_audio.py`, 샘플용 신규 작곡·가산 합성 | 외부 악보·연주·샘플·사운드폰트를 사용하지 않음. AI 도움으로 작성한 코드와 음원. 독점 저작권을 보장한다는 의미는 아님. |
| 잎·새·풀·걸음·문·물잔·차 | 7개 | `tools/create_audio.py`, 결정론적 신호 합성 | 실제 현장 녹음이 아닌 샘플용 합성 환경음. 외부 녹음 미사용. 생성 코드·시드 보관. |
| Noto Sans/Serif KR | 2개 | 시스템 `noto-fonts-cjk`, KR 서브폰트 | SIL Open Font License 1.1, `game/fonts/OFL.txt` 포함. |
| 뱀 실루엣 | 1개 | Ren’Py Text, DejaVuSans ∿∿ | 엔진 동봉 글꼴 사용, 별도 제3자 이미지 미사용. |
| 한국어 공통 UI 번역 | 1개 | Ren’Py SDK launcher의 Korean common.rpy | Ren’Py 배포본 라이선스와 함께 보관. |
| 엔진·런타임 | 1식 | 공식 Ren’Py 8.5.4.26092102+nightly SDK | Ren’Py 및 동봉 라이브러리 라이선스를 배포 패키지에 포함. |

현재 버전에는 사용자 승인 ElevenLabs Selly Han 발성 8개가 미란에게 연결되어 있다. Freesound 녹음과 기존 voice-v1/v2는 포함하지 않는다. `voice-reference.html`은 원 제공자의 공개 미리듣기를 링크하는 청취 자료다. 링크와 게임 배포용 음원을 구분한다.

## 음성 제작 후 추가할 기록

화자 ID / 음원 원본 / 전체 발성 길이 / SHA-256 / 원 제공자 / 모델·voice ID / 생성 날짜 / generation 또는 history ID / 생성 당시 유료 구독과 사용 조건 증거 / 편집 내역 / 사용자 청취 승인. 비밀 API 키나 결제 정보를 저장하지 않는다. 무료·공개 미리듣기를 상업용 제작 음원으로 전환하지 않는다.

## 근거 링크

- [Ren’Py 배포 및 빌드 문서](https://www.renpy.org/doc/html/build.html)
- [사용한 공식 nightly](https://nightly.renpy.org/8.5.4.26092102+nightly/)
- [Noto CJK](https://github.com/notofonts/noto-cjk)
- [OpenAI 이용 약관](https://openai.com/policies/terms-of-use/): 생성 자산에는 해당 서비스 약관을 적용하며 결과의 독점성·제3자 권리 무해성을 별도로 보장하지 않는다.
- [ElevenLabs 상업 사용 조건](https://help.elevenlabs.io/hc/en-us/articles/13313564601361-Can-I-publish-the-content-I-generate-on-the-platform)
- [실제 사람 hmm? 레퍼런스, esperar / CC0](https://freesound.org/people/esperar/sounds/170768/)
- [Steam 콘텐츠 설문](https://partner.steamgames.com/doc/gettingstarted/contentsurvey): 추후 출시 때 최종판의 성인 콘텐츠와 사전 생성 AI 사용을 실제 포함 내용에 맞춰 기재한다. 현재 Steam 제출·출시는 하지 않았다.

## 0.2.0 그림체 승인과 참조

사용자가 `miran-classic-otome-bust-preview.png`를 2026-10-03에 승인했다. 이 파일을 미란 평상 표정으로 그대로 사용하고 전체 미술의 기준으로 삼았다. 초기 화풍 탐색에는 사용자가 제공한 아래 게임 홍보 이미지를 시각적 참고로 사용했다. 해당 이미지 파일·로고·등장인물은 게임에 포함하지 않는다. 참조 이미지 자체의 이용 허락이나 권리를 취득했다는 의미는 아니다. 이번 생성·참조·파일 해시 기록은 프로젝트 `docs/art-style-v2/production-manifest.json`에 보관한다.

- https://wimg.mk.co.kr/meet/neds/2016/01/image_readtop_2016_10784_14519832492306904.jpg
- https://file.thisisgame.com/upload/rboard/2015/06/15/20150615133510_5610.jpg

## 사용자 지정 메인 테마

`game/audio/main_gymnopedie.ogg`: 사용자 제공 MP3를 Ogg Vorbis로 변환했습니다. 공식 배포 MP3와 SHA-256이 일치합니다. 확인 기록: `docs/s03-s04/music-source-check.json`.

Gymnopedie No 1 — Kevin MacLeod (incompetech.com)  
Licensed under Creative Commons: By Attribution 3.0  
https://creativecommons.org/licenses/by/3.0/

[공식 트랙](https://incompetech.com/music/royalty-free/index.html?isrc=USUAN1100787). 제목·정원 및 추가 장면에 연결했습니다. 식당·축음기·라디오의 별도 곡은 아직 메인 곡으로 임시 대체했습니다. 원 MP3는 수정하지 않았습니다.

## S03–S04 추가 자산

OpenAI 내장 imagegen으로 11장을 제작했습니다: 단주·현마 스탠딩 2, 미란 외출용 겉옷 1, 홀·거리·식당·영화관·아파트 및 촛불·새벽 아파트 배경 7, 촛불 CG 1. 승인된 인물 이미지를 참조했습니다. 원본 경로와 SHA-256은 `docs/s03-s04/image-sources.json`에 기록했습니다. 전체 역사 고증 및 한복 개편의 최종본은 아닙니다.

비·천둥·영사기·전차 종·라디오 잡음·식기·성냥 7개는 `tools/create_scene_audio.py`의 결정론적 신호 합성입니다. 외부 녹음과 사람 목소리는 사용하지 않았습니다. 새 음원 기록은 `docs/s03-s04/audio-manifest.json`에 있습니다.

## 미란 음성 승인

사용자가 `selly-han/previous.html`의 원본 8개를 미란 목소리로 승인했습니다. 놀람 “아!”, 안도 “아…”, 웃음 “하하.” 포함 버전입니다. 유료 플랜 전환 뒤 생성된 Eleven v3 / Selly Han 음원이며 Ogg로 변환했습니다. 생성 ID·프롬프트·원본 해시는 `docs/elevenlabs-examples/selly-han/manifest-previous.json`에 기록했습니다. 유료 플랜 확인 근거는 사용자 진술과 유료 플랜 전환 후 API 생성 성공이며 별도 결제 증빙은 수집하지 않았습니다. 게임은 로컬 음원만 재생합니다. 속말과 미승인 인물은 무음입니다.

## 나머지 인물 승인 및 음원

세란 Rosa Oh, 옥녀 Yoojin Kim, 단주 JooHwan, 현마 Shin, 영훈 HoCho를 사용자가 선택했습니다. 각 목소리의 감정 발성 8종, 합계 40개를 Ogg로 변환했습니다. `docs/voice-casting/selection.json`과 `docs/selected-voices/integration-manifest.json`에 선택·원본·해시를 기록했습니다. 비교용 문장은 배포 음원에서 제외했습니다. 영훈의 제1화 대사는 없어 이후 등장용으로 준비합니다.
