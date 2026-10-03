# Test-only routing probes use foley, never synthetic or unapproved human vocals.
# Both source and compiled test files are excluded from release packages.
label test_probe:
    scene bg garden
    $ block_id = 900
    miran "하나 둘 셋 넷 다섯 여섯 일곱 여덟 아홉 열. 이 문장은 글자 진행과 재생 중단만 검증하는 엔진 시험입니다."
    $ block_id = 901
    inner "속말은 항상 조용합니다. 읽는 속도와 관계없이 발성 채널을 재생하지 않습니다."
    $ block_id = 902
    seran "하나 둘 셋 넷 다섯 여섯 일곱 여덟 아홉 열. 메뉴에 들어가면 소리를 바로 멈춥니다."
    $ block_id = 903
    oknyeo "하나 둘 셋 넷 다섯 여섯 일곱 여덟 아홉 열. 글자를 즉시 표시하면 소리를 바로 멈춥니다."
    $ block_id = 904
    return

testsuite voice_routing:
    setup:
        $ _test.timeout = 10.0
        $ _test.transition_timeout = 0.1
        $ preferences.afm_enable = False
        $ config.skipping = None
        $ persistent.utterances = True
        $ voice_density = 1.0
        $ preferences.text_cps = 10
        $ voice_pools = {s:['audio/grass.ogg','audio/door.ogg'] for s in ('miran','seran','oknyeo')}
    teardown:
        $ voice_density = 0.5
        $ voice_pools = {}
        $ persistent.utterances = False
        $ preferences.text_cps = 28
        $ stop_utterance()
        exit
    testcase real_channel_cancellation:
        run Start('test_probe')
        advance until eval block_id == 900
        pause 0.8
        assert eval renpy.music.is_playing(channel='utterance')
        keysym "K_RETURN"
        pause 0.07
        assert eval not renpy.music.is_playing(channel='utterance')
        advance until eval block_id == 901
        pause 0.8
        pause 0.07
        assert eval not renpy.music.is_playing(channel='utterance')
        advance until eval block_id == 902
        pause 0.8
        assert eval renpy.music.is_playing(channel='utterance')
        click "설정"
        pause 0.07
        assert eval not renpy.music.is_playing(channel='utterance')
        click "돌아가기"
        pause 0.3
        pause 0.07
        assert eval not renpy.music.is_playing(channel='utterance')
        advance until eval block_id == 903
        pause 0.8
        assert eval renpy.music.is_playing(channel='utterance')
        keysym "K_RETURN"
        pause 0.07
        assert eval not renpy.music.is_playing(channel='utterance')

testsuite miran_voice:
    setup:
        $ _test.timeout = 20.0
        $ _test.transition_timeout = 0.1
        $ preferences.afm_enable = False
        $ config.skipping = None
        $ persistent.utterances = True
        $ preferences.text_cps = 10
    teardown:
        $ stop_utterance()
        exit
    testcase approved_selly_routing:
        assert eval voices_ready
        assert eval voice_density == 0.5
        $ voice_trigger_count = 1
        assert eval set(voice_pools) == {'miran','seran','oknyeo','danju','hyunma','younghun'}
        $ block_id = 63
        assert eval utterance_pool('miran') == ['audio/miran_selly/surprised.ogg']
        $ block_id = 72
        assert eval utterance_pool('miran') == ['audio/miran_selly/relieved.ogg']
        $ block_id = 350
        assert eval utterance_pool('miran') == ['audio/miran_selly/laugh.ogg']
        $ block_id = 5
        assert eval len(utterance_pool('miran')) == 3
        assert eval len(utterance_pool('seran')) == 3
        assert eval all(len(voice_pools[s]) == 8 for s in voice_pools)
        assert eval voice_manifest['speakers']['seran']['voice_name'] == 'Rosa Oh'
        assert eval voice_manifest['speakers']['oknyeo']['voice_name'] == 'Yoojin Kim'
        assert eval voice_manifest['speakers']['danju']['voice_name'] == 'JooHwan'
        assert eval voice_manifest['speakers']['hyunma']['voice_name'] == 'Shin'
        assert eval voice_manifest['speakers']['younghun']['voice_name'] == 'HoCho'
        run Start('test_probe')
        advance until eval block_id == 900
        pause 0.8
        assert eval renpy.music.get_playing(channel='utterance') in voice_pools['miran']
        keysym "K_RETURN"
        pause 0.07
        assert eval not renpy.music.is_playing(channel='utterance')
        advance until eval block_id == 901
        pause 0.8
        assert eval not renpy.music.is_playing(channel='utterance')

init python:
    def verify_voice_tail():
        store.voice_reveal_deadline = renpy.get_game_runtime() - 1.0
        renpy.music.play('audio/miran_selly/frustrated.ogg', channel='utterance')
        voice_callback('slow_done')
        assert renpy.music.get_playing(channel='utterance') == 'audio/miran_selly/frustrated.ogg', 'Natural text completion cut the vocal reaction short.'
        store.voice_reveal_deadline = renpy.get_game_runtime() + 10.0
        voice_callback('slow_done')

testsuite voice_tail:
    setup:
        $ _test.timeout = 10.0
    teardown:
        $ stop_utterance()
        exit
    testcase natural_reveal_keeps_tail:
        $ verify_voice_tail()
        pause 0.07
        assert eval not renpy.music.get_playing(channel="utterance")
