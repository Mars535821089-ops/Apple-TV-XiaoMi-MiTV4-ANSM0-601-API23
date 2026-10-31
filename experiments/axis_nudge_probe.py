"""Diagnostic aliases for the existing knob axes, with no HID layout changes.

F2..F5 send unit up/down/left/right, F6..F9 full-scale. Physical arrows retain
baseline behavior until current-frame observations establish a usable mapping.
"""


def smali_probe(source):
    anchor = '    # Xiaomi BLE voice key is F12. F1 is a keyboard diagnostic alias.'
    if source.count(anchor) != 1:
        raise ValueError('Unexpected key handler baseline')
    lines = ['    # F10 reconstructs only the receiver activity for recovery diagnosis.',
             '    const/16 v0, 0x8c', '    if-ne p1, v0, :refresh_original',
             '    invoke-virtual {p2}, Landroid/view/KeyEvent;->getAction()I',
             '    move-result v0', '    if-nez v0, :refresh_consumed',
             '    invoke-virtual {p2}, Landroid/view/KeyEvent;->getRepeatCount()I',
             '    move-result v0', '    if-nez v0, :refresh_consumed',
             '    invoke-virtual {p0}, Landroid/app/Activity;->recreate()V',
             '    :refresh_consumed', '    const/4 v0, 0x1', '    return v0',
             '    :refresh_original',
             '    # Existing-axis diagnostic only; no pointer or touchscreen events.']
    for code, axis in zip(range(132, 140), (0xff00, 0x0100, 0xff, 1, 0x8100, 0x7f00, 0x81, 0x7f)):
        lines += [f'    const/16 v0, 0x{code:x}', f'    if-ne p1, v0, :axis_next_{code}',
                  f'    const v2, 0x{axis:x}', '    goto :axis_pulse', f'    :axis_next_{code}']
    lines += ['    goto :axis_original', '    :axis_pulse',
              '    invoke-virtual {p2}, Landroid/view/KeyEvent;->getAction()I',
              '    move-result v0', '    if-nez v0, :axis_consumed',
              '    invoke-virtual {p2}, Landroid/view/KeyEvent;->getRepeatCount()I',
              '    move-result v0', '    if-nez v0, :axis_consumed',
              '    const/16 v0, 0x100', '    const/4 v1, 0x0',
              '    invoke-static {v0, v1, v2, v1}, Lai/rplay/carcast/CnInput;->enqueue(IIII)V',
              '    invoke-static {v0, v1, v1, v1}, Lai/rplay/carcast/CnInput;->enqueue(IIII)V',
              '    :axis_consumed', '    const/4 v0, 0x1', '    return v0', '    :axis_original']
    return source.replace(anchor, '\n'.join(lines) + '\n' + anchor)
