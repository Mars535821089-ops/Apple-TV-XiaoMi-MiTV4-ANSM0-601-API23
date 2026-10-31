struct constructors {void (**pre)(void);void (**init)(void);void (**fini)(void);};
extern int main(int,char **,char **);
extern void __libc_init(void *,void (*)(void),int (*)(int,char **,char **),const struct constructors *) __attribute__((noreturn));
void cn_start(void *raw){static const struct constructors none={0,0,0};__libc_init(raw,0,main,&none);}
__asm__(".text\n.thumb\n.global _start\n.type _start,%function\n.thumb_func\n_start:\nmov r0,sp\nb cn_start\n");
