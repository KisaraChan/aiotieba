#if defined(__GNUC__) || defined(__clang__)
#define TBC_NOESCAPE __attribute__((noescape))
#define TBC_UNUSED __attribute__((unused))
#else
#define TBC_NOESCAPE
#define TBC_UNUSED __pragma(warning(suppress:4100))
#endif
