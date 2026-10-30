"""Extend the existing iapPointer JNI binding with mode 0x100 for knob HID.

All original modes tail-call the original function. The extension emits the
same four-byte Knob & Buttons report through the existing authenticated
CarPlay transport used by CarCastSendHomeButton. A separate read/execute
PT_LOAD uses the PT_NOTE program-header slot; existing mappings are unchanged.
"""
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
import struct
import subprocess
from elftools.elf.elffile import ELFFile
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE
from unicorn.arm_const import *

root = Path(__file__).parent
source = root / 'CarCast-0.3.25-cn-armfix2-unsigned.apk'
output = root / 'CarCast-0.3.25-cn-knob-unsigned.apk'
library = 'lib/armeabi-v7a/libcarcast.so'
with ZipFile(source) as z:
    original = z.read(library)
# The vendor's Knob & Buttons descriptor defines signed absolute X/Y:
# logical minimum 0x81 (-127), maximum 0x7f (+127). Neutral is zero.
assert bytes.fromhex('093009311581257f750895028102') in original
elf = ELFFile(BytesIO(original))
assert elf.elfclass == 32 and elf.little_endian
segments = list(elf.iter_segments())
loads = [s for s in segments if s['p_type'] == 'PT_LOAD']
align = lambda value: (value + 4095) & ~4095
code_va = align(max(s['p_vaddr'] + s['p_memsz'] for s in loads)) + 4096
code_off = align(len(original))
note_index = next(i for i, s in enumerate(segments) if s['p_type'] == 'PT_NOTE')
binding_off = 0x5430ec
assert struct.unpack_from('<I', original, binding_off)[0] == 0x1342b9
session_va, device_va, send_va, original_va = 0x594db8, 0x594e51, 0x19c809, 0x1342b9
assembly = f'''
push {{r4, r5, r6, lr}}
adr r6, module_anchor
ldr r4, [r6]
sub r6, r6, r4
cmp.w r2, #0x100
bne fallback
sub sp, sp, #16
strb r3, [sp]
ldr r0, [sp, #32]
strb r0, [sp, #1]
lsrs r0, r0, #8
strb r0, [sp, #2]
ldr r0, [sp, #36]
strb r0, [sp, #3]
ldr r4, session_value
add r4, r4, r6
ldr r0, [r4]
cmp r0, #0
beq done
ldr r4, device_value
add r4, r4, r6
ldrb r1, [r4]
mov r2, sp
movs r3, #4
ldr r4, send_value
add r4, r4, r6
blx r4
done:
add sp, sp, #16
pop {{r4, r5, r6, pc}}
fallback:
ldr r4, original_value
add r12, r4, r6
pop.w {{r4, r5, r6, lr}}
bx r12
.align 2
module_anchor: .word module_anchor
session_value: .word {session_va}
device_value: .word {device_va}
send_value: .word {send_va}
original_value: .word {original_va}
'''
asm_path = root / 'carcast_knob_bridge.S'
obj_path = root / 'carcast_knob_bridge.o'
asm_path.write_text('.syntax unified\n.thumb\n.fpu neon\n.text\n' + assembly)
subprocess.run(['xcrun', 'clang', '-target', 'armv7a-linux-androideabi23', '-mthumb',
                '-c', '-x', 'assembler', str(asm_path), '-o', str(obj_path)], check=True)
obj = ELFFile(BytesIO(obj_path.read_bytes()))
code = bytearray(obj.get_section_by_name('.text').data())
rel = obj.get_section_by_name('.rel.text')
if rel:
    symbols = obj.get_section(rel['sh_link'])
    for relocation in rel.iter_relocations():
        assert relocation['r_info_type'] == 2, relocation.entry  # R_ARM_ABS32
        symbol = symbols.get_symbol(relocation['r_info_sym'])
        offset = relocation['r_offset']
        addend = struct.unpack_from('<I', code, offset)[0]
        struct.pack_into('<I', code, offset, code_va + symbol['st_value'] + addend)
code = bytes(code)
assert len(code) < 4096
modified = bytearray(original)
modified.extend(bytes(code_off - len(modified)) + code + bytes(4096))
struct.pack_into('<I', modified, binding_off, code_va | 1)
phoff = elf['e_phoff'] + note_index * elf['e_phentsize']
assert elf['e_phentsize'] == 32
struct.pack_into('<8I', modified, phoff, 1, code_off, code_va, code_va, len(code), len(code), 5, 4096)
new_elf = ELFFile(BytesIO(modified))
assert any(s['p_type'] == 'PT_LOAD' and s['p_vaddr'] == code_va and s['p_flags'] == 5 for s in new_elf.iter_segments())
# Android 6's linker rejects a load segment whose file end equals EOF.
assert all(s['p_offset'] + s['p_filesz'] < len(modified) for s in new_elf.iter_segments() if s['p_type'] == 'PT_LOAD')

def check(base, mode, buttons, xy, rotary, connected=True):
    cpu = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    cpu.mem_map(base, align(code_va + 4096))
    cpu.mem_write(base + code_va, code)
    cpu.mem_write(base + session_va, struct.pack('<I', 0x12345678 if connected else 0))
    cpu.mem_write(base + device_va, bytes([7]))
    stack, sentinel = 0x70001000, 0x71000000
    cpu.mem_map(0x70000000, 0x2000)
    cpu.mem_map(sentinel, 4096)
    cpu.mem_write(stack, struct.pack('<II', xy & 0xffffffff, rotary & 0xffffffff))
    initial = {UC_ARM_REG_R0: 0x11111111, UC_ARM_REG_R1: 0x22222222,
               UC_ARM_REG_R2: mode, UC_ARM_REG_R3: buttons,
               UC_ARM_REG_R4: 0x44444444, UC_ARM_REG_R5: 0x55555555,
               UC_ARM_REG_R6: 0x66666666, UC_ARM_REG_SP: stack,
               UC_ARM_REG_LR: sentinel | 1}
    for reg, value in initial.items():
        cpu.reg_write(reg, value)
    calls = []
    def hook(uc, address, size, data):
        if address == base + (send_va & ~1):
            assert uc.reg_read(UC_ARM_REG_R0) == 0x12345678
            assert uc.reg_read(UC_ARM_REG_R1) == 7
            assert uc.reg_read(UC_ARM_REG_R3) == 4
            calls.append(bytes(uc.mem_read(uc.reg_read(UC_ARM_REG_R2), 4)))
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        elif address == base + (original_va & ~1):
            assert mode != 0x100
            assert all(uc.reg_read(reg) == initial[reg] for reg in [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_SP])
            assert bytes(uc.mem_read(stack, 8)) == struct.pack('<II', xy & 0xffffffff, rotary & 0xffffffff)
            calls.append(b'forwarded')
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        elif address == sentinel:
            uc.emu_stop()
    cpu.hook_add(UC_HOOK_CODE, hook)
    cpu.emu_start(base + code_va + 1, sentinel, count=300)
    assert all(cpu.reg_read(reg) == initial[reg] for reg in [UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_SP])
    expected = [] if not connected and mode == 0x100 else [bytes([buttons & 255, xy & 255, (xy >> 8) & 255, rotary & 255])] if mode == 0x100 else [b'forwarded']
    assert calls == expected, (calls, expected)

count = 0
for base in [0x10000000, 0x40000000]:
    for args in [(0x100,0,0,0), (0x100,1,0,0), (0x100,4,0,0),
                 (0x100,0,0x81,0), (0x100,0,0x7f,0), (0x100,0,0x8100,0),
                 (0x100,0,0x7f00,0), (0x100,0,0x01,0), (0x100,0,0xff,0),
                 (0x100,0,0x0100,0), (0x100,0,0xff00,0),
                 (0x100,0,0,-1), (0,12,34,56), (8,1,2,3)]:
        if args[0] == 0x100:
            axes = struct.unpack('bb', struct.pack('<H', args[2]))
            assert all(-127 <= value <= 127 for value in axes)
        check(base, *args)
        count += 1
    check(base,0x100,1,0,0,False)
    count += 1
with ZipFile(source) as z, ZipFile(output, 'w') as target:
    for entry in z.infolist():
        target.writestr(entry, bytes(modified) if entry.filename == library else z.read(entry.filename))
print({'output': output.name, 'bridge_address': hex(code_va), 'bridge_bytes': len(code),
       'ASLR_and_ABI_cases_passed': count, 'existing_modes_forwarded': True,
       'new_mapping': 'read-execute, never writable'})
