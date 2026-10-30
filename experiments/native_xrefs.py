"""Read-only Thumb literal cross references for vendor diagnostic strings."""
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
from elftools.elf.elffile import ELFFile
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
import re, struct

root=Path(__file__).parent
with ZipFile(root/'CarCast-0.3.25.apk') as z:
    raw=z.read('lib/armeabi-v7a/libcarcast.so')
elf=ELFFile(BytesIO(raw))
targets={}
for value in ['OSStatus AudioStreamPrepare(AudioStreamRef)', 'OSStatus _AudioStreamOpen(AudioStreamRef)',
              'OSStatus _OpenOne(AudioStreamRef, Boolean, AAudioStream **)', 'audio: AAudio open failed',
              '### AAudio', 'OSStatus AudioStreamStart(AudioStreamRef)', 'Knob & Buttons',
              'audioInputFormats', 'audioOutputFormats', 'speechRecognition']:
    offset=raw.find(value.encode())
    if offset>=0:
        seg=next(s for s in elf.iter_segments() if s['p_type']=='PT_LOAD' and s['p_offset']<=offset<s['p_offset']+s['p_filesz'])
        targets[offset-seg['p_offset']+seg['p_vaddr']]=value
text=elf.get_section_by_name('.text')
data=text.data()
md=Cs(CS_ARCH_ARM,CS_MODE_THUMB)
md.skipdata=True
loads={}
for addr,size,mnemonic,ops in md.disasm_lite(data,text['sh_addr']):
    m=re.fullmatch(r'(\w+), \[pc, #(0x[0-9a-f]+|[0-9]+)\]',ops)
    if mnemonic.startswith('ldr') and m:
        literal=((addr+4)&~3)+int(m[2],0)
        seg=next((s for s in elf.iter_segments() if s['p_type']=='PT_LOAD' and s['p_vaddr']<=literal<s['p_vaddr']+s['p_filesz']),None)
        if seg:
            off=literal-seg['p_vaddr']+seg['p_offset']
            loads[m[1]]=(struct.unpack_from('<I',raw,off)[0],addr)
    m=re.fullmatch(r'(\w+), pc',ops)
    if mnemonic=='add' and m and m[1] in loads:
        value,previous=loads[m[1]]
        target=(value+addr+4)&0xffffffff
        if addr-previous<160 and target in targets:
            print(targets[target], 'xref',hex(addr),'literal_load',hex(previous))
