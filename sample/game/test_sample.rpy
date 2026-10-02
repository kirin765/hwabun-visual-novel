testsuite garden:
    setup:
        $ _test.timeout = 15.0
        $ _test.transition_timeout = 0.1
        $ _test.screenshot_directory = "tests/screenshots"
    teardown:
        exit
    testcase full_playthrough:
        assert screen "main_menu"
        screenshot "01-title.png"
        click "처음부터"
        advance until screen "say"
        $ preferences.text_cps = 0
        advance until eval block_id == 4
        screenshot "02-garden.png"
        assert eval renpy.music.get_playing(channel="music") == "audio/main_gymnopedie.ogg"
        assert eval not preferences.skip_unseen
        click "저장"
        assert screen "save"
        run FileSave(1, confirm=False)
        click "돌아가기"
        advance
        advance
        assert eval block_id == 6
        click "불러오기"
        run FileLoad(1, confirm=False)
        pause 0.5
        assert eval block_id == 4
        assert eval renpy.music.get_playing(channel="music") == "audio/main_gymnopedie.ogg"
        assert eval renpy.music.get_playing(channel="ambience") == "audio/leaves.ogg"
        click "기록"
        assert screen "history"
        screenshot "03-history.png"
        click "돌아가기"
        click "설정"
        assert screen "preferences"
        pause 0.3
        screenshot "04-preferences.png"
        assert eval not voices_ready
        assert eval not renpy.music.is_playing(channel='utterance')
        click "돌아가기"
        advance until eval block_id == 11
        screenshot "09-long-thought.png"
        advance until eval block_id == 12
        screenshot "05-cg.png"
        advance until eval block_id == 65
        screenshot "06-startled.png"
        advance until eval block_id == 84
        screenshot "07-corridor.png"
        advance until eval block_id == 125
        screenshot "10-hall.png"
        advance until screen "choice"
        screenshot "11-choice.png"
        pause 0.5
        click "아까 입 열지 말라구 했잖우."
        pause 0.2
        advance until eval block_id == 183
        assert eval c01_choice == "A"
        advance until eval block_id == 200
        screenshot "12-street.png"
        advance until eval block_id == 230
        screenshot "13-restaurant.png"
        advance until eval block_id == 290
        screenshot "14-cinema.png"
        advance until eval block_id == 340
        screenshot "15-apartment.png"
        advance until eval block_id == 380
        screenshot "16-candle.png"
        advance until screen "sample_end"
        assert eval sample_complete
        assert eval block_id == 415
        assert eval not renpy.music.is_playing(channel='utterance')
        screenshot "08-end.png"
        click "제목 화면으로"
        assert screen "main_menu"

    testcase auto_and_read_skip:
        if not screen "main_menu":
            run MainMenu(confirm=False)
        run Start()
        advance until screen "say"
        $ preferences.text_cps = 0
        $ preferences.afm_time = 1
        $ auto_start_block = block_id
        click "자동"
        pause 3.0
        assert eval block_id > auto_start_block
        click "자동"
        $ preferences.afm_time = 14
        run Skip()
        pause 1.0
        advance until screen "choice"
        pause 0.5
        click "내 얘기가 그리두 우스워요?"
        pause 0.2
        advance until eval block_id == 183
        assert eval c01_choice == "B"
        advance until screen "sample_end"
        assert eval sample_complete
        assert eval not renpy.music.is_playing(channel='utterance')
        run MainMenu(confirm=False)

    testcase new_scene_save_and_restore:
        assert screen "main_menu"
        click "새 장면 S03부터"
        advance until screen "say"
        $ preferences.text_cps = 0
        advance until screen "choice"
        pause 0.5
        click "내 얘기가 그리두 우스워요?"
        pause 0.2
        advance until eval block_id == 350
        assert eval c01_choice == "B"
        assert eval not renpy.music.is_playing(channel='utterance')
        click "저장"
        run FileSave(2, confirm=False)
        click "돌아가기"
        advance
        advance
        click "불러오기"
        run FileLoad(2, confirm=False)
        pause 0.5
        assert eval block_id == 350
        assert eval c01_choice == "B"
        screenshot "18-loaded-apartment.png"
        click "기록"
        assert screen "history"
        click "돌아가기"
        $ preferences.text_cps = 0
        advance until eval block_id == 408
        screenshot "17-dawn.png"
        advance until screen "sample_end"
        assert eval sample_complete
