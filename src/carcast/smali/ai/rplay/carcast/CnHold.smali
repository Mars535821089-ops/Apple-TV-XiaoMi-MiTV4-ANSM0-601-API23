.class public final Lai/rplay/carcast/CnHold;
.super Ljava/lang/Object;
.implements Ljava/lang/Runnable;
.field private static handler:Landroid/os/Handler;
.field private static active:Lai/rplay/carcast/CnHold;
.field private direction:I

.method public constructor <init>(I)V
    .locals 0
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V
    iput p1, p0, Lai/rplay/carcast/CnHold;->direction:I
    return-void
.end method

.method public static update(II)V
    .locals 4
    const/16 v0, 0x13
    if-lt p0, v0, :done
    const/16 v0, 0x16
    if-gt p0, v0, :done
    sget-object v0, Lai/rplay/carcast/CnHold;->handler:Landroid/os/Handler;
    if-nez v0, :ready
    new-instance v0, Landroid/os/Handler;
    invoke-static {}, Landroid/os/Looper;->getMainLooper()Landroid/os/Looper;
    move-result-object v1
    invoke-direct {v0, v1}, Landroid/os/Handler;-><init>(Landroid/os/Looper;)V
    sput-object v0, Lai/rplay/carcast/CnHold;->handler:Landroid/os/Handler;
    :ready
    sget-object v1, Lai/rplay/carcast/CnHold;->active:Lai/rplay/carcast/CnHold;
    if-eqz v1, :create
    invoke-virtual {v0, v1}, Landroid/os/Handler;->removeCallbacks(Ljava/lang/Runnable;)V
    :create
    const/4 v1, 0x0
    sput-object v1, Lai/rplay/carcast/CnHold;->active:Lai/rplay/carcast/CnHold;
    if-nez p1, :done
    const/4 v1, 0x1
    const/16 v2, 0x13
    if-eq p0, v2, :previous
    const/16 v2, 0x15
    if-ne p0, v2, :new
    :previous
    const/4 v1, -0x1
    :new
    new-instance v2, Lai/rplay/carcast/CnHold;
    invoke-direct {v2, v1}, Lai/rplay/carcast/CnHold;-><init>(I)V
    sput-object v2, Lai/rplay/carcast/CnHold;->active:Lai/rplay/carcast/CnHold;
    const-wide/16 v1, 0x258
    sget-object v3, Lai/rplay/carcast/CnHold;->active:Lai/rplay/carcast/CnHold;
    invoke-virtual {v0, v3, v1, v2}, Landroid/os/Handler;->postDelayed(Ljava/lang/Runnable;J)Z
    :done
    return-void
.end method

.method public static cancel()V
    .locals 3
    sget-object v0, Lai/rplay/carcast/CnHold;->active:Lai/rplay/carcast/CnHold;
    const/4 v1, 0x0
    sput-object v1, Lai/rplay/carcast/CnHold;->active:Lai/rplay/carcast/CnHold;
    if-eqz v0, :done
    sget-object v2, Lai/rplay/carcast/CnHold;->handler:Landroid/os/Handler;
    if-eqz v2, :done
    invoke-virtual {v2, v0}, Landroid/os/Handler;->removeCallbacks(Ljava/lang/Runnable;)V
    :done
    return-void
.end method

.method public run()V
    .locals 6
    sget-object v0, Lai/rplay/carcast/CnHold;->active:Lai/rplay/carcast/CnHold;
    if-ne v0, p0, :done
    invoke-static {}, Lai/rplay/carcast/SettingsActivity;->g()Z
    move-result v0
    if-eqz v0, :done
    const/16 v0, 0x100
    const/4 v1, 0x0
    iget v2, p0, Lai/rplay/carcast/CnHold;->direction:I
    invoke-static {v0, v1, v1, v2}, Lai/rplay/carcast/CnInput;->enqueue(IIII)V
    sget-object v3, Lai/rplay/carcast/CnHold;->handler:Landroid/os/Handler;
    const-wide/16 v4, 0xfa
    invoke-virtual {v3, p0, v4, v5}, Landroid/os/Handler;->postDelayed(Ljava/lang/Runnable;J)Z
    :done
    return-void
.end method
