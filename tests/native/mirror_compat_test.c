#include "mirror_compat.h"
extern int printf(const char *,...);
extern void *dlopen(const char *,int);
extern void *dlsym(void *,const char *);
extern int dlclose(void *);
extern void *mmap(void *,unsigned,int,int,int,long);
extern int munmap(void *,unsigned);
extern int close(int);
extern int *__errno(void);
extern long sysconf(int);
static int map_calls,fail_map,closes,unmaps;
static void *tracked_map(void *p,unsigned n,int prot,int flags,int fd,long off){
 if(++map_calls==fail_map){*__errno()=12;return (void *)-1;}
 return mmap(p,n,prot,flags,fd,off);
}
static int tracked_close(int fd){closes++;return close(fd);}
static int tracked_unmap(void *p,unsigned n){unmaps++;return munmap(p,n);}
int main(int argc,char **argv,char **env){
 (void)argc;(void)argv;(void)env;
 struct cn_mirror_ops ops={dlopen,dlsym,dlclose,tracked_map,tracked_unmap,tracked_close,__errno,sysconf,0};
 for(int mode=0;mode<2;mode++){
  volatile unsigned ctx[6]={91,92,93,94,95,96};map_calls=closes=unmaps=0;fail_map=0;
  int result=cn_mirror_fallback(ctx,10000,mode,&ops);
  if(result){printf("FAIL shared-memory fallback status=%d\n",result);return 1;}
  unsigned want=mode?16384:12288;
  if(ctx[2]!=want||ctx[1]!=ctx[0]+want||ctx[3]!=want-1||ctx[4]||ctx[5]||closes!=1){printf("FAIL ring layout or fd lifetime\n");return 2;}
  volatile unsigned char *p=(volatile unsigned char *)ctx[0];
  for(unsigned i=0;i<8;i++)p[want-4+i]=(unsigned char)(i+71);
  for(unsigned i=0;i<4;i++)if(p[i]!=(unsigned char)(i+75)){printf("FAIL alias wrap\n");return 3;}
  if(munmap((void *)ctx[0],want*2)){printf("FAIL cleanup\n");return 4;}
 }
 for(int failure=1;failure<=3;failure++){
  volatile unsigned ctx[6]={91,92,93,94,95,96};map_calls=closes=unmaps=0;fail_map=failure;
  int result=cn_mirror_fallback(ctx,10000,0,&ops);
  if(result!=12||closes!=1||unmaps!=(failure>1)){printf("FAIL mapping failure cleanup %d status%d close%d unmap%d\n",failure,result,closes,unmaps);return 5;}
  for(unsigned i=0;i<6;i++)if(ctx[i]!=91+i){printf("FAIL failed allocation changed ctx\n");return 6;}
 }
 printf("PASS: real ashmem fallback alignment, power-of-two, alias, fd lifetime and failed-map cleanup\n");return 0;
}
