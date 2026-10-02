from pathlib import Path
import json,html
ROOT=Path(__file__).resolve().parents[1]
rows=json.loads((ROOT/'docs/voice-candidates.json').read_text())
notes={
 'esperar':'자연스러운 단발 질문 반응. 0.711초의 실제 녹음으로 시작·끝의 호흡을 비교하는 기준. 한국어 발음이나 배역 적합성은 별도로 판단.',
 'Anna Kim':'제공자 설명: 젊은 한국어 여성 화자, 부드럽고 차분하며 선명함. 미란의 맑은 톤 후보.',
 'Selly Han':'제공자 설명: 차분하고 부드러우며 사려 깊은 문학 내레이션. 세란의 안정된 말투 후보.',
 'Ruach':'제공자 설명: 깊고 따뜻하며 감정적인 여성 화자. 세란 후보지만 짧은 반응에서 감정이 과해지는지 확인.',
 'Rosa Oh':'제공자 설명: 젊은 한국어 여성 화자, 깨끗하고 정돈된 발음. 옥녀의 또렷하고 빠른 응답 후보.',
 'Stella':'제공자 설명: 명료하고 밝고 경쾌한 톤. 옥녀 후보지만 광고처럼 들리지 않는지 확인.',
}
head='''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>화분 · 음색 후보</title><style>body{background:#14271f;color:#eee8db;font:17px/1.75 system-ui,sans-serif;max-width:1050px;margin:50px auto;padding:0 24px}h1{font-family:serif;font-size:44px}h2{color:#b9d4c1}a{color:#bfdae0}article{background:#213c30;border:1px solid #4d6555;border-radius:12px;padding:25px;margin:20px 0}audio{width:100%;margin-top:14px}small{color:#bed0bb}fieldset{border:0;display:flex;flex-wrap:wrap;gap:14px;padding:10px 0}label{font-size:15px}select,textarea{background:#14271f;color:#eee8db;border:1px solid #718573;padding:8px}textarea{width:95%}button{background:#d8e4d1;color:#14271f;padding:12px 25px;font-size:16px;border:0;border-radius:6px}p{max-width:920px}</style><h1>화분 · 짧은 발성의 음색 찾기</h1><p>미란·세란·옥녀별 두 후보입니다. 실제 녹음과 AI 공개 미리듣기를 비교하세요. 이 페이지는 청취용이며, 미리듣기 음원은 게임에 들어가지 않았습니다. 재생에는 인터넷이 필요합니다.</p><p>아래 음색 설명은 제공자의 설명에 따른 후보 선정이며 청취 검증 결과가 아닙니다. 먼저 각 후보를 한 번, 마음에 드는 후보를 다섯 번 들어 보세요. 문장 미리듣기가 좋아도 짧은 “음?”, “아.”가 자연스럽다는 보장은 없어 제작 후 다시 확인합니다.</p>'''
parts=[head];md=['# 화분 음색 후보 — 사용자 선택 전','', '공식 페이지와 무료 공개 미리듣기를 2026-10-02 확인했다. 설명은 제공자 메타데이터에 근거하며 실제 청취 합격 판정은 아직 하지 않았다. [바로 듣고 평가하기](voice-reference.html).','']
for character in ['미란','세란','옥녀']:
 parts.append('<h2>'+character+'</h2>');md+=['## '+character,'']
 for i,d in enumerate(x for x in rows if x['character']==character):
  code=character+' '+('A' if i==0 else 'B');key=next(k for k in notes if d['name'].startswith(k));note=notes[key]
  license='CC0 공개 녹음: 상업적 게임 이용 가능. 배포 전 원본과 라이선스 증거를 함께 보관. 현재는 레퍼런스로만 사용.' if key=='esperar' else 'AI 공개 미리듣기: 청취용 링크만 사용. 배포 음원으로 전용하지 않음. 선택 후 유료 구독 중 상업 이용 가능한 비베타 서비스로 별도 생성하고 생성 이력을 보관.'
  source=d['source'] if key=='esperar' else 'https://elevenlabs.io/app/voice-library?voiceId='+d['voiceId']
  parts.append('<article><h3>'+html.escape(code+' · '+d['name'])+'</h3><small>'+d['type']+'</small><p>'+note+'</p><audio controls preload="none" src="'+html.escape(d['previewUrl'],quote=True)+'"></audio><p><a href="'+source+'" target="_blank" rel="noopener">원문·음성 선택 페이지</a> · <a href="'+d['source']+'" target="_blank" rel="noopener">미리듣기가 만료되면 공식 페이지에서 이름 검색</a></p><small>'+license+'</small><fieldset>')
  for criterion in ['시작·끝 자연스러움','감정 절제','인물 구분','반복 피로 적음']:
   parts.append('<label>'+criterion+' <select data-key="'+code+criterion+'"><option value="">미평가</option>'+''.join('<option>'+str(n)+'</option>' for n in range(1,6))+'</select></label>')
  parts.append('</fieldset><label><input type="radio" name="'+character+'" value="'+code+'"> 이 음색 선택</label></article>')
  md+=['### '+code+' · '+d['name'],'', '- 구분: '+d['type'],'- 음색: '+note,'- 듣기: [공식 페이지]('+d['source']+') / [후보 선택]('+source+')','- 게임 사용: '+license,'']
parts.append('''<h2>선택 후 제작</h2><p>인물당 최소 6개의 완결된 짧은 발성을 만듭니다. 예: “음?”, “아.”, “어?”, “응.”, “흠.”, “오.”. 음절 중간을 자르거나 길이를 늘이지 않습니다. 같은 기본 음성의 피치만 바꿔 배역을 나누지 않습니다.</p><p>첫 소리는 네 번째 유효 글자, 이후 16글자마다 기회, 최소 1.2초 간격, 블록당 최대 3회입니다. 속말은 무음이고 스킵·메뉴·전환·즉시 표시에서는 중단합니다. 같은 직전 음원은 연속 재생하지 않습니다.</p><p>음색 선택 → 유료 계정·잔여 생성량 확인(유료 서비스 선택 시) → 신규 제작 → 인게임 켜짐/꺼짐 비교 → 사용자 청취 승인 순서입니다.</p><textarea id="memo" rows="3" placeholder="어느 인물에 어떤 음색이 어울리는지 메모"></textarea><p><button id="export">선택·평가 저장</button></p><p><a href="https://help.elevenlabs.io/hc/en-us/articles/13313564601361-Can-I-publish-the-content-I-generate-on-the-platform">ElevenLabs 공식 상업 사용 조건</a> · 무료 생성물에는 상업 라이선스가 없으며, 유료 구독 중 생성한 음원도 베타 등 예외 조건을 확인해야 합니다.</p><script>document.querySelectorAll('audio').forEach(a=>a.addEventListener('play',()=>document.querySelectorAll('audio').forEach(b=>{if(a!==b)b.pause()})));document.getElementById('export').onclick=()=>{const data={date:new Date().toISOString(),choices:{},scores:{},memo:document.getElementById('memo').value};document.querySelectorAll('input:checked').forEach(x=>data.choices[x.name]=x.value);document.querySelectorAll('select').forEach(x=>data.scores[x.dataset.key]=x.value);const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));a.download='hwabun-voice-selection.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)};</script></html>''')
(ROOT/'docs/voice-reference.html').write_text(''.join(parts))
md+=['## 선정 및 제작 절차','','네 항목을 각 1~5점으로 평가: 자연스러운 시작·끝, 과장 없는 감정, 인물 간 구분, 반복 피로가 적음. 실제 녹음은 자연스러움의 기준이며 해당 화자의 모든 배역 발성을 이미 확보했다는 의미가 아니다.','','음색을 선택한 후에만 최소 6개/인물의 완결된 발성을 새로 제작한다. ElevenLabs 선택 시 계정의 유료 상태·잔여 한도·모델 이용 조건을 확인한다. 생성 날짜·voice ID·모델 ID·구독 증거·generation/history ID·원본 해시를 저장한다. API 키는 저장하지 않는다.','','[ElevenLabs 공식 조건](https://help.elevenlabs.io/hc/en-us/articles/13313564601361-Can-I-publish-the-content-I-generate-on-the-platform): 무료 생성물은 상업 이용 불가. 유료 생성물도 베타 서비스 등 제한을 확인한다. 공개 미리듣기는 게임 제작 음원으로 간주하지 않는다.','','승인 음원만 `sample/game/audio/voices.json`에 연결한다. 배역별 `approved`, `commercial_evidence`, 중복되지 않는 6개 이상의 `clips`를 갖춰야 한다. 실제 청취 승인 전에는 음성 완성으로 표시하지 않는다.']
(ROOT/'docs/voice-reference.md').write_text('\n'.join(md))
