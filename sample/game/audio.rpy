init -10 python:
    import json
    import random
    from voice_policy import Pulse, choose_clip, allow_density
    renpy.music.register_channel('ambience', mixer='sfx', loop=True)
    renpy.music.register_channel('birds', mixer='sfx', loop=True)
    renpy.music.register_channel('utterance', mixer='voice', loop=False, tight=True)
    # Only user-approved generated clips are enabled by this manifest.
    voice_manifest = json.loads(renpy.file('audio/voices.json').read())
    voice_pools = {}
    for speaker, entry in voice_manifest['speakers'].items():
        clips = entry.get('clips', [])
        if entry.get('approved') and entry.get('commercial_evidence') and len(set(clips)) >= 6:
            if all(renpy.loadable(p) for p in clips):
                voice_pools[speaker] = clips
    voices_ready = bool(voice_pools)
    voice_previous = {}
    voice_pulse = None
    voice_speaker = None
    voice_generation = 0
    voice_suppress_once = False

    def stop_utterance():
        if store.voice_pulse is not None:
            store.voice_pulse.stop()
        renpy.music.stop(channel='utterance', fadeout=0.02)

    def voice_callback(event, interact=True, who=None, **kwargs):
        if not interact:
            return
        if event == 'begin':
            begin_character_motion(who)
            stop_utterance()
            store.voice_generation += 1
            store.voice_speaker = who
            text = kwargs.get('what', '')
            store.voice_reveal_deadline = renpy.get_game_runtime() + (len(text) / preferences.text_cps if preferences.text_cps > 0 else 0.0)
            enabled = (who in voice_pools and persistent.utterances
                       and not renpy.is_skipping() and not store.voice_suppress_once)
            store.voice_pulse = Pulse(kwargs.get('what', ''), preferences.text_cps, enabled)
            store.voice_suppress_once = False
        elif event == 'slow_done':
            if store.voice_pulse is not None:
                store.voice_pulse.stop()
            # Natural completion stops scheduling, but lets the current reaction finish.
            # Clicking to reveal the text early still cancels the reaction immediately.
            if renpy.get_game_runtime() + 0.08 < store.voice_reveal_deadline:
                stop_utterance()
        elif event == 'end':
            stop_utterance()

    def utterance_pool(speaker):
        available = voice_pools.get(speaker, [])
        entry = voice_manifest['speakers'].get(speaker, {})
        emotion = entry.get('dialogue_emotions', {}).get(str(block_id))
        kinds = entry.get('emotion_clips', {})
        selected = kinds.get(emotion, []) if emotion else sum((kinds.get(k, []) for k in ('neutral', 'hesitant', 'curious')), [])
        return [p for p in selected if p in available] or available

    class VoicePulseDisplayable(renpy.Displayable):
        def __init__(self, generation, **kwargs):
            super(VoicePulseDisplayable, self).__init__(**kwargs)
            self.generation = generation
        def render(self, width, height, st, at):
            if renpy.is_skipping() or renpy.get_screen('preferences') or not persistent.utterances:
                stop_utterance()
            elif self.generation == store.voice_generation and store.voice_pulse:
                if store.voice_pulse.tick(st):
                    sid = store.voice_speaker
                    clip = choose_clip(utterance_pool(sid), voice_previous.get(sid), random.choice)
                    if clip and not renpy.music.is_playing(channel='utterance'):
                        allowed = allow_density(store.voice_trigger_count, store.voice_density)
                        store.voice_trigger_count += 1
                        if allowed:
                            voice_previous[sid] = clip
                            renpy.music.play(clip, channel='utterance')
            renpy.redraw(self, 0.02)
            return renpy.Render(0, 0)

    def audio_interaction_guard():
        if renpy.is_skipping() or renpy.context()._menu:
            stop_utterance()
    config.interact_callbacks.append(audio_interaction_guard)

define miran = Character("미란", who_color="#a6cbbf", callback=renpy.curry(voice_callback)(who='miran'))
define seran = Character("세란", who_color="#d5b4cc", callback=renpy.curry(voice_callback)(who='seran'))
define oknyeo = Character("옥녀", who_color="#d8bc95", callback=renpy.curry(voice_callback)(who='oknyeo'))
define inner = Character(None, what_color="#e2e6db", callback=voice_callback)
define danju = Character("단주", who_color="#b1c0d7", callback=renpy.curry(voice_callback)(who='danju'))
define hyunma = Character("현마", who_color="#cfb59a", callback=renpy.curry(voice_callback)(who='hyunma'))
define younghun = Character("영훈", who_color="#bdd2bd", callback=renpy.curry(voice_callback)(who='younghun'))
define radio = Character("라디오", who_color="#c1c3c0", callback=voice_callback)
define driver = Character("운전수", who_color="#c1c3c0", callback=voice_callback)

default voice_trigger_count = 0
default voice_reveal_deadline = 0.0
define voice_density = 1.0

label after_load:
    $ stop_utterance()
    $ voice_suppress_once = True
    return

label before_main_menu:
    if not persistent.original_voice_frequency_restored:
        $ persistent.utterances = True
        $ preferences.set_mute('voice', False)
        if preferences.get_volume('voice') <= 0:
            $ preferences.set_volume('voice', config.default_voice_volume)
        if preferences.text_cps <= 0:
            $ preferences.text_cps = config.default_text_cps
        $ persistent.original_voice_frequency_restored = True
    if not persistent.miran_selly_enabled:
        $ persistent.utterances = True
        $ persistent.miran_selly_enabled = True
    return
