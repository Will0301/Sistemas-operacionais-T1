all:
	gcc threads_no_mutex.c -o threads_no_mutex -pthread
	gcc threads_mutex.c -o threads_mutex -pthread

runT1:
	./threads_no_mutex $(N)

runT2:
	./threads_mutex $(N)

clean:
	rm -f threads_no_mutex
	rm -f threads_mutex