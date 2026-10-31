"""Run real input helpers and onPause on API23, with an isolated report sink.

No APK is installed. The separate shell process uses Android's real Looper,
Handler and Activity. Only the native transport and session flag are doubled;
it cannot send input to the phone. Vendor method text stays in ignored build/.
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

HEADER = '.class public final Lai/rplay/carcast/{name};\n.super {superclass}\n'
CONSTRUCTOR = '''.method public constructor <init>()V
 .locals 4
 invoke-direct {p0}, Landroid/app/Activity;-><init>()V
 const-class v0, Landroid/app/Activity;
 const-string v1, "mApplication"
 invoke-virtual {v0,v1}, Ljava/lang/Class;->getDeclaredField(Ljava/lang/String;)Ljava/lang/reflect/Field;
 move-result-object v0
 const/4 v1, 0x1
 invoke-virtual {v0,v1}, Ljava/lang/reflect/AccessibleObject;->setAccessible(Z)V
 new-instance v1, Landroid/app/Application;
 invoke-direct {v1}, Landroid/app/Application;-><init>()V
 invoke-virtual {v0,p0,v1}, Ljava/lang/reflect/Field;->set(Ljava/lang/Object;Ljava/lang/Object;)V
 return-void
.end method
'''
SESSION = '''.field public static connected:Z
.method public static g()Z
 .locals 1
 sget-boolean v0, Lai/rplay/carcast/SettingsActivity;->connected:Z
 return v0
.end method
'''
SINK = '''.field public static reports:I
.field public static lastWheel:I
.method public static iapPointer(IIII)V
 .locals 1
 sput p3, Lai/rplay/carcast/NativeBridge;->lastWheel:I
 or-int v0, p1, p2
 or-int/2addr v0, p3
 if-eqz v0, :done
 sget v0, Lai/rplay/carcast/NativeBridge;->reports:I
 add-int/lit8 v0, v0, 0x1
 sput v0, Lai/rplay/carcast/NativeBridge;->reports:I
 :done
 return-void
.end method
'''
MAIN = '''.field public static activity:Lai/rplay/carcast/CarPlayActivity;
.field public static atPause:I
.method public static main([Ljava/lang/String;)V
 .locals 6
 invoke-static {}, Landroid/os/Looper;->prepareMainLooper()V
 const/4 v0, 0x1
 sput-boolean v0, Lai/rplay/carcast/SettingsActivity;->connected:Z
 new-instance v0, Lai/rplay/carcast/CarPlayActivity;
 invoke-direct {v0}, Lai/rplay/carcast/CarPlayActivity;-><init>()V
 sput-object v0, Lai/rplay/carcast/InputLifecycleMain;->activity:Lai/rplay/carcast/CarPlayActivity;
 new-instance v0, Landroid/os/Handler;
 invoke-static {}, Landroid/os/Looper;->getMainLooper()Landroid/os/Looper;
 move-result-object v1
 invoke-direct {v0,v1}, Landroid/os/Handler;-><init>(Landroid/os/Looper;)V
 const/4 v1, 0x0
 aget-object v1, p0, v1
 const-string v2, "hold"
 invoke-virtual {v2,v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
 move-result v1
 if-eqz v1, :queue
 const/16 v1, 0x16
 const/4 v2, 0x0
 invoke-static {v1,v2}, Lai/rplay/carcast/CnHold;->update(II)V
 goto :timers
 :queue
 new-instance v1, Lai/rplay/carcast/InputLifecycleStep;
 const/4 v2, 0x0
 invoke-direct {v1,v2}, Lai/rplay/carcast/InputLifecycleStep;-><init>(I)V
 const-wide/16 v2, 0x190
 invoke-virtual {v0,v1,v2,v3}, Landroid/os/Handler;->postDelayed(Ljava/lang/Runnable;J)Z
 :timers
 new-instance v1, Lai/rplay/carcast/InputLifecycleStep;
 const/4 v2, 0x1
 invoke-direct {v1,v2}, Lai/rplay/carcast/InputLifecycleStep;-><init>(I)V
 const-wide/16 v2, 0x384
 invoke-virtual {v0,v1,v2,v3}, Landroid/os/Handler;->postDelayed(Ljava/lang/Runnable;J)Z
 new-instance v1, Lai/rplay/carcast/InputLifecycleStep;
 const/4 v2, 0x2
 invoke-direct {v1,v2}, Lai/rplay/carcast/InputLifecycleStep;-><init>(I)V
 const-wide/16 v2, 0x6a4
 invoke-virtual {v0,v1,v2,v3}, Landroid/os/Handler;->postDelayed(Ljava/lang/Runnable;J)Z
 invoke-static {}, Landroid/os/Looper;->loop()V
 return-void
.end method
'''
STEP = '''.implements Ljava/lang/Runnable;
.field private stage:I
.method public constructor <init>(I)V
 .locals 0
 invoke-direct {p0}, Ljava/lang/Object;-><init>()V
 iput p1,p0,Lai/rplay/carcast/InputLifecycleStep;->stage:I
 return-void
.end method
.method public run()V
 .locals 6
 iget v0,p0,Lai/rplay/carcast/InputLifecycleStep;->stage:I
 if-eqz v0, :burst
 const/4 v1, 0x1
 if-ne v0,v1,:check
 sget-object v0,Lai/rplay/carcast/InputLifecycleMain;->activity:Lai/rplay/carcast/CarPlayActivity;
 invoke-virtual {v0},Lai/rplay/carcast/CarPlayActivity;->onPause()V
 sget v0,Lai/rplay/carcast/NativeBridge;->reports:I
 sput v0,Lai/rplay/carcast/InputLifecycleMain;->atPause:I
 return-void
 :burst
 const/4 v0, 0x6
 const/16 v1, 0x100
 const/4 v2, 0x1
 const/4 v3, 0x0
 :again
 invoke-static {v1,v2,v3,v3},Lai/rplay/carcast/CnInput;->enqueue(IIII)V
 invoke-static {v1,v3,v3,v3},Lai/rplay/carcast/CnInput;->enqueue(IIII)V
 add-int/lit8 v0,v0,-0x1
 if-nez v0,:again
 return-void
 :check
 sget v0,Lai/rplay/carcast/NativeBridge;->reports:I
 sget v1,Lai/rplay/carcast/InputLifecycleMain;->atPause:I
 sget-object v2,Ljava/lang/System;->out:Ljava/io/PrintStream;
 if-eqz v1,:empty
 if-ne v0,v1,:failed
 const-string v3,"PASS: no non-neutral reports after onPause"
 invoke-virtual {v2,v3},Ljava/io/PrintStream;->println(Ljava/lang/String;)V
 const/4 v0,0x0
 invoke-static {v0},Ljava/lang/System;->exit(I)V
 return-void
 :empty
 const-string v3,"ERROR: prerequisite input was not observed"
 invoke-virtual {v2,v3},Ljava/io/PrintStream;->println(Ljava/lang/String;)V
 const/4 v0,0x2
 invoke-static {v0},Ljava/lang/System;->exit(I)V
 return-void
 :failed
 const-string v3,"FAIL: non-neutral reports continued after onPause"
 invoke-virtual {v2,v3},Ljava/io/PrintStream;->println(Ljava/lang/String;)V
 const/4 v0,0x1
 invoke-static {v0},Ljava/lang/System;->exit(I)V
 return-void
.end method
'''


OVERLAP_MAIN = '''.method public static main([Ljava/lang/String;)V
 .locals 5
 invoke-static {}, Landroid/os/Looper;->prepareMainLooper()V
 const/4 v0, 0x1
 sput-boolean v0,Lai/rplay/carcast/SettingsActivity;->connected:Z
 const/16 v0,0x16
 const/4 v1,0x0
 invoke-static {v0,v1},Lai/rplay/carcast/CnHold;->update(II)V
 new-instance v0,Landroid/os/Handler;
 invoke-static {},Landroid/os/Looper;->getMainLooper()Landroid/os/Looper;
 move-result-object v1
 invoke-direct {v0,v1},Landroid/os/Handler;-><init>(Landroid/os/Looper;)V
 new-instance v1,Lai/rplay/carcast/InputOverlapStep;
 const/4 v2,0x0
 invoke-direct {v1,v2},Lai/rplay/carcast/InputOverlapStep;-><init>(I)V
 const-wide/16 v2,0xfa
 invoke-virtual {v0,v1,v2,v3},Landroid/os/Handler;->postDelayed(Ljava/lang/Runnable;J)Z
 new-instance v1,Lai/rplay/carcast/InputOverlapStep;
 const/4 v2,0x1
 invoke-direct {v1,v2},Lai/rplay/carcast/InputOverlapStep;-><init>(I)V
 const-wide/16 v2,0x3b6
 invoke-virtual {v0,v1,v2,v3},Landroid/os/Handler;->postDelayed(Ljava/lang/Runnable;J)Z
 new-instance v1,Lai/rplay/carcast/InputOverlapStep;
 const/4 v2,0x2
 invoke-direct {v1,v2},Lai/rplay/carcast/InputOverlapStep;-><init>(I)V
 const-wide/16 v2,0x578
 invoke-virtual {v0,v1,v2,v3},Landroid/os/Handler;->postDelayed(Ljava/lang/Runnable;J)Z
 invoke-static {},Landroid/os/Looper;->loop()V
 return-void
.end method
'''
OVERLAP_STEP = '''.implements Ljava/lang/Runnable;
.field private stage:I
.field private static atRelease:I
.method public constructor <init>(I)V
 .locals 0
 invoke-direct {p0},Ljava/lang/Object;-><init>()V
 iput p1,p0,Lai/rplay/carcast/InputOverlapStep;->stage:I
 return-void
.end method
.method public run()V
 .locals 5
 iget v0,p0,Lai/rplay/carcast/InputOverlapStep;->stage:I
 if-nez v0,:check
 const/16 v0,0x15
 const/4 v1,0x0
 invoke-static {v0,v1},Lai/rplay/carcast/CnHold;->update(II)V
 const/16 v0,0x16
 const/4 v1,0x1
 invoke-static {v0,v1},Lai/rplay/carcast/CnHold;->update(II)V
 return-void
 :check
 sget-object v4,Ljava/lang/System;->out:Ljava/io/PrintStream;
 sget v1,Lai/rplay/carcast/NativeBridge;->reports:I
 const/4 v2,0x1
 if-ne v0,v2,:released
 if-eqz v1,:failed
 sget v2,Lai/rplay/carcast/NativeBridge;->lastWheel:I
 const/4 v3,-0x1
 if-ne v2,v3,:failed
 sput v1,Lai/rplay/carcast/InputOverlapStep;->atRelease:I
 const/16 v0,0x15
 const/4 v1,0x1
 invoke-static {v0,v1},Lai/rplay/carcast/CnHold;->update(II)V
 return-void
 :released
 sget v2,Lai/rplay/carcast/InputOverlapStep;->atRelease:I
 if-ne v1,v2,:failed
 const-string v0,"PASS: unrelated key release preserves the held direction; matching release stops it"
 invoke-virtual {v4,v0},Ljava/io/PrintStream;->println(Ljava/lang/String;)V
 const/4 v0,0x0
 invoke-static {v0},Ljava/lang/System;->exit(I)V
 return-void
 :failed
 const-string v0,"FAIL: overlapping direction release cancelled or failed to stop the current hold"
 invoke-virtual {v4,v0},Ljava/io/PrintStream;->println(Ljava/lang/String;)V
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
    parser.add_argument('--decoded', type=Path, default=ROOT / 'build/work/carcast-cn-src')
    args = parser.parse_args()
    tv = TV(args.serial, args.adb)
    tv.identity()
    project = ROOT / 'build/input-lifecycle'
    smali = project / 'smali'
    if smali.exists():
        shutil.rmtree(smali)  # Only this generated harness directory.
    package = smali / 'ai/rplay/carcast'
    package.mkdir(parents=True)
    for filename in ('apktool.yml', 'AndroidManifest.xml'):
        shutil.copy2(args.decoded / filename, project / filename)
    for name in ('CnHold', 'CnInput', 'CnSiri'):
        shutil.copy2(ROOT / f'src/carcast/smali/ai/rplay/carcast/{name}.smali', package / f'{name}.smali')
    activity = (args.decoded / 'smali/ai/rplay/carcast/CarPlayActivity.smali').read_text()
    start = activity.index('.method public final onPause()V')
    end = activity.index('.end method', start) + len('.end method')
    classes = {
        'CarPlayActivity': ('Landroid/app/Activity;', '.field public e:Lqp;\n' + CONSTRUCTOR + activity[start:end]),
        'SettingsActivity': ('Ljava/lang/Object;', SESSION),
        'NativeBridge': ('Ljava/lang/Object;', SINK),
        'InputLifecycleMain': ('Ljava/lang/Object;', MAIN),
        'InputLifecycleStep': ('Ljava/lang/Object;', STEP),
        'InputOverlapMain': ('Ljava/lang/Object;', OVERLAP_MAIN),
        'InputOverlapStep': ('Ljava/lang/Object;', OVERLAP_STEP),
    }
    for name, (parent, body) in classes.items():
        (package / f'{name}.smali').write_text(HEADER.format(name=name, superclass=parent) + body)
    (smali / 'qp.smali').write_text('.class public Lqp;\n.super Landroid/view/View;\n.field public f:Lop;\n')
    (smali / 'op.smali').write_text('.class public Lop;\n.super Ljava/lang/Object;\n.implements Ljava/lang/Runnable;\n.method public run()V\n.locals 0\nreturn-void\n.end method\n')
    apk, dex = ROOT / 'build/input-lifecycle.apk', ROOT / 'build/input-lifecycle.dex'
    subprocess.run([args.java, '-jar', str(args.apktool), 'b', str(project), '-o', str(apk)], check=True)
    with ZipFile(apk) as archive:
        dex.write_bytes(archive.read('classes.dex'))
    remote = '/data/local/tmp/carcast-input-lifecycle-test.dex'
    tv.run('push', str(dex), remote, timeout=30)
    failed = False
    for scenario in ('hold', 'queue', 'overlap'):
        main_class = 'ai.rplay.carcast.InputOverlapMain' if scenario == 'overlap' else 'ai.rplay.carcast.InputLifecycleMain'
        result = subprocess.run(tv.prefix + ['shell', 'env', 'CLASSPATH=' + remote, 'app_process', '/',
                                             main_class, scenario],
                                capture_output=True, text=True, timeout=15)
        print(scenario + ': ' + result.stdout.strip(), flush=True)
        if result.stderr:
            print(result.stderr[-1200:], flush=True)
        failed |= result.returncode != 0 or 'PASS:' not in result.stdout
    raise SystemExit(1 if failed else 0)


if __name__ == '__main__':
    main()
