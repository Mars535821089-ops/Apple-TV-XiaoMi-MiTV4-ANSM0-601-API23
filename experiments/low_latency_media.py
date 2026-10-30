"""Experimental legacy compressed media path; does not claim measured A/V sync.

The default build remains unchanged. This probe removes the optional
mainBuffered token, omits types102/103 from the explicit capability list and
offers existing AAC-LC formats on the type100 media path. Authentication,
voice formats and receiver playback timestamps are not bypassed or forged.
"""
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
import argparse
import hashlib
import json
import struct

from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
from elftools.elf.elffile import ELFFile
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE
from unicorn.arm_const import *

LIBRARY = 'lib/armeabi-v7a/libcarcast.so'


def file_offset(elf, address):
    segment = next(s for s in elf.iter_segments() if s['p_type'] == 'PT_LOAD'
                   and s['p_vaddr'] <= address < s['p_vaddr'] + s['p_filesz'])
    return address - segment['p_vaddr'] + segment['p_offset']


def audio_capabilities(raw):
    elf = ELFFile(BytesIO(raw))
    cpu = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    end = max(s['p_vaddr'] + s['p_memsz'] for s in elf.iter_segments() if s['p_type'] == 'PT_LOAD')
    cpu.mem_map(0, (end + 4095) & ~4095)
    for segment in elf.iter_segments():
        if segment['p_type'] == 'PT_LOAD':
            cpu.mem_write(segment['p_vaddr'], segment.data())
    cpu.mem_map(0x70000000, 0x10000)
    cpu.mem_map(0x71000000, 4096)
    cpu.reg_write(UC_ARM_REG_SP, 0x70008000)
    cpu.reg_write(UC_ARM_REG_LR, 0x71000001)
    cpu.reg_write(UC_ARM_REG_R0, 0)
    records = []

    def hook(uc, address, size, user):
        if address == 0x19cbbc:
            blob = bytes(uc.mem_read(uc.reg_read(UC_ARM_REG_R2), 80))
            names = ['compatibility', 'default', 'alert', 'media', 'telephony', 'speechRecognition']
            candidates = [blob]
            for pointer in struct.unpack('<20I', blob):
                if 0x60000 <= pointer < 0x131000:
                    candidates.append(bytes(uc.mem_read(pointer, 80)))
            name = next(name for name in names if any(name.encode() + b'\0' in value for value in candidates))
            masks = struct.unpack('<QQ', bytes(uc.mem_read(uc.reg_read(UC_ARM_REG_SP), 16)))
            records.append((uc.reg_read(UC_ARM_REG_R1), name, *masks))
            uc.mem_write(uc.reg_read(UC_ARM_REG_R0), struct.pack('<I', 0x70000100))
            uc.reg_write(UC_ARM_REG_R0, 0)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        elif address == 0x71000000:
            uc.emu_stop()

    cpu.hook_add(UC_HOOK_CODE, hook)
    cpu.emu_start(0x149779, 0x71000000, count=4000)
    return records


def patch_library(raw):
    elf = ELFFile(BytesIO(raw))
    decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    modified = bytearray(raw)
    # Address, expected original instruction, explicit target for a short branch.
    branches = [(0x1489a2, ('cbz', 'r0, #0x1489ae'), 0x1489ae),
                (0x149848, ('cbz', 'r0, #0x149868'), 0x149868),
                (0x1498be, ('ldr', 'r2, [pc, #0x80]'), 0x1498da)]
    for address, expected, target in branches:
        offset = file_offset(elf, address)
        instruction = next(decoder.disasm(raw[offset:offset + 2], address))
        assert (instruction.mnemonic, instruction.op_str) == expected
        delta = target - address - 4
        assert delta % 2 == 0 and -2048 <= delta <= 2046
        replacement = struct.pack('<H', 0xe000 | ((delta >> 1) & 0x7ff))
        result = next(decoder.disasm(replacement, address))
        assert (result.mnemonic, result.op_str) == ('b', '#' + hex(target))
        modified[offset:offset + 2] = replacement
    source = file_offset(elf, 0x14984e)
    destination = file_offset(elf, 0x149808)
    old = next(decoder.disasm(raw[destination:destination + 4], 0x149808))
    new = next(decoder.disasm(raw[source:source + 4], 0x149808))
    assert (old.mnemonic, old.op_str) == ('mov.w', 'r1, #0x8800')
    assert (new.mnemonic, new.op_str) == ('mov.w', 'r1, #0xc00000')
    modified[destination:destination + 4] = raw[source:source + 4]
    before = audio_capabilities(raw)
    after = audio_capabilities(bytes(modified))
    assert (102, 'media', 0, 0xc00000) in before
    assert (100, 'media', 0, 0x8800) in before
    expected = [(type_, name, input_, 0xc00000 if (type_, name) == (100, 'media') else output)
                for type_, name, input_, output in before if type_ != 102]
    assert after == expected, {'before': before, 'after': after, 'expected': expected}
    assert len(after) == len(before) - 1
    return bytes(modified), before, after


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.source.resolve() == args.output.resolve():
        parser.error('Keep the baseline; --output must differ from --source')
    with ZipFile(args.source) as source:
        native, before, after = patch_library(source.read(LIBRARY))
        with ZipFile(args.output, 'w') as output:
            for entry in source.infolist():
                output.writestr(entry, native if entry.filename == LIBRARY else source.read(entry.filename))
    receipt = {'experiment': 'legacy-compressed-media', 'source_sha256': hashlib.sha256(args.source.read_bytes()).hexdigest(),
               'sha256': hashlib.sha256(args.output.read_bytes()).hexdigest(),
               'audio_capabilities_before': before, 'audio_capabilities_after': after,
               'on_device_audio_and_latency_verified': False}
    print(json.dumps(receipt))


if __name__ == '__main__':
    main()
