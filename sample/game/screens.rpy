style default:
    font "fonts/NotoSansKR.otf"
    size 30
    color "#ede8dd"
    language "korean-with-spaces"
style text:
    line_spacing 10
style button:
    padding (22, 12)
    hover_background "#aac6b522"
style button_text:
    color "#c7c8ba"
    hover_color "#ffffff"
    selected_color "#b4d6c5"
    insensitive_color "#72796f"
style bar:
    ysize 14
    left_bar Solid("#abcbb8")
    right_bar Solid("#47554b")
    thumb Solid("#f1eadd", xsize=14, ysize=28)
style slider is bar:
    xsize 640
    ysize 28

style scrollbar:
    xsize 8
    base_bar Solid("#465448")
    thumb Solid("#abcbb8")
style say_dialogue:
    size 36
    line_spacing 16
style say_label:
    size 29
    bold True

screen say(who, what):
    window:
        id "window"
        background Solid("#12271fec")
        xpos 80
        ypos 720
        xsize 1760
        ysize 295
        padding (54, 28)
        if who:
            text who id "who" ypos 0
        text what id "what" ypos 53 xsize 1640
    text scene_title xpos 110 ypos 44 size 24 outlines [(2,"#18291ddd",0,1)]
    add VoicePulseDisplayable(voice_generation)
    use quick_menu

screen quick_menu():
    zorder 100
    add Solid("#10291fee", xsize=1920, ysize=65) ypos 1015
    hbox:
        xalign 0.5
        ypos 1020
        spacing 8
        textbutton "기록" action [Function(stop_utterance), ShowMenu('history')] text_size 24
        textbutton "저장" action [Function(stop_utterance), ShowMenu('save')] text_size 24
        textbutton "불러오기" action [Function(stop_utterance), ShowMenu('load')] text_size 24
        textbutton "자동" action Preference('auto-forward', 'toggle') text_size 24
        textbutton "읽은 대사 스킵" action [Function(stop_utterance), Skip()] text_size 24
        textbutton "설정" action [Function(stop_utterance), ShowMenu('preferences')] text_size 24

screen main_menu():
    tag menu
    add "bg garden"
    add Solid("#0a211ad9", xsize=720)
    vbox:
        xpos 118
        ypos 140
        spacing 20
        text "화분" font "fonts/NotoSerifKR.otf" size 100 color "#f1ead9"
        text "제1화  /  푸른 집" size 28 color "#bdd0bb"
        null height 48
        textbutton "처음부터" action Start()
        textbutton "새 장면 S03부터" action Start("sample_s03")
        textbutton "불러오기" action ShowMenu('load')
        textbutton "설정" action ShowMenu('preferences')
        textbutton "조작 안내" action ShowMenu('help')
        textbutton "제작 정보" action ShowMenu('about')
        textbutton "종료" action Quit(confirm=False)
    text "제1화 전체 샘플 · S01–S04\n선택한 인물 목소리 / 음악·환경음" xpos 140 ypos 990 size 21 color "#b9c5b5"

screen choice(items):
    modal True
    on "show" action Function(stop_utterance)
    vbox:
        xalign 0.5
        yalign 0.55
        spacing 24
        for item in items:
            textbutton item.caption:
                action item.action
                xsize 1000
                padding (36, 26)
                background Solid("#15362ef2")
                hover_background Solid("#3c6154")
                text_color "#f2eadb"
                text_size 34
                text_xalign 0.5

transform rain_drop(seed):
    xpos (seed * 71) % 1920
    ypos -120
    alpha 0.18
    rotate 18
    pause (seed % 7) * 0.07
    linear 0.8 ypos 1160 xpos ((seed * 71) % 1920 - 220)
    repeat

screen rain_overlay():
    zorder -1
    for i in range(30):
        add Solid("#d1dfec", xsize=2, ysize=70) at rain_drop(i)

screen menu_frame(title):
    add "bg garden"
    add Solid("#10251bf4")
    on "show" action Function(stop_utterance)
    text title xpos 110 ypos 65 size 48 font "fonts/NotoSerifKR.otf"
    hbox:
        xpos 100
        ypos 145
        spacing 18
        textbutton "저장" action ShowMenu('save') sensitive not main_menu
        textbutton "불러오기" action ShowMenu('load')
        textbutton "설정" action ShowMenu('preferences')
        textbutton "기록" action ShowMenu('history') sensitive not main_menu
        textbutton "제목 화면" action MainMenu()
        textbutton "돌아가기" action Return()
    transclude

screen save():
    tag menu
    use file_slots("저장")
screen load():
    tag menu
    use file_slots("불러오기")
screen file_slots(title):
    use menu_frame(title):
        grid 3 2:
            xpos 135
            ypos 260
            spacing 30
            for i in range(1,7):
                button:
                    xsize 525
                    ysize 295
                    background "#263c31"
                    action FileAction(i)
                    vbox:
                        spacing 8
                        add FileScreenshot(i) xysize (440, 210) xalign 0.5
                        text FileTime(i, format="%Y-%m-%d %H:%M", empty="빈 저장 칸") size 23 xalign 0.5
                    key "save_delete" action FileDelete(i)
        hbox:
            xalign 0.5
            ypos 940
            spacing 25
            textbutton "이전" action FilePagePrevious()
            textbutton "자동 저장" action FilePage('auto')
            textbutton "빠른 저장" action FilePage('quick')
            for page in range(1,6):
                textbutton str(page) action FilePage(page)
            textbutton "다음" action FilePageNext()

screen preferences():
    tag menu
    use menu_frame("설정"):
        hbox:
            xpos 160
            ypos 280
            spacing 150
            vbox:
                xsize 640
                spacing 24
                text "읽기" size 34 color "#b7d6c3"
                text "글자 속도"
                bar value Preference('text speed')
                text "자동 진행 대기 시간"
                bar value Preference('auto-forward time')
                null height 10
                text "화면"
                hbox:
                    textbutton "창 모드" action Preference('display','window')
                    textbutton "전체 화면" action Preference('display','fullscreen')
                textbutton "인물 움직임 켜기 / 끄기" action ToggleField(persistent, 'character_motion')
                text "스킵은 이미 읽은 대사에만 적용됩니다." size 24 color "#a8b8a7"
                textbutton "모든 소리 끄기" action Preference('all mute','toggle')
            vbox:
                xsize 640
                spacing 24
                text "소리" size 34 color "#b7d6c3"
                text "음악"
                bar value Preference('music volume')
                text "환경음 · 효과음"
                bar value Preference('sound volume')
                text "짧은 발성"
                bar value Preference('voice volume')
                textbutton "발성 켜기 / 끄기" action [Function(stop_utterance), ToggleField(persistent,'utterances')] sensitive voices_ready
                if voices_ready:
                    text "미란·세란·옥녀·단주·현마 발성 / 속말 무음" size 23 color "#a8b8a7"
                if not voices_ready:
                    text "승인된 발성 음원이 없습니다.\n승인된 발성 음원을 연결하면 켤 수 있습니다." size 23 color "#a8b8a7"

screen history():
    tag menu
    predict False
    use menu_frame("대화 기록"):
        viewport:
            xpos 155
            ypos 260
            xsize 1610
            ysize 720
            scrollbars "vertical"
            mousewheel True
            draggable True
            yinitial 1.0
            vbox:
                spacing 25
                for h in _history_list:
                    vbox:
                        spacing 8
                        if h.who:
                            text h.who size 24 color "#acd0b9" substitute False
                        text h.what size 30 substitute False xsize 1500

screen help():
    tag menu
    use menu_frame("조작 안내"):
        vbox:
            xpos 165
            ypos 285
            spacing 28
            text "클릭 · Enter · Space     다음 대사 / 진행 중인 글자 즉시 표시"
            text "Esc · 마우스 오른쪽     메뉴 열기 / 돌아가기"
            text "휠 위 · Page Up     이전 대사로 돌아가기"
            text "Ctrl 길게 · Tab     읽은 대사 스킵"
            text "H     대화창 숨기기"
            text "자동 버튼     자동 진행 켜기 / 끄기"
            text "기록·저장·불러오기·설정은 화면 아래 버튼으로 열 수 있습니다."
            text "정원·손님 방문·거리와 폭풍우·새벽까지 제1화를 플레이합니다." color "#b7d6c3"

screen about():
    tag menu
    use menu_frame("제작 정보"):
        vbox:
            xpos 165
            ypos 280
            spacing 26
            text "화분 · 제1화 푸른 집" size 40
            text "S01–S04 / 선택지 1개, 두 경로 뒤 공통 합류"
            text "기존 한국어 각색 대본 / AI 제작 배경·인물·CG"
            text "Gymnopedie No 1 — Kevin MacLeod (incompetech.com)" size 28
            text "{a=https://creativecommons.org/licenses/by/3.0/}Licensed under Creative Commons: By Attribution 3.0{/a}" size 24
            text "사용자 제공 음악·합성 환경음 / Noto 한국어 글꼴 (SIL OFL)" size 28
            text "Ren’Py 8.5.4.26092102+nightly"
            text "선택한 인물 감정 발성 / 속말은 무음" color "#b7d6c3"
            text "자산별 출처·제작 방식·이용 근거: 배포 폴더의 ASSETS.md" size 25

screen confirm(message, yes_action, no_action):
    modal True
    zorder 200
    add Solid("#000a")
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1000
        background "#18372b"
        padding (55, 45)
        vbox:
            spacing 32
            text message xalign 0.5
            hbox:
                xalign 0.5
                spacing 100
                textbutton "확인" action yes_action
                textbutton "취소" action no_action
    key "game_menu" action no_action

screen notify(message):
    zorder 200
    frame:
        xpos 50
        ypos 35
        padding (30,20)
        background "#153427ed"
        text message size 25
    timer 3.0 action Hide('notify')

screen skip_indicator():
    zorder 100
    text "읽은 대사 스킵 중" xpos 1500 ypos 50 size 25 outlines [(2,"#123",0,0)]

screen sample_end():
    modal True
    add "bg garden"
    add Solid("#112b22ed")
    vbox:
        xalign 0.5
        yalign 0.5
        spacing 30
        text "푸른 집" font "fonts/NotoSerifKR.otf" size 72 xalign 0.5
        text "제1화 전체 샘플을 마쳤습니다." xalign 0.5
        text "미란이 새벽에 돌아갈 문을 여는 곳까지 이어집니다." size 26 color "#b5c9b6" xalign 0.5
        null height 20
        textbutton "다시 플레이" action Start() xalign 0.5
        textbutton "제목 화면으로" action MainMenu(confirm=False) xalign 0.5
