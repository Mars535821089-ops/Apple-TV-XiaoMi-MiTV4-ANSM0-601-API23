"""Diagnostic receiver media queue target; NOT a negotiated latency fix.

Keeps every advertised audio format and stream type. The sender still requests
its original latency. Only the receiver's type102/103 queue initialization is
changed, so real playback may underrun or remain delayed. Never use by default.
"""
import argparse
import hashlib
import json
from io import BytesIO
from pathlib import Path
import struct
from zipfile import ZipFile
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
from elftools.elf.elffile import ELFFile
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R4, UC_ARM_REG_R9
from low_latency_media import LIBRARY, file_offset, audio_capabilities


def patch_library(raw, target_ms):
    if not 150 <= target_ms <= 250:
        raise ValueError('Diagnostic queue target must be 150..250ms')
    elf = ELFFile(BytesIO(raw))
    offset = file_offset(elf, 0x196616)
    decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    before = next(decoder.disasm(raw[offset:offset+2], 0x196616))
    assert (before.mnemonic, before.op_str) == ('cmp', 'r0, #0')
    replacement = struct.pack('<H', 0x2000 | target_ms)  # MOVS R0,#imm8
    modified = raw[:offset] + replacement + raw[offset+2:]
    cases = 0
    # Execute the real conversion and store, not a copied Python equivalent.
    for rate in (44100, 48000):
        for request in (0, 75, 200, 1000):
            cpu = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
            cpu.mem_map(0x190000, 0x10000)
            start = file_offset(elf, 0x196616)
            cpu.mem_write(0x196616, modified[start:start+0x20])
            cpu.mem_map(0x70000000, 0x4000)
            cpu.reg_write(UC_ARM_REG_R0, request)
            cpu.reg_write(UC_ARM_REG_R4, 0x70000000)
            cpu.reg_write(UC_ARM_REG_R9, 0x70002000)
            cpu.mem_write(0x70002048, struct.pack('<I', rate))
            cpu.emu_start(0x196617, 0x196634, count=15)
            frames = struct.unpack('<I', bytes(cpu.mem_read(0x7000088c, 4)))[0]
            assert frames == rate * target_ms // 1000
            cases += 1
    assert audio_capabilities(raw) == audio_capabilities(modified)
    return modified, cases


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--target-ms', type=int, default=200)
    args = parser.parse_args()
    if args.source.resolve() == args.output.resolve():
        parser.error('Keep the baseline; output must differ')
    with ZipFile(args.source) as source:
        native, cases = patch_library(source.read(LIBRARY), args.target_ms)
        with ZipFile(args.output, 'w') as output:
            for entry in source.infolist():
                output.writestr(entry, native if entry.filename == LIBRARY else source.read(entry.filename))
    print(json.dumps({'experiment': 'receiver-media-queue-probe', 'target_ms': args.target_ms,
                      'conversion_emulation_cases': cases, 'audio_capabilities_unchanged': True,
                      'sha256': hashlib.sha256(args.output.read_bytes()).hexdigest(),
                      'on_device_audio_and_latency_verified': False}))


if __name__ == '__main__':
    main()
