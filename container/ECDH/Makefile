CC=gcc

CFLAGS= -ggdb3 -I/usr/local/ssl/include/ -Wl,-rpath,/usr/local/ssl/lib/ -L/usr/local/ssl/lib/ -lcrypto

OBJ = test.c

LD_LIBRARY_PATH=/usr/local/ssl/lib

build: $(OBJ)
	@ echo "building ECDH..."
	@ mkdir -p "build"
	@ $(CC) -o build/test $^ $(CFLAGS)
	@ echo "\e[32mSUCCESS\e[0m"

callgrind:
	@ mkdir -p "benchmarks"
	@ echo "Running callgrind..."
	# @ sudo ../drop-caches.sh
	@ valgrind --tool=callgrind --callgrind-out-file=benchmarks/callgrind.out build/test  2> /dev/null
	@ echo "\e[32mSUCCESS\e[0m"

massif:
	@ mkdir -p "benchmarks"
	@ echo "Running massif..."
	# @ sudo ../drop-caches.sh
	@ valgrind --tool=massif --stacks=yes --massif-out-file=benchmarks/massif.out build/test  2> /dev/null
	@ echo "\e[32mSUCCESS\e[0m"

clean_benchmarks:
	rm -r benchmarks/
	
clean:
	rm -r build/ && rm -r benchmarks/