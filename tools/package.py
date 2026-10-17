#!/usr/bin/env python3
"""Build allowlisted skill ZIPs. Never collect local private inputs or logs."""
import hashlib
import json
import zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
VERSION='0.4.0-rc.6'

def build():
    manifest=json.loads((ROOT/'tools/package-manifest.json').read_text(encoding='utf-8'))
    out=ROOT/'dist'; out.mkdir(exist_ok=True)
    sums=[]
    for package,names in manifest.items():
        base=(ROOT/'packages'/package).resolve()
        target=out/(package+'-'+VERSION+'.zip')
        with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
            for name in names:
                path=(base/name).resolve()
                if not path.is_relative_to(base) or (base/name).is_symlink() or not path.is_file():
                    raise ValueError('Invalid source: '+name)
                info=zipfile.ZipInfo(package+'/'+name,date_time=(2026,10,12,0,0,0))
                info.create_system=3  # Stable ZIP metadata across build operating systems.
                info.compress_type=zipfile.ZIP_DEFLATED
                info.external_attr=0o644<<16
                z.writestr(info,path.read_bytes())
        with zipfile.ZipFile(target) as z:
            expected={package+'/'+name for name in names}
            if set(z.namelist()) != expected or z.testzip() is not None: raise ValueError('ZIP verification failed')
        sums.append(hashlib.sha256(target.read_bytes()).hexdigest()+'  '+target.name)
        print(target.name+': '+str(len(names))+' files')
    (out/'SHA256SUMS').write_text('\n'.join(sums)+'\n')
    print('SHA256SUMS written')

if __name__=='__main__': build()
