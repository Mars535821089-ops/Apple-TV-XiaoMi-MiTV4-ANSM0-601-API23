"""Execute the real experimental key handler on API23 with isolated sinks.

No APK install and no phone input. Real Android KeyEvent is used; only the
coordinator and transport boundaries are doubled to exercise key dispatch.
"""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys
from zipfile import ZipFile
from run_input_lifecycle import HEADER
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from device import TV

def method(name,args,body,result='V',locals=2):
 return f'.method public static {name}({args}){result}\n.locals {locals}\n{body}\n.end method\n'

NAV=''.join('.field public static '+n+':'+t+'\n' for n,t in [('active','Z'),('unknown','Z'),('requests','I')])
for name,field in [('busy','active'),('uncertain','unknown')]:
 NAV+=method(name,'',f'sget-boolean v0,Lai/rplay/carcast/CnSpatialNavigator;->{field}:Z\nreturn v0','Z')
NAV+=method('request','I','sget v0,Lai/rplay/carcast/CnSpatialNavigator;->requests:I\nadd-int/lit8 v0,v0,0x1\nsput v0,Lai/rplay/carcast/CnSpatialNavigator;->requests:I\nreturn-void')
NAV+=method('stop','','const/4 v0,0x0\nsput-boolean v0,Lai/rplay/carcast/CnSpatialNavigator;->active:Z\nreturn-void')
NAV+=method('cancel','','const/4 v0,0x0\nsput-boolean v0,Lai/rplay/carcast/CnSpatialNavigator;->active:Z\nsput-boolean v0,Lai/rplay/carcast/CnSpatialNavigator;->unknown:Z\nreturn-void')
PROBE=method('busy','','const/4 v0,0x0\nreturn v0','Z')+method('request','I','return-void')+method('cancel','','return-void')
INPUT='.field public static reports:I\n.field public static buttons:I\n'+method('enqueue','IIII','sget v0,Lai/rplay/carcast/CnInput;->reports:I\nadd-int/lit8 v0,v0,0x1\nsput v0,Lai/rplay/carcast/CnInput;->reports:I\nsput p1,Lai/rplay/carcast/CnInput;->buttons:I\nreturn-void')
MAIN=method('press','II','new-instance v0,Landroid/view/KeyEvent;\ninvoke-direct {v0,p1,p0},Landroid/view/KeyEvent;-><init>(II)V\nconst/4 v1,0x0\ninvoke-static {v1,p0,v0},Lai/rplay/carcast/CnKeys;->handle(Lai/rplay/carcast/CarPlayActivity;ILandroid/view/KeyEvent;)Z\nreturn-void')
MAIN+=method('expect','IILjava/lang/String;','if-eq p0,p1,:ok\nnew-instance v0,Ljava/lang/AssertionError;\ninvoke-direct {v0,p2},Ljava/lang/AssertionError;-><init>(Ljava/lang/Object;)V\nthrow v0\n:ok\nreturn-void')
body=['invoke-static {},Landroid/os/Looper;->prepareMainLooper()V',':test_start','const/4 v0,0x1','sput-boolean v0,Lai/rplay/carcast/CnSpatialNavigator;->active:Z']
def press(key,action):
 body.extend([f'const/16 v0,{hex(key)}',f'const/4 v1,{hex(action)}','invoke-static {v0,v1},Lai/rplay/carcast/SpatialKeysMain;->press(II)V'])
def expect(owner,field,value,label):
 body.extend([f'sget v0,Lai/rplay/carcast/{owner};->{field}:I',f'const/16 v1,{hex(value)}',f'const-string v2,"{label}"','invoke-static {v0,v1,v2},Lai/rplay/carcast/SpatialKeysMain;->expect(IILjava/lang/String;)V'])
press(23,0);expect('CnInput','reports',0,'Select DOWN escaped while navigation busy')
press(23,1);expect('CnInput','reports',1,'Select UP release must pass');expect('CnInput','buttons',0,'release must be neutral')
body.extend(['const/4 v0,0x0','sput-boolean v0,Lai/rplay/carcast/CnSpatialNavigator;->active:Z','sput v0,Lai/rplay/carcast/CnInput;->reports:I','const/4 v0,0x1','sput-boolean v0,Lai/rplay/carcast/CnSpatialNavigator;->unknown:Z'])
press(66,0);expect('CnInput','reports',0,'Enter DOWN escaped with unknown focus')
press(24,0);press(66,0);expect('CnInput','reports',0,'volume unlocked unknown focus')
press(82,0);expect('CnInput','reports',1,'Home must remain usable');expect('CnInput','buttons',2,'Home report must be preserved')
press(66,0);expect('CnInput','reports',2,'Select must work after explicit Home');expect('CnInput','buttons',1,'Select report must be preserved')
press(19,0);press(19,1);expect('CnSpatialNavigator','requests',1,'direction must route once to spatial coordinator');expect('CnInput','reports',2,'direction cannot also send old rotary mapping')
body.extend(['sget-object v0,Ljava/lang/System;->out:Ljava/io/PrintStream;','const-string v1,"PASS: real API23 key dispatch, Select gate, release, volume isolation and spatial routing"','invoke-virtual {v0,v1},Ljava/io/PrintStream;->println(Ljava/lang/String;)V','return-void'])
body.extend([':test_end','.catch Ljava/lang/Throwable; {:test_start .. :test_end} :failed',':failed','move-exception v0','invoke-virtual {v0},Ljava/lang/Throwable;->printStackTrace()V','sget-object v1,Ljava/lang/System;->out:Ljava/io/PrintStream;','invoke-virtual {v1,v0},Ljava/io/PrintStream;->println(Ljava/lang/Object;)V','const/4 v0,0x1','invoke-static {v0},Ljava/lang/System;->exit(I)V','return-void'])
MAIN+=method('main','[Ljava/lang/String;','\n'.join(body),locals=4)

def main():
 p=argparse.ArgumentParser(description=__doc__)
 for n in ('serial','adb','java','apktool'):p.add_argument('--'+n,required=True)
 p.add_argument('--baseline',action='store_true');a=p.parse_args();tv=TV(a.serial,a.adb);tv.identity()
 decoded=ROOT/'build/work/carcast-cn-src';project=ROOT/'build/spatial-keys';package=project/'smali/ai/rplay/carcast'
 if project.exists():shutil.rmtree(project)
 package.mkdir(parents=True)
 for name in ('apktool.yml','AndroidManifest.xml'):shutil.copy2(decoded/name,project/name)
 keys=ROOT/'src/carcast/smali/ai/rplay/carcast/CnKeys.smali' if a.baseline else decoded/'smali/ai/rplay/carcast/CnKeys.smali'
 shutil.copy2(keys,package/'CnKeys.smali')
 for name,source in {'CnSpatialNavigator':NAV,'CnFocusProbe':PROBE,'CnInput':INPUT,'CnHold':method('update','II','return-void'),'CnSiri':method('start','','return-void'),'SpatialKeysMain':MAIN,'CarPlayActivity':''}.items():
  superclass='Landroid/app/Activity;' if name=='CarPlayActivity' else 'Ljava/lang/Object;'
  (package/(name+'.smali')).write_text(HEADER.format(name=name,superclass=superclass)+source)
 apk,dex=ROOT/'build/spatial-keys.apk',ROOT/'build/spatial-keys.dex'
 subprocess.run([a.java,'-jar',a.apktool,'b',str(project),'-o',str(apk)],check=True,stdout=subprocess.DEVNULL)
 with ZipFile(apk) as z:dex.write_bytes(z.read('classes.dex'))
 remote='/data/local/tmp/carcast-spatial-keys-test.dex';tv.run('push',str(dex),remote,timeout=30)
 r=subprocess.run(tv.prefix+['shell','env','CLASSPATH='+remote,'app_process','/','ai.rplay.carcast.SpatialKeysMain'],capture_output=True,text=True,timeout=10)
 print(r.stdout.strip());print(r.stderr[-1200:]);return 0 if r.returncode==0 and 'PASS:' in r.stdout else 1
if __name__=='__main__':raise SystemExit(main())
