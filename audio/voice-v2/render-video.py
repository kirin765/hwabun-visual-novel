#!/usr/bin/env python3
"""Optional captioned MP4 audition. Requires ffmpeg and a Korean font."""
import array, json, subprocess, tempfile, wave
from pathlib import Path
ROOT=Path(__file__).resolve().parent
FONT='/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc'

def main():
    manifest=json.loads((ROOT/'manifest.json').read_text())
    auditions=[a for label in ('같은 문장','실제 1화') for a in manifest['auditions'] if a['label']==label]
    frames=array.array('h'); segments=[]; sr=manifest['sample_rate']
    for a in auditions:
        start=len(frames)/sr
        with wave.open(str(ROOT/a['file'])) as w:
            frames.extend(array.array('h',w.readframes(w.getnframes())))
        frames.extend([0]*int(.55*sr))
        segments.append((start,len(frames)/sr,a))
    with tempfile.TemporaryDirectory(prefix='hwabun-audition-') as tmp:
        tmp=Path(tmp)
        audio=tmp/'combined.wav'
        with wave.open(str(audio),'wb') as w:
            w.setparams((1,2,sr,0,'NONE','not compressed'));w.writeframes(frames.tobytes())
        filters=[]
        for i,(start,end,a) in enumerate(segments):
            name=manifest['profiles'][a['speaker']]['name']
            title=tmp/f'title{i}.txt'; title.write_text(f'{a["label"]} · {name}')
            text=tmp/f'text{i}.txt'
            words=a['text']; lines=[]
            while len(words)>25:
                pos=words.rfind(' ',0,26)
                if pos<10:pos=25
                lines.append(words[:pos]);words=words[pos:].lstrip()
            lines.append(words);text.write_text('\n'.join(lines))
            for path,y,size in ((title,130,44),(text,290,36)):
                filters.append(f"drawtext=expansion=none:fontfile={FONT}:textfile={path}:fontcolor=0xefe5ce:fontsize={size}:line_spacing=18:x=100:y={y}:enable='gte(t,{start})*lt(t,{end})'")
        footer=tmp/'footer.txt';footer.write_text('화분 · 짧은 사람 발성 v2 / 기본 음량 25% / 청취 검토용 초안')
        filters.append(f'drawtext=expansion=none:fontfile={FONT}:textfile={footer}:fontcolor=0xb6bbaa:fontsize=24:x=100:y=620')
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','lavfi','-i',
          f'color=c=0x25352f:s=1280x720:r=12:d={len(frames)/sr}',
          '-i',str(audio),'-vf',','.join(filters),'-c:v','libx264','-preset','fast','-crf','22',
          '-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-shortest',
          str(ROOT/'episode1-comparison.mp4')],check=True)
    print(f'Created episode1-comparison.mp4 ({len(frames)/sr:.2f}s, {len(segments)} captioned clips)')

if __name__=='__main__':main()
