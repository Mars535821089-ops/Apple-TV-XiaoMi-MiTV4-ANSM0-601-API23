.class public final Lai/rplay/carcast/CnRender;
.super Landroid/view/TextureView;
.implements Landroid/view/TextureView$SurfaceTextureListener;
.implements Ljava/lang/Runnable;

.field private static current:Lai/rplay/carcast/CnRender;
.field private static output:Landroid/view/Surface;
.field private watch:Landroid/os/Handler;
.field private lastFrame:J
.field private frames:J

.method public constructor <init>(Landroid/content/Context;)V
    .locals 2
    invoke-direct {p0, p1}, Landroid/view/TextureView;-><init>(Landroid/content/Context;)V
    invoke-virtual {p0, p0}, Landroid/view/TextureView;->setSurfaceTextureListener(Landroid/view/TextureView$SurfaceTextureListener;)V
    new-instance v0, Landroid/os/Handler;
    invoke-static {}, Landroid/os/Looper;->getMainLooper()Landroid/os/Looper;
    move-result-object v1
    invoke-direct {v0, v1}, Landroid/os/Handler;-><init>(Landroid/os/Looper;)V
    iput-object v0, p0, Lai/rplay/carcast/CnRender;->watch:Landroid/os/Handler;
    return-void
.end method

.method public static attach(Lai/rplay/carcast/CarPlayActivity;)V
    .locals 5
    iget-boolean v0, p0, Lai/rplay/carcast/CarPlayActivity;->f:Z
    if-nez v0, :done
    iget-object v0, p0, Lai/rplay/carcast/CarPlayActivity;->a:Landroid/view/SurfaceView;
    if-eqz v0, :done
    invoke-virtual {v0}, Landroid/view/View;->getParent()Landroid/view/ViewParent;
    move-result-object v1
    instance-of v2, v1, Landroid/view/ViewGroup;
    if-eqz v2, :done
    check-cast v1, Landroid/view/ViewGroup;
    sget-object v2, Lai/rplay/carcast/CnRender;->output:Landroid/view/Surface;
    if-eqz v2, :create
    const/4 v3, 0x0
    const/4 v4, 0x0
    invoke-static {v3, v4}, Lai/rplay/carcast/NativeBridge;->setScreenSurface(ILandroid/view/Surface;)V
    invoke-virtual {v2}, Landroid/view/Surface;->release()V
    sput-object v4, Lai/rplay/carcast/CnRender;->output:Landroid/view/Surface;
    :create
    new-instance v2, Lai/rplay/carcast/CnRender;
    invoke-direct {v2, p0}, Lai/rplay/carcast/CnRender;-><init>(Landroid/content/Context;)V
    sput-object v2, Lai/rplay/carcast/CnRender;->current:Lai/rplay/carcast/CnRender;
    const/4 v3, 0x0
    invoke-virtual {v2, v3}, Landroid/view/View;->setFocusable(Z)V
    invoke-virtual {v2, v3}, Landroid/view/View;->setClickable(Z)V
    # TextureView participates in hit testing; use the original normalized
    # CarPlay touch listener with the same view dimensions.
    new-instance v3, Lai/rplay/carcast/e;
    invoke-direct {v3, p0}, Lai/rplay/carcast/e;-><init>(Lai/rplay/carcast/CarPlayActivity;)V
    invoke-virtual {v2, v3}, Landroid/view/View;->setOnTouchListener(Landroid/view/View$OnTouchListener;)V
    invoke-virtual {v1, v0}, Landroid/view/ViewGroup;->indexOfChild(Landroid/view/View;)I
    move-result v3
    add-int/lit8 v3, v3, 0x1
    invoke-virtual {v0}, Landroid/view/View;->getLayoutParams()Landroid/view/ViewGroup$LayoutParams;
    move-result-object v4
    invoke-virtual {v1, v2, v3, v4}, Landroid/view/ViewGroup;->addView(Landroid/view/View;ILandroid/view/ViewGroup$LayoutParams;)V
    :done
    return-void
.end method

.method public static route(ILandroid/view/Surface;)V
    .locals 1
    if-nez p0, :native
    # Legacy SurfaceView release must not detach the active TextureView.
    # The texture destruction callback owns its native detach and release.
    sget-object v0, Lai/rplay/carcast/CnRender;->current:Lai/rplay/carcast/CnRender;
    if-eqz v0, :native
    sget-object p1, Lai/rplay/carcast/CnRender;->output:Landroid/view/Surface;
    if-eqz p1, :done
    :native
    invoke-static {p0, p1}, Lai/rplay/carcast/NativeBridge;->setScreenSurface(ILandroid/view/Surface;)V
    :done
    return-void
.end method

.method public onSurfaceTextureAvailable(Landroid/graphics/SurfaceTexture;II)V
    .locals 2
    new-instance v0, Landroid/view/Surface;
    invoke-direct {v0, p1}, Landroid/view/Surface;-><init>(Landroid/graphics/SurfaceTexture;)V
    sput-object v0, Lai/rplay/carcast/CnRender;->output:Landroid/view/Surface;
    const/4 v1, 0x0
    invoke-static {v1, v0}, Lai/rplay/carcast/NativeBridge;->setScreenSurface(ILandroid/view/Surface;)V
    const-string v0, "CnRender"
    const-string v1, "CarPlay TextureView surface ready"
    invoke-static {v0, v1}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I
    invoke-static {}, Landroid/os/SystemClock;->elapsedRealtime()J
    move-result-wide v0
    iput-wide v0, p0, Lai/rplay/carcast/CnRender;->lastFrame:J
    invoke-direct {p0}, Lai/rplay/carcast/CnRender;->schedule()V
    return-void
.end method

.method public onSurfaceTextureDestroyed(Landroid/graphics/SurfaceTexture;)Z
    .locals 2
    iget-object v0, p0, Lai/rplay/carcast/CnRender;->watch:Landroid/os/Handler;
    invoke-virtual {v0, p0}, Landroid/os/Handler;->removeCallbacks(Ljava/lang/Runnable;)V
    sget-object v0, Lai/rplay/carcast/CnRender;->current:Lai/rplay/carcast/CnRender;
    if-ne v0, p0, :done
    const/4 v0, 0x0
    const/4 v1, 0x0
    invoke-static {v0, v1}, Lai/rplay/carcast/NativeBridge;->setScreenSurface(ILandroid/view/Surface;)V
    sget-object v0, Lai/rplay/carcast/CnRender;->output:Landroid/view/Surface;
    if-eqz v0, :clear
    invoke-virtual {v0}, Landroid/view/Surface;->release()V
    :clear
    sput-object v1, Lai/rplay/carcast/CnRender;->output:Landroid/view/Surface;
    sput-object v1, Lai/rplay/carcast/CnRender;->current:Lai/rplay/carcast/CnRender;
    :done
    const/4 v0, 0x1
    return v0
.end method

.method public onSurfaceTextureSizeChanged(Landroid/graphics/SurfaceTexture;II)V
    .locals 0
    return-void
.end method

.method public onSurfaceTextureUpdated(Landroid/graphics/SurfaceTexture;)V
    .locals 4
    invoke-static {}, Landroid/os/SystemClock;->elapsedRealtime()J
    move-result-wide v0
    iput-wide v0, p0, Lai/rplay/carcast/CnRender;->lastFrame:J
    iget-wide v0, p0, Lai/rplay/carcast/CnRender;->frames:J
    const-wide/16 v2, 0x1
    add-long/2addr v0, v2
    iput-wide v0, p0, Lai/rplay/carcast/CnRender;->frames:J
    return-void
.end method

.method private schedule()V
    .locals 3
    iget-object v0, p0, Lai/rplay/carcast/CnRender;->watch:Landroid/os/Handler;
    const-wide/16 v1, 0x7530
    invoke-virtual {v0, p0, v1, v2}, Landroid/os/Handler;->postDelayed(Ljava/lang/Runnable;J)Z
    return-void
.end method

.method public run()V
    .locals 8
    sget-object v0, Lai/rplay/carcast/CnRender;->current:Lai/rplay/carcast/CnRender;
    if-ne v0, p0, :done
    invoke-static {}, Landroid/os/SystemClock;->elapsedRealtime()J
    move-result-wide v0
    iget-wide v2, p0, Lai/rplay/carcast/CnRender;->lastFrame:J
    sub-long v2, v0, v2
    new-instance v4, Ljava/lang/StringBuilder;
    const-string v5, "CarPlay frameAgeMs="
    invoke-direct {v4, v5}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V
    invoke-virtual {v4, v2, v3}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;
    const-string v5, " frames="
    invoke-virtual {v4, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    iget-wide v6, p0, Lai/rplay/carcast/CnRender;->frames:J
    invoke-virtual {v4, v6, v7}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;
    invoke-virtual {v4}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;
    move-result-object v4
    const-string v5, "CnFrameHealth"
    invoke-static {v5, v4}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I
    # A static phone UI or a missing TextureView callback does not prove the
    # session is dead. Keep this observer read-only with respect to transport;
    # genuine SDK session-ended events retain their existing reconnect path.
    invoke-direct {p0}, Lai/rplay/carcast/CnRender;->schedule()V
    :done
    return-void
.end method
