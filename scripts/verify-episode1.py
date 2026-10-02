#!/usr/bin/env python3
"""Verify editorial structure, source excerpts, counts and audition references."""
import hashlib, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'1화대본.md').read_text()
body=s.split('## S01',1)[1].split('## 제작 확인 메모',1)[0]
pattern=r'^(미란 속말|미란|세란|단주|현마|옥녀|운전수|라디오):'
def blocks(text):return [b for b in text.split('\n\n') if re.match(pattern,b)]
def words(text):return [b.split(': ',1)[1].replace('\n',' ') for b in blocks(text)]
def count(text):return sum(map(len,words(text)))
assert re.findall(r'^## (S\d+)',s,re.M)==['S01','S02','S03','S04']
assert re.findall(r'^### C\d+',s,re.M)==['### C01']
a=body.split('### A 경로')[1].split('### B 경로')[0]
b=body.split('### B 경로')[1].split('### 공통 합류')[0]
assert a.count('[다음: 공통 합류.]')==b.count('[다음: 공통 합류.]')==1
for route in (a,b):assert '미란:' in route and '세란:' in route
buttons=re.findall(r'\[선택 [AB]: (.*?)\]',body)
assert len(buttons)==2
assert buttons[0]==words(a)[0] and buttons[1]==words(b)[0]
assert '미란은 21세' in s and '집에서 두 해를 보냈다' in body
assert '알았다. 싫다는데 입을 열겠니.' in body
external=body.split('[짧은 외부 장면.')[1].split('## S04')[0]
assert '미란 속말:' not in external
assert body.count('[발성 무음]')==8
for i,part in enumerate(body.split('\n\n')):
 if part=='[발성 무음]':assert re.match(r'^(미란|단주):',body.split('\n\n')[i+1])
assert '술' not in '\n'.join(words(body))
all_count=count(body)+sum(map(len,buttons));route_a=all_count-count(b);route_b=all_count-count(a)
assert (all_count,route_a,route_b)==(11282,11142,11094)
assert all(f'{n:,}자' in s for n in (all_count,route_a,route_b))
source=Path('/home/giwan/Downloads/hwabun_이효석/이효석-화분.txt').read_text()
quotes=['무슨 냄새 같을까. 언니.','백합 냄새 같지.','무엇 말인데.','네 얼굴 말야.','괴덕만 부리네. 누가 얼굴 말인가, 라일락 말이지.','점잖게 언니 행세 좀 해요. 괴덕만 부리지 말구.','찔레 가시 조심해라.','그까짓 가시쯤.','찔레를 꺾으려는데 굼틀하고 손을 스치겠나요.','단주 자네 쫓아가 보게. 행여나 무슨 일 없도록 달래서 데려와야 해.','탐정인가 뒤를 쫓게.','달래서 데려오라는 분부이니.','폭풍경보예요.']
for q in quotes:assert q in source and q in body,q
links=0
for version in ('voice-v1','voice-v2'):
 root=ROOT/'audio'/version;m=json.loads((root/'manifest.json').read_text());page=(root/'preview.html').read_text()
 for entry in m['assets']+m['auditions']:assert (root/entry['file']).is_file()
 for entry in m['auditions']:
  if entry['label'] in ('실제 1화','실제 1화 라디오'):assert any(entry['text'] in w for w in words(body))
  assert entry['text'] in page
 for link in re.findall(r'(?:src|href)="([^"]+)"',page):
  assert (root/link).exists(),link;links+=1
 if version=='voice-v2':assert m['source_script_sha256']==hashlib.sha256(s.encode()).hexdigest()
 assert len(m['assets'])==39 and len(m['auditions'])==13
report={'status':'passed','text_blocks':len(blocks(body)),'body_chars_all_routes':all_count,'route_a_chars':route_a,'route_b_chars':route_b,'reading_minutes_at_550_to_350_cpm':{'A':[round(route_a/550,1),round(route_a/350,1)],'B':[round(route_b/550,1),round(route_b/350,1)]},'checks':['S01–S04','one C01 with both paths to common merge','choice wording matches first utterance','adult age and two years','privacy request precedes both paths','external scene has no Miran inner speech','8 one-block mute cues','13 direct source excerpts','audition captions match script','all audio and page links exist','v2 source script hash'],'page_links_checked':links,'pending':['actual reading time','subjective v2 listening','browser UI interactions','game engine implementation']}
(ROOT/'검증기록.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))
