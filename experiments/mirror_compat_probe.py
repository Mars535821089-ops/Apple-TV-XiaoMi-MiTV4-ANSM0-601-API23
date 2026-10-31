"""Opt-in ENOSYS-only shared-memory fallback; audio capabilities are unchanged."""
import argparse
from io import BytesIO
from pathlib import Path
import shutil,struct,subprocess
from zipfile import ZipFile
from elftools.elf.elffile import ELFFile
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE
from unicorn.arm_const import *
from video_return_probe import LIB,branch,offset
ROOT=Path(__file__).resolve().parents[1]
SITE=0x174db8
EXPECTED=bytes.fromhex('f0b503af')
IMPORTS=['dlopen','dlsym','dlclose','mmap','munmap','close','__errno','sysconf','__android_log_print']

def linker():
    found=shutil.which('ld.lld')
    if found:return [found]
    candidates=sorted((Path.home()/'.rustup/toolchains').glob('*/lib/rustlib/*/bin/rust-lld'))
    if not candidates:raise FileNotFoundError('LLVM ld.lld or rust-lld is required')
    return [str(candidates[0]),'-flavor','gnu']

def imports(elf):
    rel=elf.get_section_by_name('.rel.plt');symbols=elf.get_section(rel['sh_link'])
    result={symbols.get_symbol(r['r_info_sym']).name:r['r_offset'] for r in rel.iter_relocations()}
    if any(name not in result for name in IMPORTS):raise ValueError('Required existing imports missing')
    return {name:result[name] for name in IMPORTS}

def check(data,elf,patched=None,code_va=0,code=b''):
    cases=0;got=imports(elf)
    modes=[('memfd',0,0),('memfd-pow2',0,1),('old-kernel',38,0),('pow2',38,1),('denied',13,0),('create',38,0),('map1',38,0),('map2',38,0),('map3',38,0),('zero-map2',38,0)]
    for base in (0x10000000,0x40000000):
      for mode,error,pow2 in modes:
        cpu=Uc(UC_ARCH_ARM,UC_MODE_THUMB)
        end=max(s['p_vaddr']+s['p_memsz'] for s in elf.iter_segments() if s['p_type']=='PT_LOAD')
        cpu.mem_map(base,(end+4095)&~4095)
        for s in elf.iter_segments():
            if s['p_type']=='PT_LOAD':cpu.mem_write(base+s['p_vaddr'],data[s['p_offset']:s['p_offset']+s['p_filesz']])
        if patched:cpu.mem_write(base+SITE,patched);cpu.mem_write(base+code_va,code)
        stack,arena,functions,stop=0x70008000,0x71000000,0x72000000,0x74000000
        cpu.mem_map(0x70000000,65536);cpu.mem_map(arena,65536);cpu.mem_map(functions,65536);cpu.mem_map(stop,4096)
        ctx,errno_at=arena+0x100,arena+0x200
        cpu.mem_write(ctx,b'\xa5'*24);cpu.mem_write(errno_at,struct.pack('<I',error))
        dispatch={functions+i*0x100:name for i,name in enumerate(IMPORTS)}
        create=functions+0x1000
        for address,name in dispatch.items():cpu.mem_write(base+got[name],struct.pack('<I',address|1))
        regs=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
        initial=[0x44444444+i for i in range(8)]
        for reg,value in zip(regs,initial):cpu.reg_write(reg,value)
        cpu.reg_write(UC_ARM_REG_SP,stack);cpu.reg_write(UC_ARM_REG_LR,stop|1)
        cpu.reg_write(UC_ARM_REG_R0,ctx);cpu.reg_write(UC_ARM_REG_R1,10000);cpu.reg_write(UC_ARM_REG_R2,pow2)
        calls=[];maps=[];closes=[];unmaps=[]
        size=16384 if pow2 else 12288;region=0 if mode=='zero-map2' else arena+0x4000
        def string(uc,p):
            out=bytearray()
            for i in range(100):
                c=uc.mem_read(p+i,1)[0]
                if not c:return out.decode()
                out.append(c)
            raise AssertionError('unterminated string')
        def ret(uc,value):uc.reg_write(UC_ARM_REG_R0,value&0xffffffff);uc.reg_write(UC_ARM_REG_PC,uc.reg_read(UC_ARM_REG_LR))
        def hook(uc,address,length,user):
            if address==stop:uc.emu_stop();return
            if address==base+0x5427c0:
                assert uc.reg_read(UC_ARM_REG_R0)==385 and uc.reg_read(UC_ARM_REG_R2)==0
                ret(uc,33 if mode.startswith('memfd') else -1);return
            if address==base+0x53ef90:
                n,d=uc.reg_read(UC_ARM_REG_R0),uc.reg_read(UC_ARM_REG_R1)
                uc.reg_write(UC_ARM_REG_R1,n%d);ret(uc,n//d);return
            if address==base+0x541e30:ret(uc,errno_at);return
            native={base+0x542730:'sysconf',base+0x5427d0:'ftruncate',base+0x5427e0:'mmap',base+0x5427f0:'munmap',base+0x541c80:'close'}
            name=dispatch.get(address) or native.get(address)
            if address==create:name='create'
            if not name:return
            calls.append(name)
            if name=='sysconf':assert uc.reg_read(UC_ARM_REG_R0)==40;ret(uc,4096)
            elif name=='ftruncate':assert uc.reg_read(UC_ARM_REG_R0)==33 and uc.reg_read(UC_ARM_REG_R1)==size;ret(uc,0)
            elif name=='__errno':ret(uc,errno_at)
            elif name=='dlopen':assert string(uc,uc.reg_read(UC_ARM_REG_R0))=='/system/lib/libcutils.so';ret(uc,0x1234)
            elif name=='dlsym':assert string(uc,uc.reg_read(UC_ARM_REG_R1))=='ashmem_create_region';ret(uc,create|1)
            elif name=='dlclose':ret(uc,0)
            elif name=='create':
                assert string(uc,uc.reg_read(UC_ARM_REG_R0))=='CnCarPlayRing' and uc.reg_read(UC_ARM_REG_R1)==size
                if mode=='create':uc.mem_write(errno_at,struct.pack('<I',13));ret(uc,-1)
                else:ret(uc,33)
            elif name=='mmap':
                number=len(maps)+1;p=uc.reg_read(UC_ARM_REG_R0);n=uc.reg_read(UC_ARM_REG_R1)
                prot,flags=uc.reg_read(UC_ARM_REG_R2),uc.reg_read(UC_ARM_REG_R3)
                fd,off=struct.unpack('<II',uc.mem_read(uc.reg_read(UC_ARM_REG_SP),8));maps.append((p,n,prot,flags,fd,off))
                expected=(0,size*2,0,0x22,0xffffffff,0) if number==1 else (region+(number-2)*size,size,3,0x11,33,0)
                assert maps[-1]==expected,(mode,maps[-1],expected)
                if mode=='map'+str(number) or (mode=='zero-map2' and number==2):uc.mem_write(errno_at,struct.pack('<I',12));ret(uc,-1)
                else:ret(uc,region if number==1 else p)
            elif name=='munmap':unmaps.append((uc.reg_read(UC_ARM_REG_R0),uc.reg_read(UC_ARM_REG_R1)));ret(uc,0)
            elif name=='close':closes.append(uc.reg_read(UC_ARM_REG_R0));ret(uc,0)
            elif name=='__android_log_print':
                assert string(uc,uc.reg_read(UC_ARM_REG_R1))=='CnMirror';ret(uc,0)
        cpu.hook_add(UC_HOOK_CODE,hook)
        cpu.emu_start(base+SITE+1,stop,count=5000)
        value=cpu.reg_read(UC_ARM_REG_R0);want=13 if mode in ('denied','create') else 12 if mode.startswith('map') or mode=='zero-map2' else 0
        assert value==want,('fallback status',mode,value,want)
        assert cpu.reg_read(UC_ARM_REG_SP)==stack
        for reg,value in zip(regs,initial):assert cpu.reg_read(reg)==value
        if want==0:
            assert struct.unpack('<6I',cpu.mem_read(ctx,24))==(region,region+size,size,size-1,0,0)
            assert closes==[33] and not unmaps
        else:
            assert bytes(cpu.mem_read(ctx,24))==b'\xa5'*24
            assert closes==([33] if mode.startswith('map') or mode=='zero-map2' else [])
            assert unmaps==([(region,size*2)] if mode in ('map2','map3','zero-map2') else [])
        if mode=='denied':assert not calls
        if mode.startswith('memfd'):assert not any(n in calls for n in ('dlopen','dlsym','create','__android_log_print'))
        cases+=1
    return cases


def patch(source,output):
    if source.resolve()==output.resolve():raise ValueError('Output must differ from source')
    with ZipFile(source) as z:data=z.read(LIB)
    elf=ELFFile(BytesIO(data))
    if elf.elfclass!=32 or not elf.little_endian or elf['e_machine']!='EM_ARM':raise ValueError('Expected ARM32')
    flags={t.entry.d_tag:t.entry.d_val for t in elf.get_section_by_name('.dynamic').iter_tags() if t.entry.d_tag in ('DT_FLAGS','DT_FLAGS_1')}
    if not(flags.get('DT_FLAGS',0)&8 or flags.get('DT_FLAGS_1',0)&1):raise ValueError('Immediate binding required')
    site=offset(elf,SITE)
    if data[site:site+4]!=EXPECTED:raise ValueError('Unexpected ring initializer entry')
    lower=elf.get_section_by_name('.ARM.extab');upper=elf.get_section_by_name('.rodata')
    va=((lower['sh_addr']+lower['sh_size']+3)&~3)+1024;limit=upper['sh_addr']-512
    if not 1024<=limit-va<=4096:raise ValueError('Unexpected compatibility padding')
    rx=next(seg for seg in elf.iter_segments() if seg['p_type']=='PT_LOAD' and seg['p_flags']==5 and seg['p_vaddr']<=va<limit<=seg['p_vaddr']+seg['p_filesz'])
    pos=offset(elf,va)
    if any(data[pos:pos+limit-va]):raise ValueError('Compatibility padding is occupied')
    for sec in elf.iter_sections():
        if sec['sh_flags']&2 and sec['sh_size'] and sec['sh_addr']<limit and sec['sh_addr']+sec['sh_size']>va:raise ValueError('Allocated section overlaps padding')
        if sec['sh_type'] in ('SHT_REL','SHT_RELA') and any(va<=r['r_offset']<limit for r in sec.iter_relocations()):raise ValueError('Relocation overlaps padding')
    got=imports(elf);work=ROOT/'build/mirror-compat';work.mkdir(parents=True,exist_ok=True)
    code=['.syntax unified','.thumb','.fpu neon','.section .text.entry,"ax",%progbits',
          '.global cn_mirror_entry','.type cn_mirror_entry,%function','.thumb_func','cn_mirror_entry:',
          'push.w {r4,r5,r6,r7,r8,r9,r10,r11,r12,lr}','sub sp,#40',
          'mov r4,r0','mov r5,r1','mov r6,r2','adr.w r11,module_anchor','ldr.w r0,[r11]',
          'sub.w r11,r11,r0','mov r0,r4','mov r1,r5','mov r2,r6','bl mirror_original',
          'cmp r0,#38','bne completed']
    for i,name in enumerate(IMPORTS):
        code+=['ldr r0,import_'+str(i),'add.w r0,r0,r11','ldr r0,[r0]',f'str r0,[sp,#{i*4}]']
    code+=['mov r0,r4','mov r1,r5','mov r2,r6','mov r3,sp','bl cn_mirror_fallback',
           'completed:','add sp,#40','pop.w {r4,r5,r6,r7,r8,r9,r10,r11,r12,lr}','bx lr',
           '.align 2','module_anchor: .word module_anchor']
    for i,name in enumerate(IMPORTS):code.append(f'import_{i}: .word {got[name]}')
    code+=['.align 2','.global mirror_original','.type mirror_original,%function','.thumb_func',
           'mirror_original:','.byte '+','.join(hex(x) for x in EXPECTED),'.global mirror_jump','mirror_jump: .word 0']
    wrapper=work/'wrapper.S';wrapper.write_text('\n'.join(code)+'\n')
    subprocess.run(['xcrun','clang','-target','armv7a-linux-androideabi23','-mthumb','-c',str(wrapper),'-o',str(work/'wrapper.o')],check=True)
    subprocess.run(['xcrun','clang','-target','armv7a-linux-androideabi23','-mthumb','-fPIC','-mstrict-align','-fno-stack-protector','-fno-builtin','-O2','-I'+str(ROOT/'src/carcast/native'),'-c',str(ROOT/'src/carcast/native/mirror_compat.c'),'-o',str(work/'compat.o')],check=True)
    script=work/'layout.ld';script.write_text(f'SECTIONS {{ . = {va}; .text : {{ *(.text.entry) *(.text*) *(.rodata*) }} /DISCARD/ : {{ *(.ARM.exidx*) *(.ARM.extab*) *(.comment*) *(.note*) }} }}')
    linked=work/'compat.elf'
    subprocess.run(linker()+['-m','armelf_linux_eabi','-static','-e','cn_mirror_entry','-T',str(script),str(work/'wrapper.o'),str(work/'compat.o'),'-o',str(linked)],check=True)
    e=ELFFile(BytesIO(linked.read_bytes()));text=e.get_section_by_name('.text');blob=bytearray(text.data())
    if text['sh_addr']!=va or len(blob)>limit-va:raise ValueError('Compatibility code out of bounds')
    if any(sec['sh_size'] and sec['sh_type'] in ('SHT_REL','SHT_RELA') for sec in e.iter_sections()):raise ValueError('Unresolved compatibility relocations')
    symbols={q.name:q for q in e.get_section_by_name('.symtab').iter_symbols()}
    if any(q['st_shndx']=='SHN_UNDEF' and q.name for q in symbols.values()):raise ValueError('External compatibility symbol')
    jump_at=symbols['mirror_jump']['st_value']-va
    blob[jump_at:jump_at+4]=branch(va+jump_at,SITE+4)
    entry=symbols['cn_mirror_entry']['st_value']&~1;jump=branch(SITE,entry)
    cases=check(data,elf,jump,va,bytes(blob))
    modified=bytearray(data);modified[site:site+4]=jump;modified[pos:pos+len(blob)]=blob
    with ZipFile(source) as original,ZipFile(output,'w') as target:
        for item in original.infolist():target.writestr(item,bytes(modified) if item.filename==LIB else original.read(item.filename))
    print('PASS:',cases,'ASLR/error/layout/cleanup cases; ENOSYS-only ashmem fallback; unchanged audio capabilities')

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path);p.add_argument('--check-baseline',action='store_true')
    a=p.parse_args()
    with ZipFile(a.source) as z:data=z.read(LIB)
    elf=ELFFile(BytesIO(data))
    if a.check_baseline:check(data,elf);return
    if a.output is None:p.error('--output is required')
    patch(a.source,a.output)
if __name__=='__main__':main()
