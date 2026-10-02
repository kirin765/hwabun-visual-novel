"""Offline auditions from cached neural vowel sources; never modifies game assets."""
import array, hashlib, html, json, math, wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / 'voice-v2'
SR = 24000
PROFILES = json.loads((SOURCE / 'manifest.json').read_text())['profiles']
SPEAKERS = ['miran', 'seran', 'danju', 'hyunma', 'younghun', 'gaya', 'oknyeo']
VARIANTS = [('short', '짧고 가볍게', 100), ('medium', '보통 길이', 180), ('long', '여유 있는 길이', 300)]

def read(path):
    with wave.open(str(path)) as w:
        assert (w.getframerate(), w.getnchannels(), w.getsampwidth()) == (SR, 1, 2)
        return [v / 32768 for v in array.array('h', w.readframes(w.getnframes()))]

def write(path, samples):
    assert samples and max(map(abs, samples)) < 1
    with wave.open(str(path), 'wb') as w:
        w.setparams((1, 2, SR, 0, 'NONE', 'not compressed'))
        w.writeframes(array.array('h', (round(v * 32767) for v in samples)).tobytes())

records, cards = [], []
for sid in SPEAKERS:
    rows = []
    for variant, label, duration in VARIANTS:
        clips, controls = [], []
        for vowel, korean in [('a', '아'), ('eo', '어'), ('eu', '으')]:
            src = SOURCE / 'sources' / f'{sid}_{vowel}.wav'
            raw = read(src)
            energy = [sum(v*v for v in raw[i:i+240]) / len(raw[i:i+240]) for i in range(0, len(raw), 240)]
            active = [i for i, e in enumerate(energy) if e > max(energy) * .0144]
            assert active
            start, end = active[0]*240, min(len(raw), (active[-1]+1)*240)
            n = min(round(duration * SR / 1000), end-start)
            clip = raw[start:start+n]
            for i in range(n):
                clip[i] *= math.sin(min(1, i/(SR*.008))*math.pi/2)**2 * math.sin(min(1, (n-1-i)/(SR*.025))*math.pi/2)**2
            gain = .20 / max(map(abs, clip))
            clip = [v*gain for v in clip]
            name = f'{sid}_{variant}_{vowel}.wav'
            write(ROOT / name, clip)
            assert clip[0] == clip[-1] == 0
            records.append(dict(file=name, speaker=sid, variant=variant, vowel=korean, duration_ms=round(n/SR*1000), source=str(src.relative_to(ROOT.parent)), source_sha256=hashlib.sha256(src.read_bytes()).hexdigest()))
            clips.append(clip)
            controls.append(f'<label>{korean}<audio controls preload="none" src="{name}"></audio></label>')
        sequence = []
        for clip in clips:
            sequence.extend(clip)
            sequence.extend([0.] * round(.7*SR))
        name = f'{sid}_{variant}_sequence.wav'
        write(ROOT / name, sequence)
        rows.append(f'<section><h3>{label}</h3><audio controls preload="none" src="{name}"></audio><details><summary>개별 아·어·으</summary>{"".join(controls)}</details></section>')
    cards.append(f'<article><h2>{html.escape(PROFILES[sid]["name"])}</h2><div class="grid">{"".join(rows)}</div></article>')

(ROOT / 'preview.html').write_text('''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>화분 발성 추가 샘플</title><style>body{max-width:1100px;margin:40px auto;padding:20px;background:#17221f;color:#eee;font-family:sans-serif}article{padding:20px;margin:20px 0;background:#263630;border-radius:12px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px}audio{max-width:100%;display:block;margin:12px 0}button{padding:12px}</style><h1>화분 · 아·어·으 추가 샘플</h1><p>7명 × 3가지 길이. 각 재생기는 아 → 어 → 으 순서입니다. 기존 TTS 원본에서 추출한 비교 시안으로, 새 성우나 감정 연기를 녹음한 것은 아닙니다. 긴 버전도 원음보다 늘리지 않습니다.</p><button onclick="document.querySelectorAll('audio').forEach(a=>{a.pause();a.currentTime=0})">모두 중단</button>''' + ''.join(cards) + '''<script>document.querySelectorAll('audio').forEach(a=>{a.volume=.65;a.addEventListener('play',()=>document.querySelectorAll('audio').forEach(b=>{if(b!==a)b.pause()}))})</script></html>''')
(ROOT / 'manifest.json').write_text(json.dumps(dict(status='audition-only-not-applied-to-game', source='cached voice-v2 neural TTS', assets=records), ensure_ascii=False, indent=2))
print(f'Created {len(records)} vowel clips and {len(SPEAKERS)*len(VARIANTS)} comparison sequences; mono PCM, no clipping, zero endpoints verified.')
