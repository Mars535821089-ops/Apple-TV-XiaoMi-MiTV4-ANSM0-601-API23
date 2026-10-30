.class public final Lai/rplay/carcast/CnRemote;
.super Ljava/lang/Object;

.method public static configure(Landroid/content/Context;)V
    .locals 4
    const-string v0, "carcast"
    const/4 v1, 0x0
    invoke-virtual {p0, v0, v1}, Landroid/content/Context;->getSharedPreferences(Ljava/lang/String;I)Landroid/content/SharedPreferences;
    move-result-object v0
    const-string v2, "cn.tv.profile.v4"
    invoke-interface {v0, v2, v1}, Landroid/content/SharedPreferences;->getBoolean(Ljava/lang/String;Z)Z
    move-result v3
    if-nez v3, :done
    invoke-interface {v0}, Landroid/content/SharedPreferences;->edit()Landroid/content/SharedPreferences$Editor;
    move-result-object v0
    const/4 v3, 0x1
    invoke-interface {v0, v2, v3}, Landroid/content/SharedPreferences$Editor;->putBoolean(Ljava/lang/String;Z)Landroid/content/SharedPreferences$Editor;
    const-string v2, "carcast.carplay.ultra"
    invoke-interface {v0, v2, v1}, Landroid/content/SharedPreferences$Editor;->putBoolean(Ljava/lang/String;Z)Landroid/content/SharedPreferences$Editor;
    const-string v2, "carcast.carplay.alt_screen"
    invoke-interface {v0, v2, v1}, Landroid/content/SharedPreferences$Editor;->putBoolean(Ljava/lang/String;Z)Landroid/content/SharedPreferences$Editor;
    const-string v2, "carcast.carplay.nowplaying"
    invoke-interface {v0, v2, v1}, Landroid/content/SharedPreferences$Editor;->putBoolean(Ljava/lang/String;Z)Landroid/content/SharedPreferences$Editor;
    const-string v2, "carcast.carplay.vehicle_state"
    invoke-interface {v0, v2, v1}, Landroid/content/SharedPreferences$Editor;->putBoolean(Ljava/lang/String;Z)Landroid/content/SharedPreferences$Editor;
    const-string v2, "carcast.carplay.custom_knob"
    const/4 v3, 0x1
    invoke-interface {v0, v2, v3}, Landroid/content/SharedPreferences$Editor;->putBoolean(Ljava/lang/String;Z)Landroid/content/SharedPreferences$Editor;
    const-string v2, "carcast.carplay.no_knob"
    invoke-interface {v0, v2, v1}, Landroid/content/SharedPreferences$Editor;->putBoolean(Ljava/lang/String;Z)Landroid/content/SharedPreferences$Editor;
    const-string v2, "carcast.carplay.preset"
    const-string v3, "custom"
    invoke-interface {v0, v2, v3}, Landroid/content/SharedPreferences$Editor;->putString(Ljava/lang/String;Ljava/lang/String;)Landroid/content/SharedPreferences$Editor;
    const-string v2, "carcast.carplay.custom_width"
    const/16 v3, 0x500
    invoke-interface {v0, v2, v3}, Landroid/content/SharedPreferences$Editor;->putInt(Ljava/lang/String;I)Landroid/content/SharedPreferences$Editor;
    const-string v2, "carcast.carplay.custom_height"
    const/16 v3, 0x2d0
    invoke-interface {v0, v2, v3}, Landroid/content/SharedPreferences$Editor;->putInt(Ljava/lang/String;I)Landroid/content/SharedPreferences$Editor;
    invoke-interface {v0}, Landroid/content/SharedPreferences$Editor;->commit()Z
    :done
    return-void
.end method

.method public static handle(Lai/rplay/carcast/CarPlayActivity;ILandroid/view/KeyEvent;)Z
    .locals 12
    const/16 v0, 0x13
    if-lt p1, v0, :no
    const/16 v0, 0x17
    if-le p1, v0, :supported
    const/16 v0, 0x42
    if-eq p1, v0, :supported
    const/16 v0, 0xa0
    if-ne p1, v0, :no
    :supported
    iget-object v0, p0, Lai/rplay/carcast/CarPlayActivity;->a:Landroid/view/SurfaceView;
    if-eqz v0, :no
    invoke-virtual {v0}, Landroid/view/View;->getWidth()I
    move-result v4
    if-lez v4, :no
    iget-object v7, p0, Lai/rplay/carcast/CarPlayActivity;->cnCursor:Landroid/widget/TextView;
    if-nez v7, :ready
    const/high16 v1, 0x3f000000
    iput v1, p0, Lai/rplay/carcast/CarPlayActivity;->cnX:F
    iput v1, p0, Lai/rplay/carcast/CarPlayActivity;->cnY:F
    new-instance v7, Landroid/widget/TextView;
    invoke-direct {v7, p0}, Landroid/widget/TextView;-><init>(Landroid/content/Context;)V
    const-string v1, "+"
    invoke-virtual {v7, v1}, Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V
    const/4 v1, -0x1
    invoke-virtual {v7, v1}, Landroid/widget/TextView;->setTextColor(I)V
    const/high16 v1, 0x41c00000
    invoke-virtual {v7, v1}, Landroid/widget/TextView;->setTextSize(F)V
    const/16 v1, 0x11
    invoke-virtual {v7, v1}, Landroid/widget/TextView;->setGravity(I)V
    const v1, -0x33da9c15
    invoke-virtual {v7, v1}, Landroid/view/View;->setBackgroundColor(I)V
    const/4 v1, 0x0
    invoke-virtual {v7, v1}, Landroid/view/View;->setFocusable(Z)V
    invoke-virtual {v7, v1}, Landroid/view/View;->setClickable(Z)V
    const v1, 0x1020002
    invoke-virtual {p0, v1}, Landroid/app/Activity;->findViewById(I)Landroid/view/View;
    move-result-object v8
    check-cast v8, Landroid/widget/FrameLayout;
    new-instance v9, Landroid/widget/FrameLayout$LayoutParams;
    const/16 v1, 0x30
    invoke-direct {v9, v1, v1}, Landroid/widget/FrameLayout$LayoutParams;-><init>(II)V
    const/16 v1, 0x33
    iput v1, v9, Landroid/widget/FrameLayout$LayoutParams;->gravity:I
    invoke-virtual {v8, v7, v9}, Landroid/view/ViewGroup;->addView(Landroid/view/View;Landroid/view/ViewGroup$LayoutParams;)V
    iput-object v7, p0, Lai/rplay/carcast/CarPlayActivity;->cnCursor:Landroid/widget/TextView;
    const-string v1, "方向键移动光标 · 确定选择 · 返回 CarPlay 首页"
    const/4 v2, 0x1
    invoke-static {p0, v1, v2}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;
    move-result-object v1
    invoke-virtual {v1}, Landroid/widget/Toast;->show()V
    :ready
    iget v1, p0, Lai/rplay/carcast/CarPlayActivity;->cnX:F
    iget v2, p0, Lai/rplay/carcast/CarPlayActivity;->cnY:F
    const v3, 0x3d23d70a
    const/16 v9, 0x13
    if-ne p1, v9, :down
    sub-float/2addr v2, v3
    goto :position
    :down
    const/16 v9, 0x14
    if-ne p1, v9, :left
    add-float/2addr v2, v3
    goto :position
    :left
    const/16 v9, 0x15
    if-ne p1, v9, :right
    sub-float/2addr v1, v3
    goto :position
    :right
    const/16 v9, 0x16
    if-ne p1, v9, :select
    add-float/2addr v1, v3
    goto :position
    :select
    invoke-virtual {p2}, Landroid/view/KeyEvent;->getRepeatCount()I
    move-result v9
    if-nez v9, :position
    int-to-float v5, v4
    mul-float/2addr v5, v1
    invoke-virtual {v0}, Landroid/view/View;->getHeight()I
    move-result v6
    int-to-float v6, v6
    mul-float/2addr v6, v2
    invoke-static {v0, v5, v6}, Lai/rplay/carcast/CnRemote;->click(Landroid/view/View;FF)V
    :position
    const v3, 0x3c23d70a
    const v9, 0x3f7d70a4
    invoke-static {v1, v9}, Ljava/lang/Math;->min(FF)F
    move-result v1
    invoke-static {v1, v3}, Ljava/lang/Math;->max(FF)F
    move-result v1
    invoke-static {v2, v9}, Ljava/lang/Math;->min(FF)F
    move-result v2
    invoke-static {v2, v3}, Ljava/lang/Math;->max(FF)F
    move-result v2
    iput v1, p0, Lai/rplay/carcast/CarPlayActivity;->cnX:F
    iput v2, p0, Lai/rplay/carcast/CarPlayActivity;->cnY:F
    const/4 v9, 0x2
    new-array v6, v9, [I
    invoke-virtual {v0, v6}, Landroid/view/View;->getLocationOnScreen([I)V
    int-to-float v4, v4
    mul-float/2addr v1, v4
    invoke-virtual {v0}, Landroid/view/View;->getHeight()I
    move-result v5
    int-to-float v5, v5
    mul-float/2addr v2, v5
    const/4 v9, 0x0
    aget v4, v6, v9
    int-to-float v4, v4
    add-float/2addr v1, v4
    const/4 v9, 0x1
    aget v5, v6, v9
    int-to-float v5, v5
    add-float/2addr v2, v5
    invoke-virtual {v7}, Landroid/view/View;->getParent()Landroid/view/ViewParent;
    move-result-object v8
    check-cast v8, Landroid/view/View;
    invoke-virtual {v8, v6}, Landroid/view/View;->getLocationOnScreen([I)V
    const/4 v9, 0x0
    aget v4, v6, v9
    int-to-float v4, v4
    sub-float/2addr v1, v4
    const/4 v9, 0x1
    aget v5, v6, v9
    int-to-float v5, v5
    sub-float/2addr v2, v5
    const/high16 v3, 0x41c00000
    sub-float/2addr v1, v3
    sub-float/2addr v2, v3
    invoke-virtual {v7, v1}, Landroid/view/View;->setTranslationX(F)V
    invoke-virtual {v7, v2}, Landroid/view/View;->setTranslationY(F)V
    invoke-virtual {v7}, Landroid/view/View;->bringToFront()V
    const/4 v0, 0x1
    return v0
    :no
    const/4 v0, 0x0
    return v0
.end method

.method private static click(Landroid/view/View;FF)V
    .locals 10
    invoke-static {}, Landroid/os/SystemClock;->uptimeMillis()J
    move-result-wide v0
    move-wide v2, v0
    const/4 v4, 0x0
    move v5, p1
    move v6, p2
    const/4 v7, 0x0
    invoke-static/range {v0 .. v7}, Landroid/view/MotionEvent;->obtain(JJIFFI)Landroid/view/MotionEvent;
    move-result-object v8
    invoke-virtual {p0, v8}, Landroid/view/View;->dispatchTouchEvent(Landroid/view/MotionEvent;)Z
    const/4 v9, 0x1
    invoke-virtual {v8, v9}, Landroid/view/MotionEvent;->setAction(I)V
    invoke-virtual {p0, v8}, Landroid/view/View;->dispatchTouchEvent(Landroid/view/MotionEvent;)Z
    invoke-virtual {v8}, Landroid/view/MotionEvent;->recycle()V
    return-void
.end method
