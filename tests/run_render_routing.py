"""Run the actual surface-routing method in an isolated Android process.

Only the native sink and unrelated View construction are doubled. Real Android
Surface objects identify which output is routed; no phone input or video is sent.
"""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from device import TV

MAIN = '''.class public Lai/rplay/carcast/RenderRoutingMain;
.super Ljava/lang/Object;
.method public static main([Ljava/lang/String;)V
 .locals 6
 new-instance v0,Lai/rplay/carcast/CnRender;
 invoke-direct {v0},Lai/rplay/carcast/CnRender;-><init>()V
 sput-object v0,Lai/rplay/carcast/CnRender;->current:Lai/rplay/carcast/CnRender;
 new-instance v1,Landroid/view/Surface;
 invoke-direct {v1},Landroid/view/Surface;-><init>()V
 sput-object v1,Lai/rplay/carcast/CnRender;->output:Landroid/view/Surface;
 const/4 v2,0x0
 const/4 v3,0x0
 invoke-static {v2,v3},Lai/rplay/carcast/CnRender;->route(ILandroid/view/Surface;)V
 sget-object v4,Lai/rplay/carcast/NativeBridge;->last:Landroid/view/Surface;
 if-ne v4,v1,:failed
 new-instance v5,Landroid/view/Surface;
 invoke-direct {v5},Landroid/view/Surface;-><init>()V
 invoke-static {v2,v5},Lai/rplay/carcast/CnRender;->route(ILandroid/view/Surface;)V
 sget-object v4,Lai/rplay/carcast/NativeBridge;->last:Landroid/view/Surface;
 if-ne v4,v1,:failed
 const/4 v2,0x1
 invoke-static {v2,v5},Lai/rplay/carcast/CnRender;->route(ILandroid/view/Surface;)V
 sget-object v4,Lai/rplay/carcast/NativeBridge;->last:Landroid/view/Surface;
 if-ne v4,v5,:failed
 sput-object v3,Lai/rplay/carcast/CnRender;->current:Lai/rplay/carcast/CnRender;
 const/4 v2,0x0
 invoke-static {v2,v3},Lai/rplay/carcast/CnRender;->route(ILandroid/view/Surface;)V
 sget-object v4,Lai/rplay/carcast/NativeBridge;->last:Landroid/view/Surface;
 if-nez v4,:failed
 invoke-virtual {v1},Landroid/view/Surface;->release()V
 invoke-virtual {v5},Landroid/view/Surface;->release()V
 sget-object v0,Ljava/lang/System;->out:Ljava/io/PrintStream;
 const-string v1,"PASS: legacy destruction preserves active texture output; other slots and real clearing still forward"
 invoke-virtual {v0,v1},Ljava/io/PrintStream;->println(Ljava/lang/String;)V
 return-void
 :failed
 sget-object v0,Ljava/lang/System;->out:Ljava/io/PrintStream;
 const-string v1,"FAIL: legacy surface callback cleared or misrouted the active video output"
 invoke-virtual {v0,v1},Ljava/io/PrintStream;->println(Ljava/lang/String;)V
 const/4 v0,0x1
 invoke-static {v0},Ljava/lang/System;->exit(I)V
 return-void
.end method
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--serial', required=True)
    parser.add_argument('--adb', required=True)
    parser.add_argument('--java', required=True)
    parser.add_argument('--apktool', required=True, type=Path)
    args = parser.parse_args()
    tv = TV(args.serial, args.adb)
    tv.identity()
    project = ROOT / 'build/render-routing'
    package = project / 'smali/ai/rplay/carcast'
    package.mkdir(parents=True, exist_ok=True)
    for filename in ('apktool.yml', 'AndroidManifest.xml'):
        shutil.copy2(ROOT / 'build/work/carcast-cn-src' / filename, project / filename)
    source = (ROOT / 'src/carcast/smali/ai/rplay/carcast/CnRender.smali').read_text()
    start = source.index('.method public static route(')
    end = source.index('.end method', start) + len('.end method')
    (package / 'CnRender.smali').write_text('''.class public Lai/rplay/carcast/CnRender;
.super Ljava/lang/Object;
.field public static current:Lai/rplay/carcast/CnRender;
.field public static output:Landroid/view/Surface;
.method public constructor <init>()V
.locals 0
invoke-direct {p0},Ljava/lang/Object;-><init>()V
return-void
.end method
''' + source[start:end])
    (package / 'NativeBridge.smali').write_text('''.class public Lai/rplay/carcast/NativeBridge;
.super Ljava/lang/Object;
.field public static last:Landroid/view/Surface;
.method public static setScreenSurface(ILandroid/view/Surface;)V
.locals 0
sput-object p1,Lai/rplay/carcast/NativeBridge;->last:Landroid/view/Surface;
return-void
.end method
''')
    (package / 'RenderRoutingMain.smali').write_text(MAIN)
    apk, dex = ROOT / 'build/render-routing.apk', ROOT / 'build/render-routing.dex'
    subprocess.run([args.java, '-jar', str(args.apktool), 'b', str(project), '-o', str(apk)], check=True)
    with ZipFile(apk) as archive:
        dex.write_bytes(archive.read('classes.dex'))
    remote = '/data/local/tmp/carcast-render-routing-test.dex'
    tv.run('push', str(dex), remote, timeout=30)
    result = subprocess.run(tv.prefix + ['shell', 'env', 'CLASSPATH=' + remote, 'app_process', '/',
                                        'ai.rplay.carcast.RenderRoutingMain'],
                            capture_output=True, text=True, timeout=15)
    print(result.stdout.strip())
    if result.stderr:
        print(result.stderr[-1200:])
    return 0 if result.returncode == 0 and 'PASS:' in result.stdout else 1


if __name__ == '__main__':
    raise SystemExit(main())
