CXX=g++
CXXFLAGS= -std=c++11 -Wall -pedantic -Werror -Wextra -Wshadow -pthread -O2

all: pqsort

bin:
	mkdir -p bin

pqsort: src/pqsort.cpp bin/thread_pool.o include/*.h bin
	$(CXX) $(CXXFLAGS) -o $@ -Iinclude $< bin/*

bin/%.o: src/%.cpp include/*.h bin
	$(CXX) $(CXXFLAGS) -c -o $@ -Iinclude $<

clean:
	rm -rf bin pqsort