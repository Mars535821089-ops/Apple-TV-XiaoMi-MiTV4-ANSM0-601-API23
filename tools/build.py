#!/usr/bin/env python3
"""Build the audited local overlay; upstream code stays in ignored build/."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            hasher.update(chunk)
    return hasher.hexdigest()


def verified(path: Path, expected: str) -> Path:
    if not path.is_file() or digest(path) != expected:
        raise ValueError(f'Artifact SHA256 mismatch: {path.name}')
    return path


def artifact(spec: dict, cache: Path, supplied: Path | None, offline: bool) -> Path:
    if supplied is not None:
        return verified(supplied.resolve(), spec['sha256'])
    target = cache / spec['filename']
    if target.exists():
        return verified(target, spec['sha256'])
    if offline:
        raise FileNotFoundError(f"Missing cached dependency: {spec['filename']}")
    cache.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=cache, prefix='.fetch-', delete=False) as out:
            temporary = Path(out.name)
            request = urllib.request.Request(spec['url'], headers={'User-Agent': 'MiTV-CarPlay-source-build'})
            with urllib.request.urlopen(request, timeout=60) as response:
                shutil.copyfileobj(response, out)
        verified(temporary, spec['sha256'])
        temporary.replace(target)
        return target
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def run(*args: object, cwd: Path = ROOT, input_text: str | None = None) -> None:
    subprocess.run([str(arg) for arg in args], cwd=cwd, input=input_text,
                   text=True, check=True)


def verify_resources(original: Path, output: Path) -> int:
    with ZipFile(original) as source, ZipFile(output) as built:
        resources = [name for name in source.namelist()
                     if name.startswith(('res/', 'assets/')) or name == 'resources.arsc']
        for name in resources:
            if source.read(name) != built.read(name):
                raise ValueError(f'Changed or missing upstream resource: {name}')
        if built.testzip() is not None:
            raise ValueError('APK ZIP integrity failure')
        return len(resources)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--java', default='java')
    parser.add_argument('--upstream-apk', type=Path)
    parser.add_argument('--apktool', type=Path)
    parser.add_argument('--signer', type=Path)
    parser.add_argument('--offline', action='store_true')
    parser.add_argument('--unsigned', action='store_true')
    parser.add_argument('--label', default='audit11-rebuild')
    args = parser.parse_args()
    if not args.label or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_' for c in args.label):
        parser.error('--label accepts only letters, digits, hyphens and underscores')
    lock = json.loads((ROOT / 'dependencies.lock.json').read_text())
    build = ROOT / 'build'
    cache, work, output = build / 'deps', build / 'work', build / 'outputs'
    for folder in (work, output):
        folder.mkdir(parents=True, exist_ok=True)
    upstream = artifact(lock['carcast'], cache, args.upstream_apk, args.offline)
    apktool = artifact(lock['apktool'], cache, args.apktool, args.offline)
    signer = None if args.unsigned else artifact(lock['signer'], cache, args.signer, args.offline)
    baseline = work / 'CarCast-0.3.25.apk'
    if baseline.resolve() != upstream.resolve():
        shutil.copy2(upstream, baseline)
    decoded = work / 'carcast-cn-src'
    run(args.java, '-jar', apktool, 'd', '-f', '-r', '-o', decoded, baseline)
    patch = (ROOT / 'src/carcast/vendor-hooks.patch').read_text()
    # Reject absolute or escaping paths before invoking the platform patch utility.
    for line in patch.splitlines():
        if line.startswith(('--- ', '+++ ')):
            value = line[4:].split('\t', 1)[0]
            path = Path(value)
            if path.is_absolute() or '..' in path.parts or path.parts[0] not in ('a', 'b'):
                raise ValueError('Invalid vendor patch path')
    run('patch', '-p1', '--batch', '--fuzz=0', '-d', decoded, input_text=patch)
    for source in (ROOT / 'src/carcast').rglob('*.smali'):
        target = decoded / source.relative_to(ROOT / 'src/carcast')
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    raw = work / 'CarCast-0.3.25-cn-unsigned.apk'
    run(args.java, '-jar', apktool, 'b', decoded, '-o', raw)
    stages = ['assemble_carcast_cn.py', 'fix_carcast_arm_alignment.py',
              'add_carcast_knob_bridge.py', 'add_carcast_voice_hid.py']
    for name in stages:
        shutil.copy2(ROOT / 'tools' / name, work / name)
    for name in stages[:3]:
        run(sys.executable, work / name)
    # Keep original wireless audio capabilities. PCM restriction is an experiment,
    # deliberately excluded from the current build.
    candidate = output / f'CarCast-0.3.25-{args.label}-unsigned.apk'
    run(sys.executable, work / stages[-1], '--source', work / 'CarCast-0.3.25-cn-knob-unsigned.apk',
        '--output', candidate)
    resources = verify_resources(upstream, candidate)
    final = candidate
    if signer is not None:
        run(args.java, '-jar', signer, '-a', candidate, '-o', output, '--allowResign')
        final = output / f'CarCast-0.3.25-{args.label}-aligned-debugSigned.apk'
        if not final.is_file():
            raise FileNotFoundError('Signer did not produce the expected APK')
        verify_resources(upstream, final)
    receipt = {'label': args.label, 'apk': final.name, 'sha256': digest(final),
               'upstream_sha256': digest(upstream), 'resources_preserved': resources,
               'original_audio_capabilities': True, 'device_acceptance': 'not implied by build'}
    (output / f'{args.label}.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
