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
	void wait();
	void *arg;
	ThreadPool* pool;
	bool finished;
private:
	pthread_cond_t *cond;

};

class ThreadPool {
public:
	ThreadPool(unsigned int threads_numb);
	~ThreadPool();

	void submit(Task *task);
	void finit();
	void started_locked_decr();

	pthread_mutex_t *m;
	pthread_cond_t *cond;
	bool stop;

	std::queue<Task*> q;
private:
	std::vector<pthread_t> workers;
	unsigned int threads_nm;
	int started;
	pthread_cond_t *condend;
};

#endif