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

    def callgrind_average(self):
        results = []
        


        for i in progressbar.progressbar(range(self.count), redirect_stdout=True, prefix="    Callgrind "):
            count = 0
            while True:
                try:
                    bash('make callgrind -C {}'.format(self.path))
                    res = self.callgrind_result()
                    results.append(res)
                    break
                except Exception as e:
                    count +=1
                    if count == 10:
                        print("Callgrind failed 10 times...")
                        break

        df = pandas.DataFrame(results)
        average = dict(df.mean())

        return average
    
    def get_expensive(self):
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


    def massif_average(self):
        results = []
        for i in progressbar.progressbar(range(self.count), redirect_stdout=True, prefix="    Massif    "):
            bash('make massif -C {}'.format(self.path))
            res = self.massif_result()
            results.append(res)
        return int(mean(results))


    def get_benchmarks(self, args):
        #compile and generate benchmark outputs
        bash('make build -B -C {} {}'.format(self.path, args))

        result = self.callgrind_average()
        result["Memory"] = self.massif_average()

        return {k:format(int(v), ",").replace(",", ".") for k, v in result.items()}

    def get_statistics(self):
        #Generate statistics for all defined curves
        print("\n" + bcolors.WARNING + type(self).__name__ + bcolors.ENDC)

        result = []
        for curve in self.curves:
            print(bcolors.BOLD + "Handling curve "+curve+"..." + bcolors.ENDC)
            res = {}
            res["Curve"]= "p"+curve
            res["Expensive"] = self.get_expensive()
            res.update(self.get_benchmarks("{} PARAM={}".format(self.args, curve)))
            result.append(res)
        return result
