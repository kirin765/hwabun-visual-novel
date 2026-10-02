"""Integrate only the five explicit user choices, with no audition sentences."""
import json,subprocess,hashlib,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
choices=json.loads((ROOT/'docs/voice-casting/selection.json').read_text())['selected']
new=json.loads((ROOT/'docs/selected-voices/manifest.json').read_text())
auditions=json.loads((ROOT/'docs/voice-casting/manifest.json').read_text())
manifest_path=ROOT/'sample/game/audio/voices.json';manifest=json.loads(manifest_path.read_text())
routes={
 'seran':{'curious':[32,97,103,136,165],'laugh':[15,19,46,48,50,57,124,160,162,167],'worried':[59,64,68,73,75,79,187,191],'relieved':[71,107,109],'frustrated':[164,172,178],'surprised':[174]},
 'oknyeo':{'worried':[81,83,85,87],'laugh':[90,92,118,120],'curious':[95]},
 'danju':{'worried':[200,213,215,227,229,282,294,301,306,308,347,349,351],'hesitant':[194,311,385,387],'laugh':[126,141,221,272,274,320,327,359,366],'curious':[131,154,223,254,277,362,364,381,393],'relieved':[357,389,406,413]},
 'hyunma':{'laugh':[125,140,144,148,150],'frustrated':[152,182,185],'worried':[193,195],'curious':[129,165]},
 'younghun':{},
}
records=[]
for c in choices:
 sid=c['speaker'];dest=ROOT/'sample/game/audio'/('voice_'+sid);dest.mkdir(exist_ok=True)
 clips={}
 for emotion in ['neutral','hesitant','curious','surprised','relieved','laugh','worried','frustrated']:
  if emotion in ['curious','relieved']:
   r=next(r for r in auditions if r['speaker']==sid and r['option']==c['option'] and r['prompt_id']=={'curious':'reaction','relieved':'sigh'}[emotion]);source=ROOT/'docs/voice-casting'/r['file']
  else:
   r=next(r for r in new if r['speaker']==sid and r['prompt_id']==emotion and 'file' in r);source=ROOT/'docs/selected-voices'/r['file']
  p=dest/(emotion+'.ogg');subprocess.run(['ffmpeg','-v','error','-y','-i',str(source),'-c:a','libvorbis','-q:a','5',str(p)],check=True)
  level=subprocess.run(['ffmpeg','-hide_banner','-i',str(p),'-af','volumedetect','-f','null','-'],capture_output=True,text=True,check=True)
  peak=float(re.search(r'max_volume: ([\-\d.]+) dB',level.stderr)[1]);assert peak > -45,(sid,emotion,peak)
  clip=str(p.relative_to(ROOT/'sample/game'));clips[emotion]=[clip]
  records.append({'speaker':sid,'emotion':emotion,'source':str(source.relative_to(ROOT)),'file':clip,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'peak_dbfs':peak,'voice_id':c['voice_id'],'prompt':r['prompt'],'history_item_id':r.get('history_item_id'),'approved_voice_choice':True})
 manifest['speakers'][sid]={'approved':True,'voice_id':c['voice_id'],'voice_name':c['voice_name'],'model_id':'eleven_v3','clips':[p for ps in clips.values() for p in ps],'emotion_clips':clips,'dialogue_emotions':{str(i):emotion for emotion,ids in routes[sid].items() for i in ids},'commercial_evidence':{'basis':'User reported paid plan before API generation; selected this voice explicitly.','selection':'docs/voice-casting/selection.json','generation_manifest':'docs/selected-voices/manifest.json'}}
manifest['status']='six-characters-selected';manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(ROOT/'docs/selected-voices/integration-manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
print('Integrated',len(records),'emotion clips; audition sentences excluded.')
