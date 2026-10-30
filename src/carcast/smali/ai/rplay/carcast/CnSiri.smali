.class public final Lai/rplay/carcast/CnSiri;
.super Ljava/lang/Object;
.implements Ljava/lang/Runnable;
.field private static active:Z
.field private static handler:Landroid/os/Handler;

.method public constructor <init>()V
    .locals 0
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V
    return-void
.end method

.method public static start()V
    .locals 5
    sget-boolean v0, Lai/rplay/carcast/CnSiri;->active:Z
    if-nez v0, :done
    invoke-static {}, Lai/rplay/carcast/SettingsActivity;->g()Z
    move-result v0
    if-eqz v0, :done
    const/4 v0, 0x1
    sput-boolean v0, Lai/rplay/carcast/CnSiri;->active:Z
    new-instance v0, Landroid/os/Handler;
    invoke-static {}, Landroid/os/Looper;->getMainLooper()Landroid/os/Looper;
    move-result-object v1
    invoke-direct {v0, v1}, Landroid/os/Handler;-><init>(Landroid/os/Looper;)V
    sput-object v0, Lai/rplay/carcast/CnSiri;->handler:Landroid/os/Handler;
    const/16 v1, 0x100
    const/16 v2, 0x8
    const/4 v3, 0x0
    invoke-static {v1, v2, v3, v3}, Lai/rplay/carcast/CnInput;->enqueue(IIII)V
    new-instance v1, Lai/rplay/carcast/CnSiri;
    invoke-direct {v1}, Lai/rplay/carcast/CnSiri;-><init>()V
    const-wide/16 v2, 0x5dc
    invoke-virtual {v0, v1, v2, v3}, Landroid/os/Handler;->postDelayed(Ljava/lang/Runnable;J)Z
    const-string v0, "CnSiri"
    const-string v1, "CarPlay voice activation requested"
    invoke-static {v0, v1}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I
    :done
    return-void
.end method

.method public run()V
    .locals 2
    const/16 v0, 0x100
    const/4 v1, 0x0
    invoke-static {v0, v1, v1, v1}, Lai/rplay/carcast/CnInput;->enqueue(IIII)V
    sput-boolean v1, Lai/rplay/carcast/CnSiri;->active:Z
    return-void
.end method
