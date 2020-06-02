ifeq ($(origin VARNAME),undefined)
PARAM:=434
endif


CC=gcc
PREPATH=/home/joy/Bachelorarbeit/SIDH_Implementations/SIKE/Reference_Implementation/
CFLAGS=\
-I .. \
-I . \
-I $(PREPATH)/include/ \
-I $(PREPATH)/test/ \
-I $(PREPATH)/symmetric/ \
-ggdb -DPARAM$(PARAM)
# -DTARGET_OS=1 \
# -DTARGET=4 \

OBJ = \
test.c \
../countcpu.c \
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
	@ $(CC) -o build/test $^ $(CFLAGS) $(LIBS)
	@ echo "\e[32mSUCCESS\e[0m"


callgrind:
	@ mkdir -p "benchmarks"
	@ echo "Running callgrind..."
	@ valgrind --tool=callgrind --callgrind-out-file=benchmarks/callgrind.out build/test  2> /dev/null
	@ callgrind_annotate benchmarks/callgrind.out  --tree=calling --threshold=100 > benchmarks/callgrind_annotate.out 2> /dev/null
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
