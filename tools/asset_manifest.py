"""Record exactly the media shipped in this build."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[1]/'sample'
records=[]
for folder,kind in [('images','AI imagegen'),('audio','original procedural audio'),('fonts','SIL OFL font')]:
 for p in sorted((root/'game'/folder).iterdir()):
  if p.suffix in ('.png','.ogg','.otf'):
   records.append(dict(file=str(p.relative_to(root/'game')),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),kind=kind,ai_assisted=folder!='fonts'))
for record in records:
 if record['file'] == 'audio/main_gymnopedie.ogg':
  record.update(kind='user-provided music recording; converted to Ogg Vorbis', ai_assisted=False)
(root/'asset-manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
print('Recorded',len(records),'media assets')
