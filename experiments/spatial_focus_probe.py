"""No-cursor diagnostic: one wheel step and transient focus geometry only."""
from pathlib import Path
import shutil

ROOT=Path(__file__).resolve().parents[1]


def smali_probe(source):
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
    if-ne p1, v0, :focus_probe_original
    :focus_probe_select
    invoke-virtual {p2}, Landroid/view/KeyEvent;->getAction()I
    move-result v0
    if-nez v0, :focus_probe_original
    invoke-static {}, Lai/rplay/carcast/CnFocusProbe;->busy()Z
    move-result v0
    if-eqz v0, :focus_probe_original
    goto :focus_probe_consumed
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
    source.write_text(text.replace(anchor,anchor+'\n    invoke-static {}, Lai/rplay/carcast/CnFocusProbe;->cancel()V'))
