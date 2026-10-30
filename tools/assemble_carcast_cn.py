"""Retain all original APK entries; replace only the patched DEX bytecode.

Repacking from the original ZIP avoids case-insensitive filesystem collisions
between the vendor's obfuscated resource filenames on macOS.
"""
from pathlib import Path
from zipfile import ZipFile

root = Path(__file__).parent
original = root / 'CarCast-0.3.25.apk'
compiled = root / 'CarCast-0.3.25-cn-unsigned.apk'
output = root / 'CarCast-0.3.25-cn-preserved-unsigned.apk'
with ZipFile(original) as source, ZipFile(compiled) as patched, ZipFile(output, 'w') as target:
    dex = {n for n in patched.namelist() if n.startswith('classes') and n.endswith('.dex')}
    for entry in source.infolist():
        if entry.filename.startswith('META-INF/'):
            continue
        data = patched.read(entry.filename) if entry.filename in dex else source.read(entry.filename)
        target.writestr(entry, data)
with ZipFile(original) as source, ZipFile(output) as target:
    retained = [n for n in source.namelist() if not n.startswith('META-INF/') and n not in dex]
    assert all(source.read(n) == target.read(n) for n in retained)
    assert target.read('res/Dt.png') == source.read('res/Dt.png')
    print({'original_entries_preserved': len(retained), 'patched_dex': sorted(dex), 'output': output.name})
