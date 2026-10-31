#include "mirror_compat.h"

static int failure(const struct cn_mirror_ops *ops){int value=*ops->error();return value>0?value:12;}

/* No media is persisted: the fd is anonymous ashmem, held only by its VMAs. */
int cn_mirror_fallback(volatile unsigned int *ctx,cn_size requested,int power_of_two,const struct cn_mirror_ops *ops) {
 long page=ops->configuration(40);
 if(page<=0 || ((unsigned)page&((unsigned)page-1)) || !requested || requested>0x7fffffffU-(unsigned)page)return 22;
 unsigned size=(requested+(unsigned)page-1)&~((unsigned)page-1);
 if(power_of_two){unsigned next=1;while(next<size && next<0x80000000U)next<<=1;size=next;}
 if(!size || size>0x7fffffffU)return 12;
 void *library=ops->open_library("/system/lib/libcutils.so",2);
 if(!library)return 38;
 int (*create)(const char *,unsigned)=(int (*)(const char *,unsigned))ops->symbol(library,"ashmem_create_region");
 int result=38,fd=-1,reserved=0;void *base=(void *)0;
 if(!create)goto finished;
 fd=create("CnCarPlayRing",size);
 if(fd<0){result=failure(ops);goto finished;}
 base=ops->map((void *)0,size*2,0,0x22,-1,0);
 if(base==(void *)-1){result=failure(ops);goto finished;}
 reserved=1;
 if(ops->map(base,size,3,0x11,fd,0)!=base){result=failure(ops);goto finished;}
 if(ops->map((char *)base+size,size,3,0x11,fd,0)!=(char *)base+size){result=failure(ops);goto finished;}
 ctx[0]=(unsigned)base;ctx[1]=(unsigned)base+size;ctx[2]=size;ctx[3]=size-1;ctx[4]=0;ctx[5]=0;
 result=0;
finished:
 if(result && reserved)ops->unmap(base,size*2);
 if(fd>=0)ops->close_fd(fd);
 ops->close_library(library);
 if(ops->log)ops->log(4,"CnMirror","ashmem fallback status=%d size=%u",result,size);
 return result;
}
