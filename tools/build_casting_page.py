"""Render local auditions with A/B choices; no network or game changes."""
import html,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/'docs/voice-casting'
rs=json.loads((ROOT/'manifest.json').read_text())
parts=[]
for sid,title in [('seran','세란'),('oknyeo','옥녀'),('danju','단주'),('hyunma','현마'),('younghun','영훈')]:
 cards=[]
 for option in ['A','B']:
  clips=[r for r in rs if r.get('speaker')==sid and r.get('option')==option and 'file' in r]
  if not clips:continue
  first=clips[0]
  audios=''.join('<p>'+html.escape(r['prompt_label'])+' <small>'+str(round(r['duration_seconds'],2))+'초</small></p><audio controls preload="none" src="'+html.escape(r['file'])+'"></audio>' for r in sorted(clips,key=lambda r:['reaction','sigh','dialogue'].index(r['prompt_id'])))
  cards.append('<article><label><input type="radio" name="'+sid+'" value="'+option+'" data-character="'+title+'" data-voice="'+html.escape(first['voice_name'])+'"> '+option+' · '+html.escape(first['voice_name'])+'</label><p>'+html.escape(first['casting_direction'])+'</p>'+audios+'</article>')
 parts.append('<section><h2>'+title+'</h2><div class="pair">'+''.join(cards)+'</div></section>')
(ROOT/'index.html').write_text('''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>화분 인물 목소리 선택</title><style>body{max-width:1100px;margin:40px auto;padding:20px;background:#14251f;color:#f0eee5;font-family:sans-serif;line-height:1.6}h1{font-size:30px}.pair{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px}article{background:#243a30;padding:20px;border-radius:12px}label{font-size:21px;font-weight:bold}audio{width:100%}small{color:#bed2c5}textarea{box-sizing:border-box;width:100%;min-height:180px;background:#243a30;color:#fff;padding:16px;font-size:18px}a{color:#bfdec9}</style><h1>화분 인물 목소리 선택</h1><p>미란은 승인한 Selly Han을 유지합니다. 나머지 다섯 인물은 각각 A/B 후보입니다. 같은 “음?”, 한숨 “아…”, 비교용 문장을 들은 뒤 골라 주세요. 비교 문장은 게임 대사가 아닙니다. 후보 설명은 라이브러리 설명에 따른 캐스팅 방향이며 실제 음색의 평가는 청취로 결정합니다. 게임에는 아직 연결하지 않았습니다.</p>'''+''.join(parts)+'''<h2>선택 결과</h2><p>선택 후 아래 내용을 복사해 채팅에 보내 주세요. 라디오 버튼 선택만으로 게임에 적용되지는 않습니다.</p><textarea id="result" readonly aria-label="선택 결과"></textarea><script>function update(){const picked=[...document.querySelectorAll('input:checked')];document.getElementById('result').value='미란: Selly Han (유지)\n'+picked.map(x=>x.dataset.character+': '+x.value+' / '+x.dataset.voice).join('\n')}document.querySelectorAll('input').forEach(x=>x.addEventListener('change',update));document.querySelectorAll('audio').forEach(a=>a.addEventListener('play',()=>document.querySelectorAll('audio').forEach(b=>{if(b!==a)b.pause()})));update();</script></html>''')
selection_path=ROOT/'selection.json'
if selection_path.exists():
 chosen={r['speaker']:r['option'] for r in json.loads(selection_path.read_text())['selected']}
 page=ROOT/'index.html'
 content=page.read_text()
 for sid,option in chosen.items():
  content=content.replace('name="'+sid+'" value="'+option+'"','name="'+sid+'" value="'+option+'" checked')
 page.write_text(content)
print('Casting page:',sum('file' in r for r in rs),'audio files')
