/* Synthetic shared-memory compatibility probe. No audio, network or user data. */
typedef unsigned int size_t;
extern int printf(const char *, ...);
extern int syscall(int, ...);
extern int *__errno(void);
extern int close(int);
extern int ashmem_create_region(const char *, size_t);
extern void *mmap(void *, size_t, int, int, int, long);
extern int munmap(void *, size_t);
struct constructors { void (**pre)(void); void (**init)(void); void (**fini)(void); };
extern void __libc_init(void *, void (*)(void), int (*)(int,char **,char **), const struct constructors *) __attribute__((noreturn));

int main(int argc, char **argv, char **env) {
    (void)argc;(void)argv;(void)env;
    int original=syscall(385,"CnKernelProbe",0);
    int error=original<0?*__errno():0;
    printf("memfd_create fd=%d errno=%d\n",original,error);
    if(original>=0)close(original);
    const size_t size=12288;
    int fd=ashmem_create_region("CnMirrorProbe",size);
    if(fd<0){printf("FAIL ashmem create errno=%d\n",*__errno());return 1;}
    void *base=mmap((void *)0,size*2,0,0x22,-1,0);
    if(base==(void *)-1){close(fd);printf("FAIL reserve errno=%d\n",*__errno());return 2;}
    void *first=mmap(base,size,3,0x11,fd,0);
    void *second=first==base?mmap((char *)base+size,size,3,0x11,fd,0):(void *)-1;
    close(fd);
    if(first!=base || second!=(char *)base+size){munmap(base,size*2);printf("FAIL shared mappings\n");return 3;}
    volatile unsigned char *bytes=(volatile unsigned char *)base;
    for(size_t i=0;i<64;i++)bytes[i]=(unsigned char)(i+19);
    for(size_t i=0;i<64;i++)if(bytes[size+i]!=(unsigned char)(i+19)){munmap(base,size*2);printf("FAIL alias\n");return 4;}
    for(size_t i=0;i<8;i++)bytes[size-4+i]=(unsigned char)(i+91);
    for(size_t i=0;i<4;i++)if(bytes[i]!=(unsigned char)(i+95)){munmap(base,size*2);printf("FAIL boundary wrap\n");return 5;}
    if(munmap(base,size*2)){printf("FAIL unmap errno=%d\n",*__errno());return 6;}
    printf("PASS ashmem double mapping, alias, boundary wrap and cleanup; no media recorded\n");
    return 0;
}
void cn_start(void *raw) {
    static const struct constructors empty={0,0,0};
    __libc_init(raw,(void (*)(void))0,main,&empty);
}
__asm__(".text\n.thumb\n.global _start\n.type _start,%function\n.thumb_func\n_start:\nmov r0,sp\nb cn_start\n");
