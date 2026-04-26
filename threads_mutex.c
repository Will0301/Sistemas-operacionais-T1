#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

long TOTAL = 1000000000;
long long counter = 0;
int N;
pthread_mutex_t lock;

void *count_to_billion();

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Uso: %s <N>\n", argv[0]);
        return 1;
    }

    N = atoi(argv[1]);
    pthread_mutex_init(&lock, NULL);
    pthread_t threads[N];

    for (int i = 0; i < N; i++) {
        pthread_create(&threads[i], NULL, count_to_billion, NULL);
    }

    for (int i = 0; i < N; i++) {
        pthread_join(threads[i], NULL);
    }

    pthread_mutex_destroy(&lock);
    printf("Contador final: %lld\n", counter);

    return 0;
}

void *count_to_billion() {
    const long long parte = TOTAL / N;

    for (long long i = 0; i < parte; i++) {
        pthread_mutex_lock(&lock);
        counter++;
        pthread_mutex_unlock(&lock);
    }

    return NULL;
}
