import msparser
import subprocess
import pandas
import progressbar
import statistics
import os

from src.utils.benchmarks import BenchmarkImpl, BenchmarkCurve, Benchmark
from src.utils.callgrind import extract_function_calls, extract_hotspots

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def bash(command):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    stream = process.communicate()
    return_code = process.returncode
    if return_code != 0:
        print ("Error during command: " + command)
        raise Exception(stream)
    return

class BaseImplementation():

    def __init__(self, count, path, args, callgrind_main, curves):
        self.path = path
        self.args = args
        self.curves = curves
        self.callgrind_main = callgrind_main
        self.count = count

    def map_functions(self, callgrind_result):
        res = {
            "PrivateKeyA": 0,
            "PublicKeyA": 0 ,
            "PrivateKeyB": 0,
            "PublicKeyB": 0,
            "SecretA": 0,
            "SecretB": 0
        }
        raise NotImplementedError("Mapping not implemented")

    def callgrind_result(self):
        calls = extract_function_calls(self.path+"/benchmarks/callgrind.out", self.callgrind_main)
        return self.map_functions(calls)

    def callgrind(self):
        results = []

        for _ in progressbar.progressbar(range(self.count), redirect_stdout=True, prefix="    Callgrind "):
            fails = 0
            while True:
                try:
                    bash('make callgrind -C {}'.format(self.path))
                    res = self.callgrind_result()
                    results.append(res)
                    break
                except Exception as e:
                    fails += 1
                    if fails == 10:            
                        print("Callgrind failed 10 times...")
                        break
        
        # Combine single benchmarks to a common result
        benchmarks = []
        for description in ["PrivateKeyA", "PublicKeyA",  "PrivateKeyB", "PublicKeyB", "SecretA", "SecretB"]:
            values = [res[description] for res in results]
            benchmark = Benchmark(description, values)
            benchmarks.append(benchmark)

        return benchmarks
    
    def hotspots(self):
        result = []
        for e in extract_hotspots(self.path+"/benchmarks/callgrind.out", 3):
                result.append(str(e))
        return "\n".join(result)

    def massif_result(self):
        data = msparser.parse_file(self.path+"/benchmarks/massif.out")
        peak =  data["peak_snapshot_index"]
        peak_data = data["snapshots"][peak]
        peak_mem = int(peak_data["mem_heap"]) + int(peak_data["mem_heap_extra"]) + int(peak_data ["mem_stack"])
        return peak_mem


    def massif(self):
        values = []
        for i in progressbar.progressbar(range(self.count), redirect_stdout=True, prefix="    Massif    "):
            bash('make massif -C {}'.format(self.path))
            res = self.massif_result()
            values.append(res)
        return Benchmark("Memory", values)


    def benchmark_curve(self, curve):
        #compile and generate benchmark outputs for specific curve
        args = "{} {} PARAM={}".format(self.path, self.args, curve)
        bash('make build -B -C {}'.format(args))

        benchmark_curve = BenchmarkCurve(curve)
        benchmark_curve.add_benchmarks(self.callgrind())
        benchmark_curve.add_benchmarks(self.massif())
        benchmark_curve.set_hotspots(self.hotspots())

        return benchmark_curve

    def get_statistics(self):
        #Generate statistics for all curves
        print("\n" + bcolors.WARNING + type(self).__name__ + bcolors.ENDC)

        benchmark = BenchmarkImpl(type(self).__name__)
        
        for curve in self.curves:
            print(bcolors.BOLD + "Handling curve "+curve+"..." + bcolors.ENDC)
            benchmark.add_curve(self.benchmark_curve(curve))

        return benchmark