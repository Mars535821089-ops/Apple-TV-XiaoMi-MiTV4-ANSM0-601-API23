"""Controlled first-poll wait only; subsequent decoder polls stay nonblocking."""
import argparse
from io import BytesIO
from pathlib import Path
import struct
import subprocess
from zipfile import ZipFile
from elftools.elf.elffile import ELFFile
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE
from unicorn.arm_const import *
from video_return_probe import branch,offset,LIB

SITE,RESUME,LOOP=0x14c8f6,0x14c924,0x14c918
EXPECTED=bytes.fromhex('c9487844')

def check(data,elf,jump=None,stub_va=0,code=b'',got=0):
    cases=0
    for base in (0x10000000,0x40000000):
        for result in (7,-1,-2):
            cpu=Uc(UC_ARCH_ARM,UC_MODE_THUMB)
            pages={SITE&~4095,0x542000}
            if jump:pages.update((stub_va&~4095,got&~4095))
            for page in pages:cpu.mem_map(base+page,4096)
            p=offset(elf,SITE&~4095);cpu.mem_write(base+(SITE&~4095),data[p:p+4096])
            logger,video,stack=0x72000000,0x71000000,0x70001000
            cpu.mem_map(logger,4096);cpu.mem_map(video,4096);cpu.mem_map(0x70000000,8192)
            if jump:
                cpu.mem_write(base+SITE,jump);cpu.mem_write(base+stub_va,code)
                cpu.mem_write(base+got,struct.pack('<I',logger|1))
            codec=video+0x200;cpu.mem_write(video+0x54,struct.pack('<I',codec))
            regs=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,
                  UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
            values=[video,0x55555555,0x66666666,0x77777777,0x88888888,
                    stack+0x30,0xaaaaaaaa,0xbbbbbbbb]
            for reg,value in zip(regs,values):cpu.reg_write(reg,value)
            cpu.reg_write(UC_ARM_REG_SP,stack);cpu.reg_write(UC_ARM_REG_LR,0x12345679)
            calls=[]
            def callback(uc,address,size,unused):
                if address in (logger,base+0x5423c0):
                    timeout=uc.reg_read(UC_ARM_REG_R2)|(uc.reg_read(UC_ARM_REG_R3)<<32)
                    want=5000 if not calls else 0
                    assert timeout==want,('first-poll wait',timeout,want)
                    assert uc.reg_read(UC_ARM_REG_SP)==stack
                    assert uc.reg_read(UC_ARM_REG_R0)==codec
                    assert uc.reg_read(UC_ARM_REG_R1)==stack+0x30
                    calls.append(timeout)
                    for reg in (UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R12):uc.reg_write(reg,0xdeadbeef)
                    uc.reg_write(UC_ARM_REG_R0,result&0xffffffff)
                    uc.reg_write(UC_ARM_REG_PC,uc.reg_read(UC_ARM_REG_LR))
                elif address==base+RESUME:uc.emu_stop()
            cpu.hook_add(UC_HOOK_CODE,callback)
            cpu.emu_start(base+SITE+1,base+RESUME,count=100)
            assert struct.unpack('<I',cpu.mem_read(stack+0x24,4))[0]==base+0x69120
            assert cpu.reg_read(UC_ARM_REG_R0)==result&0xffffffff
            assert cpu.reg_read(UC_ARM_REG_LR)==base+RESUME+1
            assert cpu.reg_read(UC_ARM_REG_SP)==stack
            for reg,value in zip(regs,values):assert cpu.reg_read(reg)==value
            cpu.emu_start(base+LOOP+1,base+RESUME,count=100)
            assert calls==[5000,0]
            cases+=1
    return cases


def patch(source,output):
    if source.resolve()==output.resolve():raise ValueError('Output must differ from source')
    with ZipFile(source) as z:data=z.read(LIB)
    elf=ELFFile(BytesIO(data))
    if elf.elfclass!=32 or not elf.little_endian or elf['e_machine']!='EM_ARM':raise ValueError('Expected ARM32')
    flags={t.entry.d_tag:t.entry.d_val for t in elf.get_section_by_name('.dynamic').iter_tags() if t.entry.d_tag in ('DT_FLAGS','DT_FLAGS_1')}
    if not(flags.get('DT_FLAGS',0)&8 or flags.get('DT_FLAGS_1',0)&1):raise ValueError('Immediate import binding required')
    if data[offset(elf,SITE):offset(elf,SITE)+4]!=EXPECTED:raise ValueError('Unexpected first-drain header')
    literal=struct.unpack_from('<I',data,offset(elf,0x14cc1c))[0]
    if (literal+0x14c8fc)&0xffffffff!=0x69120:raise ValueError('Unexpected fallback address')
    high=elf.get_section_by_name('.rodata')['sh_addr'];va=high-256;p=offset(elf,va)
    rx=next(x for x in elf.iter_segments() if x['p_type']=='PT_LOAD' and x['p_flags']==5 and x['p_vaddr']<=va<high<=x['p_vaddr']+x['p_filesz'])
    if any(data[p:p+256]):raise ValueError('First-wait padding is not empty')
    for sec in elf.iter_sections():
        if sec['sh_flags']&2 and sec['sh_size'] and sec['sh_addr']<high and sec['sh_addr']+sec['sh_size']>va:raise ValueError('Allocated section overlap')
        if sec['sh_type'] in ('SHT_REL','SHT_RELA') and any(va<=r['r_offset']<high for r in sec.iter_relocations()):raise ValueError('Relocation overlap')
    rel=elf.get_section_by_name('.rel.plt');sym=elf.get_section(rel['sh_link'])
    got=[r['r_offset'] for r in rel.iter_relocations() if sym.get_symbol(r['r_info_sym']).name=='AMediaCodec_dequeueOutputBuffer']
    if len(got)!=1:raise ValueError('Expected one dequeue import')
    work=Path(__file__).resolve().parents[1]/'build/video-first-wait';work.mkdir(parents=True,exist_ok=True)
    asm=f""".syntax unified
.thumb
.fpu neon
.text
adr.w r12,module_anchor
ldr.w r0,[r12]
sub.w r12,r12,r0
ldr r0,fallback
add.w r0,r0,r12
str r0,[sp,#0x24]
ldr r0,dequeue_got
add.w r12,r12,r0
ldr.w r12,[r12]
ldr r0,[r4,#0x54]
mov r1,r9
movw r2,#5000
movs r3,#0
blx r12
adr r2,module_anchor
ldr r3,[r2]
sub.w r2,r2,r3
ldr r3,continuation
add.w r3,r3,r2
mov lr,r3
bx lr
.align 2
module_anchor: .word module_anchor
fallback: .word 0x69120
dequeue_got: .word {got[0]}
continuation: .word 0x14c925
"""
    src,obj=work/'first-wait.S',work/'first-wait.o';src.write_text(asm)
    subprocess.run(['xcrun','clang','-target','armv7a-linux-androideabi23','-mthumb','-c','-x','assembler',str(src),'-o',str(obj)],check=True)
    e=ELFFile(BytesIO(obj.read_bytes()));code=bytearray(e.get_section_by_name('.text').data())
    r=e.get_section_by_name('.rel.text')
    if r:
        symbols=e.get_section(r['sh_link'])
        for relocation in r.iter_relocations():
            if relocation['r_info_type']!=2:raise ValueError('Unexpected relocation')
            q=relocation['r_offset'];symbol=symbols.get_symbol(relocation['r_info_sym'])
            value=struct.unpack_from('<I',code,q)[0];struct.pack_into('<I',code,q,va+symbol['st_value']+value)
    if len(code)>256:raise ValueError('First-wait stub exceeds reserved padding')
    jump=branch(SITE,va);cases=check(data,elf,jump,va,bytes(code),got[0])
    patched=bytearray(data);patched[offset(elf,SITE):offset(elf,SITE)+4]=jump;patched[p:p+len(code)]=code
    with ZipFile(source) as original,ZipFile(output,'w') as out:
        for entry in original.infolist():out.writestr(entry,bytes(patched) if entry.filename==LIB else original.read(entry.filename))
    print('PASS:',cases,'ASLR/status cases: first poll5000us, following poll0, stack/callee registers/fallback/result preserved')

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',required=True,type=Path)
    p.add_argument('--output',type=Path);p.add_argument('--check-baseline',action='store_true')
    a=p.parse_args()
    with ZipFile(a.source) as z:data=z.read(LIB)
    elf=ELFFile(BytesIO(data))
    if a.check_baseline:
        check(data,elf);return
    if a.output is None:p.error('--output is required')
    patch(a.source,a.output)

if __name__=='__main__':main()
