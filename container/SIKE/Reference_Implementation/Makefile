# Default compiler
CC=gcc

# Default parameter
PARAM:=434

# Path to prebuild libs
PREPATH=../.src/Reference_Implementation/
CFLAGS=\
-I .. \
-I . \
-I $(PREPATH)/include/ \
-I $(PREPATH)/test/ \
-I $(PREPATH)/symmetric/ \
-O3 -DPARAM$(PARAM)

OBJ = \
benchmark.c \
$(PREPATH)/test/test_sike.c \
$(PREPATH)symmetric/rng.c\
$(PREPATH)symmetric/aes_c.c\
$(PREPATH)symmetric/fips202.c\
$(PREPATH)test/printing.c \
$(PREPATH)test/test_extras.c \
$(PREPATH)src/*.c

LIBS=-lgmp

build: $(OBJ)
	@ echo "building reference implementation..."
	@ mkdir -p "build"
	@ $(CC) -o build/benchmark $^ $(CFLAGS) $(LIBS)
	@ echo "\e[32mSUCCESS\e[0m"


callgrind:
	@ mkdir -p "benchmarks"
	@ echo "Running callgrind..."
	@ sudo ../../drop-caches.sh
	@ valgrind --tool=callgrind --callgrind-out-file=benchmarks/callgrind.out build/benchmark  2> /dev/null
	@ echo "\e[32mSUCCESS\e[0m"

massif:
	@ mkdir -p "benchmarks"
	@ echo "Running massif..."
	@ sudo ../../drop-caches.sh
	@ valgrind --tool=massif --stacks=yes --massif-out-file=benchmarks/massif.out build/benchmark  2> /dev/null
	@ echo "\e[32mSUCCESS\e[0m"

clean_benchmarks:
	rm -r benchmarks/
	
clean:
	rm -r build/ && rm -r benchmarks/
