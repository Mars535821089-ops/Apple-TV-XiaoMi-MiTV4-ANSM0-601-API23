"""Diagnostic only: preserve video codec calls, log their ignored return values."""
import argparse
from io import BytesIO
from pathlib import Path
import struct
import subprocess
from zipfile import ZipFile
from elftools.elf.elffile import ELFFile
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE
from unicorn.arm_const import *

LIB='lib/armeabi-v7a/libcarcast.so'
HOOKS=((0x14cba6,bytes.fromhex('d4e91801'),'queue',0x60,0x14cbb4),
       (0x14c940,bytes.fromhex('d4e91a01'),'release',0x68,0x14c950))

def branch(source,target):
    delta=target-source-4
    if delta&1 or not -(1<<24)<=delta<(1<<24):raise ValueError('Thumb branch range')
    value=delta&((1<<25)-1);s=(value>>24)&1;i1=(value>>23)&1;i2=(value>>22)&1
    return struct.pack('<HH',0xf000|(s<<10)|((value>>12)&0x3ff),
                       0x9000|((1^i1^s)<<13)|((1^i2^s)<<11)|((value>>1)&0x7ff))

def offset(elf,va):
    for s in elf.iter_segments():
        if s['p_type']=='PT_LOAD' and s['p_vaddr']<=va< s['p_vaddr']+s['p_filesz']:
            return s['p_offset']+va-s['p_vaddr']
    raise ValueError('Unmapped code address')

def assemble(work,va,log_got,site,original,name):
    assembly=f'''.syntax unified
.thumb
.fpu neon
.text
push.w {{r0,r1,r2,r3,r12,lr}}
adr.w r12, module_anchor
ldr.w r2, [r12]
sub.w r12,r12,r2
ldr r2, log_got
add.w r12,r12,r2
ldr.w r12,[r12]
mov r3,r0
movs r0,#4
adr r1, tag
adr r2, message
blx r12
pop.w {{r0,r1,r2,r3,r12,lr}}
.byte {','.join(hex(x) for x in original)}
push {{r0,r1,lr}}
adr r0, module_anchor
ldr r1,[r0]
sub.w r0,r0,r1
ldr r1, continuation
add.w r1,r1,r0
str r1,[sp,#8]
pop {{r0,r1,pc}}
.align 2
module_anchor: .word module_anchor
log_got: .word {log_got}
continuation: .word {(site+4)|1}
tag: .asciz "CnVideoReturn"
message: .asciz "{name} status=%d"
'''
    src,obj=work/(name+'.S'),work/(name+'.o');src.write_text(assembly)
    subprocess.run(['xcrun','clang','-target','armv7a-linux-androideabi23','-mthumb',
                    '-c','-x','assembler',str(src),'-o',str(obj)],check=True)
    e=ELFFile(BytesIO(obj.read_bytes()));code=bytearray(e.get_section_by_name('.text').data())
    rel=e.get_section_by_name('.rel.text')
    if rel:
        symbols=e.get_section(rel['sh_link'])
        for r in rel.iter_relocations():
            if r['r_info_type']!=2:raise ValueError('Unexpected relocation')
            symbol=symbols.get_symbol(r['r_info_sym']);p=r['r_offset']
            addend=struct.unpack_from('<I',code,p)[0]
            struct.pack_into('<I',code,p,va+symbol['st_value']+addend)
    return bytes(code)

def check(data,elf,patched,stub_va,code,log_got,hook):
    site,original,name,counter,stop=hook
    checks=0
    for base in (0x10000000,0x40000000):
        for status in (0,-1,-10000):
            cpu=Uc(UC_ARCH_ARM,UC_MODE_THUMB)
            for address in (site&~4095,stub_va&~4095,log_got&~4095):cpu.mem_map(base+address,4096)
            cpu.mem_write(base+site,patched)
            p=offset(elf,site+4);cpu.mem_write(base+site+4,data[p:p+stop-site-4])
            cpu.mem_write(base+stub_va,code)
            stack,video,logger=0x70001000,0x71000000,0x72000000
            cpu.mem_map(0x70000000,8192);cpu.mem_map(video,4096);cpu.mem_map(logger,4096)
            cpu.mem_write(base+log_got,struct.pack('<I',logger|1))
            cpu.mem_write(video+counter,struct.pack('<Q',0x100000002))
            regs=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,
                  UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,
                  UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]
            values=[status&0xffffffff,0x11111111,0x22222222,0x33333333,video,
                    0x55555555,0x66666666,0x77777777,0x88888888,0x99999999,
                    0xaaaaaaaa,0xbbbbbbbb,0xcccccccc]
            for r,v in zip(regs,values):cpu.reg_write(r,v)
            cpu.reg_write(UC_ARM_REG_SP,stack);cpu.reg_write(UC_ARM_REG_LR,0x12345679)
            logs=[]
            def cstr(uc,address):
                result=bytearray()
                for i in range(80):
                    x=uc.mem_read(address+i,1)[0]
                    if not x:return result.decode()
                    result.append(x)
                raise AssertionError('Unterminated diagnostic string')
            def callback(uc,address,size,unused):
                if address==logger:
                    assert uc.reg_read(UC_ARM_REG_SP)%8==0
                    assert uc.reg_read(UC_ARM_REG_R0)==4
                    assert cstr(uc,uc.reg_read(UC_ARM_REG_R1))=='CnVideoReturn'
                    assert cstr(uc,uc.reg_read(UC_ARM_REG_R2))==name+' status=%d'
                    logs.append(uc.reg_read(UC_ARM_REG_R3))
                    for reg in (UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R12):uc.reg_write(reg,0xdeadbeef)
                    uc.reg_write(UC_ARM_REG_PC,uc.reg_read(UC_ARM_REG_LR))
                if address==base+stop:uc.emu_stop()
            cpu.hook_add(UC_HOOK_CODE,callback)
            cpu.emu_start(base+site+1,base+stop,count=150)
            assert logs==[status&0xffffffff]
            assert cpu.reg_read(UC_ARM_REG_SP)==stack and cpu.reg_read(UC_ARM_REG_LR)==0x12345679
            # Original counter arithmetic changes r0/r1 (and release r2/r3).
            preserved=range(2,13) if name=='queue' else range(4,13)
            for i in preserved:assert cpu.reg_read(regs[i])==values[i],(name,i)
            assert struct.unpack('<Q',cpu.mem_read(video+counter,8))[0]==0x100000003
            checks+=1
    return checks

def patch(source,output):
    if source.resolve()==output.resolve():raise ValueError('Diagnostic output must not overwrite its source')
    with ZipFile(source) as z:data=z.read(LIB)
    elf=ELFFile(BytesIO(data))
    if elf.elfclass!=32 or not elf.little_endian or elf['e_machine']!='EM_ARM':raise ValueError('Expected ARM32 library')
    flags={t.entry.d_tag:t.entry.d_val for t in elf.get_section_by_name('.dynamic').iter_tags()
           if t.entry.d_tag in ('DT_FLAGS','DT_FLAGS_1')}
    if not (flags.get('DT_FLAGS',0)&8 or flags.get('DT_FLAGS_1',0)&1):
        raise ValueError('Direct logger import requires immediate binding')
    loads=[(i,s) for i,s in enumerate(elf.iter_segments()) if s['p_type']=='PT_LOAD']
    segment=next(s for _,s in loads if s['p_flags']==5 and s['p_vaddr']==0)
    low=elf.get_section_by_name('.ARM.extab');high=elf.get_section_by_name('.rodata')
    start=(low['sh_addr']+low['sh_size']+3)&~3;limit=high['sh_addr']
    if not 512<=limit-start<=4096:raise ValueError('Unexpected unwind-section padding')
    if not segment['p_vaddr']<=start<limit<=segment['p_vaddr']+segment['p_filesz']:
        raise ValueError('Padding is outside the original RX mapping')
    for sec in elf.iter_sections():
        if sec['sh_flags']&2 and sec['sh_size'] and sec['sh_addr']<limit and sec['sh_addr']+sec['sh_size']>start:
            raise ValueError('Padding overlaps an allocated section')
    for sec in elf.iter_sections():
        if sec['sh_type'] in ('SHT_REL','SHT_RELA'):
            if any(start<=r['r_offset']<limit for r in sec.iter_relocations()):raise ValueError('Padding is a relocation target')
    gap=offset(elf,start)
    if any(data[gap:gap+limit-start]):raise ValueError('Expected unused zero-filled section gap')
    rel=elf.get_section_by_name('.rel.plt');symbols=elf.get_section(rel['sh_link'])
    got=[r['r_offset'] for r in rel.iter_relocations() if symbols.get_symbol(r['r_info_sym']).name=='__android_log_print']
    if len(got)!=1:raise ValueError('Expected existing Android log import')
    work=Path(__file__).resolve().parents[1]/'build/video-return-trace';work.mkdir(parents=True,exist_ok=True)
    result=bytearray(data);used=0;checks=0
    for hook in HOOKS:
        site,expected,name,_,_=hook;p=offset(elf,site)
        if data[p:p+4]!=expected:raise ValueError('Unexpected video return boundary')
        used=(used+3)&~3;va=start+used
        code=assemble(work,va,got[0],site,expected,name);filepos=gap+used
        if va+len(code)>limit or any(data[filepos:filepos+len(code)]):raise ValueError('RX section padding is not available')
        jump=branch(site,va);checks+=check(data,elf,jump,va,code,got[0],hook)
        result[p:p+4]=jump;result[filepos:filepos+len(code)]=code;used+=len(code)
    with ZipFile(source) as original,ZipFile(output,'w') as out:
        for item in original.infolist():out.writestr(item,bytes(result) if item.filename==LIB else original.read(item.filename))
    print('PASS:',checks,'ASLR/status/ABI/counter cases; decoder return telemetry only')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',required=True,type=Path);p.add_argument('--output',required=True,type=Path)
    a=p.parse_args();patch(a.source,a.output)
