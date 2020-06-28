PARAM:=434

build:
	@ echo "building p$(PARAM)$(COMPRESSED)..."
	@ mkdir -p "build"
	@ mkdir -p "lib"
	@ cd go; go build -tags "p$(PARAM) amd64" -gcflags="all=-N -l" -o ../build/test
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
	rm -r build/ && rm -r benchmarks/ && rm -r lib/
