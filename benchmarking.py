import subprocess
import os
from statistics import mean
import pandas
from prettytable import PrettyTable


import msparser

import gprof2dot

curves=["434" , "503", "610", "751"]

def bash(command):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    stream = process.communicate()
    return_code = process.returncode
    if return_code != 0:
        print ("Error during command: " + command)
        print(stream)
        exit(0)
    return

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


def printTable(result):
    TABLE = PrettyTable()
    TABLE.field_names = ["Parameter", "Memory"] + list(result[0][0].keys())
    for (index, r) in enumerate(result):

        values = list(map(int, r[0].values()))
        values = [f'{int(elem):,}' for elem in r[0].values()]

        TABLE.add_row(["p" + curves[index], f'{r[1]:,}'] +  values)
    print(TABLE)


    
class Sike_Implementation():

    def __init__(self):
        pass

    def callgrind_result(self):
        calls = getCallgrindFunctionCalls(self.path+"/benchmarks/callgrind.out", "benchmark_keygen")
        return calls

    def callgrind_average(self, count):
        results = []
        for i in range(count):
            bash('make callgrind -C {}'.format(self.path))
            res = self.callgrind_result()
            results.append(res)

        df = pandas.DataFrame(results)
        average = dict(df.mean())

        return average


    def massif_average(self, count):
        results = []
        for i in range(count):
            bash('make massif -C {}'.format(self.path))
            data = msparser.parse_file(self.path+"/benchmarks/massif.out")
            peak =  data["peak_snapshot_index"]
            peak_data = data["snapshots"][peak]
            peak_mem = int(peak_data["mem_heap"]) + int(peak_data["mem_heap_extra"]) + int(peak_data ["mem_stack"])
            results.append(peak_mem)
        return results


    def get_statistics(self, count):
        res = []
        print(type(self).__name__)

        for curve in curves:
            #compile and generate benchmark outputs
            print("Handeling curve " + curve + "...")
            
            bash('make build -B -C {}  PARAM={} {}'.format(self.path, curve, self.args))

            callgrind_avg = self.callgrind_average(count)
            massif_avg = int(mean(self.massif_average(count)))
            res.append((callgrind_avg, massif_avg))

        return res

class Sike_Reference_Implementation(Sike_Implementation):
    def __init__(self):
        self.path = "SIKE/Reference_Implementation"
        self.args = ""
    
    def callgrind_result(self):
        result = {}

        c1 = getCallgrindFunctionCalls(self.path+"/benchmarks/callgrind.out", "benchmark_keygen_A")
        c2 = getCallgrindFunctionCalls(self.path+"/benchmarks/callgrind.out", "benchmark_secret_A")
        c1.update(c2)
        for key in c1.keys():
            result[str(key) + "_A"] = c1[key]
    

        c1 = getCallgrindFunctionCalls(self.path+"/benchmarks/callgrind.out", "benchmark_keygen_B")
        c2 = getCallgrindFunctionCalls(self.path+"/benchmarks/callgrind.out", "benchmark_secret_B")
        c1.update(c2)
        for key in c1.keys():
            result[str(key) + "_B"] = c1[key]
        
        del result["gmp_init_A"]
        del result["gmp_init_B"]
        del result["fp2_Init_A"]
        del result["fp2_Init_B"]
        del result["public_key_init_A"]
        del result["public_key_init_B"]
        return result

class Sike_Optimized_Implementation(Sike_Implementation):
    def __init__(self):
        self.path = "SIKE/Optimized_Implementation"
        self.args = ""

class Sike_Optimized_Implementation_Compressed(Sike_Implementation):
    def __init__(self):
        self.path = "SIKE/Optimized_Implementation"
        self.args = "COMPRESSED=_compressed"

class Sike_x64_Implementation(Sike_Implementation):
    def __init__(self):
        self.path = "SIKE/x64"
        self.args = ""

class Sike_x64_Implementation_Compressed(Sike_Implementation):
    def __init__(self):
        self.path = "SIKE/x64"
        self.args = "COMPRESSED=_compressed"


if __name__ == "__main__":
    COUNT = 10

    RI = Sike_Reference_Implementation()
    result = RI.get_statistics(COUNT)
    printTable(result)

    OI = Sike_Optimized_Implementation()
    result = OI.get_statistics(COUNT)
    printTable(result)

    OI_compressed = Sike_Optimized_Implementation_Compressed()
    result = OI_compressed.get_statistics(COUNT)
    printTable(result)

    x64 = Sike_x64_Implementation()
    result = x64.get_statistics(COUNT)
    printTable(result)

    x64_compressed = Sike_x64_Implementation_Compressed()
    result = x64_compressed.get_statistics(COUNT)
    printTable(result)