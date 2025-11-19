#include "sched.h"

/// this test is supposed to evaluate whether the l1d cache is actually cleared on each schedule/context switch. A miss rate of close to 100% is desired

char arr[64*512] = {5};

int main()
{
    register unsigned long cnt asm ("r12") = 0;
    register unsigned long idx asm ("r13") = 0;
    register unsigned long res asm ("r14") = 0;

    while(1)
    {
        res += arr[idx];
        idx+=64;
        idx%=(64*4);
        if (++cnt == 4)
        {
            cnt = 0;
            sched_yield();
        }
    }
}