.class public final Lai/rplay/carcast/CnKeys;
.super Ljava/lang/Object;

# Standard CarPlay Knob & Buttons report. No screen coordinates or cursor.
.method public static handle(Lai/rplay/carcast/CarPlayActivity;ILandroid/view/KeyEvent;)Z
    .locals 5
    # Xiaomi BLE voice key is F12. F1 is a keyboard diagnostic alias.
    const/16 v0, 0x8e
    if-eq p1, v0, :voice
    const/16 v0, 0x83
    if-eq p1, v0, :voice
    const/16 v0, 0xe7
    if-eq p1, v0, :voice
    const/16 v0, 0xdb
    if-eq p1, v0, :voice
    const/16 v0, 0x54
    if-ne p1, v0, :directions
    :voice
    invoke-virtual {p2}, Landroid/view/KeyEvent;->getAction()I
    move-result v0
    if-nez v0, :consumed
    invoke-virtual {p2}, Landroid/view/KeyEvent;->getRepeatCount()I
    move-result v0
    if-nez v0, :consumed
    invoke-static {}, Lai/rplay/carcast/CnSiri;->start()V
    goto :consumed
    :directions
    const/16 v0, 0x13
    if-lt p1, v0, :other
    const/16 v0, 0x17
    if-le p1, v0, :supported
    :other
    const/4 v0, 0x4
    if-eq p1, v0, :supported
    const/16 v0, 0x42
    if-eq p1, v0, :supported
    const/16 v0, 0xa0
    if-eq p1, v0, :supported
    const/16 v0, 0x52
    if-ne p1, v0, :no
    :supported
    const/4 v1, 0x0
    const/4 v2, 0x0
    const/4 v3, 0x0
    invoke-virtual {p2}, Landroid/view/KeyEvent;->getAction()I
    move-result v4
    const/4 v0, 0x1
    if-eq v4, v0, :send
    if-nez v4, :no
    invoke-virtual {p2}, Landroid/view/KeyEvent;->getRepeatCount()I
    move-result v4
    if-nez v4, :consumed
    :spatial
    const/16 v0, 0x13
    if-ne p1, v0, :down
    # Absolute joystick Y jumps within groups; rotary is one focus item.
    const/4 v3, -0x1
    goto :send
    :down
    const/16 v0, 0x14
    if-ne p1, v0, :left
    const/4 v3, 0x1
    goto :send
    :left
    const/16 v0, 0x15
    if-ne p1, v0, :right
    # Horizontal joystick jumps between focus groups. Rotary traverses each
    # element, including items within tab bars and segmented controls.
    const/4 v3, -0x1
    goto :send
    :right
    const/16 v0, 0x16
    if-ne p1, v0, :back
    const/4 v3, 0x1
    goto :send
    :back
    const/4 v0, 0x4
    if-ne p1, v0, :home
    const/4 v1, 0x4
    goto :send
    :home
    const/16 v0, 0x52
    if-ne p1, v0, :select
    const/4 v1, 0x2
    goto :send
    :select
    const/4 v1, 0x1
    :send
    invoke-virtual {p2}, Landroid/view/KeyEvent;->getAction()I
    move-result v4
    invoke-static {p1, v4}, Lai/rplay/carcast/CnHold;->update(II)V
    const/16 v0, 0x100
    const/16 p0, 0x13
    if-lt p1, p0, :normal
    const/16 p0, 0x16
    if-gt p1, p0, :normal
    if-nez v4, :consumed
    # Discrete direction pulse: do not let physical hold become joystick
    # auto-repeat as well as our deliberate rotary traversal.
    invoke-static {v0, v1, v2, v3}, Lai/rplay/carcast/CnInput;->enqueue(IIII)V
    const/4 v1, 0x0
    invoke-static {v0, v1, v1, v1}, Lai/rplay/carcast/CnInput;->enqueue(IIII)V
    goto :consumed
    :normal
    invoke-static {v0, v1, v2, v3}, Lai/rplay/carcast/CnInput;->enqueue(IIII)V
    :consumed
    const/4 v0, 0x1
    return v0
    :no
    const/4 v0, 0x0
    return v0
.end method
