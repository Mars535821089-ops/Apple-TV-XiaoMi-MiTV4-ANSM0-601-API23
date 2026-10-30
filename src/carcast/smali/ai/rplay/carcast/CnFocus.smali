.class public final Lai/rplay/carcast/CnFocus;
.super Ljava/lang/Object;
.implements Landroid/view/View$OnFocusChangeListener;

.method public constructor <init>()V
    .locals 0
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V
    return-void
.end method

.method public onFocusChange(Landroid/view/View;Z)V
    .locals 3
    if-eqz p2, :normal
    const v0, 0x3f851eb8
    goto :scale
    :normal
    const/high16 v0, 0x3f800000
    :scale
    invoke-virtual {p1, v0}, Landroid/view/View;->setScaleX(F)V
    invoke-virtual {p1, v0}, Landroid/view/View;->setScaleY(F)V
    invoke-virtual {p1}, Landroid/view/View;->getBackground()Landroid/graphics/drawable/Drawable;
    move-result-object v0
    instance-of v1, v0, Landroid/graphics/drawable/GradientDrawable;
    if-eqz v1, :done
    check-cast v0, Landroid/graphics/drawable/GradientDrawable;
    const/4 v1, 0x3
    if-eqz p2, :dim
    const v2, -0x9e5b01
    goto :stroke
    :dim
    const/4 v1, 0x1
    const v2, -0xcfbf9e
    :stroke
    invoke-virtual {v0, v1, v2}, Landroid/graphics/drawable/GradientDrawable;->setStroke(II)V
    :done
    return-void
.end method
