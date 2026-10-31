"""API23: actual probe send/queue emits one delta, cancellation still releases."""
import argparse
from pathlib import Path
import shutil,subprocess,sys
from zipfile import ZipFile
from run_input_lifecycle import HEADER,SESSION
from run_probe_queue import PROBE
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from device import TV
SINK='''.field public static count:I
.field public static wheel:I
.method public static iapPointer(IIII)V
.locals 1
sget v0,Lai/rplay/carcast/NativeBridge;->count:I
add-int/lit8 v0,v0,0x1
sput v0,Lai/rplay/carcast/NativeBridge;->count:I
sput p3,Lai/rplay/carcast/NativeBridge;->wheel:I
return-void
.end method
'''
NAV='''.method public static stop()V
.locals 0
invoke-static {},Lai/rplay/carcast/CnFocusProbe;->cancel()V
return-void
.end method
'''
MAIN='''.implements Ljava/lang/Runnable;
.field private stage:I
.field private static h:Landroid/os/Handler;
.method public constructor <init>(I)V
.locals 0
invoke-direct {p0},Ljava/lang/Object;-><init>()V
iput p1,p0,Lai/rplay/carcast/WheelDeltaMain;->stage:I
return-void
.end method
.method public static main([Ljava/lang/String;)V
.locals 5
invoke-static {},Landroid/os/Looper;->prepareMainLooper()V
const/4 v0,0x1
sput-boolean v0,Lai/rplay/carcast/SettingsActivity;->connected:Z
sput-boolean v0,Lai/rplay/carcast/CnFocusProbe;->active:Z
const/16 v1,0x1001
invoke-static {v0,v1},Lai/rplay/carcast/CnProbeHost;->send(II)V
new-instance v0,Landroid/os/Handler;
invoke-static {},Landroid/os/Looper;->getMainLooper()Landroid/os/Looper;
move-result-object v1
invoke-direct {v0,v1},Landroid/os/Handler;-><init>(Landroid/os/Looper;)V
sput-object v0,Lai/rplay/carcast/WheelDeltaMain;->h:Landroid/os/Handler;
new-instance v1,Lai/rplay/carcast/WheelDeltaMain;
const/4 v2,0x0
invoke-direct {v1,v2},Lai/rplay/carcast/WheelDeltaMain;-><init>(I)V
const-wide/16 v2,0x2bc
invoke-virtual {v0,v1,v2,v3},Landroid/os/Handler;->postDelayed(Ljava/lang/Runnable;J)Z
invoke-static {},Landroid/os/Looper;->loop()V
return-void
.end method
.method public run()V
.locals 5
iget v0,p0,Lai/rplay/carcast/WheelDeltaMain;->stage:I
sget v1,Lai/rplay/carcast/NativeBridge;->count:I
if-nez v0,:release
const/4 v2,0x1
if-ne v1,v2,:failed
sget v1,Lai/rplay/carcast/NativeBridge;->wheel:I
if-ne v1,v2,:failed
invoke-static {},Lai/rplay/carcast/CnInput;->cancel()V
sget-object v0,Lai/rplay/carcast/WheelDeltaMain;->h:Landroid/os/Handler;
new-instance v1,Lai/rplay/carcast/WheelDeltaMain;
invoke-direct {v1,v2},Lai/rplay/carcast/WheelDeltaMain;-><init>(I)V
const-wide/16 v2,0x12c
invoke-virtual {v0,v1,v2,v3},Landroid/os/Handler;->postDelayed(Ljava/lang/Runnable;J)Z
return-void
:release
const/4 v2,0x2
if-ne v1,v2,:failed
sget v1,Lai/rplay/carcast/NativeBridge;->wheel:I
if-nez v1,:failed
sget-object v0,Ljava/lang/System;->out:Ljava/io/PrintStream;
const-string v1,"PASS: one relative wheel report; normal cancellation still emits neutral release"
invoke-virtual {v0,v1},Ljava/io/PrintStream;->println(Ljava/lang/String;)V
const/4 v0,0x0
invoke-static {v0},Ljava/lang/System;->exit(I)V
return-void
:failed
sget-object v0,Ljava/lang/System;->out:Ljava/io/PrintStream;
const-string v2,"FAIL: extra zero wheel report or missing cancellation release; report count="
invoke-virtual {v0,v2},Ljava/io/PrintStream;->print(Ljava/lang/String;)V
invoke-virtual {v0,v1},Ljava/io/PrintStream;->println(I)V
const/4 v0,0x1
invoke-static {v0},Ljava/lang/System;->exit(I)V
return-void
.end method
'''

def main():
 p=argparse.ArgumentParser(description=__doc__)
 for n in ('serial','adb','java','apktool'):p.add_argument('--'+n,required=True)
 a=p.parse_args();tv=TV(a.serial,a.adb);tv.identity()
 decoded=ROOT/'build/work/carcast-cn-src';project=ROOT/'build/wheel-delta-test';package=project/'smali/ai/rplay/carcast'
 if project.exists():shutil.rmtree(project)
 package.mkdir(parents=True)
 for n in ('apktool.yml','AndroidManifest.xml'):shutil.copy2(decoded/n,project/n)
 for n in ('CnInput','CnHold','CnSiri'):shutil.copy2(decoded/f'smali/ai/rplay/carcast/{n}.smali',package/f'{n}.smali')
 host=(decoded/'smali/ai/rplay/carcast/CnProbeHost.smali').read_text();start=host.index('.method public static send(');end=host.index('.end method',start)+len('.end method')
 for n,body in {'SettingsActivity':SESSION,'NativeBridge':SINK,'CnFocusProbe':PROBE,'CnSpatialNavigator':NAV,'CnProbeHost':host[start:end],'WheelDeltaMain':MAIN}.items():
  (package/f'{n}.smali').write_text(HEADER.format(name=n,superclass='Ljava/lang/Object;')+body)
 apk,dex=ROOT/'build/wheel-delta-test.apk',ROOT/'build/wheel-delta-test.dex'
 subprocess.run([a.java,'-jar',a.apktool,'b',str(project),'-o',str(apk)],check=True,stdout=subprocess.DEVNULL)
 with ZipFile(apk) as z:dex.write_bytes(z.read('classes.dex'))
 remote='/data/local/tmp/carcast-wheel-delta-test.dex';tv.run('push',str(dex),remote,timeout=30)
 r=subprocess.run(tv.prefix+['shell','env','CLASSPATH='+remote,'app_process','/','ai.rplay.carcast.WheelDeltaMain'],capture_output=True,text=True,timeout=10)
 print(r.stdout.strip());print(r.stderr[-800:]);return 0 if r.returncode==0 and 'PASS:' in r.stdout else 1
if __name__=='__main__':raise SystemExit(main())
