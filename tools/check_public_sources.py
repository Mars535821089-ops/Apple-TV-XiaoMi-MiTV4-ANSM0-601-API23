#!/usr/bin/env python3
"""Check staged Git blobs; never crawl or print private local/runtime contents."""
from pathlib import Path
import re
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
EXTENSIONS = {'.c', '.h', '.java', '.py', '.smali', '.patch', '.md', '.txt', '.json', '.yml', '.yaml', '.toml'}
SPECIAL = {'.gitignore', '.gitattributes', '.python-version', '.gitmodules'}
SECRETS = [re.compile(pattern, re.MULTILINE) for pattern in [
    r'^-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
    r'\bsk-[A-Za-z0-9_-]{24,}\b',
    r'\bgh[pousr]_[A-Za-z0-9]{30,}\b',
    r'\bgithub_pat_[A-Za-z0-9_]{40,}\b',
    r'^\s*(?:wifi_password|passphrase|api_key|access_token|refresh_token)\s*[:=]\s*[\x22\x27][^\x22\x27]{8,}[\x22\x27]',
]]


def inspect_entry(name: str, data: bytes, mode: str = '100644') -> list[str]:
    if mode == '160000' and name == 'upstream/aerial-tv' and re.fullmatch(b'[0-9a-f]{40}', data):
        return []
    path = Path(name)
    issues = []
    if path.is_absolute() or '..' in path.parts or any(p in {'local', 'build', '.venv', '__pycache__'} for p in path.parts):
        issues.append('private or generated path')
    if mode not in {'100644', '100755'}:
        issues.append('symlink or unsupported Git entry')
    if path.suffix not in EXTENSIONS and path.name not in SPECIAL:
        issues.append('not an allowed source format')
    if len(data) > 512 * 1024 or b'\0' in data:
        issues.append('binary or oversized payload')
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError:
        issues.append('not UTF-8 source')
    else:
        if any(pattern.search(text) for pattern in SECRETS):
            issues.append('possible credential; value deliberately not printed')
    return issues


def main() -> int:
    raw = subprocess.check_output(['git', 'ls-files', '-s', '-z'], cwd=ROOT)
    entries = [item for item in raw.split(b'\0') if item]
    if not entries:
        print('No staged source files')
        return 1
    failures = []
    lock = json.loads(subprocess.check_output(['git', 'show', ':dependencies.lock.json'], cwd=ROOT))
    for entry in entries:
        metadata, filename = entry.split(b'\t', 1)
        mode = metadata.split()[0].decode()
        name = filename.decode('utf-8')
        if mode == '160000':
            data = metadata.split()[1]
        else:
            data = subprocess.check_output(['git', 'show', ':' + name], cwd=ROOT)
        issues = inspect_entry(name, data, mode)
        if mode == '160000':
            if name != 'upstream/aerial-tv' or data.decode() != lock['aerial']['source_commit']:
                issues.append('unapproved or unpinned submodule')
            modules = subprocess.check_output(['git', 'show', ':.gitmodules'], cwd=ROOT).decode()
            urls = re.findall(r'^\s*url\s*=\s*(\S+)\s*$', modules, re.MULTILINE)
            paths = re.findall(r'^\s*path\s*=\s*(\S+)\s*$', modules, re.MULTILINE)
            if urls != [lock['aerial']['source_repo']] or paths != ['upstream/aerial-tv']:
                issues.append('unexpected submodule origin or path')
        if issues:
            failures.append((name, issues))
    for name, issues in failures:
        print(name + ': ' + '; '.join(issues))
    print(f'Checked {len(entries)} staged source files; violations={len(failures)}')
    return bool(failures)


if __name__ == '__main__':
    raise SystemExit(main())
