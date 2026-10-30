"""Negotiate PCM for interactive voice; retain separate media formats.

The observed speechRecognition request selects AAC-ELD 24 kHz and fails
with status 38 before the phone tears down the whole session. The vendor
advertises PCM alternatives already. This selects those alternatives for
default/telephony/speechRecognition, without suppressing the features.
"""
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
import struct
from elftools.elf.elffile import ELFFile
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE
from unicorn.arm_const import *

root=Path(__file__).parent
source=root/'CarCast-0.3.25-cn-knob-unsigned.apk'
output=root/'CarCast-0.3.25-cn-audio-unsigned.apk'
library='lib/armeabi-v7a/libcarcast.so'
with ZipFile(source) as z: original=z.read(library)
elf=ELFFile(BytesIO(original))
modified=bytearray(original)
decoder=Cs(CS_ARCH_ARM,CS_MODE_THUMB)
patches=[(0x1497ec,'r0, #0x3000'),(0x14986e,'r0, #0x7000'),(0x14988c,'r0, #0x2000')]
for address, expected in patches:
    segment=next(s for s in elf.iter_segments() if s['p_type']=='PT_LOAD' and s['p_vaddr']<=address<s['p_vaddr']+s['p_filesz'])
    offset=address-segment['p_vaddr']+segment['p_offset']
    assert [(i.mnemonic,i.op_str) for i in decoder.disasm(original[offset:offset+4],address)]==[('movt',expected)]
    replacement=bytes.fromhex('c0f20000')
    assert [(i.mnemonic,i.op_str) for i in decoder.disasm(replacement,address)]==[('movt','r0, #0')]
    modified[offset:offset+4]=replacement

def advertised(raw):
    e=ELFFile(BytesIO(raw))
    end=max(s['p_vaddr']+s['p_memsz'] for s in e.iter_segments() if s['p_type']=='PT_LOAD')
    cpu=Uc(UC_ARCH_ARM,UC_MODE_THUMB)
    cpu.mem_map(0,(end+4095)&~4095)
    for s in e.iter_segments():
        if s['p_type']=='PT_LOAD':cpu.mem_write(s['p_vaddr'],raw[s['p_offset']:s['p_offset']+s['p_filesz']])
    cpu.mem_map(0x70000000,0x10000)
    cpu.mem_map(0x71000000,4096)
    cpu.reg_write(UC_ARM_REG_SP,0x70008000)
    cpu.reg_write(UC_ARM_REG_LR,0x71000001)
    cpu.reg_write(UC_ARM_REG_R0,0)
    records=[]
    def hook(uc,address,size,user):
        if address==0x19cbbc:
            blob=bytes(uc.mem_read(uc.reg_read(UC_ARM_REG_R2),80))
            names=['compatibility','default','alert','media','telephony','speechRecognition']
            candidates=[blob]
            for ptr in struct.unpack('<20I',blob):
                if 0x60000<=ptr<0x131000:candidates.append(bytes(uc.mem_read(ptr,80)))
            name=next((name for name in names if any(name.encode()+b'\0' in value for value in candidates)),None)
            assert name is not None,blob.hex()
            masks=struct.unpack('<QQ',bytes(uc.mem_read(uc.reg_read(UC_ARM_REG_SP),16)))
            records.append((uc.reg_read(UC_ARM_REG_R1),name,*masks))
            uc.mem_write(uc.reg_read(UC_ARM_REG_R0),struct.pack('<I',0x70000100))
            uc.reg_write(UC_ARM_REG_R0,0)
            uc.reg_write(UC_ARM_REG_PC,uc.reg_read(UC_ARM_REG_LR))
        elif address==0x71000000:uc.emu_stop()
    cpu.hook_add(UC_HOOK_CODE,hook)
    cpu.emu_start(0x149779,0x71000000,count=4000)
    return records

before=advertised(original)
after=advertised(bytes(modified))
assert len(before)==len(after)>=8,(before,after)
changed=[]
for old,new in zip(before,after):
    assert old[:2]==new[:2]
    if old!=new:
        assert old[1] in ['default','telephony','speechRecognition'],(old,new)
        assert new[2:]==tuple(mask & 0xffff for mask in old[2:])
        changed.append((old,new))
assert len(changed)==3,changed
with ZipFile(source) as z,ZipFile(output,'w') as target:
    for entry in z.infolist():target.writestr(entry,bytes(modified) if entry.filename==library else z.read(entry.filename))
print({'changed_audio_capabilities':changed,'media_capabilities_preserved':True,'records_checked':len(after),'output':output.name})
