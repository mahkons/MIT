#include<cstdio>
#include<cstdlib>
#include<cstddef>
#include<cassert>
#include<algorithm>
#include<unistd.h>
#include<ctime>
#include<string.h>
#include"thread_pool.h"

int *make_array_of_random(int sz){
	srand(42);
	int *arr = new int [sz];
	for(int i = 0; i < sz; i++)
		arr[i] = rand();
	return arr;
}

bool check(int *arr, int sz){
	for(int i = 0; i + 1 < sz; i++)
		if(arr[i] > arr[i + 1])
			return 0;
	return 1;
}

void print_array(int *arr, int sz){
	printf("%d\n", sz);
	for(int i = 0; i < sz; i++)
		printf("%d ", arr[i]);
	printf("\n");
}

void delete_array(int *arr){
	delete [] arr;
}

struct qsort_args{
	int* arr;
	int sz;
	int depth;
};

void finish_task(Task *task){
	delete (qsort_args*)(task->arg);
	delete task;
}

void thread_qsort(void* get_arg){

	Task *task = (Task *)get_arg;
	qsort_args *args = (qsort_args *)(task->arg);

	if(args->sz <= 1){
		finish_task(task);
		return;
	}

	if(!args->depth){
		std::sort(args->arr, args->arr + args->sz);
		finish_task(task);
		return;
	}
	
	int pivot = args->arr[rand() % args->sz];
	int* bound_l = (int *)std::partition(args->arr, args->arr + args->sz, [pivot](const int x){ return x < pivot; });
	int* bound_r = (int *)std::partition(bound_l, args->arr + args->sz, [pivot](const int x){ return x <= pivot; });

	qsort_args *arg1 = new qsort_args({args->arr, int(bound_l - args->arr), args->depth - 1});
	Task *task1 = new Task(thread_qsort, (void*)arg1, task->pool);
	task->pool->submit(task1);

	qsort_args *arg2 = new qsort_args({bound_r, int(args->arr - bound_r) + args->sz, args->depth - 1});
	Task *task2 = new Task(thread_qsort, (void*)arg2, task->pool);
	task->pool->submit(task2);

	finish_task(task);

	return;
}

int main(int argc, char **argv){
	assert(argc == 4 && "Wrong number of arguments");

	clock_t t_st = clock();
	
	int sz = atoi(argv[2]);
	int *rand_arr = make_array_of_random(sz);

	int threads_nm = atoi(argv[1]);
	ThreadPool* pool = new ThreadPool(threads_nm);

	int depth = atoi(argv[3]);

	qsort_args *args = new qsort_args({rand_arr, sz, depth});
	Task *task = new Task(thread_qsort, (void*)args, pool);

	pool->submit(task);

	delete pool;

	if(check(rand_arr, sz))
		printf("OK\n");
	else{
		printf("WRONG\n");
		if(sz <= 30)
			print_array(rand_arr, sz);
	}

	printf("%lf\n", double(clock() - t_st) / CLOCKS_PER_SEC);


	delete_array(rand_arr);
	return 0;
}
