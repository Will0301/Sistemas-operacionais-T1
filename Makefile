all:
	gcc threads_no_mutex.c -o threads_no_mutex -pthread
	gcc threads_mutex.c -o threads_mutex -pthread
	gcc process_free.c -o processes_free
	gcc process_sem.c -o process_sem -pthread

runT1:
	./threads_no_mutex $(or $(N),4)

runT2:
	./threads_mutex $(or $(N),4)

runP1:
	./processes_free $(or $(N),4)

runP2:
	./process_sem $(or $(N),4)

clean:
	rm -f threads_no_mutex threads_mutex processes_free process_sem