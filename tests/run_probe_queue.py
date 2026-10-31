"""Actual API23 input queue: cancelling a probe must not cancel user reports."""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys
from zipfile import ZipFile
from run_input_lifecycle import HEADER, SESSION, SINK

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from device import TV

PROBE='''.field public static active:Z
.method public static cancel()V
.locals 1
const/4 v0,0x0
sput-boolean v0,Lai/rplay/carcast/CnFocusProbe;->active:Z
return-void
.end method
.method public static validToken(I)Z
.locals 1
sget-boolean v0,Lai/rplay/carcast/CnFocusProbe;->active:Z
return v0
.end method
'''
MAIN='''.implements Ljava/lang/Runnable;
.method public constructor <init>()V
.locals 0
invoke-direct {p0},Ljava/lang/Object;-><init>()V
return-void
.end method
.method public static main([Ljava/lang/String;)V
.locals 6
invoke-static {},Landroid/os/Looper;->prepareMainLooper()V
const/4 v0,0x1
sput-boolean v0,Lai/rplay/carcast/SettingsActivity;->connected:Z
sput-boolean v0,Lai/rplay/carcast/CnFocusProbe;->active:Z
const/16 v0,0x1001
const/4 v1,0x0
const/4 v2,0x1
invoke-static {v0,v1,v1,v2},Lai/rplay/carcast/CnInput;->enqueue(IIII)V
const/16 v0,0x100
const/4 v2,-0x1
invoke-static {v0,v1,v1,v2},Lai/rplay/carcast/CnInput;->enqueue(IIII)V
invoke-static {},Lai/rplay/carcast/CnFocusProbe;->cancel()V
new-instance v0,Landroid/os/Handler;
invoke-static {},Landroid/os/Looper;->getMainLooper()Landroid/os/Looper;
move-result-object v1
invoke-direct {v0,v1},Landroid/os/Handler;-><init>(Landroid/os/Looper;)V
new-instance v1,Lai/rplay/carcast/ProbeQueueMain;
invoke-direct {v1},Lai/rplay/carcast/ProbeQueueMain;-><init>()V
const-wide/16 v2,0x1f4
invoke-virtual {v0,v1,v2,v3},Landroid/os/Handler;->postDelayed(Ljava/lang/Runnable;J)Z
invoke-static {},Landroid/os/Looper;->loop()V
return-void
.end method
.method public run()V
.locals 4
sget v0,Lai/rplay/carcast/NativeBridge;->reports:I
const/4 v1,0x1
sget-object v2,Ljava/lang/System;->out:Ljava/io/PrintStream;
if-ne v0,v1,:failed
sget v0,Lai/rplay/carcast/NativeBridge;->lastWheel:I
const/4 v1,-0x1
if-ne v0,v1,:failed
const-string v3,"PASS: cancelled probe report skipped; queued user report preserved"
invoke-virtual {v2,v3},Ljava/io/PrintStream;->println(Ljava/lang/String;)V
const/4 v0,0x0
invoke-static {v0},Ljava/lang/System;->exit(I)V
return-void
:failed
const-string v3,"FAIL: cancelled probe report escaped or user report was removed"
invoke-virtual {v2,v3},Ljava/io/PrintStream;->println(Ljava/lang/String;)V
const/4 v0,0x1
invoke-static {v0},Ljava/lang/System;->exit(I)V
return-void
.end method
'''

def main():
 p=argparse.ArgumentParser(description=__doc__)
 for n in ('serial','adb','java','apktool'):p.add_argument('--'+n,required=True)
 a=p.parse_args();tv=TV(a.serial,a.adb);tv.identity()
 decoded=ROOT/'build/work/carcast-cn-src';project=ROOT/'build/probe-queue';package=project/'smali/ai/rplay/carcast';package.mkdir(parents=True,exist_ok=True)
 for name in ('apktool.yml','AndroidManifest.xml'):shutil.copy2(decoded/name,project/name)
 for name in ('CnHold','CnInput','CnSiri'):shutil.copy2(decoded/f'smali/ai/rplay/carcast/{name}.smali',package/f'{name}.smali')
 nav='''.method public static stop()V
.locals 0
invoke-static {},Lai/rplay/carcast/CnFocusProbe;->cancel()V
return-void
.end method
'''
 for name,body in {'SettingsActivity':SESSION,'NativeBridge':SINK,'CnFocusProbe':PROBE,'CnSpatialNavigator':nav,'ProbeQueueMain':MAIN}.items():
  (package/f'{name}.smali').write_text(HEADER.format(name=name,superclass='Ljava/lang/Object;')+body)
 apk,dex=ROOT/'build/probe-queue.apk',ROOT/'build/probe-queue.dex'
 subprocess.run([a.java,'-jar',a.apktool,'b',str(project),'-o',str(apk)],check=True)
 with ZipFile(apk) as z:dex.write_bytes(z.read('classes.dex'))
 remote='/data/local/tmp/carcast-probe-queue-test.dex';tv.run('push',str(dex),remote,timeout=30)
 r=subprocess.run(tv.prefix+['shell','env','CLASSPATH='+remote,'app_process','/','ai.rplay.carcast.ProbeQueueMain'],capture_output=True,text=True,timeout=10)
 print(r.stdout.strip());print(r.stderr[-800:])
 return 0 if r.returncode==0 and 'PASS:' in r.stdout else 1

if __name__=='__main__':raise SystemExit(main())
