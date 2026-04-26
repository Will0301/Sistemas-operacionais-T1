#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>


long TOTAL = 1000000000;
long long counter = 0;
int N;
void *count_to_billion();


int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Uso: %s <N>\n", argv[0]);
        return 1;
    }

    N = atoi(argv[1]);

    pthread_t threads[N];

    for (int i = 0; i < N; i++) {
        pthread_create(&threads[i], NULL, count_to_billion, NULL);
    }

    for (int i = 0; i < N; i++) {
        pthread_join(threads[i], NULL);
    }

    printf("Contador final: %lld\n", counter);

    return 0;
}

void *count_to_billion() {
    const long long parte = TOTAL / N;

    for (long long i = 0; i < parte; i++) {
        counter++;
    }

    return NULL;
}