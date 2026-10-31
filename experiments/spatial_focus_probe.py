"""No-cursor diagnostic: one wheel step and transient focus geometry only."""
from pathlib import Path
import shutil

ROOT=Path(__file__).resolve().parents[1]


def smali_probe(source, spatial=False):
    anchor='    # Xiaomi BLE voice key is F12. F1 is a keyboard diagnostic alias.'
    if source.count(anchor)!=1: raise ValueError('Unexpected key handler')
    prefix='''    const/16 v0, 0x84
    if-eq p1, v0, :focus_probe_next
    const/16 v0, 0x85
    if-eq p1, v0, :focus_probe_previous
    const/16 v0, 0x8c
    if-eq p1, v0, :focus_probe_refresh
    # A new Select press cannot activate an intermediate probe target.
    const/16 v0, 0x17
    if-eq p1, v0, :focus_probe_select
    const/16 v0, 0x42
    if-eq p1, v0, :focus_probe_select
    const/16 v0, 0xa0
    if-ne p1, v0, :focus_probe_other
    :focus_probe_select
    invoke-virtual {p2}, Landroid/view/KeyEvent;->getAction()I
    move-result v0
    if-nez v0, :focus_probe_original
    invoke-static {}, Lai/rplay/carcast/CnFocusProbe;->busy()Z
    move-result v0
    if-eqz v0, :focus_probe_original
    goto :focus_probe_consumed
    :focus_probe_other
    invoke-virtual {p2}, Landroid/view/KeyEvent;->getAction()I
    move-result v0
    if-nez v0, :focus_probe_original
    invoke-static {}, Lai/rplay/carcast/CnFocusProbe;->cancel()V
    goto :focus_probe_original
    :focus_probe_next
    const/4 v1, 0x1
    goto :focus_probe_request
    :focus_probe_previous
    const/4 v1, -0x1
    :focus_probe_request
    invoke-virtual {p2}, Landroid/view/KeyEvent;->getAction()I
    move-result v0
    if-nez v0, :focus_probe_consumed
    invoke-virtual {p2}, Landroid/view/KeyEvent;->getRepeatCount()I
    move-result v0
    if-nez v0, :focus_probe_consumed
    invoke-static {v1}, Lai/rplay/carcast/CnFocusProbe;->request(I)V
    goto :focus_probe_consumed
    :focus_probe_refresh
    invoke-virtual {p2}, Landroid/view/KeyEvent;->getAction()I
    move-result v0
    if-nez v0, :focus_probe_consumed
    invoke-virtual {p2}, Landroid/view/KeyEvent;->getRepeatCount()I
    move-result v0
    if-nez v0, :focus_probe_consumed
    invoke-static {}, Lai/rplay/carcast/CnFocusProbe;->cancel()V
    invoke-virtual {p0}, Landroid/app/Activity;->recreate()V
    :focus_probe_consumed
    const/4 v0, 0x1
    return v0
    :focus_probe_original
'''
    prefix=prefix.replace('Lai/rplay/carcast/CnFocusProbe;->cancel()V',
                          'Lai/rplay/carcast/CnSpatialNavigator;->cancel()V')
    if spatial:
        stop='''    const/4 v0, 0x4
    if-eq p1, v0, :spatial_explicit_cancel
    const/16 v0, 0x52
    if-eq p1, v0, :spatial_explicit_cancel
    invoke-static {}, Lai/rplay/carcast/CnSpatialNavigator;->stop()V
    goto :focus_probe_original
    :spatial_explicit_cancel
'''
        marker='''    if-nez v0, :focus_probe_original
    invoke-static {}, Lai/rplay/carcast/CnSpatialNavigator;->cancel()V
    goto :focus_probe_original'''
        replacement='''    if-nez v0, :focus_probe_original
'''+stop+'''    invoke-static {}, Lai/rplay/carcast/CnSpatialNavigator;->cancel()V
    goto :focus_probe_original'''
        if prefix.count(marker)!=1:raise ValueError('Unexpected unrelated-key cancellation')
        prefix=prefix.replace(marker,replacement)
        gate='''    invoke-static {}, Lai/rplay/carcast/CnSpatialNavigator;->busy()Z
    move-result v0
    if-nez v0, :focus_probe_consumed
    invoke-static {}, Lai/rplay/carcast/CnSpatialNavigator;->uncertain()Z
    move-result v0
    if-nez v0, :focus_probe_consumed
'''
        prefix=prefix.replace('    invoke-static {}, Lai/rplay/carcast/CnFocusProbe;->busy()Z',
                              gate+'    invoke-static {}, Lai/rplay/carcast/CnFocusProbe;->busy()Z')
        directions='''    const/16 v0, 0x13
    if-lt p1, v0, :spatial_diagnostic
    const/16 v0, 0x16
    if-gt p1, v0, :spatial_diagnostic
    invoke-virtual {p2}, Landroid/view/KeyEvent;->getAction()I
    move-result v0
    if-nez v0, :focus_probe_consumed
    invoke-virtual {p2}, Landroid/view/KeyEvent;->getRepeatCount()I
    move-result v0
    if-nez v0, :focus_probe_consumed
    invoke-static {p1}, Lai/rplay/carcast/CnSpatialNavigator;->request(I)V
    goto :focus_probe_consumed
    :spatial_diagnostic
'''
        prefix=directions+prefix
    return source.replace(anchor,prefix+anchor)


def patch_helpers(decoded, java, apktool, offline):
    from compile_focus import compile_focus
    generated=compile_focus(java,apktool,decoded,offline)
    for source in generated.rglob('*.smali'):
        target=decoded/'smali'/source.relative_to(generated)
        target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
    host=decoded/'smali/ai/rplay/carcast/CnProbeHost.smali'
    shutil.copy2(ROOT/'experiments/spatial-focus/CnProbeHost.smali',host)
    render=decoded/'smali/ai/rplay/carcast/CnRender.smali'
    render.write_text(render.read_text()+(ROOT/'experiments/spatial-focus/render-capture.smali').read_text())
    source=decoded/'smali/ai/rplay/carcast/CnInput.smali'
    text=source.read_text();anchor='.method public static cancel()V\n    .locals 4'
    if text.count(anchor)!=1: raise ValueError('Unexpected input cancellation baseline')
    text=text.replace(anchor,anchor+'\n    invoke-static {}, Lai/rplay/carcast/CnSpatialNavigator;->stop()V')
    text=text.replace('.field private wheel:I','.field private wheel:I\n.field private probeToken:I\n.field private static held:I')
    marker='    invoke-direct {v3, p1, p2, p3}, Lai/rplay/carcast/CnInput;-><init>(III)V'
    if text.count(marker)!=1: raise ValueError('Unexpected input report constructor')
    text=text.replace(marker,marker+'\n    iput p0, v3, Lai/rplay/carcast/CnInput;->probeToken:I')
    text=text.replace('.method public run()V\n    .locals 6', '''.method public run()V
    .locals 6
    iget v0, p0, Lai/rplay/carcast/CnInput;->probeToken:I
    const/16 v1, 0x100
    if-eq v0, v1, :probe_regular
    invoke-static {v0}, Lai/rplay/carcast/CnFocusProbe;->validToken(I)Z
    move-result v0
    if-eqz v0, :done
    :probe_regular''')
    marker='    invoke-static {v0, v1, v2, v3}, Lai/rplay/carcast/NativeBridge;->iapPointer(IIII)V'
    text=text.replace(marker,marker+'\n    or-int v4, v1, v2\n    sput v4, Lai/rplay/carcast/CnInput;->held:I')
    text+='''
.method public static canProbe()Z
 .locals 5
 sget-object v0,Lai/rplay/carcast/CnInput;->handler:Landroid/os/Handler;
 if-eqz v0,:state
 const/4 v1,0x0
 invoke-virtual {v0,v1},Landroid/os/Handler;->hasMessages(I)Z
 move-result v0
 if-nez v0,:busy
 :state
 sget v0,Lai/rplay/carcast/CnInput;->held:I
 if-nez v0,:busy
 sget-wide v0,Lai/rplay/carcast/CnInput;->next:J
 invoke-static {},Landroid/os/SystemClock;->uptimeMillis()J
 move-result-wide v2
 cmp-long v4,v0,v2
 if-gtz v4,:busy
 const/4 v0,0x1
 return v0
 :busy
 const/4 v0,0x0
 return v0
.end method
'''
    source.write_text(text)
    bridge=decoded/'smali/ai/rplay/carcast/NativeBridge.smali'
    text=bridge.read_text()
    marker='    invoke-static {}, Lai/rplay/carcast/CnReconnect;->cancel()V'
    if text.count(marker)!=1:raise ValueError('Unexpected primary-screen connection boundary')
    text=text.replace(marker,marker+'\n    invoke-static {}, Lai/rplay/carcast/CnSpatialNavigator;->cancel()V')
    bridge.write_text(text)
