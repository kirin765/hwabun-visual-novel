"""Generate auditions only. Credentials come from getpass or the environment."""
import threading
import os,getpass,json,urllib.request,urllib.error,hashlib,datetime,concurrent.futures,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/'docs/voice-casting'
CANDIDATES=[
 ('seran','세란','A','UqW1DivwFt1NwUMSGnTn','Suzie','차분한 30대 서울말 후보'),
 ('seran','세란','B','sf8Bpb1IU97NI9BHSMRf','Rosa Oh','단정하고 깨끗한 후보'),
 ('oknyeo','옥녀','A','1YzIw7PZ7iaD4alelyHY','Stella','밝고 명료한 후보'),
 ('oknyeo','옥녀','B','Cm89zxZzEGaMu7ajYw2K','Yoojin Kim','젊고 친근한 한국어 후보'),
 ('danju','단주','A','wRlh0NOM5bmw1KzaE4XZ','JooHwan','밝고 가벼운 청년 후보'),
 ('danju','단주','B','wGZU4vSkwwD4Sj5jpW2V','Martin','부드러운 청년 후보'),
 ('hyunma','현마','A','GNmgFU0yNiLKxTCw3OT9','Shin','낮고 따뜻한 후보'),
 ('hyunma','현마','B','0KAffrKIwvdtnXfLpNRl','Hongsuk','성숙하고 자연스러운 대화 후보'),
 ('younghun','영훈','A','jctVgUrrEJoJjGpfN5Ef','MJ','차분하고 선명한 중음 후보'),
 ('younghun','영훈','B','ZXhi0czBiSzyk3bQNu5W','HoCho','차분하고 안정된 후보'),
]
PROMPTS=[('reaction','짧은 반응','음?'),('sigh','한숨·안도','[sighs] 아…'),('dialogue','비교용 문장','잠깐만요. 지금은 제 이야기를 들어 주세요.')]
def main():
 key=os.environ.get('ELEVENLABS_API_KEY') or getpass.getpass('API credential (hidden): ')
 ROOT.mkdir(exist_ok=True)
 locks={c[3]:threading.Lock() for c in CANDIDATES}
 def generate_locked(job):
  with locks[job[3]]:
   return generate(job)
 def generate(job):
  sid,character,option,voice_id,name,direction,pid,label,prompt=job
  dest=ROOT/sid/option/(pid+'.mp3');dest.parent.mkdir(parents=True,exist_ok=True)
  body={'text':prompt,'model_id':'eleven_v3','language_code':'ko','voice_settings':{'stability':0.5}}
  req=urllib.request.Request('https://api.elevenlabs.io/v1/text-to-speech/'+voice_id+'?output_format=mp3_44100_128',data=json.dumps(body).encode(),headers={'xi-api-key':key,'Content-Type':'application/json'})
  try:
   with urllib.request.urlopen(req,timeout=60) as r:audio=r.read();generation=r.headers.get('history-item-id');rid=r.headers.get('request-id');cost=r.headers.get('character-cost')
   dest.write_bytes(audio)
   duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(dest)]).decode())
   subprocess.run(['ffmpeg','-v','error','-i',str(dest),'-f','null','-'],check=True)
   record={'speaker':sid,'character':character,'option':option,'voice_id':voice_id,'voice_name':name,'casting_direction':direction,'prompt_id':pid,'prompt_label':label,'prompt':prompt,'model_id':'eleven_v3','file':str(dest.relative_to(ROOT)),'sha256':hashlib.sha256(audio).hexdigest(),'duration_seconds':duration,'history_item_id':generation,'request_id':rid,'character_cost':cost,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'approved':False,'game_integrated':False}
   print('Generated: '+character+' '+option+' '+name+' / '+label,flush=True);return record
  except urllib.error.HTTPError as e:return {'speaker':sid,'option':option,'voice_name':name,'prompt_id':pid,'http_status':e.code,'error':e.read().decode(errors='replace').replace(key,'[redacted]')[:500]}
  except Exception as e:return {'speaker':sid,'option':option,'prompt_id':pid,'error_type':type(e).__name__}
 jobs=[c+p for c in CANDIDATES for p in PROMPTS]
 records=json.loads((ROOT/'manifest.json').read_text()) if (ROOT/'manifest.json').exists() else []
 records=[r for r in records if 'file' in r]
 completed={(r['speaker'],r['option'],r['prompt_id']) for r in records}
 jobs=[j for j in jobs if (j[0],j[2],j[6]) not in completed]
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
  for r in executor.map(generate_locked,jobs):
   records.append(r);(ROOT/'manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
 good=sum('file' in r for r in records);print('Completed '+str(good)+'/'+str(len(CANDIDATES)*len(PROMPTS)),flush=True)
 for r in records:
  if 'error' in r or 'error_type' in r:print(json.dumps(r,ensure_ascii=False),flush=True)
if __name__=='__main__':main()
