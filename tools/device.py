#!/usr/bin/env python3
"""Bounded ADB operations for the explicitly selected, already authorized TV."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
from zipfile import ZipFile

KEYS = {'up': 19, 'down': 20, 'left': 21, 'right': 22, 'ok': 23,
        'back': 4, 'menu': 82, 'home': 3, 'volume_up': 24,
        'volume_down': 25, 'mute': 164, 'wake': 224, 'sleep': 223, 'voice': 142}
COMPONENTS = {'carcast': 'ai.rplay.carcast/.SettingsActivity',
              'aerial': 'app.orchard.tv/.MainActivity'}


class TV:
    def __init__(self, serial: str, adb: str = 'adb', server_port: int = 5040):
        if not serial or len(serial) > 128 or any(c.isspace() for c in serial):
            raise ValueError('Provide one explicit ADB serial, without whitespace')
        self.prefix = [adb, '-P', str(server_port), '-s', serial]

    def run(self, *args: str, timeout: int = 15) -> str:
        result = subprocess.run(self.prefix + list(args), capture_output=True,
                                text=True, errors='replace', timeout=timeout, check=True)
        return result.stdout.strip()

    def identity(self) -> dict:
        if self.run('get-state') != 'device':
            raise RuntimeError('TV is not connected and authorized')
        model = self.run('shell', 'getprop', 'ro.product.model')
        sdk = self.run('shell', 'getprop', 'ro.build.version.sdk')
        abi = self.run('shell', 'getprop', 'ro.product.cpu.abi')
        normalized = re.sub('[^A-Z0-9]', '', model.upper())
        if normalized != 'MITV4ANSM0' or sdk != '23' or abi != 'armeabi-v7a':
            raise RuntimeError('Selected device is not the validated MiTV4-ANSM0 / API23 / ARM32 target')
        return {'model': model, 'sdk': sdk, 'abi': abi}


def validate_install(apk: Path, receipt_path: Path) -> dict:
    receipt = json.loads(receipt_path.read_text())
    expected = receipt.get('sha256')
    if not isinstance(expected, str) or not re.fullmatch('[0-9a-f]{64}', expected):
        raise ValueError('Build receipt has no valid SHA256')
    actual = hashlib.sha256(apk.read_bytes()).hexdigest()
    if receipt.get('apk') != apk.name or actual != expected:
        raise ValueError('APK does not match the build receipt')
    with ZipFile(apk) as archive:
        if 'lib/armeabi-v7a/libcarcast.so' not in archive.namelist() or archive.testzip() is not None:
            raise ValueError('APK is not a valid ARM32 CarCast build')
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--serial', default=os.environ.get('TV_SERIAL'))
    parser.add_argument('--adb', default=os.environ.get('ADB_BINARY', 'adb'))
    parser.add_argument('--server-port', type=int, default=5040)
    sub = parser.add_subparsers(dest='action', required=True)
    sub.add_parser('status')
    remote = sub.add_parser('remote')
    remote.add_argument('keys', choices=KEYS, nargs='+')
    launch = sub.add_parser('launch')
    launch.add_argument('app', choices=COMPONENTS)
    install = sub.add_parser('install')
    install.add_argument('--apk', required=True, type=Path)
    install.add_argument('--receipt', required=True, type=Path)
    args = parser.parse_args()
    if not args.serial:
        parser.error('--serial or TV_SERIAL is required; no device address is stored in source')
    tv = TV(args.serial, args.adb, args.server_port)
    identity = tv.identity()
    if args.action == 'status':
        print(json.dumps(identity | {'adb_enabled': tv.run('shell', 'settings', 'get', 'global', 'adb_enabled')},
                         ensure_ascii=False))
    elif args.action == 'remote':
        for key in args.keys:
            tv.run('shell', 'input', 'keyevent', str(KEYS[key]))
        print(json.dumps({'keys_sent': args.keys, 'visible_effect_verified': False,
                          'screenshot_or_recording_created': False}))
    elif args.action == 'launch':
        tv.run('shell', 'am', 'start', '-n', COMPONENTS[args.app], timeout=30)
        print(json.dumps({'launch_requested': args.app, 'visible_effect_verified': False}))
    elif args.action == 'install':
        receipt = validate_install(args.apk, args.receipt)
        tv.run('install', '-r', str(args.apk.resolve()), timeout=180)
        remote = tv.run('shell', 'pm', 'path', 'ai.rplay.carcast')
        if not remote.startswith('package:') or '\n' in remote:
            raise RuntimeError('Cannot identify the installed CarCast APK')
        path = remote.removeprefix('package:')
        installed = tv.run('shell', 'md5sum', path).split()[0]
        if installed != hashlib.md5(args.apk.read_bytes()).hexdigest():
            raise RuntimeError('Installed APK byte identity check failed')
        print(json.dumps({'installed_sha256': receipt['sha256'], 'data_preserved_by_install_r': True,
                          'functional_acceptance': 'not implied by installation'}))


if __name__ == '__main__':
    main()
