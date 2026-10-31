"""Exercise actual reconnect and main-screen callback in a separate Android VM.

The test never reaches Bluetooth: an exhausted old task is replaced by a main
screen event, then its obsolete callback is replayed. Context/activity launches
are isolated sinks. No APK is installed and no phone session is changed.
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

SERVICE = '''.class public Lai/rplay/carcast/CarPlayService;
.super Landroid/content/ContextWrapper;
.implements Lip;
.field public static A:Lai/rplay/carcast/CarPlayService;
.field public static v:Z
.field public static w:Ljava/lang/String;
.field public static x:Z
.field public static z:Landroid/content/Intent;
.method public constructor <init>()V
 .locals 1
 const/4 v0,0x0
 invoke-direct {p0,v0},Landroid/content/ContextWrapper;-><init>(Landroid/content/Context;)V
 return-void
.end method
.method public getApplicationContext()Landroid/content/Context;
 .locals 0
 return-object p0
.end method
.method public getPackageName()Ljava/lang/String;
 .locals 1
 const-string v0,"isolated.reconnect.test"
 return-object v0
.end method
.method public startActivity(Landroid/content/Intent;)V
 .locals 0
 return-void
.end method
.method public static o(Ljava/lang/String;)V
 .locals 0
 return-void
.end method
.method public static p(Landroid/content/Context;Landroid/content/Intent;)V
 .locals 0
 return-void
.end method
'''
MAIN = '''.class public Lai/rplay/carcast/ReconnectMain;
.super Ljava/lang/Object;
.method public static main([Ljava/lang/String;)V
 .locals 9
 invoke-static {},Landroid/os/Looper;->prepareMainLooper()V
 new-instance v0,Lai/rplay/carcast/CarPlayService;
 invoke-direct {v0},Lai/rplay/carcast/CarPlayService;-><init>()V
 sput-object v0,Lai/rplay/carcast/CarPlayService;->A:Lai/rplay/carcast/CarPlayService;
 sput-object v0,Lai/rplay/carcast/NativeBridge;->sListener:Lip;
 const/4 v1,0x1
 sput-boolean v1,Lai/rplay/carcast/CarPlayService;->v:Z
 const-string v2,"carplay"
 sput-object v2,Lai/rplay/carcast/CarPlayService;->w:Ljava/lang/String;
 invoke-static {v0},Lai/rplay/carcast/CnReconnect;->start(Landroid/content/Context;)V
 const-class v2,Lai/rplay/carcast/CnReconnect;
 const-string v3,"task"
 invoke-virtual {v2,v3},Ljava/lang/Class;->getDeclaredField(Ljava/lang/String;)Ljava/lang/reflect/Field;
 move-result-object v3
 invoke-virtual {v3,v1},Ljava/lang/reflect/AccessibleObject;->setAccessible(Z)V
 const/4 v4,0x0
 invoke-virtual {v3,v4},Ljava/lang/reflect/Field;->get(Ljava/lang/Object;)Ljava/lang/Object;
 move-result-object v5
 check-cast v5,Lai/rplay/carcast/CnReconnect;
 const-string v6,"attempts"
 invoke-virtual {v2,v6},Ljava/lang/Class;->getDeclaredField(Ljava/lang/String;)Ljava/lang/reflect/Field;
 move-result-object v6
 invoke-virtual {v6,v1},Ljava/lang/reflect/AccessibleObject;->setAccessible(Z)V
 const/4 v2,0x6
 invoke-virtual {v6,v5,v2},Ljava/lang/reflect/Field;->setInt(Ljava/lang/Object;I)V
 const/4 v1,0x0
 const/16 v2,0x500
 const/16 v7,0x2d0
 invoke-static {v1,v2,v7},Lai/rplay/carcast/NativeBridge;->onScreenStart(III)V
 invoke-static {v0},Lai/rplay/carcast/CnReconnect;->start(Landroid/content/Context;)V
 invoke-virtual {v3,v4},Ljava/lang/reflect/Field;->get(Ljava/lang/Object;)Ljava/lang/Object;
 move-result-object v7
 if-eq v5,v7,:failed
 if-eqz v7,:failed
 invoke-virtual {v6,v7},Ljava/lang/reflect/Field;->getInt(Ljava/lang/Object;)I
 move-result v8
 if-nez v8,:failed
 invoke-virtual {v5},Lai/rplay/carcast/CnReconnect;->run()V
 invoke-virtual {v3,v4},Ljava/lang/reflect/Field;->get(Ljava/lang/Object;)Ljava/lang/Object;
 move-result-object v8
 if-ne v7,v8,:failed
 const/4 v1,0x1
 const/16 v2,0x500
 const/16 v5,0x2d0
 invoke-static {v1,v2,v5},Lai/rplay/carcast/NativeBridge;->onScreenStart(III)V
 invoke-virtual {v3,v4},Ljava/lang/reflect/Field;->get(Ljava/lang/Object;)Ljava/lang/Object;
 move-result-object v8
 if-ne v7,v8,:failed
 sput-object v4,Lai/rplay/carcast/CarPlayService;->A:Lai/rplay/carcast/CarPlayService;
 check-cast v7,Lai/rplay/carcast/CnReconnect;
 invoke-virtual {v7},Lai/rplay/carcast/CnReconnect;->run()V
 invoke-virtual {v3,v4},Ljava/lang/reflect/Field;->get(Ljava/lang/Object;)Ljava/lang/Object;
 move-result-object v8
 if-nez v8,:failed
 sget-object v0,Ljava/lang/System;->out:Ljava/io/PrintStream;
 const-string v1,"PASS: main-screen connection resets exhausted retry; obsolete task cannot clear replacement; secondary slot preserves it; stopped service cancels"
 invoke-virtual {v0,v1},Ljava/io/PrintStream;->println(Ljava/lang/String;)V
 const/4 v0,0x0
 invoke-static {v0},Ljava/lang/System;->exit(I)V
 return-void
 :failed
 sget-object v0,Ljava/lang/System;->out:Ljava/io/PrintStream;
 const-string v1,"FAIL: reconnect retry belongs to the wrong session or service lifecycle"
 invoke-virtual {v0,v1},Ljava/io/PrintStream;->println(Ljava/lang/String;)V
 const/4 v0,0x1
 invoke-static {v0},Ljava/lang/System;->exit(I)V
 return-void
.end method
'''


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('serial', 'adb', 'java', 'apktool'):
        p.add_argument('--' + name, required=True)
    args = p.parse_args()
    tv = TV(args.serial, args.adb)
    tv.identity()
    project = ROOT / 'build/reconnect-lifecycle'
    package = project / 'smali/ai/rplay/carcast'
    package.mkdir(parents=True, exist_ok=True)
    decoded = ROOT / 'build/work/carcast-cn-src'
    for name in ('apktool.yml', 'AndroidManifest.xml'):
        shutil.copy2(decoded / name, project / name)
    shutil.copy2(ROOT / 'src/carcast/smali/ai/rplay/carcast/CnReconnect.smali', package / 'CnReconnect.smali')
    original = (decoded / 'smali/ai/rplay/carcast/NativeBridge.smali').read_text()
    start = original.index('.method public static onScreenStart(III)V')
    end = original.index('.end method', start) + len('.end method')
    classes = {'CarPlayService': SERVICE, 'ReconnectMain': MAIN,
               'NativeBridge': '.class public Lai/rplay/carcast/NativeBridge;\n.super Ljava/lang/Object;\n.field public static sListener:Lip;\n' + original[start:end],
               'CarPlayActivity': '.class public Lai/rplay/carcast/CarPlayActivity;\n.super Ljava/lang/Object;\n.field public static h:Z\n',
               'SettingsActivity': '.class public Lai/rplay/carcast/SettingsActivity;\n.super Ljava/lang/Object;\n.method public static g()Z\n.locals 1\nconst/4 v0,0x0\nreturn v0\n.end method\n',
               'BtControl': '.class public Lai/rplay/carcast/BtControl;\n.super Ljava/lang/Object;\n.method public static start(Landroid/content/Context;)V\n.locals 0\nreturn-void\n.end method\n'}
    for name, source in classes.items():
        (package / (name + '.smali')).write_text(source)
    (project / 'smali/ip.smali').write_text('.class public interface abstract Lip;\n.super Ljava/lang/Object;\n')
    (project / 'smali/qn.smali').write_text('.class public Lqn;\n.super Ljava/lang/Object;\n.method public static Y(Landroid/content/Context;)Z\n.locals 1\nconst/4 v0,0x0\nreturn v0\n.end method\n')
    apk, dex = ROOT / 'build/reconnect-lifecycle.apk', ROOT / 'build/reconnect-lifecycle.dex'
    subprocess.run([args.java, '-jar', args.apktool, 'b', str(project), '-o', str(apk)], check=True)
    with ZipFile(apk) as archive:
        dex.write_bytes(archive.read('classes.dex'))
    remote = '/data/local/tmp/carcast-reconnect-lifecycle-test.dex'
    tv.run('push', str(dex), remote, timeout=30)
    r = subprocess.run(tv.prefix + ['shell', 'env', 'CLASSPATH=' + remote, 'app_process', '/',
                                    'ai.rplay.carcast.ReconnectMain'], capture_output=True, text=True, timeout=15)
    print(r.stdout.strip())
    if r.stderr:
        print(r.stderr[-1200:])
    return 0 if r.returncode == 0 and 'PASS:' in r.stdout else 1


if __name__ == '__main__':
    raise SystemExit(main())
