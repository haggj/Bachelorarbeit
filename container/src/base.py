import msparser
import gprof2dot
import subprocess
import pandas
import progressbar

import os

from statistics import mean

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class callgrindResult():
    def __init__(self, dic):
        self.privateKeyA = dic["PrivateKeyA"]
        self.privateKeyB = dic["PrivateKeyB"]
        self.publicKeyA = dic["PublicKeyA"]
        self.publicKeyB = dic["PublicKeyB"]
        self.SecretA = dic["SecretA"]
        self.SecretB = dic["SecretB"]
        self.raw = dic

def bash(command):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    stream = process.communicate()
    return_code = process.returncode
    if return_code != 0:
        print ("Error during command: " + command)
        raise Exception(stream)
    return

def mostExpensiveFunctions(callgrind, count):
    """Opens a callgrind.out file and finds the most expensive functions

    Args:
        callgrind (path): Path to callgrind function
        count (int): Number of functions to return

    Returns:
       list of the most expensive functions.
    """
    f = open(callgrind)
    parser = gprof2dot.CallgrindParser(f)
    profile = parser.parse()

    
    class function:
        def __init__(self, name, instructions, percentage):
            self.absolute_instructions = instructions
            self.name = name
            self.percentage = percentage

        def __str__(self):
            return self.name.split("/")[-1] + ": " + str(round(self.percentage*100,2)) + "%"
    
    functions = []
    for name, fun in profile.functions.items():
        percentage=None
        samples=None
        for event, value in fun.events.items():
            if event.name=="Time ratio":
                percentage=value
            elif event.name=="Samples":
                samples=value
        if percentage and samples:
            functions.append(function(name, samples, percentage))


    functions = sorted(functions, key=lambda func: func.percentage, reverse=True)
    return functions[:count]

def getCallgrindFunctionCalls(callgrind, function):
    """Opens a callgrind.out file and returns all functions called within the specified function.

    Args:
        callgrind (path): Path to callgrind file
        function (string): Name of a called function

    Returns:
       dict: dictionary that contains all called function with the specified function as keys (values are the measured opcounts)
    """
    f = open(callgrind)
    parser = gprof2dot.CallgrindParser(f)
    profile = parser.parse()

    ret = {}

    for call in profile.functions[function].calls.values():
        callee = profile.functions[call.callee_id]

        for event, data in call.events.items():
            if event.name == "Samples":
                ret[callee.name] = int(data)
    return ret

class BenchmarkImpl:
    def __init__(self, description):
        self.name = description
        self.curves = []

    def add_curve(self, curve):
        curve.impl = self
        self.curves.append(curve)
    
    def get_benchmark_names(self):
        if len(self.curves) == 0:
            return None
        return self.curves[0].get_benchmark_names()
    
    def get_benchmarks_of_curve(self, name):
        for curve in self.curves:
            if curve.name == name:
                return curve
        return None

    def __str__(self):
        return "%s\n\t%s" % (self.name, "\n".join([str(curve) for curve in self.curves]))

class BenchmarkCurve:
    def __init__(self, description):
        self.name = description
        self.benchmarks = []
        self.hotspots = None

    def add_benchmarks(self, append):
        if isinstance(append, list):
            self.benchmarks = self.benchmarks + append
        else:
            self.benchmarks.append(append)

    def set_hotspots(self, hotspots):
        self.hotspots = hotspots

    def get_hotspots(self):
        return self.hotspots

    def get_benchmark_names(self):
        return [benchmark.name for benchmark in self.benchmarks] + ["Hotspots"]
    
    def get_benchmark_values(self):
        return [benchmark.get_average() for benchmark in self.benchmarks] + [self.hotspots]
    
    def get_benchmarks_for_plot(self):

        benchmarks = []
        #KeyGenA
        val = self.find_benchmark("PublicKeyA",0)
        val += self.find_benchmark("PrivateKeyA",0)
        benchmarks.append(val if val != 0 else "no values")
        #KeyGenB
        val = self.find_benchmark("PublicKeyB",0)
        val += self.find_benchmark("PrivateKeyB",0)
        benchmarks.append(val if val != 0 else "no values")
        #SecretA
        val = self.find_benchmark("SecretA",0)
        benchmarks.append(val if val != 0 else "no values")
        #SecretB
        val = self.find_benchmark("SecretB",0)
        benchmarks.append(val if val != 0 else "no values")
        return benchmarks

    def find_benchmark(self, name, alternative):
        for benchmark in self.benchmarks:
            if benchmark.name == name:
                return benchmark.get_average()
        return alternative

    def __str__(self):
        seperator = "\n\t\t"
        return "p%s%s%s" % (self.name, seperator, seperator.join([str(benchmark) for benchmark in self.benchmarks]))

class Benchmarks:
    def __init__(self, description, values):
        self.name = description
        self.values = values
    def get_minimum(self):
        return min(self.values)
    def get_maximum(self):
        return max(self.values)
    def get_average(self):
        return round(mean(self.values))
    def __str__(self):
         return self.name + ": " + str(self.get_average())

class Base_Implementation():

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
        calls = getCallgrindFunctionCalls(self.path+"/benchmarks/callgrind.out", self.callgrind_main)
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
            benchmark = Benchmarks(description, values)
            benchmarks.append(benchmark)

        return benchmarks
    
    def hotspots(self):
        result = []
        for e in mostExpensiveFunctions(self.path+"/benchmarks/callgrind.out", 3):
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
        return Benchmarks("Memory", values)


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
