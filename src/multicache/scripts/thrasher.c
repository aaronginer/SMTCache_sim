#include <stdio.h>
#include <unistd.h>
#include <sys/mman.h>
#include <stdlib.h>
#include <pthread.h>
#include <assert.h>

#define PAGE 4096
#define LINE_SIZE 64
#define CACHE_SIZE 4096 * 8
#define MEM_SIZE 2*CACHE_SIZE

char array[MEM_SIZE] = {1};


int main(int argc, char* argv[])
{
    register char* addr asm ("r12") = array;

    register unsigned long idx asm ("r13") = 0;
    register unsigned long store_val asm ("r14") = 0;

    register unsigned long cnt asm ("r15") = 0;

    while(cnt++ < 100000000)
    // while (1)
    {
        idx += LINE_SIZE;
        idx %= MEM_SIZE;

        //addr[idx] = 1;
        store_val += addr[idx];
    }
    return 0;
}
