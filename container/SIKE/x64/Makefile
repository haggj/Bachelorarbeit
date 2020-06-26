ifeq ($(origin VARNAME),undefined)
PARAM:=434
endif

CC=gcc
PREPATH=../.src/SIKE/x64/SIKEp$(PARAM)$(COMPRESSED)

CFLAGS=\
-I .. \
-I $(PREPATH)/P$(PARAM)/ \
-O3 \
-ggdb\
-D __LINUX__ \
-D _AMD64_  \
-D _FAST_ \
-D _MULX_ \
-D _ADX_

ifdef COMPRESSED
CFLAGS := $(CFLAGS) -D COMPRESSED
endif


OBJ = \
test.c \
$(PREPATH)/P$(PARAM)/P$(PARAM).c \
$(PREPATH)/P$(PARAM)/AMD64/fp_x64.c \
$(PREPATH)/P$(PARAM)/AMD64/fp_x64_asm.S \
$(PREPATH)/random/random.c \
$(PREPATH)/sha3/fips202.c 


LIBS=-lm

build: $(OBJ)
	@ echo "building p$(PARAM)$(COMPRESSED)..."
	@ mkdir -p "build"
	@ $(CC) -o build/test $^ $(CFLAGS) $(LIBS)
	@ echo "\e[32mSUCCESS\e[0m"

callgrind:
	@ mkdir -p "benchmarks"
	@ echo "Running callgrind..."
	# @ sudo ../../drop-caches.sh
	@ valgrind --tool=callgrind --callgrind-out-file=benchmarks/callgrind.out build/test  2> /dev/null
	@ echo "\e[32mSUCCESS\e[0m"

massif:
	@ mkdir -p "benchmarks"
	@ echo "Running massif..."
	# @ sudo ../../drop-caches.sh
	@ valgrind --tool=massif --stacks=yes --massif-out-file=benchmarks/massif.out build/test  2> /dev/null
	@ echo "\e[32mSUCCESS\e[0m"

clean_benchmarks:
	rm -r benchmarks/
	
clean:
	rm -r build/ && rm -r benchmarks/
