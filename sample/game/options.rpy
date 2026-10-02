init -30 python:
    # NVIDIA/XWayland can block buffer presentation for >11 seconds. Use the
    # same supported override verified in the user's native playback, before
    # the renderer chooses its swap interval. Explicit caller settings win.
    if renpy.linux:
        import os
        os.environ.setdefault("RENPY_GL_VSYNC", "0")

init -20 python:
    gui.init(1920, 1080)

define config.name = "화분 · 푸른 집"
define config.language = "korean"
define config.version = "0.3.0-episode1"
define build.name = "HwabunGarden"
define config.save_directory = "HwabunGarden-20261002"
define config.window_title = "화분 — 제1화 푸른 집"
define config.has_music = True
define config.has_sound = True
define config.has_voice = True
define config.check_conflicting_properties = True
define config.history_length = 250
define config.default_text_cps = 28
define config.default_afm_time = 14
define config.window = "auto"
define config.enter_transition = Dissolve(0.2)
define config.exit_transition = Dissolve(0.2)
define config.after_load_transition = Dissolve(0.2)
define config.end_game_transition = Fade(0.3, 0.1, 0.3)
define config.default_music_volume = 0.45
define config.default_sfx_volume = 0.55
define config.default_voice_volume = 0.25
define config.main_menu_music = "audio/main_gymnopedie.ogg"
default persistent.utterances = False
default scene_title = "S01 라일락 곁의 자매"
default block_id = 0
default sample_complete = False
default c01_choice = None

init python:
    config.keymap['game_menu'] = ['K_ESCAPE', 'mouseup_3']
    config.keymap['hide_windows'].append('K_h')
    build.classify('tests/**', None)
    build.classify('game/test_*.rpy', None)
    build.classify('game/test_*.rpyc', None)
    build.classify('game/saves/**', None)
    build.classify('**/__pycache__/**', None)
    build.classify('**.log', None)
    build.classify('**.pyc', None)
    build.classify('**.bak', None)
    build.classify('errors.txt', None)
    build.classify('traceback.txt', None)
    build.classify('log.txt', None)
    build.classify('game/cache/**', None)
    build.documentation('README.txt')
