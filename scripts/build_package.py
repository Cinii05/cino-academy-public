"""Build a reproducible skills-only OpenAI plugin archive from checked-in source."""
from pathlib import Path
import hashlib, json, zipfile

ROOT=Path(__file__).resolve().parents[1]
PLUGIN=json.loads((ROOT/'plugin.json').read_text(encoding='utf-8-sig'))
VERSION=PLUGIN['version']
OUT=ROOT/'dist'
OUT.mkdir(exist_ok=True)
ZIP=OUT/f'cino-academy-{VERSION}-review-candidate.zip'
files=[ROOT/'plugin.json', ROOT/'assets'/'icon.svg']
files += [p for p in (ROOT/'skills').rglob('*') if p.is_file() and p.suffix=='.md']
files=sorted(files,key=lambda p:p.relative_to(ROOT).as_posix())
manifest_files=[]
with zipfile.ZipFile(ZIP,'w',compression=zipfile.ZIP_STORED) as z:
    for p in files:
        rel=p.relative_to(ROOT).as_posix()
        # Normalise Windows CRLF checkouts to LF so ZIP bytes match Linux CI.
        data=p.read_bytes().replace(b'\r\n',b'\n')
        info=zipfile.ZipInfo(rel,date_time=(2020,1,1,0,0,0))
        info.create_system=3  # fixed Unix header on every build host
        info.compress_type=zipfile.ZIP_STORED  # no zlib-version dependence
        info.external_attr=(0o100644 << 16)
        z.writestr(info,data,compress_type=zipfile.ZIP_STORED)
        manifest_files.append({'path':rel,'sha256':hashlib.sha256(data).hexdigest()})
assert zipfile.ZipFile(ZIP).testzip() is None
sha=hashlib.sha256(ZIP.read_bytes()).hexdigest()
manifest={'version':VERSION,'status':'isolated-candidate-not-submitted','zip_sha256':sha,'files':manifest_files}
(OUT/'CANDIDATE-MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'zip':str(ZIP),'sha256':sha,'skills':[p.name for p in (ROOT/'skills').iterdir() if p.is_dir()], 'file_count':len(files)},indent=2))
