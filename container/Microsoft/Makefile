# Default compiler
CC=gcc

# Default parameter
PARAM:=434

# Include files
PREPATH=.src/$(VERSION)src/P$(PARAM)
CFLAGS=\
-I ./ \
-I $(PREPATH)/ \
-O3

CFLAGS := $(CFLAGS) -D p${PARAM}

ifdef COMPRESSED
	CFLAGS := $(CFLAGS) -D COMPRESSED -L.src/$(VERSION)lib$(PARAM)comp/ -lsidh
else
	CFLAGS := $(CFLAGS) -L.src/$(VERSION)lib$(PARAM)/ -lsidh
endif

OBJ = benchmark.c

build: $(OBJ)
	@ echo "building p$(PARAM)$(COMPRESSED)..."
	@ mkdir -p "build"
	$(CC) -o build/benchmark $^ $(CFLAGS) $(LIBS)
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