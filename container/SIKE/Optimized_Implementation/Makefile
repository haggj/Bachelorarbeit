# Default compiler
CC=gcc

# Default parameter
PARAM:=434

# Path to prebuild libs
PREPATH=../.src/Optimized_Implementation/portable/SIKEp$(PARAM)$(COMPRESSED)/

CFLAGS=\
-I .. \
-I $(PREPATH)/P$(PARAM)/ \
-O3 \
-D __NIX__ \
-D _AMD64_  \
-D _GENERIC_ \

ifdef COMPRESSED
	CFLAGS := $(CFLAGS) -D COMPRESSED
endif


OBJ = \
benchmark.c \
$(PREPATH)/P$(PARAM)/P$(PARAM)$(COMPRESSED).c \
$(PREPATH)/P$(PARAM)/generic/fp_generic.c \
$(PREPATH)/random/random.c \
$(PREPATH)/sha3/fips202.c 


LIBS=-lm

build: $(OBJ)
	@ echo "building p$(PARAM)$(COMPRESSED)..."
	@ mkdir -p "build"
	@ $(CC) -o build/benchmark $^ $(CFLAGS) $(LIBS) -Wno-implicit
	@ echo "\e[32mSUCCESS\e[0m"

callgrind:
	@ mkdir -p "benchmarks"
	@ echo "Running callgrind..."
	@ sudo ../../helper/drop-caches.sh
	@ valgrind --tool=callgrind --callgrind-out-file=benchmarks/callgrind.out build/benchmark  2> /dev/null
	@ echo "\e[32mSUCCESS\e[0m"

massif:
	@ mkdir -p "benchmarks"
	@ echo "Running massif..."
	@ sudo ../../helper/drop-caches.sh
	@ valgrind --tool=massif --stacks=yes --massif-out-file=benchmarks/massif.out build/benchmark  2> /dev/null
	@ echo "\e[32mSUCCESS\e[0m"

clean_benchmarks:
	rm -r benchmarks/
	
clean:
	rm -r build/ && rm -r benchmarks/
