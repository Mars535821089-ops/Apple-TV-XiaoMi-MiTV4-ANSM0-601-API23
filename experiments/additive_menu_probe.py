"""Unverified Consumer Menu bits in the existing report's four padding bits.

Keeps X/Y, wheel and every existing button at its original offset. The larger
descriptor lives after our own RX bridge, in its existing zero file padding.
No vendor data region, authentication or expiration logic is overwritten.
This diagnoses iPhone acceptance; it does not claim spatial navigation works.
"""
from io import BytesIO
import struct
from elftools.elf.elffile import ELFFile
from consumer_menu_probe import VOICE, check_copy, smali_probe as array_smali_probe
from hid_descriptor import input_fields
from low_latency_media import file_offset


def smali_probe(text, dpad=False):
    prepared = array_smali_probe(text)
    line = '    add-int/lit8 v2, p1, -0x42\n'
    assert prepared.count(line) == 1
    result = prepared.replace(line, '''    add-int/lit16 v4, p1, -0x84
    const/16 v1, 0x10
    shl-int/2addr v1, v4
''')
    if dpad:
        # Generic Desktop order is Up, Down, Right, Left.
        result = result.replace('    :menu_probe_send\n', '''    const/16 v0, 0x86
    if-ne p1, v0, :dpad_right
    const/16 v1, 0x80
    goto :menu_probe_send
    :dpad_right
    const/16 v0, 0x87
    if-ne p1, v0, :menu_probe_send
    const/16 v1, 0x40
    :menu_probe_send
''')
    return result


def patch_library(raw, dpad=False):
    old_padding = bytes.fromhex('950481010501')
    new_padding = bytes.fromhex('050119902993950481020501' if dpad else '19422945950481020501')
    assert VOICE.count(old_padding) == 1 and raw.count(VOICE) == 1
    descriptor = VOICE.replace(old_padding, new_padding)
    length = 78 if dpad else 76
    assert len(descriptor) == length
    old_bits, old_fields = input_fields(VOICE)
    bits, fields = input_fields(descriptor)
    assert bits == old_bits == 32
    assert [f for f in fields if f[0] not in range(4, 8)] == [f for f in old_fields if f[0] not in range(4, 8)]
    assert [(f[0], f[1], f[2], f[3]) for f in fields if f[0] in range(4, 8)] == [
        (4 + n, 1, ((1, 0x90 + n) if dpad else (12, 0x42 + n)), 2) for n in range(4)]
    elf = ELFFile(BytesIO(raw))
    # Locate the already installed, project-owned mode-0x100 bridge by JNI slot.
    entry = struct.unpack_from('<I', raw, 0x5430ec)[0] & ~1
    owned = [(i, s) for i, s in enumerate(elf.iter_segments())
             if s['p_type'] == 'PT_LOAD' and s['p_vaddr'] == entry]
    assert len(owned) == 1
    index, segment = owned[0]
    assert segment['p_flags'] == 5 and segment['p_filesz'] == segment['p_memsz'] == 104
    address = entry + 104
    offset = segment['p_offset'] + 104
    assert raw[offset:offset+len(descriptor)] == bytes(len(descriptor))
    patched = bytearray(raw)
    patched[offset:offset+len(descriptor)] = descriptor
    ph = elf['e_phoff'] + index * elf['e_phentsize']
    struct.pack_into('<II', patched, ph + 16, 104 + len(descriptor), 104 + len(descriptor))
    for va, before, after in [(0x1a9456, '4820', struct.pack('<H', 0x2000 | length)),
                              (0x1a945a, '4ff04808', bytes([0x4f, 0xf0, length, 0x08])),
                              (0x1a9466, '4822', struct.pack('<H', 0x2200 | length))]:
        position = file_offset(elf, va)
        assert raw[position:position+len(bytes.fromhex(before))] == bytes.fromhex(before)
        patched[position:position+len(bytes.fromhex(before))] = after
    literal = file_offset(elf, 0x1a948c)
    old_address = (struct.unpack_from('<I', raw, literal)[0] + 0x1a946e) & 0xffffffff
    assert raw[file_offset(elf, old_address):file_offset(elf, old_address)+72] == VOICE
    struct.pack_into('<I', patched, literal, (address - 0x1a946e) & 0xffffffff)
    assert len(patched) == len(raw)
    new_elf = ELFFile(BytesIO(patched))
    assert all(s['p_offset'] + s['p_filesz'] < len(patched)
               for s in new_elf.iter_segments() if s['p_type'] == 'PT_LOAD')
    for base in (0x10000000, 0x40000000):
        check_copy(raw, VOICE, base)
        check_copy(bytes(patched), descriptor, base)
    return bytes(patched)


if __name__ == '__main__':
    import argparse
    from pathlib import Path
    from zipfile import ZipFile
    from low_latency_media import LIBRARY
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--dpad', action='store_true', help='Generic Desktop D-pad usages instead of Consumer Menu')
    args = parser.parse_args()
    if args.source.resolve() == args.output.resolve():
        parser.error('Keep the baseline; output must differ')
    with ZipFile(args.source) as source:
        native = patch_library(source.read(LIBRARY), dpad=args.dpad)
        with ZipFile(args.output, 'w') as output:
            for item in source.infolist():
                output.writestr(item, native if item.filename == LIBRARY else source.read(item.filename))
    print({'report_bits': 32, 'descriptor_bytes': 78 if args.dpad else 76,
           'all_original_input_fields_preserved': True, 'allocation_copy_cases': 4,
           'on_device_directions_verified': False})
