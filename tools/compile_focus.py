#!/usr/bin/env python3
"""Compile only project-owned Java; Android glue stays in project-owned Smali."""
from pathlib import Path
import argparse
import json
import shutil
import subprocess
from zipfile import ZipFile
from build import ROOT, artifact


def compile_focus(java, apktool, decoded, offline=True):
    lock=json.loads((ROOT/'dependencies.lock.json').read_text())
    cache=ROOT/'build/deps'
    ecj=artifact(lock['ecj'],cache,None,offline)
    r8=artifact(lock['r8'],cache,None,offline)
    work=ROOT/'build/focus-compile'
    classes=work/'classes'
    if classes.exists(): shutil.rmtree(classes)
    classes.mkdir(parents=True)
    sources=sorted((ROOT/'src/carcast/java').rglob('*.java'))
    stub=ROOT/'tests/stubs/ai/rplay/carcast/CnProbeHost.java'
    subprocess.run([str(java),'-jar',str(ecj),'-1.8','-proc:none','-g:none','-d',str(classes),
                    *map(str,sources),str(stub)],check=True)
    jar=work/'own.jar'
    with ZipFile(jar,'w') as z:
        for p in sorted(classes.rglob('*.class')):
            if p.name=='CnProbeHost.class': continue
            z.write(p,p.relative_to(classes).as_posix())
    dex=work/'dex';dex.mkdir(exist_ok=True)
    subprocess.run([str(java),'-cp',str(r8),'com.android.tools.r8.D8','--release',
                    '--no-desugaring','--min-api','23','--output',str(dex),str(jar)],check=True)
    apk=work/'own.apk'
    with ZipFile(apk,'w') as z:
        z.write(dex/'classes.dex','classes.dex')
        z.write(Path(decoded)/'AndroidManifest.xml','AndroidManifest.xml')
    out=work/'decoded'
    subprocess.run([str(java),'-jar',str(apktool),'d','-f','-r','-o',str(out),str(apk)],check=True)
    result=out/'smali'
    if any(p.name=='CnProbeHost.smali' for p in result.rglob('*.smali')):
        raise RuntimeError('Compile-time host stub leaked into device code')
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--java',required=True);p.add_argument('--apktool',required=True)
    p.add_argument('--decoded',type=Path,required=True)
    a=p.parse_args()
    print(compile_focus(a.java,a.apktool,a.decoded))
