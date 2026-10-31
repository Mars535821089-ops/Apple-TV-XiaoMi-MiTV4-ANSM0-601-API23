/* Own adapter ABI for the legacy kernel's mirrored ring backing. */
typedef unsigned int cn_size;
struct cn_mirror_ops {
 void *(*open_library)(const char *, int);
 void *(*symbol)(void *, const char *);
 int (*close_library)(void *);
 void *(*map)(void *,cn_size,int,int,int,long);
 int (*unmap)(void *,cn_size);
 int (*close_fd)(int);
 int *(*error)(void);
 long (*configuration)(int);
 int (*log)(int,const char *,const char *,...);
};
int cn_mirror_fallback(volatile unsigned int *,cn_size,int,const struct cn_mirror_ops *);
