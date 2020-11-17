# Default compiler
CC=gcc

# Default parameter
PARAM:=434

# Path to prebuild libs
PREPATH=../.src/x64/SIKEp$(PARAM)$(COMPRESSED)

CFLAGS=\
-I .. \
-I $(PREPATH)/P$(PARAM)/ \
-O3 \
-D __NIX__ \
-D _AMD64_  \
-D _FAST_ \
-D _MULX_ \
-D _ADX_

ifdef COMPRESSED
CFLAGS := $(CFLAGS) -D COMPRESSED
endif


OBJ = \
benchmark.c \
$(PREPATH)/P$(PARAM)/P$(PARAM)$(COMPRESSED).c \
$(PREPATH)/P$(PARAM)/AMD64/fp_x64.c \
$(PREPATH)/P$(PARAM)/AMD64/fp_x64_asm.S \
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
