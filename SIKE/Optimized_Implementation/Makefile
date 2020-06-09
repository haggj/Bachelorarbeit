ifeq ($(origin VARNAME),undefined)
PARAM:=434
endif

CC=gcc
PREPATH=/home/joy/Bachelorarbeit/SIDH_Implementations/SIKE/Optimized_Implementation/portable/SIKEp$(PARAM)$(COMPRESSED)/

CFLAGS=\
-I .. \
-I $(PREPATH)/P$(PARAM)/ \
-O3 -ggdb\
-D __LINUX__ \
-D _AMD64_  \
-D _GENERIC_ \

ifdef COMPRESSED
CFLAGS := $(CFLAGS) -D COMPRESSED
endif


OBJ = \
test.c \
$(PREPATH)/P$(PARAM)/P$(PARAM).c \
$(PREPATH)/P$(PARAM)/generic/fp_generic.c \
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
	@ valgrind --tool=callgrind --callgrind-out-file=benchmarks/callgrind.out build/test  2> /dev/null
	@ echo "\e[32mSUCCESS\e[0m"

massif:
	@ mkdir -p "benchmarks"
	@ echo "Running massif..."
	@ valgrind --tool=massif --stacks=yes --massif-out-file=benchmarks/massif.out build/test  2> /dev/null
	@ echo "\e[32mSUCCESS\e[0m"

clean_benchmarks:
	rm -r benchmarks/
	
clean:
	rm -r build/ && rm -r benchmarks/
