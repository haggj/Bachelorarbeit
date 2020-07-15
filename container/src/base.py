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
            return str(round(self.percentage*100,2)) + "% -- " + self.name
    
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

class Base_Implementation():

    def __init__(self):
        self.path = ""

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
        calls = getCallgrindFunctionCalls(self.path+"/benchmarks/callgrind.out", "benchmark_keygen")
        return self.map_functions(calls)

    def callgrind_average(self, count):
        results = []
        
        for i in progressbar.progressbar(range(count), redirect_stdout=True, prefix="    Callgrind "):
            bash('make callgrind -C {}'.format(self.path))
            res = self.callgrind_result()
            results.append(res)

        df = pandas.DataFrame(results)
        average = dict(df.mean())

        if "LISTEXP" in os.environ:
            for e in mostExpensiveFunctions(self.path+"/benchmarks/callgrind.out", 3):
                print(e)

        return average

    def massif_result(self):
        data = msparser.parse_file(self.path+"/benchmarks/massif.out")
        peak =  data["peak_snapshot_index"]
        peak_data = data["snapshots"][peak]
        peak_mem = int(peak_data["mem_heap"]) + int(peak_data["mem_heap_extra"]) + int(peak_data ["mem_stack"])
        return peak_mem


    def massif_average(self, count):
        results = []
        for i in progressbar.progressbar(range(count), redirect_stdout=True, prefix="    Massif    "):
            bash('make massif -C {}'.format(self.path))
            res = self.massif_result()
            results.append(res)
        return int(mean(results))


    def get_statistics(self, count, args):
        #compile and generate benchmark outputs  
        bash('make build -B -C {} {}'.format(self.path, args))

        result = self.callgrind_average(count)
        result["Memory"] = self.massif_average(count)

        return {k:format(int(v), ",").replace(",", ".") for k, v in result.items()}
