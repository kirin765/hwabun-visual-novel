init -15 python:
    import math

    def begin_character_motion(speaker):
        store.motion_previous = store.motion_speaker
        store.motion_speaker = speaker
        store.motion_changed_at = renpy.get_game_runtime()

    def character_motion(trans, st, at, speaker, expression):
        if not persistent.character_motion or renpy.is_skipping():
            trans.xoffset = 0
            trans.yoffset = 0
            trans.rotate = 0
            return 0.1
        # Leave the last pose in place while reading a menu.
        if renpy.context()._menu:
            return 0.1
        phase = {'miran':0.0, 'seran':1.1, 'oknyeo':2.2, 'danju':0.7, 'hyunma':1.8}[speaker]
        now = renpy.get_game_runtime()
        blend = min(1.0, max(0.0, (now - motion_changed_at) / 0.22))
        blend = blend * blend * (3.0 - 2.0 * blend)
        emphasis = (blend if motion_speaker == speaker else 0.0)
        emphasis += (1.0 - blend if motion_previous == speaker else 0.0)
        # Animate only composite transforms; the source portrait is unchanged.
        breath = math.sin(st * 1.45 + phase)
        trans.yoffset = 3.5 * breath - 7.0 * emphasis
        trans.xoffset = 1.5 * math.sin(st * 0.75 + phase)
        trans.rotate = 0.035 * breath
        if expression == 'startled' and st < 0.65:
            trans.xoffset += 10.0 * math.sin(st * 32.0) * (1.0 - st / 0.65)
        return 1.0 / 30.0

default motion_speaker = None
default motion_previous = None
default motion_changed_at = 0.0
default persistent.character_motion = True
