#!/usr/bin/env python3
"""Original sample score and procedural foley. No third-party recordings or voices.
Run: uv run --with numpy python tools/create_audio.py
"""
from pathlib import Path
import json, subprocess, wave, hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'sample/game/audio'
SR=44100
rng=np.random.default_rng(20261002)
records=[]
def save(name,y,description):
    y=np.asarray(y,dtype=float)
    n=min(len(y)//2,2205)
    y[:n]*=np.linspace(0,1,n);y[-n:]*=np.linspace(1,0,n)
    peak=np.max(np.abs(y))
    if peak>.85:y*=.85/peak
    wav=OUT/(name+'.wav');ogg=OUT/(name+'.ogg')
    with wave.open(str(wav),'wb') as w:
        w.setparams((1,2,SR,0,'NONE','not compressed'));w.writeframes((y*32767).astype('<i2').tobytes())
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(wav),'-c:a','libvorbis','-q:a','5',str(ogg)],check=True)
    wav.unlink()
    records.append(dict(file='audio/'+ogg.name,seconds=round(len(y)/SR,3),sha256=hashlib.sha256(ogg.read_bytes()).hexdigest(),source='tools/create_audio.py',description=description,method='original deterministic procedural synthesis; agent-authored',third_party_samples=False,ai_assisted=True,usage='Created for this project; no third-party recording license required. No claim of exclusive copyright.'))
def time(n):return np.arange(round(n*SR))/SR
def noise(n):return rng.normal(0,1,round(n*SR))
def smooth(x,n):return np.convolve(x,np.ones(n)/n,mode='same')
def piano(midi,dur=4):
    t=time(dur); f=440*2**((midi-69)/12)
    y=np.zeros(len(t))
    for h,a in enumerate([1,.45,.22,.11,.07,.04,.018],1):
        y+=a*np.sin(2*np.pi*f*h*np.sqrt(1+.00008*h*h)*t)*np.exp(-t*(.7+h*.22))
    return y*(1-np.exp(-t*220))*.12
# Original 64-bar sparse pentatonic waltz, ~192 seconds, no borrowed melody.
score=np.zeros(SR*196)
chords=[(48,55,60),(45,52,57),(53,60,65),(43,50,55),(48,55,64),(45,52,60),(50,57,62),(43,55,59)]
melody=[72,76,79,76,74,72,69,67,69,72,76,74,72,69,67,64]
def place(y,at,gain=1):
    start=round(at*SR);end=min(len(score),start+len(y));score[start:end]+=y[:end-start]*gain
for bar in range(64):
    bass,third,fifth=chords[bar%8]
    place(piano(bass),bar*3,.65)
    place(piano(third),bar*3+1,.42);place(piano(fifth),bar*3+2,.38)
    if bar%4!=3:
        place(piano(melody[(bar*3)%16]),bar*3+.06,.75)
        if bar%2==0:place(piano(melody[(bar*3+1)%16]),bar*3+1.52,.48)
# Restrained room resonance, no external impulse response.
for delay,gain in [(.09,.14),(.19,.10),(.31,.07)]:
    n=int(delay*SR);score[n:]+=score[:-n]*gain
save('garden_piano',score,'M01: original gentle pentatonic piano-like waltz, 60 bpm')
t=time(32); wind=smooth(noise(32),80)*(.10+.05*np.sin(t*.7))
wind+=smooth(noise(32),8)*(.007+.009*np.sin(t*.21)**2)
save('leaves',wind,'A01: layered filtered noise, slow leaf rustling loop')
y=np.zeros(SR*29)
for at in [1.4,6.7,12.8,20.3,25.1]:
    for k in range(3):
        t=time(.16);f=2300+650*np.sin(t*19+k); chirp=np.sin(2*np.pi*np.cumsum(f)/SR)*np.sin(np.pi*t/.16)**2*.045
        i=int((at+k*.24)*SR);y[i:i+len(chirp)]+=chirp
save('birds',y,'A01: sparse distant synthesized birds, separate loop')
t=time(1.6);save('grass',smooth(noise(1.6),6)*np.sin(np.pi*t/1.6)**2*.18,'A02: brief dry grass rustle')
y=np.zeros(SR*2)
for at in [.05,.55,1.03,1.52]:
    t=time(.24);step=(smooth(noise(.24),40)*.4+np.sin(2*np.pi*90*t)*.10)*np.exp(-t*22)
    i=int(at*SR);y[i:i+len(step)]+=step
save('steps',y,'A03: four soft wooden footsteps')
t=time(1.2);door=(np.sin(2*np.pi*(170*t+15*t*t))*.025+smooth(noise(1.2),70)*.05)*np.sin(np.pi*t/1.2)
door+=np.sin(2*np.pi*74*t)*np.exp(-t*25)*.2
save('door',door,'A03: wooden door creak and soft latch')
t=time(1.2);glass=sum(np.sin(2*np.pi*f*t)*np.exp(-t*d)*a for f,d,a in [(1700,8,.14),(2710,12,.06),(3990,15,.025)])
save('glass',glass,'A03: water glass gently set on a tray')
t=time(4.5);env=np.sin(np.pi*t/4.5)**2
car=sum(np.sin(2*np.pi*h*(48*t+2*t*t))*a for h,a in [(1,.08),(2,.05),(3,.03),(5,.013)])
car+=smooth(noise(4.5),50)*.10
save('car',car*env,'A06: distant low motor approaching, restrained and short')
(ROOT/'docs/audio-manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
print('Rendered',len(records),'original music/ambience/effect assets')
