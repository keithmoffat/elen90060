from pathlib import Path
import hashlib,json,shutil
root=Path(__file__).resolve().parent
out=root/'_site';out.mkdir(exist_ok=True)
for pattern in ('*.html','*.css','*.woff2','*.pdf','LICENSE.txt','CNAME'):
 for source in root.glob(pattern):shutil.copy2(source,out/source.name)
manifest=json.loads((root/'final-pdf-manifest.json').read_text())
for item in manifest:
 name=item['file'];parts=sorted(root.glob(name+'.part[0-9][0-9]'))
 if parts:
  assert [p.name for p in parts]==[name+f'.part{i:02d}' for i in range(len(parts))]
  with (out/name).open('wb') as dest:
   for part in parts:
    with part.open('rb') as src:shutil.copyfileobj(src,dest)
 data=(out/name).read_bytes()
 assert len(data)==item['bytes'],name+' length mismatch'
 assert hashlib.sha256(data).hexdigest()==item['sha256'],name+' SHA256 mismatch'
 print('VERIFIED',name,item['sha256'])
assert not list(out.glob('*data-centres*'))
