"""Add standard Consumer Voice Command in the knob report's spare bit.

The report stays four bytes. Existing Select/Home/Back, axes and rotary
fields retain their bit positions. Apple's local IOHIDUsageTables.h defines
Consumer Voice Command as 0xCF. Live Siri behavior still requires acceptance.
"""
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
import struct
import argparse
from elftools.elf.elffile import ELFFile
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE
from unicorn.arm_const import *

root=Path(__file__).parent
parser=argparse.ArgumentParser()
parser.add_argument('--source',type=Path,default=root/'CarCast-0.3.25-cn-audio-unsigned.apk')
parser.add_argument('--output',type=Path,default=root/'CarCast-0.3.25-cn-siri-unsigned.apk')
args=parser.parse_args()
source=args.source
output=args.output
name='lib/armeabi-v7a/libcarcast.so'
with ZipFile(source) as z: original=z.read(name)
elf=ELFFile(BytesIO(original))
def offset(va):
    s=next(s for s in elf.iter_segments() if s['p_type']=='PT_LOAD' and s['p_vaddr']<=va<s['p_vaddr']+s['p_filesz'])
    return va-s['p_vaddr']+s['p_offset']
old=bytes.fromhex('05010908a1010509090115002501750195018102050c0a23020a2402950281029505810105010901a100093009311581257f750895028102c009381581257f750895018106c0')
new=old.replace(bytes.fromhex('0a2402950281029505'),bytes.fromhex('0a240209cf950381029504'))
assert len(old)==70 and len(new)==72
start=original.index(old)
assert original[start+70:start+72]==b'\0\0'
modified=bytearray(original)
modified[start:start+72]=new
for va,before,after in [(0x1a9456,'4620','4820'),
                        (0x1a945a,'4ff04608','4ff04808'),
                        (0x1a9466,'4622','4822')]:
    p=offset(va);before=bytes.fromhex(before);after=bytes.fromhex(after)
    assert modified[p:p+len(before)]==before,hex(va)
    modified[p:p+len(after)]=after

def fields(raw):
    page=size=count=bits=0; usages=[]; result=[]; i=0
    while i<len(raw):
        prefix=raw[i];i+=1;n=prefix&3;n=4 if n==3 else n
        data=raw[i:i+n];i+=n;value=int.from_bytes(data,'little')
        typ=(prefix>>2)&3;tag=prefix>>4
        if typ==1 and tag==0:page=value
        elif typ==1 and tag==7:size=value
        elif typ==1 and tag==9:count=value
        elif typ==2 and tag==0:usages.append((page,value))
        elif typ==0:
            if tag==8:
                for j in range(count):
                    result.append((bits,size,usages[min(j,len(usages)-1)] if usages and not value&1 else None,value))
                    bits+=size
            usages=[]
    return bits,result
old_bits,old_fields=fields(old);new_bits,new_fields=fields(new)
assert old_bits==new_bits==32
assert [(b,s,u,v) for b,s,u,v in old_fields if u] == [(b,s,u,v) for b,s,u,v in new_fields if u and b!=3]
assert next(x for x in new_fields if x[0]==3)==(3,1,(12,207),2)

def check(raw,base,expected):
    e=ELFFile(BytesIO(raw));cpu=Uc(UC_ARCH_ARM,UC_MODE_THUMB)
    end=max(s['p_vaddr']+s['p_memsz'] for s in e.iter_segments() if s['p_type']=='PT_LOAD')
    cpu.mem_map(base,(end+4095)&~4095)
    for s in e.iter_segments():
        if s['p_type']=='PT_LOAD':cpu.mem_write(base+s['p_vaddr'],s.data())
    stack=0x70001000;heap=0x72000000;sentinel=0x71000000
    cpu.mem_map(0x70000000,0x3000);cpu.mem_map(heap,4096);cpu.mem_map(sentinel,4096)
    cpu.reg_write(UC_ARM_REG_R0,stack+0x100)
    cpu.reg_write(UC_ARM_REG_R1,stack+0x104)
    cpu.reg_write(UC_ARM_REG_SP,stack)
    cpu.reg_write(UC_ARM_REG_LR,sentinel|1)
    calls=[]
    def hook(uc,addr,size,user):
        if addr==base+0x541e20:
            assert uc.reg_read(UC_ARM_REG_R0)==len(expected)
            calls.append('allocate');uc.reg_write(UC_ARM_REG_R0,heap)
            uc.reg_write(UC_ARM_REG_PC,uc.reg_read(UC_ARM_REG_LR))
        elif addr==base+0x53ef6c:
            dest=uc.reg_read(UC_ARM_REG_R0);src=uc.reg_read(UC_ARM_REG_R1);n=uc.reg_read(UC_ARM_REG_R2)
            assert dest==heap and n==len(expected)
            uc.mem_write(dest,bytes(uc.mem_read(src,n)))
            calls.append('copy');uc.reg_write(UC_ARM_REG_PC,uc.reg_read(UC_ARM_REG_LR))
        elif addr==sentinel:uc.emu_stop()
    cpu.hook_add(UC_HOOK_CODE,hook)
    cpu.emu_start(base+0x1a944d,sentinel,count=200)
    assert calls==['allocate','copy']
    assert struct.unpack('<II',bytes(cpu.mem_read(stack+0x100,8)))==(heap,len(expected))
    assert bytes(cpu.mem_read(heap,len(expected)))==expected
    assert cpu.reg_read(UC_ARM_REG_R0)==0 and cpu.reg_read(UC_ARM_REG_SP)==stack
for base in [0x10000000,0x40000000]:
    check(original,base,old);check(bytes(modified),base,new)
with ZipFile(source) as z,ZipFile(output,'w') as target:
    for entry in z.infolist():target.writestr(entry,bytes(modified) if entry.filename==name else z.read(entry.filename))
print({'report_bits':new_bits,'voice_command_bit':3,'existing_fields_preserved':True,
       'native_allocation_copy_cases_passed':4,'output':output.name})
