testsuite weather:
    setup:
        $ _test.timeout = 20.0
        $ preferences.afm_enable = False
        $ preferences.text_cps = 0
        $ config.skipping = None
    teardown:
        $ set_weather('off', fade=0.0)
        exit
    testcase indoor_outdoor_scene_audio:
        run Start('sample_s04')
        advance until eval block_id == 196
        pause 2.1
        assert eval weather_place == 'outside' and weather_levels == (0.0, 0.42)
        assert eval renpy.music.get_playing(channel='weather_wind') == 'audio/storm_wind_outside.ogg'
        advance until eval block_id == 230
        pause 2.1
        assert eval weather_place == 'inside' and weather_levels == (0.0, 0.12)
        assert eval renpy.music.get_playing(channel='weather_wind') == 'audio/storm_wind_inside.ogg'
        advance until eval block_id == 301
        pause 0.2
        assert eval renpy.music.get_playing(channel='sound') == 'audio/thunder_cinema.ogg'
        pause 2.1
        assert eval renpy.music.get_playing(channel='ambience') == 'audio/projector.ogg'
        assert eval renpy.music.get_playing(channel='weather_rain') == 'audio/storm_rain_inside.ogg'
        advance until eval block_id == 305
        pause 2.1
        assert eval weather_place == 'outside' and weather_levels == (0.85, 0.70)
        assert eval renpy.music.get_playing(channel='weather_rain') == 'audio/storm_rain_outside.ogg'
        advance until eval block_id == 317
        pause 2.1
        assert eval weather_place == 'inside' and weather_levels == (0.25, 0.20)
        assert eval renpy.music.get_playing(channel='weather_rain') == 'audio/storm_rain_inside.ogg'
        advance until eval block_id == 412
        pause 2.1
        assert eval weather_levels == (0.06, 0.03)
        advance until screen "sample_end"
        pause 1.7
        assert eval not renpy.music.is_playing(channel='weather_rain')
        assert eval not renpy.music.is_playing(channel='weather_wind')
