#include <stdio.h>
#include <unistd.h>
#include <sys/mman.h>
#include <stdlib.h>
#include <assert.h>
#include <wait.h>
#include <sys/types.h>
#include <signal.h>

int main(int argc, char* argv[])
{
    int processes = 128;
    int timeout = 60;

    if (argc > 1)
    {   
        processes = atoi(argv[1]);
    }

    printf("Thrashing with %d processes for %d seconds\n", processes, timeout);
    
    pid_t pids[processes];

    for (int i = 0; i < processes; i++)
    {
        int pid = fork();

        if (!pid)
        {
            char* args[] = {0};
            execv("./thrasher", args);
        }
        else
        {
            pids[i] = pid;
        }
    }

    for (int i = 0; i < processes; i++)
    {
        waitpid(pids[i], 0x0, 0x0);
    }
}