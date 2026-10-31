.class public final Lai/rplay/carcast/CnProbeHost;
.super Ljava/lang/Object;
.field private static handler:Landroid/os/Handler;

.method public static frame()[I
 .locals 1
 invoke-static {},Lai/rplay/carcast/CnRender;->captureProbeFrame()[I
 move-result-object v0
 return-object v0
.end method
.method public static version()J
 .locals 2
 invoke-static {},Lai/rplay/carcast/CnRender;->captureProbeVersion()J
 move-result-wide v0
 return-wide v0
.end method
.method public static now()J
 .locals 2
 invoke-static {},Landroid/os/SystemClock;->elapsedRealtime()J
 move-result-wide v0
 return-wide v0
.end method
.method public static generation()J
 .locals 2
 invoke-static {},Lai/rplay/carcast/CnRender;->captureProbeGeneration()J
 move-result-wide v0
 return-wide v0
.end method
.method public static send(II)V
 .locals 2
 const/4 v1,0x0
 invoke-static {p1,v1,v1,p0},Lai/rplay/carcast/CnInput;->enqueue(IIII)V
 invoke-static {p1,v1,v1,v1},Lai/rplay/carcast/CnInput;->enqueue(IIII)V
 return-void
.end method
.method public static post(Ljava/lang/Runnable;J)V
 .locals 2
 sget-object v0,Lai/rplay/carcast/CnProbeHost;->handler:Landroid/os/Handler;
 if-nez v0,:ready
 new-instance v0,Landroid/os/Handler;
 invoke-static {},Landroid/os/Looper;->getMainLooper()Landroid/os/Looper;
 move-result-object v1
 invoke-direct {v0,v1},Landroid/os/Handler;-><init>(Landroid/os/Looper;)V
 sput-object v0,Lai/rplay/carcast/CnProbeHost;->handler:Landroid/os/Handler;
 :ready
 invoke-virtual {v0,p0,p1,p2},Landroid/os/Handler;->postDelayed(Ljava/lang/Runnable;J)Z
 return-void
.end method
.method public static clear()V
 .locals 2
 sget-object v0,Lai/rplay/carcast/CnProbeHost;->handler:Landroid/os/Handler;
 if-eqz v0,:done
 const/4 v1,0x0
 invoke-virtual {v0,v1},Landroid/os/Handler;->removeCallbacksAndMessages(Ljava/lang/Object;)V
 :done
 return-void
.end method
.method public static log(Ljava/lang/String;)V
 .locals 1
 const-string v0,"CnFocusProbe"
 invoke-static {v0,p0},Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I
 return-void
.end method

.method public static ready()Z
 .locals 1
 invoke-static {},Lai/rplay/carcast/CnInput;->canProbe()Z
 move-result v0
 return v0
.end method
