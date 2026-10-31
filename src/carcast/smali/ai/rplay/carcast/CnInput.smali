.class public final Lai/rplay/carcast/CnInput;
.super Ljava/lang/Object;
.implements Ljava/lang/Runnable;
.field private static handler:Landroid/os/Handler;
.field private static next:J
.field private static pressed:J
.field private static minimum:J
.field private buttons:I
.field private axes:I
.field private wheel:I

.method public constructor <init>(III)V
    .locals 0
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V
    iput p1, p0, Lai/rplay/carcast/CnInput;->buttons:I
    iput p2, p0, Lai/rplay/carcast/CnInput;->axes:I
    iput p3, p0, Lai/rplay/carcast/CnInput;->wheel:I
    return-void
.end method

.method public static enqueue(IIII)V
    .locals 7
    sget-object v0, Lai/rplay/carcast/CnInput;->handler:Landroid/os/Handler;
    if-nez v0, :ready
    new-instance v0, Landroid/os/Handler;
    invoke-static {}, Landroid/os/Looper;->getMainLooper()Landroid/os/Looper;
    move-result-object v1
    invoke-direct {v0, v1}, Landroid/os/Handler;-><init>(Landroid/os/Looper;)V
    sput-object v0, Lai/rplay/carcast/CnInput;->handler:Landroid/os/Handler;
    :ready
    invoke-static {}, Landroid/os/SystemClock;->uptimeMillis()J
    move-result-wide v1
    sget-wide v3, Lai/rplay/carcast/CnInput;->next:J
    invoke-static {v1, v2, v3, v4}, Ljava/lang/Math;->max(JJ)J
    move-result-wide v1
    or-int v5, p1, p2
    or-int/2addr v5, p3
    if-nez v5, :down
    sget-wide v3, Lai/rplay/carcast/CnInput;->pressed:J
    sget-wide v5, Lai/rplay/carcast/CnInput;->minimum:J
    add-long/2addr v3, v5
    invoke-static {v1, v2, v3, v4}, Ljava/lang/Math;->max(JJ)J
    move-result-wide v1
    goto :queue
    :down
    sput-wide v1, Lai/rplay/carcast/CnInput;->pressed:J
    const-wide/16 v3, 0x64
    if-eqz p2, :duration
    const-wide/16 v3, 0x1e
    :duration
    sput-wide v3, Lai/rplay/carcast/CnInput;->minimum:J
    :queue
    const-wide/16 v3, 0x8
    add-long/2addr v3, v1
    sput-wide v3, Lai/rplay/carcast/CnInput;->next:J
    new-instance v3, Lai/rplay/carcast/CnInput;
    invoke-direct {v3, p1, p2, p3}, Lai/rplay/carcast/CnInput;-><init>(III)V
    invoke-virtual {v0, v3, v1, v2}, Landroid/os/Handler;->postAtTime(Ljava/lang/Runnable;J)Z
    return-void
.end method

.method public static cancel()V
    .locals 4
    invoke-static {}, Lai/rplay/carcast/CnHold;->cancel()V
    invoke-static {}, Lai/rplay/carcast/CnSiri;->cancel()V
    sget-object v0, Lai/rplay/carcast/CnInput;->handler:Landroid/os/Handler;
    const/4 v1, 0x0
    if-eqz v0, :reset
    invoke-virtual {v0, v1}, Landroid/os/Handler;->removeCallbacksAndMessages(Ljava/lang/Object;)V
    :reset
    const-wide/16 v2, 0x0
    sput-wide v2, Lai/rplay/carcast/CnInput;->next:J
    sput-wide v2, Lai/rplay/carcast/CnInput;->pressed:J
    sput-wide v2, Lai/rplay/carcast/CnInput;->minimum:J
    invoke-static {}, Lai/rplay/carcast/SettingsActivity;->g()Z
    move-result v0
    if-eqz v0, :done
    const/16 v0, 0x100
    # Release on the main queue, never inside a native session-ended callback.
    invoke-static {v0, v1, v1, v1}, Lai/rplay/carcast/CnInput;->enqueue(IIII)V
    :done
    return-void
.end method

.method public run()V
    .locals 6
    invoke-static {}, Lai/rplay/carcast/SettingsActivity;->g()Z
    move-result v0
    if-eqz v0, :done
    const/16 v0, 0x100
    iget v1, p0, Lai/rplay/carcast/CnInput;->buttons:I
    iget v2, p0, Lai/rplay/carcast/CnInput;->axes:I
    iget v3, p0, Lai/rplay/carcast/CnInput;->wheel:I
    invoke-static {v0, v1, v2, v3}, Lai/rplay/carcast/NativeBridge;->iapPointer(IIII)V
    new-instance v4, Ljava/lang/StringBuilder;
    const-string v5, "HID buttons="
    invoke-direct {v4, v5}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V
    invoke-virtual {v4, v1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;
    const-string v5, " axes="
    invoke-virtual {v4, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    invoke-virtual {v4, v2}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;
    const-string v5, " wheel="
    invoke-virtual {v4, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    invoke-virtual {v4, v3}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;
    invoke-virtual {v4}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;
    move-result-object v4
    const-string v5, "CnInput"
    invoke-static {v5, v4}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I
    :done
    return-void
.end method
