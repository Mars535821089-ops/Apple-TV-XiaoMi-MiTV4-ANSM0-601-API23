#!/usr/bin/env python3
"""Read bounded, redacted stability and audio events; never record screen/audio."""
import argparse
import codecs
import os
from pathlib import Path
import re
import selectors
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
KEEP = re.compile(r'CnInput|CnRender|CnFocusProbe|CnVideoReturn|CnReconnect|CnSiri|CnFrameHealth|CarPlay session|'
                  r'screen (?:start|stop) slot|slot [0-9]+: surface |no surface yet|waiting for surface|audio (?:setup|torn)|AudioStream|AudioTrack|'
                  r'decoder (?:started|released|configured|up|input stalled|fed)|configure/start failed|SetAVCC|output format|first frame|OMX\.[A-Za-z0-9._-]+|'
                  r'Main(?:High)?Audio|audioFormat|audioType|audioLatencyMs|latencyMs|'
                  r'latencyMin|latencyMax|preferredLatency|outputLatencyMicros|inputLatencyMicros|'
                  r'Setup session failed|Fatal signal|FATAL EXCEPTION|underrun|underflow|'
                  r'late packets|lost packets|JitterBuffer.*Statistics', re.I)
EXCLUDE = re.compile(r'password|passphrase|psk|token|authorization|credential|secret|private.?key|cookie', re.I)


def redact(line):
    if not KEEP.search(line) or EXCLUDE.search(line):
        return None
    line = re.sub(r'(?:[0-9a-f]{2}:){5}[0-9a-f]{2}', '<device>', line, flags=re.I)
    line = re.sub(r'(?:[0-9a-f]{0,4}:){3,}[0-9a-f:%wlan0.]+', '<peer>', line, flags=re.I)
    line = re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', '<address>', line)
    return line.rstrip()[:800]


def main():
    from device import TV
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--serial', default=os.environ.get('TV_SERIAL'))
    parser.add_argument('--adb', default=os.environ.get('ADB_BINARY', 'adb'))
    parser.add_argument('--server-port', type=int, default=5040)
    parser.add_argument('--seconds', type=int, default=300)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if not args.serial or not 1 <= args.seconds <= 7200:
        parser.error('An explicit target and --seconds in 1..7200 are required')
    if args.output:
        output = args.output.resolve()
        if not output.is_relative_to(ROOT / 'local'):
            parser.error('--output must stay inside ignored local/')
        output.parent.mkdir(parents=True, exist_ok=True)
    tv = TV(args.serial, args.adb, args.server_port)
    tv.identity()
    tags = ['CarCast:I', 'CarCast-sdk:I', 'CarCast-screen:D', 'ACodec:I', 'OMXClient:I', 'OMXNodeInstance:I', 'MediaCodec:I', 'CnInput:D', 'CnRender:I', 'CnReconnect:I',
            'CnSiri:I', 'CnFocusProbe:I', 'CnVideoReturn:I', 'CnFrameHealth:I', 'AudioTrack:W', 'AudioFlinger:W', 'libc:F', 'AndroidRuntime:E']
    process = subprocess.Popen(tv.prefix + ['logcat', '-b', 'main', '-b', 'crash', '-v', 'threadtime',
                                           '-T', '1', '-s'] + tags, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ)
    decoder = codecs.getincrementaldecoder('utf-8')(errors='replace')
    pending = ''
    end = time.monotonic() + args.seconds
    file = args.output.open('a', buffering=1) if args.output else None
    try:
        while time.monotonic() < end and process.poll() is None:
            for key, event in selector.select(timeout=1):
                chunk = os.read(key.fd, 65536)
                if not chunk:
                    break
                pending += decoder.decode(chunk)
                lines = pending.split('\n')
                pending = lines.pop()[-65536:]
                for line in lines:
                    safe = redact(line)
                    if safe:
                        print(safe, flush=True)
                        if file:
                            file.write(safe + '\n')
    finally:
        selector.close()
        process.terminate()
        process.wait(timeout=5)
        if file:
            file.close()


if __name__ == '__main__':
    main()
