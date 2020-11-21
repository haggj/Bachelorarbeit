# Default Parameter
PARAM:=434

# Note: circl does not support gccgo -> need to use default compiler gc, which does not enable gcc optimazation flags

build:
	@ echo "building p$(PARAM)$(COMPRESSED)..."
	@ mkdir -p "build"
	@ mkdir -p "lib"
	@ echo $(VERSION)
	@ cd go; go build -tags "p$(PARAM) $(ARCH) $(ASM)" -gcflags="all=-l" -o ../build/benchmark
	@ echo "\e[32mSUCCESS\e[0m"


callgrind:
	@ mkdir -p "benchmarks"
	@ echo "Running callgrind..."
	@ sudo ../helper/drop-caches.sh
	@ valgrind --tool=callgrind --callgrind-out-file=benchmarks/callgrind.out build/benchmark  2> /dev/null
	@ echo "\e[32mSUCCESS\e[0m"

massif:
	@ mkdir -p "benchmarks"
	@ echo "Running massif..."
	@ sudo ../helper/drop-caches.sh
	@ valgrind --tool=massif --stacks=yes --massif-out-file=benchmarks/massif.out build/benchmark  2> /dev/null
	@ echo "\e[32mSUCCESS\e[0m"

clean_benchmarks:
	rm -r benchmarks/
	
clean:
	rm -r build/ && rm -r benchmarks/ && rm -r lib/
