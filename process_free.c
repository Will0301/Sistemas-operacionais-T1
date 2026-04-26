#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/ipc.h>
#include <sys/shm.h>

long TOTAL = 1000000000;

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Uso: %s <N>\n", argv[0]);
        return 1;
    }

    int N = atoi(argv[1]);

    int memory = shmget(IPC_PRIVATE, sizeof(long long), IPC_CREAT | 0666);
    long long *counter = shmat(memory, NULL, 0);

    *counter = 0;

    long long distribution = TOTAL / N;

    for (int i = 0; i < N; i++) {
        pid_t pid = fork();

        if (pid == 0) {
            for (long long j = 0; j < distribution; j++) {
                (*counter)++;
            }
            exit(0);
        }
    }

    for (int i = 0; i < N; i++) {
        wait(NULL);
    }

    printf("Contador final: %lld\n", *counter);

    shmdt(counter);
    shmctl(memory, IPC_RMID, NULL);

    return 0;
}
