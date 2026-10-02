"""Deterministic procedural S03/S04 ambience; no voices or borrowed recordings."""
import hashlib, json, subprocess, wave
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'sample/game/audio'
SR = 24000
rng = np.random.default_rng(20261003)
records = []
def save(name, y):
    y = np.asarray(y, dtype=float)
    n = min(1000, len(y)//2)
    y[:n] *= np.linspace(0, 1, n)
    y[-n:] *= np.linspace(1, 0, n)
    assert np.max(np.abs(y)) < 1
    wav, ogg = OUT / (name+'.wav'), OUT / (name+'.ogg')
    with wave.open(str(wav), 'wb') as w:
        w.setparams((1, 2, SR, 0, 'NONE', 'not compressed'))
        w.writeframes((y*32767).astype('<i2').tobytes())
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(wav),'-c:a','libvorbis','-q:a','5',str(ogg)],check=True)
    wav.unlink()
    records.append(dict(file='audio/'+ogg.name, duration_seconds=len(y)/SR, sha256=hashlib.sha256(ogg.read_bytes()).hexdigest(), source='original deterministic procedural synthesis', human_voice=False))
def noise(seconds): return rng.normal(0, .1, round(seconds*SR))
def smooth(y, n): return np.convolve(y, np.ones(n)/n, mode='same')
t = np.arange(SR*24)/SR
rain = noise(24)*.38 + smooth(noise(24), 12)*.8
rain *= .85+.15*np.sin(t*.47)
save('rain', rain)
t = np.arange(SR*4)/SR
save('thunder', smooth(noise(4), 180)*5*np.exp(-t*.9))
t = np.arange(SR*16)/SR
save('projector', (smooth(noise(16),5)*.4+np.sin(2*np.pi*72*t)*.008)*(0.5+0.5*np.sin(2*np.pi*12*t)**8))
t = np.arange(SR*2)/SR
save('tram_bell', (np.sin(2*np.pi*740*t)+.35*np.sin(2*np.pi*1220*t))*.08*np.exp(-t*4))
save('radio_noise', noise(1.2)*.18)
t = np.arange(SR*2)/SR
save('tableware', (np.sin(2*np.pi*1700*t)*.055+np.sin(2*np.pi*2900*t)*.02)*np.exp(-t*9))
t = np.arange(round(SR*.8))/SR
save('match', noise(.8)*np.exp(-t*9))
(ROOT/'docs/s03-s04/audio-manifest.json').write_text(json.dumps(records,indent=2))
print('Generated 7 procedural ambience/effects; no clipping or character voices.')
