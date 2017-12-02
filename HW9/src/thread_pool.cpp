#include "thread_pool.h"
#include<cstdio>

void Task::wait(){
	pthread_mutex_lock(pool->m);
	while (!finished) {
		pthread_cond_wait(cond, pool->m);
	}
	pthread_mutex_unlock(pool->m);
}

Task::Task(void (*func)(void *), void *argument, ThreadPool *Tpool) : 
			f(func), arg(argument), pool(Tpool), finished(false), cond(new pthread_cond_t) {
	pthread_cond_init(cond, NULL);
}

void ThreadPool::started_locked_decr(){
	started--;
	if(!started)
		pthread_cond_signal(condend);
}

Task::~Task(){
	pthread_mutex_lock(pool->m);
	finished = true;
	pool->started_locked_decr();
	pthread_cond_signal(cond);
	pthread_mutex_unlock(pool->m);

	pthread_cond_destroy(cond);
	delete cond;
}

void *get_task(void* arg){
	ThreadPool *pool = (ThreadPool *)arg;

	while (true) {
		pthread_mutex_lock(pool->m);
		if(pool->stop){
			pthread_mutex_unlock(pool->m);
			break;
		}

		while (pool->q.empty() && !pool->stop) {
			pthread_cond_wait(pool->cond, pool->m);
		}

		Task *task = NULL;

		if(!pool->q.empty()){
			task = pool->q.front();
			pool->q.pop();
		}

		pthread_mutex_unlock(pool->m);

		if(task)
			task->f(task);

	}
	return NULL;
}

ThreadPool::ThreadPool(unsigned int threads_numb) : 
		m(new pthread_mutex_t), cond(new pthread_cond_t), stop(false), threads_nm(threads_numb), started(0), condend(new pthread_cond_t) {

	pthread_mutex_init(m, NULL);
	pthread_cond_init(cond, NULL);
	pthread_cond_init(condend, NULL);

	pthread_mutex_lock(m);
	workers.resize(threads_nm);
	for(unsigned int i = 0; i < threads_nm; i++){
		pthread_create(&workers[i], NULL, get_task, (void *)this);
	}
	pthread_mutex_unlock(m);
}

void ThreadPool::finit(){
	pthread_mutex_lock(m);
	while(started){
		pthread_cond_wait(condend, m);
	}
	pthread_mutex_unlock(m);
}

ThreadPool::~ThreadPool(){

	pthread_mutex_lock(m);
	stop = true;
	pthread_cond_broadcast(cond);
	pthread_mutex_unlock(m);

	for(unsigned int i = 0; i < threads_nm; i++)
		pthread_join(workers[i], NULL);
	workers.clear();

	pthread_mutex_destroy(m);
	pthread_cond_destroy(cond);
	pthread_cond_destroy(condend);
	delete m;
	delete cond;
	delete condend;
}

void ThreadPool::submit(Task *task){
	pthread_mutex_lock(task->pool->m);
	q.push(task);
	task->pool->started++;
	pthread_cond_signal(cond);
	pthread_mutex_unlock(task->pool->m);
}