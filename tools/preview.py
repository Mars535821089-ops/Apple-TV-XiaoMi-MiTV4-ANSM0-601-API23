#!/usr/bin/env python3
"""Ordinary 800x450 live window, no audio capture, screenshots or recording."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess

from device import TV

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--serial', default=os.environ.get('TV_SERIAL'))
parser.add_argument('--adb', default=os.environ.get('ADB_BINARY', 'adb'))
parser.add_argument('--scrcpy', default=os.environ.get('SCRCPY_BINARY', 'scrcpy'))
parser.add_argument('--server-port', type=int, default=5040)
args = parser.parse_args()
if not args.serial:
    parser.error('--serial or TV_SERIAL is required')
tv = TV(args.serial, args.adb, args.server_port)
tv.identity()
environment = os.environ.copy()
environment['ADB'] = shutil.which(args.adb) or str(Path(args.adb).resolve())
environment['ADB_SERVER_SOCKET'] = f'tcp:localhost:{args.server_port}'
command = [args.scrcpy, '--serial', args.serial, '--no-audio', '--no-clipboard-autosync',
           '--video-codec=h264', '--video-encoder=OMX.amlogic.video.encoder.avc',
           '--max-size=800', '--max-fps=8', '--video-bit-rate=768K',
           '--window-width=800', '--window-height=450', '--window-title=Mars电视配置']
raise SystemExit(subprocess.call(command, env=environment))
