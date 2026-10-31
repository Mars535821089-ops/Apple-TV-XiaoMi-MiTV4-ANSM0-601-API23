/* Exercise the exact pinned APK library in a separate process, synthetic bytes only. */
extern int printf(const char *,...);
extern void *dlopen(const char *,int);
extern void *dlsym(void *,const char *);
extern char *dlerror(void);
extern int dlclose(void *);
int main(int argc,char **argv,char **env){
 (void)env;
 if(argc!=2){printf("FAIL expected staged library path\n");return 1;}
 void *library=dlopen(argv[1],2);
 if(!library){printf("FAIL loading pinned library: %s\n",dlerror());return 2;}
 void *symbol=dlsym(library,"JNI_OnLoad");
 if(!symbol){printf("FAIL missing pinned anchor\n");return 3;}
 unsigned base=(unsigned)symbol-0x1327d1U;
 int (*initialize)(volatile unsigned *,unsigned,int)=(void *)(base+0x174db9U);
 void (*destroy)(volatile unsigned *)=(void *)(base+0x174eb1U);
 for(int mode=0;mode<2;mode++){
  volatile unsigned ctx[6]={0,0,0,0,0,0};
  int result=initialize(ctx,10000,mode);
  if(result){printf("FAIL actual APK initializer returned %d\n",result);return 4;}
  unsigned size=mode?16384:12288;
  if(ctx[2]!=size||ctx[1]!=ctx[0]+size||ctx[3]!=size-1){printf("FAIL actual APK ring layout\n");return 5;}
  volatile unsigned char *p=(void *)ctx[0];
  for(unsigned i=0;i<8;i++)p[size-4+i]=(unsigned char)(i+91);
  for(unsigned i=0;i<4;i++)if(p[i]!=(unsigned char)(i+95)){printf("FAIL actual APK wrap alias\n");return 6;}
  destroy(ctx);
  for(unsigned i=0;i<6;i++)if(ctx[i]){printf("FAIL original APK destructor did not clear ring\n");return 7;}
 }
 dlclose(library);
 printf("PASS: actual patched APK initializer, double mapping, wrap alias and original destructor; no phone or audio input\n");
 return 0;
}
