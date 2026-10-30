"""Read-only Thumb literal cross references for vendor diagnostic strings."""
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
from elftools.elf.elffile import ELFFile
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
import re, struct, argparse

root=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--apk',type=Path,default=root/'build/work/CarCast-0.3.25.apk')
parser.add_argument('--strings',nargs='+')
parser.add_argument('--disassemble',nargs=2,type=lambda s:int(s,0),metavar=('START','END'))
args=parser.parse_args()
with ZipFile(args.apk) as z:
    raw=z.read('lib/armeabi-v7a/libcarcast.so')
elf=ELFFile(BytesIO(raw))
targets={}
if args.disassemble:
    start,end=args.disassemble
    assert 0<=start<end and end-start<=4096
    segment=next(s for s in elf.iter_segments() if s['p_type']=='PT_LOAD' and s['p_vaddr']<=start<end<=s['p_vaddr']+s['p_filesz'])
    offset=start-segment['p_vaddr']+segment['p_offset']
    decoder=Cs(CS_ARCH_ARM,CS_MODE_THUMB);decoder.skipdata=True
    for instruction in decoder.disasm(raw[offset:offset+end-start],start):
        print(hex(instruction.address),instruction.mnemonic,instruction.op_str)
    raise SystemExit(0)
for value in args.strings or ['OSStatus AudioStreamPrepare(AudioStreamRef)', 'OSStatus _AudioStreamOpen(AudioStreamRef)',
              'OSStatus _OpenOne(AudioStreamRef, Boolean, AAudioStream **)', 'audio: AAudio open failed',
              '### AAudio', 'OSStatus AudioStreamStart(AudioStreamRef)', 'Knob & Buttons',
              'audioInputFormats', 'audioOutputFormats', 'speechRecognition']:
    for match in re.finditer(re.escape(value.encode())+b'\0',raw):
        offset=match.start()
        seg=next(s for s in elf.iter_segments() if s['p_type']=='PT_LOAD' and s['p_offset']<=offset<s['p_offset']+s['p_filesz'])
        address=offset-seg['p_offset']+seg['p_vaddr']
        targets[address]=value
        if offset>=8 and raw[offset-8:offset]==bytes.fromhex('56070100ffffff7f'):
            targets[address-8]=value+' [CFLString]'
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
