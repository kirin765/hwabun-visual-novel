import hashlib,json,tarfile,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
records=[]
for p in sorted((ROOT/'dist').glob('HwabunGarden-*')):
 if p.suffix=='.zip':
  with zipfile.ZipFile(p) as z:
   assert z.testzip() is None
   names=z.namelist();read=z.read
   prefix=names[0].split('/')[0]+'/'
   assert prefix+'HwabunGarden.exe' in names
   assert any('lib/py3-windows-x86_64/python.exe' in n for n in names)
   manifest=json.loads(z.read(prefix+'asset-manifest.json'))
   for item in manifest:
    assert hashlib.sha256(z.read(prefix+'game/'+item['file'])).hexdigest()==item['sha256']
 elif p.name.endswith('.tar.bz2'):
  with tarfile.open(p) as t:
   names=t.getnames();prefix=names[0].split('/')[0]+'/'
   assert t.getmember(prefix+'HwabunGarden.sh').mode & 0o111
   manifest=json.load(t.extractfile(prefix+'asset-manifest.json'))
   for item in manifest:
    assert hashlib.sha256(t.extractfile(prefix+'game/'+item['file']).read()).hexdigest()==item['sha256']
 else:continue
 assert not any('/game/test_' in n or '/game/saves/' in n or 'voice-v2' in n or '.env' in n for n in names)
 assert prefix+'game/python-packages/voice_policy.py' in names
 assert prefix+'game/tl/korean/common.rpy' in names
 assert prefix+'game/fonts/OFL.txt' in names
 assert prefix+'voice-reference.html' in names
 records.append(dict(package=p.name,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),entries=len(names),assets_verified=len(manifest),test_and_save_files_excluded=True))
(ROOT/'docs/package-verification.json').write_text(json.dumps(records,indent=2))
print(json.dumps(records,indent=2))
