"""Unverified Consumer Menu direction HID probe. Default builds never use it.

USB-IF Consumer usages 0x42..45 are Up/Down/Left/Right. Their existence in
the standard does not establish that iPhone CarPlay accepts this collection.
The 4-byte transport remains: buttons, uint16 menu usage, relative wheel.
F2..F5 are diagnostic aliases; physical D-pad mappings remain unchanged.
"""
import argparse
from io import BytesIO
from pathlib import Path
import struct
from zipfile import ZipFile
from elftools.elf.elffile import ELFFile
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE
from unicorn.arm_const import *
from low_latency_media import LIBRARY, file_offset

VOICE = bytes.fromhex('05010908a1010509090115002501750195018102050c0a23020a240209cf950381029504810105010901a100093009311581257f750895028102c009381581257f750895018106c0')
XY = bytes.fromhex('05010901a100093009311581257f750895028102c0')
MENU = bytes.fromhex('050c19002945150025457510950181000501')


def smali_probe(text):
    marker = '    :directions\n'
    assert text.count(marker) == 1
    return text.replace(marker, marker + '''    # Diagnostic only: F2/F3/F4/F5 send Consumer Menu directions.
    const/16 v0, 0x84
    if-lt p1, v0, :physical_directions
    const/16 v0, 0x87
    if-gt p1, v0, :physical_directions
    invoke-virtual {p2}, Landroid/view/KeyEvent;->getAction()I
    move-result v4
    const/4 v1, 0x0
    const/4 v2, 0x0
    const/4 v3, 0x0
    if-nez v4, :menu_probe_send
    invoke-virtual {p2}, Landroid/view/KeyEvent;->getRepeatCount()I
    move-result v0
    if-nez v0, :consumed
    add-int/lit8 v2, p1, -0x42
    :menu_probe_send
    const/16 v0, 0x100
    invoke-static {v0, v1, v2, v3}, Lai/rplay/carcast/CnInput;->enqueue(IIII)V
    goto :consumed
    :physical_directions
''')


def check_copy(raw, expected, base):
    elf = ELFFile(BytesIO(raw))
    cpu = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    end = max(s['p_vaddr'] + s['p_memsz'] for s in elf.iter_segments() if s['p_type'] == 'PT_LOAD')
    cpu.mem_map(base, (end + 4095) & ~4095)
    for segment in elf.iter_segments():
        if segment['p_type'] == 'PT_LOAD':
            cpu.mem_write(base + segment['p_vaddr'], segment.data())
    stack, heap, stop = 0x70001000, 0x72000000, 0x71000000
    cpu.mem_map(0x70000000, 0x3000)
    cpu.mem_map(heap, 4096)
    cpu.mem_map(stop, 4096)
    cpu.reg_write(UC_ARM_REG_R0, stack + 0x100)
    cpu.reg_write(UC_ARM_REG_R1, stack + 0x104)
    cpu.reg_write(UC_ARM_REG_SP, stack)
    cpu.reg_write(UC_ARM_REG_LR, stop | 1)
    calls = []

    def hook(uc, address, size, user):
        if address == base + 0x541e20:
            assert uc.reg_read(UC_ARM_REG_R0) == len(expected)
            calls.append('allocate')
            uc.reg_write(UC_ARM_REG_R0, heap)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        elif address == base + 0x53ef6c:
            dest, source, length = [uc.reg_read(r) for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2)]
            assert dest == heap and length == len(expected)
            uc.mem_write(dest, bytes(uc.mem_read(source, length)))
            calls.append('copy')
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        elif address == stop:
            uc.emu_stop()

    cpu.hook_add(UC_HOOK_CODE, hook)
    cpu.emu_start(base + 0x1a944d, stop, count=200)
    assert calls == ['allocate', 'copy']
    assert struct.unpack('<II', bytes(cpu.mem_read(stack + 0x100, 8))) == (heap, len(expected))
    assert bytes(cpu.mem_read(heap, len(expected))) == expected
    assert cpu.reg_read(UC_ARM_REG_SP) == stack


def patch_library(raw):
    assert len(VOICE) == 72 and raw.count(VOICE) == 1
    descriptor = VOICE.replace(XY, MENU)
    assert len(descriptor) == 69
    # Bits remain 8(buttons/padding)+16(menu array)+8(relative wheel).
    assert bytes.fromhex('751095018100') in descriptor
    elf = ELFFile(BytesIO(raw))
    patched = bytearray(raw)
    start = raw.index(VOICE)
    patched[start:start+72] = descriptor + bytes(3)
    for va, before, after in [(0x1a9456, '4820', '4520'),
                              (0x1a945a, '4ff04808', '4ff04508'),
                              (0x1a9466, '4822', '4522')]:
        offset = file_offset(elf, va)
        assert patched[offset:offset+len(bytes.fromhex(before))] == bytes.fromhex(before)
        patched[offset:offset+len(bytes.fromhex(before))] = bytes.fromhex(after)
    for base in (0x10000000, 0x40000000):
        check_copy(raw, VOICE, base)
        check_copy(bytes(patched), descriptor, base)
    return bytes(patched)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.source.resolve() == args.output.resolve():
        parser.error('Keep the baseline; output must differ')
    with ZipFile(args.source) as source:
        native = patch_library(source.read(LIBRARY))
        with ZipFile(args.output, 'w') as output:
            for entry in source.infolist():
                output.writestr(entry, native if entry.filename == LIBRARY else source.read(entry.filename))
    print({'descriptor_bytes': 69, 'report_bits': 32, 'allocation_copy_cases': 4,
           'on_device_directions_verified': False})


if __name__ == '__main__':
    main()
