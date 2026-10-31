"""Run the own C adapter on API23 using real anonymous ashmem, never media."""
import argparse
from pathlib import Path
import subprocess
import sys
from zipfile import ZipFile
from hashlib import sha256
import json

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
sys.path.insert(0,str(ROOT/'experiments'))
from device import TV
from mirror_compat_probe import linker


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--serial',required=True)
    parser.add_argument('--adb',required=True)
    parser.add_argument('--apk',type=Path)
    parser.add_argument('--receipt',type=Path)
    args=parser.parse_args()
    if bool(args.apk)!=bool(args.receipt):parser.error('--apk and --receipt are required together')
    tv=TV(args.serial,args.adb);tv.identity()
    work=ROOT/'build/mirror-native-tests';work.mkdir(parents=True,exist_ok=True)
    private=ROOT/'local/system-libs';private.mkdir(parents=True,exist_ok=True)
    for library in ('libc.so','libdl.so'):
        if not (private/library).exists():
            tv.run('pull','/system/lib/'+library,str(private/library),timeout=30)
    objects=[]
    sources=([ROOT/'tests/native/mirror_apk_test.c'] if args.apk else
             [ROOT/'src/carcast/native/mirror_compat.c',ROOT/'tests/native/mirror_compat_test.c'])+[ROOT/'tests/native/start.c']
    for i,source in enumerate(sources):
        obj=work/(str(i)+'.o');objects.append(str(obj))
        subprocess.run(['xcrun','clang','-target','armv7a-linux-androideabi23','-mthumb',
                        '-fPIC','-mstrict-align','-fno-stack-protector','-fno-builtin','-O2',
                        '-I'+str(ROOT/'src/carcast/native'),'-c',str(source),'-o',str(obj)],check=True)
    executable=work/'mirror-test'
    subprocess.run(linker()+['-m','armelf_linux_eabi','-pie','--dynamic-linker','/system/bin/linker',
                            '--hash-style=both','-z','max-page-size=4096','-e','_start',
                            '--allow-shlib-undefined','-L',str(private),*objects,'-lc','-ldl',
                            '-o',str(executable)],check=True)
    remote='/data/local/tmp/carcast-mirror-compat-test'
    tv.run('push',str(executable),remote,timeout=30)
    tv.run('shell','chmod','755',remote)
    parameters=[]
    if args.apk:
        receipt=json.loads(args.receipt.read_text())
        if sha256(args.apk.read_bytes()).hexdigest()!=receipt['sha256']:raise ValueError('APK receipt mismatch')
        staged=work/'libcarcast-test.so'
        with ZipFile(args.apk) as archive:staged.write_bytes(archive.read('lib/armeabi-v7a/libcarcast.so'))
        target='/data/local/tmp/libcarcast-memory-test.so'
        tv.run('push',str(staged),target,timeout=90);parameters=[target]
    result=tv.run('shell',remote,*parameters,timeout=20)
    print(result)
    return 0 if 'PASS:' in result else 1

if __name__=='__main__':raise SystemExit(main())
