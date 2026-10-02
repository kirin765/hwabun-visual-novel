#!/usr/bin/env python3
"""Offline audition assets only. Python stdlib; no engine or recorded voices."""
import array, html, json, math, random, re, unicodedata, wave
from pathlib import Path
ROOT = Path(__file__).resolve().parent
SR = 24000
# id, name, fundamental, duration ms, formant scale, harmonic rolloff, level
ROWS = [
 ('miran','미란',240,74,1.08,1.35,.90),
 ('seran','세란',205,86,.88,1.70,.94),
 ('danju','단주',165,78,1.04,1.85,.92),
 ('hyunma','현마',110,90,.75,1.10,.86),
 ('younghun','영훈',140,70,1.12,1.15,.88),
 ('gaya','가야',220,82,1.18,1.95,.88),
 ('oknyeo','옥녀',255,60,1.15,1.40,.84),
 ('gapjae','갑재',125,62,.90,1.05,.85),
 ('jukseok','죽석',210,68,.94,1.65,.90),
 ('mantae','만태',135,88,.82,1.80,.92),
 ('support_low','조연 낮은 발성',155,80,.92,1.65,.88),
 ('support_light','조연 가벼운 발성',225,68,1.09,1.75,.86),
]
PROFILES = {r[0]:dict(zip(('id','name','f0_hz','duration_ms','formant_scale','rolloff','level'),r)) for r in ROWS}
PROFILES['radio'] = dict(PROFILES['support_low'], id='radio',name='라디오',radio=True)
VOWELS = {'a':(730,1090,2440),'eo':(520,1190,2390),'eu':(350,1450,2500)}

def synth(p, vowel, pitch=1, length=1, seed=0):
    n=round(SR*max(60,min(90,p['duration_ms']*length))/1000)
    f0=p['f0_hz']*pitch
    rng=random.Random(seed)
    harmonics=[]
    for k in range(1,min(65,int(5000/f0))+1):
        freq=k*f0
        resonances=sum(w*math.exp(-.5*((freq-center*p['formant_scale'])/bw)**2)
                       for center,bw,w in zip(VOWELS[vowel],(140,190,260),(1,.6,.22)))
        weight=(.075+resonances)/k**p['rolloff']
        if p.get('radio'):
            weight*= (1-math.exp(-(freq/330)**4))*math.exp(-(freq/2700)**6)
        harmonics.append((freq,weight,rng.uniform(-.18,.18)))
    out=[]
    noise_low=0.0; noise_slow=0.0
    for i in range(n):
        t=i/SR
        value=sum(w*math.sin(2*math.pi*f*t+phase) for f,w,phase in harmonics)
        if p.get('radio'):
            noise_low += .45*(rng.uniform(-.006,.006)-noise_low)
            noise_slow += .08*(noise_low-noise_slow)
            value += noise_low-noise_slow
        # 8 ms attack and 16 ms release; zero endpoints.
        env=math.sin(math.pi/2*min(1,i/(SR*.008)))**2
        env*=math.sin(math.pi/2*min(1,(n-1-i)/(SR*.016)))**2
        out.append(value*env)
    peak=max(map(abs,out))
    return [x/peak*.22*p['level'] for x in out]

def write(name,data):
    assert max(map(abs,data),default=0)<1
    path=ROOT/name
    with wave.open(str(path),'wb') as w:
        w.setparams((1,2,SR,0,'NONE','not compressed'))
        w.writeframes(array.array('h',(round(x*32767) for x in data)).tobytes())
    return name

def events(text, kind='spoken', mute=False, char_ms=55):
    if kind!='spoken' or mute: return []
    eligible=0; last=-100; result=[]
    for i,c in enumerate(unicodedata.normalize('NFC',text)):
        if not c.isalnum(): continue
        eligible+=1
        when=i*char_ms
        if eligible%2==0 and when-last>=100:
            result.append(when); last=when
    return result

def phrase(p,text,mix=False):
    data=[0.] * round((len(text)*.055+.35)*SR)
    for j,ms in enumerate(events(text)):
        grain=synth(p,list(VOWELS)[j%3],1+(-.016,.009,.022,-.008)[j%4],
                    (1,.95,1)[j%3],j+17)
        start=round(ms*SR/1000)
        for i,x in enumerate(grain): data[start+i]+=x*.25
    if mix:
        rng=random.Random(41); rain=0
        for i in range(len(data)):
            t=i/SR
            rain=.8*rain+.2*rng.uniform(-1,1)
            # Synthetic listening bed; not the project's M01/M03/A04.
            note=(220,261.63,329.63,293.66)[int(t/.65)%4]
            phase=t%.65
            piano=sum(math.sin(2*math.pi*note*k*t)/k**2 for k in (1,2,3))*math.exp(-phase*7)
            data[i]+=rain*.023+piano*.009
    return data

def main():
    manifest={'version':1,'status':'audition-draft','sample_rate':SR,
              'defaults':{'enabled':True,'volume':.25,'minimum_interval_ms':100,'eligible_chars_per_grain':2},
              'speaker_aliases':{'음악가':'younghun','운전수':'support_low','점원':'support_light','역무원':'support_low','관리인':'support_low','이모':'support_light','애영':'support_light','라디오':'radio'},
              'profiles':PROFILES,'assets':[],'auditions':[]}
    # Produce the episode-one reference set first, then extend the same synthesis.
    for sid,p in PROFILES.items():
        for v in VOWELS:
            name=write(f'{sid}_{v}.wav',synth(p,v,seed=7))
            manifest['assets'].append({'speaker':sid,'variant':v,'file':name})
    script = (ROOT.parents[1]/'1화대본.md').read_text()
    body = script.split('## S01',1)[1].split('## 제작 확인 메모',1)[0]
    blocks = [b for b in body.split('\n\n') if re.match(r'^(미란 속말|미란|세란|단주|현마|옥녀|운전수|라디오):', b)]
    picks = {'miran':52, 'seran':9, 'danju':136, 'hyunma':139, 'oknyeo':89}
    actual = {sid: blocks[i].split(': ',1)[1].replace('\n',' ') for sid,i in picks.items()}
    for sid,i in picks.items():
        assert blocks[i].startswith(PROFILES[sid]['name']+': ')
    common = blocks[391].split(': ',1)[1]+' '+blocks[394].split(': ',1)[1]
    for sid,text in actual.items():
        for label,words in [('같은 문장',common),('실제 1화',text)]:
            suffix='common' if label=='같은 문장' else 'episode1'
            name=write(f'{sid}_{suffix}.wav',phrase(PROFILES[sid],words))
            manifest['auditions'].append({'speaker':sid,'label':label,'text':words,'file':name})
    long=blocks[225].split(': ',1)[1].replace('\n',' ')+' '+common+' '+common
    for label,words,mix in [('긴 대사 반복',long,False),('피아노·비와 함께',long,True)]:
        name=write('miran_'+('mixed' if mix else 'long')+'.wav',phrase(PROFILES['miran'],words,mix))
        manifest['auditions'].append({'speaker':'miran','label':label,'text':words,'file':name})
    name=write('radio_episode1.wav',phrase(PROFILES['radio'],blocks[336].split(': ',1)[1].split('\n')[0]))
    manifest['auditions'].append({'speaker':'radio','label':'실제 1화 라디오','text':blocks[336].split(': ',1)[1].split('\n')[0],'file':name})
    (ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    cards=[]
    for a in manifest['auditions']:
        cards.append(f'<article><h2>{PROFILES[a["speaker"]]["name"]} · {a["label"]}</h2><p>{html.escape(a["text"])}</p><audio controls preload="none" src="{a["file"]}"></audio></article>')
    # Common-sentence clips in a fixed hidden order for face-free comparison.
    blind=''.join(f'<article><h2>소리 {i+1}</h2><audio controls preload="none" src="{sid}_common.wav"></audio></article>' for i,sid in enumerate(['danju','oknyeo','hyunma','miran','seran']))
    extras=''.join(f'<article><h2>{p["name"]} · 세 발성</h2>'+''.join(f'<p>{v}<br><audio controls preload="none" src="{sid}_{v}.wav"></audio></p>' for v in VOWELS)+'</article>' for sid,p in PROFILES.items())
    (ROOT/'preview.html').write_text('''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>화분 발성 비교 시청본</title><style>body{max-width:900px;margin:40px auto;padding:0 20px;background:#f3eee4;color:#292c29;font:18px/1.6 sans-serif}article{border-top:1px solid #bbb;padding:16px 0}audio{width:100%;max-width:500px}button,input{font:inherit}h2{font-size:22px}label{display:inline-block;margin:12px}button{padding:8px}</style><h1>화분 발성 비교 시청본 v1</h1><p>합성 발성 초안입니다. 문장을 읽는 음성이 아닙니다. 먼저 같은 문장으로 1화 다섯 인물을 비교하고 실제 대사를 들어보세요. 원본 음원은 외부 녹음 없이 새로 합성했습니다.</p><label><input id="enabled" type="checkbox" checked>대사 효과음 켜기</label><label>별도 음량 <input id="volume" type="range" min="0" max="1" step="0.01" value="0.25"><output id="value">25%</output></label><button id="stop">모두 중단</button><p>미리 듣기 전용 설정입니다. 파일의 대사 비교 음원에는 낮은 기본 음량 25%가 이미 적용되어 있어 슬라이더 25%를 기준으로 조절합니다. 혼합 음원에서는 피아노·비도 함께 조절됩니다. 게임 설정은 아직 구현하지 않았습니다.</p><p><a href="episode1-comparison.mp4">1화 다섯 인물 비교 영상 보기</a></p><h2>이름을 가린 비교</h2>'''+blind+'''<details><summary>정답 보기</summary>1 단주 / 2 옥녀 / 3 현마 / 4 미란 / 5 세란</details><h2>같은 문장과 실제 1화 대사</h2>'''+''.join(cards)+'''<h2>인물별 개별 발성 · 나머지 인물은 확장 초안</h2>'''+extras+'''<script>
const audios=[...document.querySelectorAll('audio')], enabled=document.querySelector('#enabled'), volume=document.querySelector('#volume');
function stop(){audios.forEach(a=>{a.pause();a.currentTime=0;});}
function update(){document.querySelector('#value').textContent=Math.round(volume.value*100)+'%';audios.forEach(a=>{a.muted=!enabled.checked;a.volume=Math.min(1,Number(volume.value)/(a.src.match(/_(common|episode1|long|mixed)\\.wav$/)?.25:1));});if(!enabled.checked)stop();}
audios.forEach(a=>a.addEventListener('play',()=>{if(!enabled.checked){a.pause();return;}audios.forEach(b=>{if(b!==a){b.pause();b.currentTime=0;}});}));
enabled.addEventListener('change',update);volume.addEventListener('input',update);document.querySelector('#stop').addEventListener('click',stop);document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});window.addEventListener('pagehide',stop);update();
</script></html>''')
    # Objective asset / rule verification; engine interaction checks remain pending.
    for a in manifest['assets']:
        with wave.open(str(ROOT/a['file'])) as w:
            samples=array.array('h',w.readframes(w.getnframes()))
            assert w.getframerate()==SR and w.getnchannels()==1
            assert .060<=len(samples)/SR<=.090
            assert samples[0]==samples[-1]==0 and max(map(abs,samples))<32767
    for kind in ('inner','narration','letter','choice','instruction','song'):
        assert events(common,kind)==[]
    assert events(common,mute=True)==[] and events('…… ! ? —')==[]
    assert events('가 나,다. 라')==[110,385]
    for speed in (10,35,55,100):
        e=events(long,char_ms=speed)
        assert all(b-a>=100 for a,b in zip(e,e[1:]))
    report={'asset_count':len(manifest['assets']),'audition_count':len(manifest['auditions']),
            'checks_passed':['PCM mono 24kHz','60–90ms','zero endpoints','no clipping','nonspoken and mute silence','punctuation excluded','100ms minimum interval'],
            'pending':['subjective listening','engine skip/instant/menu/auto/off interaction checks']}
    (ROOT/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__': main()
