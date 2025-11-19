#include "stdio.h"
#include "sys/mman.h"
#include "assert.h"
#include "sched.h"

#define WAYS 8
#define CACHE_SIZE (32 * 1024)
#define MEM (2 * CACHE_SIZE)
#ifndef USE_SETS
    #define USE_SETS 8
#endif
#define TEST_RUNS 500000

#define INDEX(a) ((a >> 6) & 0x3f)

int main()
{
    unsigned long total = 0;
    // __uint32_t lower, upper;

    char* memory = mmap(0, MEM, PROT_READ|PROT_WRITE, MAP_ANONYMOUS|MAP_PRIVATE, -1, 0);
    int flip = 0;

    register unsigned long lower asm ("r12") = 0;
    register unsigned long upper asm ("r13") = 0;
    long tsc_after = 0;
    long tsc_before = 0;
    unsigned long set_index = 0;
    unsigned long way_index = 0;
    unsigned char* base_addr = 0;
    unsigned long base_offset = 0;

    for (int t = 0; t < TEST_RUNS; t++)
    {
        flip = (flip == 0) ? 1 : 0;

        base_addr = memory + flip * CACHE_SIZE;

        for (set_index = 0; set_index < USE_SETS; set_index++)
        {
            for (way_index = 0; way_index < WAYS; way_index++)
            {
                base_offset = way_index * 4096 + set_index * 64;
                *(base_addr + base_offset) = 1;
            }
        }

        asm volatile("rdtsc"
            : "=a" (lower), "=d" (upper));
        tsc_before = ((__int64_t) upper << 32) | lower;

        sched_yield();

        asm volatile("rdtsc"
            : "=a" (lower), "=d" (upper));
        tsc_after = ((__int64_t) upper << 32) | lower;

        total += tsc_after - tsc_before;
    }

    printf("%f\n", (float) total / TEST_RUNS);

    return 0;
}
