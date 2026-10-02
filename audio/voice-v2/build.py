#!/usr/bin/env python3
"""Humanlike vowel audition. First run uses Edge neural TTS for isolated vowels only.
Cached sources are retained; subsequent renders are offline. Not a game engine.
Run: uv run --with edge-tts==7.2.8 python audio/voice-v2/build.py
"""
import array, asyncio, hashlib, html, json, math, re, subprocess, unicodedata, wave
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SR=24000
SOURCES=ROOT/'sources'
# Relative character qualities retained, new neural sources replace v1 oscillators.
ROWS=[
 ('miran','미란','ko-KR-SunHiNeural','+0Hz',180),
 ('seran','세란','ko-KR-SunHiNeural','-25Hz',210),
 ('danju','단주','ko-KR-InJoonNeural','+10Hz',190),
 ('hyunma','현마','ko-KR-HyunsuMultilingualNeural','-15Hz',220),
 ('younghun','영훈','ko-KR-InJoonNeural','-5Hz',180),
 ('gaya','가야','ko-KR-SunHiNeural','+6Hz',190),
 ('oknyeo','옥녀','ko-KR-SunHiNeural','+15Hz',160),
 ('gapjae','갑재','ko-KR-HyunsuMultilingualNeural','+0Hz',170),
 ('jukseok','죽석','ko-KR-SunHiNeural','-12Hz',185),
 ('mantae','만태','ko-KR-HyunsuMultilingualNeural','-5Hz',215),
 ('support_low','조연 낮은 발성','ko-KR-InJoonNeural','+0Hz',190),
 ('support_light','조연 가벼운 발성','ko-KR-SunHiNeural','+10Hz',175),
 ('radio','라디오','ko-KR-InJoonNeural','+0Hz',190),
]
VOWELS={'a':'아.','eo':'어.','eu':'으.'}
PROFILES={r[0]:dict(zip(('id','name','source_voice','source_pitch','duration_ms'),r), synthesis='neural-vowel-excerpt', source_rate=('-45%' if r[2]=='ko-KR-InJoonNeural' else '-15%')) for r in ROWS}

def read_wav(path):
    with wave.open(str(path)) as w:
        assert w.getframerate()==SR and w.getnchannels()==1 and w.getsampwidth()==2
        return [x/32768 for x in array.array('h',w.readframes(w.getnframes()))]

def write_wav(path,data):
    samples=array.array('h',(round(max(-1,min(1,x))*32767) for x in data))
    with wave.open(str(path),'wb') as w:
        w.setparams((1,2,SR,0,'NONE','not compressed')); w.writeframes(samples.tobytes())

async def fetch_sources():
    missing=[(sid,v) for sid in PROFILES for v in VOWELS if not (SOURCES/f'{sid}_{v}.mp3').exists()]
    if not missing:return
    import edge_tts
    SOURCES.mkdir(exist_ok=True)
    sem=asyncio.Semaphore(3)
    async def one(sid,v):
        p=PROFILES[sid]
        async with sem:
            path=SOURCES/f'{sid}_{v}.mp3'
            await edge_tts.Communicate(VOWELS[v],p['source_voice'],pitch=p['source_pitch'],rate=p['source_rate']).save(str(path)+'.part')
            Path(str(path)+'.part').replace(path)
            print(f'Generated {sid} {v}',flush=True)
    await asyncio.gather(*(one(*x) for x in missing))

def grain(p,v):
    src=SOURCES/f'{p["id"]}_{v}.mp3'; wav=src.with_suffix('.wav')
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(src),'-ac','1','-ar',str(SR),str(wav)],check=True)
    raw=read_wav(wav); peak=max(map(abs,raw)); assert peak>0.01
    # Find active vowel by 10ms RMS; keep a short contiguous excerpt, no oscillator,
    # pitch shifting, time stretching, looping, vocoder, or synthetic formants.
    step=240
    energy=[math.sqrt(sum(x*x for x in raw[i:i+step])/len(raw[i:i+step])) for i in range(0,len(raw),step)]
    active=[i for i,e in enumerate(energy) if e>max(energy)*.12]
    assert active
    first=max(0,active[0]*step-120); last=min(len(raw),(active[-1]+1)*step+120)
    n=round(p['duration_ms']*SR/1000)
    n=min(n,last-first)
    assert n>=round(.10*SR)
    # Offset slightly inside vowel onset, preserving its unsteady human harmonics.
    start=min(first+round(.025*SR),last-n)
    out=raw[start:start+n]
    for i in range(n):
        attack=min(1,i/(SR*.012)); release=min(1,(n-1-i)/(SR*.024))
        out[i]*=math.sin(attack*math.pi/2)**2*math.sin(release*math.pi/2)**2
    gain=.20/max(map(abs,out)); out=[x*gain for x in out]
    write_wav(ROOT/f'{p["id"]}_{v}.wav',out)
    return out

def events(text,kind='spoken',mute=False,char_ms=55):
    if kind!='spoken' or mute:return []
    eligible=0;last=-260;out=[]
    for i,c in enumerate(unicodedata.normalize('NFC',text)):
        if not c.isalnum():continue
        eligible+=1;t=i*char_ms
        if eligible%4==0 and t-last>=260:out.append(t);last=t
    return out

GRAINS={}
def phrase(sid,text,mix=False):
    data=[0.] * round((len(text)*.055+.35)*SR)
    for j,t in enumerate(events(text)):
        g=GRAINS[sid,list(VOWELS)[j%3]];start=round(t*SR/1000)
        # Alternate gently in level, keep source pitch and original timing.
        gain=.25*(1,.92,.97)[j%3]
        for i,x in enumerate(g): data[start+i]+=x*gain
    if mix:
        import random
        rng=random.Random(41);rain=0
        for i in range(len(data)):
            t=i/SR;rain=.8*rain+.2*rng.uniform(-1,1)
            note=(220,261.63,329.63,293.66)[int(t/.65)%4];phase=t%.65
            piano=sum(math.sin(2*math.pi*note*k*t)/k**2 for k in (1,2,3))*math.exp(-phase*7)
            data[i]+=rain*.023+piano*.009
    return data

def main():
    asyncio.run(fetch_sources())
    for sid,p in PROFILES.items():
        for v in VOWELS:GRAINS[sid,v]=grain(p,v)
    script=(ROOT.parents[1]/'1화대본.md').read_text();body=script.split('## S01',1)[1].split('## 제작 확인 메모',1)[0]
    blocks=[b for b in body.split('\n\n') if re.match(r'^(미란 속말|미란|세란|단주|현마|옥녀|운전수|라디오):',b)]
    picks={'miran':52,'seran':9,'danju':136,'hyunma':139,'oknyeo':89}
    actual={sid:blocks[i].split(': ',1)[1].replace('\n',' ') for sid,i in picks.items()}
    for sid,i in picks.items(): assert blocks[i].startswith(PROFILES[sid]['name']+': ')
    common=blocks[391].split(': ',1)[1]+' '+blocks[394].split(': ',1)[1]
    long=blocks[225].split(': ',1)[1].replace('\n',' ')+' '+common+' '+common
    manifest={'version':2,'status':'audition-draft-awaiting-listening','sample_rate':SR,'defaults':{'enabled':True,'volume':.25,'minimum_interval_ms':260,'eligible_chars_per_grain':4},'profiles':PROFILES,'assets':[],'auditions':[], 'source_script_sha256':hashlib.sha256(script.encode()).hexdigest(),'speaker_aliases':json.loads((ROOT.parent/'voice-v1/manifest.json').read_text())['speaker_aliases'],'source_policy':'Only isolated 아/어/으 sent to neural TTS. No script dialogue uploaded. AI generated voices; no voice cloning.'}
    for sid in PROFILES:
        for v in VOWELS:manifest['assets'].append({'speaker':sid,'variant':v,'file':f'{sid}_{v}.wav','source_file':f'sources/{sid}_{v}.mp3'})
    def audition(sid,label,text,file,mix=False):
        write_wav(ROOT/file,phrase(sid,text,mix));manifest['auditions'].append({'speaker':sid,'label':label,'text':text,'file':file})
    for sid,text in actual.items():
        audition(sid,'같은 문장',common,f'{sid}_common.wav')
        audition(sid,'실제 1화',text,f'{sid}_episode1.wav')
    audition('miran','긴 대사 반복',long,'miran_long.wav')
    audition('miran','피아노·비와 함께',long,'miran_mixed.wav',True)
    audition('radio','실제 1화 라디오',blocks[336].split(': ',1)[1].split('\n')[0],'radio_episode1.wav')
    (ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    cards=''.join(f'<article><h2>{PROFILES[a["speaker"]]["name"]} · {a["label"]}</h2><p>{html.escape(a["text"])}</p><audio controls preload="none" src="{a["file"]}"></audio></article>' for a in manifest['auditions'])
    blind=''.join(f'<article><h2>소리 {i+1}</h2><audio controls preload="none" src="{sid}_common.wav"></audio></article>' for i,sid in enumerate(['danju','oknyeo','hyunma','miran','seran']))
    extra=''.join(f'<article><h2>{p["name"]} · 짧은 모음</h2>'+''.join(f'<p>{v} <audio controls preload="none" src="{sid}_{v}.wav"></audio></p>' for v in VOWELS)+'</article>' for sid,p in PROFILES.items())
    # Reuse proven static player controls and styling, replace the complete content.
    old=(ROOT.parent/'voice-v1/preview.html').read_text();style=old.split('<style>')[1].split('</style>')[0];js=old.split('<script>')[1].split('</script>')[0]
    page=f'''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>화분 사람 발성 비교 v2</title><style>{style}</style><h1>화분 · 짧은 사람 발성 v2</h1><p>AI로 생성한 사람 목소리 모음의 짧은 부분을 사용합니다. 대사를 낭독하지 않습니다. 네 글자마다 발성 기회를 만들고 최소 260ms 간격으로 재생합니다. 인물 구분과 자연스러움은 청취 검토 대기입니다.</p><label><input id="enabled" type="checkbox" checked>대사 효과음 켜기</label><label>별도 음량 <input id="volume" type="range" min="0" max="1" step="0.01" value="0.25"><output id="value">25%</output></label><button id="stop">모두 중단</button><p>문장 비교 음원은 25% 게인이 적용되어 있습니다. 혼합 음량은 배경도 함께 바뀝니다. 한 번에 하나만 재생합니다.</p><p><a href="episode1-comparison.mp4">새 대사·자막 비교 영상</a> · <a href="../voice-v1/preview.html">이전 전자음 v1</a></p><h2>같은 문장으로 전후 비교 · 미란</h2><p>v1 · 전자음 / 두 글자마다, 최소 100ms</p><audio controls preload="none" src="../voice-v1/miran_common.wav"></audio><p>v2 · 사람 발성 / 네 글자마다, 최소 260ms</p><audio controls preload="none" src="miran_common.wav"></audio><h2>이름을 가린 비교</h2>{blind}<details><summary>정답 보기</summary>1 단주 / 2 옥녀 / 3 현마 / 4 미란 / 5 세란</details><h2>같은 문장과 실제 1화 대사</h2>{cards}<h2>인물별 발성 · 후속 인물은 확장 초안</h2>{extra}<script>{js}</script></html>'''
    (ROOT/'preview.html').write_text(page)
    metrics=[]
    for asset in manifest['assets']:
        data=read_wav(ROOT/asset['file']);duration=len(data)/SR
        assert .10<=duration<=.22 and data[0]==data[-1]==0 and max(map(abs,data))<.21
        metrics.append({'file':asset['file'],'duration_ms':round(duration*1000),'peak':round(max(map(abs,data)),4)})
    for a in manifest['auditions']:
        assert max(map(abs,read_wav(ROOT/a['file'])))<1
    for kind in ('inner','narration','letter','choice','instruction','song'):assert events(common,kind)==[]
    assert events(common,mute=True)==[] and events('…… ! ? —')==[]
    for speed in (10,35,55,100):
        e=events(long,char_ms=speed);assert all(b-a>=260 for a,b in zip(e,e[1:]))
    report={'asset_count':len(manifest['assets']),'audition_count':len(manifest['auditions']),'checks_passed':['mono PCM 24kHz 16bit','100–220ms neural excerpts','zero endpoints','no clipping','nonspoken and mute silence','punctuation excluded','260ms minimum interval','script-based captions'],'asset_metrics':metrics,'pending':['subjective listening / character distinction','game engine implementation and interactions'],'source_script_sha256':manifest['source_script_sha256']}
    (ROOT/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='asset_metrics'},ensure_ascii=False))
if __name__=='__main__':main()
