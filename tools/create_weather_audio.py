"""Original weather loops and muffled thunder; no external recordings.
Run: uv run --with numpy python tools/create_weather_audio.py
"""
import hashlib, json, subprocess, wave
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'sample/game/audio'
SR = 24000
SECONDS = 48
rng = np.random.default_rng(20261004)
n = SR * SECONDS
t = np.arange(n) / SR
freq = np.fft.rfftfreq(n, 1 / SR)

def filtered_noise(low, high):
    spectrum = np.fft.rfft(rng.normal(size=n))
    response = (1 - np.exp(-(freq / low)**2)) / (1 + (freq / high)**4)
    y = np.fft.irfft(spectrum * response, n=n)
    return y / np.std(y)

rain = filtered_noise(220, 8500) * .085
rain *= .85 + .10*np.cos(2*np.pi*t/12) + .05*np.sin(2*np.pi*t/24)
# Periodic envelopes keep the 48-second seam continuous; gusts move across stereo.
gust = .55 + .25*np.cos(2*np.pi*t/16) + .20*np.sin(2*np.pi*t/24)**2
wind = filtered_noise(35, 1100) * .085 * gust
pan = .15 * np.sin(2*np.pi*t/24)
records = []

def muffled(y):
    return np.fft.irfft(np.fft.rfft(y) / (1 + (freq/700)**4), n=n)

def save(name, y):
    assert np.max(np.abs(y)) < .95
    wav = OUT / (name + '.wav'); ogg = wav.with_suffix('.ogg')
    with wave.open(str(wav), 'wb') as w:
        w.setparams((2, 2, SR, 0, 'NONE', 'not compressed'))
        w.writeframes((y*32767).astype('<i2').tobytes())
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(wav),'-c:a','libvorbis','-q:a','5',str(ogg)],check=True)
    wav.unlink()
    records.append(dict(file='audio/'+ogg.name, duration_seconds=len(y)/SR, channels=2,
                        sha256=hashlib.sha256(ogg.read_bytes()).hexdigest(),
                        source='original deterministic procedural synthesis', human_voice=False))

save('storm_rain_outside', np.column_stack((rain*(1-pan), rain*(1+pan))))
save('storm_wind_outside', np.column_stack((wind*(1+pan), wind*(1-pan))))
save('storm_rain_inside', np.column_stack((muffled(rain), muffled(rain))))
save('storm_wind_inside', np.column_stack((muffled(wind), muffled(wind))))
# The single screenplay thunder cue is heard from inside the apartment.
src = OUT/'thunder.ogg'; dest = OUT/'thunder_inside.ogg'
subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-af','lowpass=f=650,volume=0.45','-c:a','libvorbis','-q:a','5',str(dest)],check=True)
records.append(dict(file='audio/'+dest.name,sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),source='original thunder.ogg; lowpass 650Hz, gain 0.45',human_voice=False))
(ROOT/'docs/s03-s04/weather-manifest.json').write_text(json.dumps(records,indent=2)+'\n')
print('Generated four 48-second stereo weather loops and indoor thunder.')
