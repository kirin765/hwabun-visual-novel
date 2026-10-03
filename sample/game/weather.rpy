init -9 python:
    renpy.music.register_channel('weather_rain', mixer='sfx', loop=True)
    renpy.music.register_channel('weather_wind', mixer='sfx', loop=True)

    def set_weather(place='off', rain=0.0, wind=0.0, fade=1.5):
        """Separate weather from birds/projector, with indoor low-pass recordings."""
        store.weather_place = place
        store.weather_levels = (rain, wind)
        if place == 'off':
            renpy.music.stop(channel='weather_rain', fadeout=fade)
            renpy.music.stop(channel='weather_wind', fadeout=fade)
            return
        if place not in ('outside', 'inside'):
            raise ValueError('Unknown weather location: ' + place)
        for channel, kind, volume in (
                ('weather_rain', 'rain', rain), ('weather_wind', 'wind', wind)):
            clip = 'audio/storm_%s_%s.ogg' % (kind, place)
            renpy.music.set_volume(volume, delay=fade, channel=channel)
            if renpy.music.get_playing(channel=channel) != clip:
                renpy.music.play(clip, channel=channel, loop=True, fadein=fade, fadeout=fade)

default weather_place = "off"
default weather_levels = (0.0, 0.0)
