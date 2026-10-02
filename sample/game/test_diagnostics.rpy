init python:
    import os
    if os.environ.get('HWABUN_FREEZE_PROBE'):
        # Avoid faulthandler timer: this runtime crashed inside _Py_DumpTracebackThreads.
        # Frame heartbeats + external monitoring suffice to detect presentation stalls.
        import time
        from renpy.display import core as _freeze_core
        _freeze_max_draw = 0.0
        _freeze_original_draw = _freeze_core.Interface.draw_screen
        def freeze_draw(self, *args, **kwargs):
            # HWABUN_FREEZE_PROBE only: native timing; no periodic callback or VSync changes.
            global _freeze_max_draw
            state = {'time':time.time(), 'drawing':True, 'block':store.block_id, 'main_menu':bool(renpy.get_screen('main_menu')), 'preferences':bool(renpy.get_screen('preferences')), 'game_menu':bool(renpy.context()._menu), 'fullscreen':preferences.fullscreen, 'music':renpy.music.get_playing(channel='music'), 'music_position':renpy.music.get_pos(channel='music'), 'volume':preferences.get_volume('music'), 'mute':preferences.get_mute('music'), 'max_draw_seconds':_freeze_max_draw}
            with open(os.environ['HWABUN_FREEZE_PROBE'] + '.heartbeat', 'w') as f:
                f.write(json.dumps(state))
            rv = _freeze_original_draw(self, *args, **kwargs)
            state['drawing'] = False
            state['duration'] = time.time() - state['time']
            _freeze_max_draw = max(_freeze_max_draw, state['duration'])
            state['max_draw_seconds'] = _freeze_max_draw
            if state['duration'] > 1.0:
                with open(os.environ['HWABUN_FREEZE_PROBE'] + '.slow-frames', 'a') as f:
                    f.write(json.dumps(state) + '\n')
            with open(os.environ['HWABUN_FREEZE_PROBE'] + '.heartbeat', 'w') as f:
                f.write(json.dumps(state))
            return rv
        _freeze_core.Interface.draw_screen = freeze_draw
