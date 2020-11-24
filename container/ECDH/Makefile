# Default compiler
CC=gcc

# Include Files
CFLAGS= -ggdb -O3 -I/usr/local/ssl/include/ -Wl,-rpath,/usr/local/ssl/lib/ -L/usr/local/ssl/lib/ -lcrypto -D ${PARAM}
LD_LIBRARY_PATH=/usr/local/ssl/lib

OBJ = benchmark.c

build: $(OBJ)
	@ echo "building ECDH..."
	@ echo ${PARAM}
	@ mkdir -p "build"
	@ $(CC) -o build/benchmark $^ $(CFLAGS)
	@ echo "\e[32mSUCCESS\e[0m"

callgrind:
	@ mkdir -p "benchmarks"
	@ echo "Running callgrind..."
	@ valgrind --tool=callgrind --callgrind-out-file=benchmarks/callgrind.out build/benchmark  2> /dev/null
	@ echo "\e[32mSUCCESS\e[0m"

massif:
	@ mkdir -p "benchmarks"
	@ echo "Running massif..."
	@ valgrind --tool=massif --stacks=yes --massif-out-file=benchmarks/massif.out build/benchmark  2> /dev/null
	@ echo "\e[32mSUCCESS\e[0m"

clean_benchmarks:
	rm -r benchmarks/
	
clean:
	rm -r build/ && rm -r benchmarks/