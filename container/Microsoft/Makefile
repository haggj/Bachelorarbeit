PARAM:=434

CC=gcc
PREPATH=.src/src/P$(PARAM)

CFLAGS=\
-I ./ \
-I $(PREPATH)/ \
-O3 -ggdb


CFLAGS := $(CFLAGS) -D PARAM=${PARAM}
ifdef COMPRESSED
CFLAGS := $(CFLAGS) -D COMPRESSED -L.src/lib$(PARAM)comp/ -lsidh
else
CFLAGS := $(CFLAGS) -L.src/lib$(PARAM)/ -lsidh
endif




OBJ = \
test.c


build: $(OBJ)
	@ echo "building p$(PARAM)$(COMPRESSED)..."
	@ mkdir -p "build"
	$(CC) -o build/test $^ $(CFLAGS) $(LIBS)
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
