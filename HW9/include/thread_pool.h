#ifndef THREAD_POOL_H
#define THREAD_POOL_H

#include <pthread.h>
#include <queue>
#include <vector>

class ThreadPool;

class Task {
public:
	Task(){};
	Task(void (*func)(void *), void* argument, ThreadPool* Tpool);
	~Task();

	void (*f)(void *);
	void *arg;

	ThreadPool* pool;
	bool finished;
	pthread_cond_t *cond;

	void wait();
};

class ThreadPool {
public:
	ThreadPool(unsigned int threads_numb);
	~ThreadPool();

	void submit(Task *task);

	pthread_mutex_t *m;
	pthread_cond_t *cond;
	pthread_cond_t *condend;
	bool stop;
	int started;

	std::queue<Task*> q;
private:
	std::vector<pthread_t> workers;
	unsigned int threads_nm;
};

#endif