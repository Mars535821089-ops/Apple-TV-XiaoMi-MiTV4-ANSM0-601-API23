"""Replace one unaligned STRD with two equivalent Thumb STR instructions.

The observed crash is at libcarcast.so+0x143f18 in both vendor and Chinese
builds. R4 ends in ...c6; STRD writes at R4+4, which is not word-aligned.
The preceding ordinary STR.W to R4+12 already succeeds on the same device.
The replacement has identical length, writes and flag/register semantics.
No connection/authentication/expiry logic is changed.
"""
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
import hashlib
from elftools.elf.elffile import ELFFile
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R4, UC_ARM_REG_CPSR

root = Path(__file__).parent
source = root / 'CarCast-0.3.25-cn-preserved-unsigned.apk'
output = root / 'CarCast-0.3.25-cn-armfix2-unsigned.apk'
library = 'lib/armeabi-v7a/libcarcast.so'
with ZipFile(source) as z:
    original = z.read(library)
elf = ELFFile(BytesIO(original))
decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB)

def emulate(code, base, r1, r2, count):
    cpu = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    cpu.mem_map(0x1000, 0x1000)
    cpu.mem_map(0x10000, 0x2000)
    cpu.mem_write(0x1000, code)
    cpu.mem_write(base, bytes([0xA5]) * 32)
    cpu.reg_write(UC_ARM_REG_R1, r1)
    cpu.reg_write(UC_ARM_REG_R2, r2)
    cpu.reg_write(UC_ARM_REG_R0, r2)
    cpu.reg_write(UC_ARM_REG_R4, base)
    cpu.reg_write(UC_ARM_REG_CPSR, 0xA0000030)
    cpu.emu_start(0x1001, 0x1004, count=count)
    assert cpu.reg_read(UC_ARM_REG_R1) == r1
    assert cpu.reg_read(UC_ARM_REG_R2) == r2
    assert cpu.reg_read(UC_ARM_REG_R0) == r2
    assert cpu.reg_read(UC_ARM_REG_R4) == base
    assert cpu.reg_read(UC_ARM_REG_CPSR) & 0xF0000000 == 0xA0000000
    return bytes(cpu.mem_read(base, 32))

cases = 0
modified = original
changes = []
for address, replacement_hex, operands, expected_new in [
    (0x143f18, '6260a160', 'r2, r1, [r4, #4]', [('str', 'r2, [r4, #4]'), ('str', 'r1, [r4, #8]')]),
    # The next real device run passed handoff, then crashed in the corresponding
    # object cleanup at this second STRD. It is the same proven alignment issue.
    (0x143f80, '6060a060', 'r0, r0, [r4, #4]', [('str', 'r0, [r4, #4]'), ('str', 'r0, [r4, #8]')]),
]:
    segment = next(s for s in elf.iter_segments() if s['p_type'] == 'PT_LOAD' and s['p_vaddr'] <= address < s['p_vaddr'] + s['p_filesz'])
    offset = address - segment['p_vaddr'] + segment['p_offset']
    before = original[offset:offset+4]
    replacement = bytes.fromhex(replacement_hex)
    old = [(i.mnemonic, i.op_str) for i in decoder.disasm(before, address)]
    new = [(i.mnemonic, i.op_str) for i in decoder.disasm(replacement, address)]
    assert old == [('strd', operands)], old
    assert new == expected_new, new
    for r1, r2 in [(0, 0), (0xffffffff, 0x12345678), (0xabcdef01, 2), (1, 0x80000000)]:
        expected = emulate(before, 0x10100, r1, r2, 1)
        for alignment in range(4):
            assert emulate(replacement, 0x10100 + alignment, r1, r2, 2) == expected
            cases += 1
    modified = modified[:offset] + replacement + modified[offset+4:]
    changes.append({'address': hex(address), 'before': old, 'after': new})
assert len(modified) == len(original)
assert sum(a != b for a, b in zip(original, modified)) <= 8
with ZipFile(source) as z, ZipFile(output, 'w') as target:
    for entry in z.infolist():
        target.writestr(entry, modified if entry.filename == library else z.read(entry.filename))
with ZipFile(source) as z, ZipFile(output) as target:
    assert all(z.read(n) == target.read(n) for n in z.namelist() if n != library)
print({'changes': changes, 'emulation_cases_passed': cases,
       'library_sha256_before': hashlib.sha256(original).hexdigest(),
       'library_sha256_after': hashlib.sha256(modified).hexdigest(), 'output': output.name})
