import subprocess
import os
from statistics import mean 

import msparser


curves=["751" , "503", "610", "751"]

def bash(command):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    return process.communicate()

    
class Sike_Optimized_Implementation():

    def __init__(self):
        self.path = "Optimized_Implementation"
        self.fun = "EphemeralKeyGeneration_A"
        self.args = ""

    def read_callgrind_function(self, function):
        dump = open(self.path+"/benchmarks/callgrind_annotate.out").read()

        dump = dump.split("/sidh.c:" + function + " (1x)")[0]
        dump = dump.split("\n")[-1]
        dump = dump.split(">")[0]
        dump = dump.replace(",", "")

        return dump


    def callgrind_average(self, count):
        results = []
        for i in range(count):
            bash('make callgrind -C {}'.format(self.path))
            res = int(self.read_callgrind_function(self.fun))
            results.append(res)
        return results


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



    def get_statistics(self):
        for curve in curves:
            #compile and generate benchmark outputs
            print("Handeling curve " + curve + "...")
            res, _ = bash('make build -B -C {}  PARAM={} {}'.format(self.path, curve, self.args))

            res = self.callgrind_average(3)
            print(res)
            print("Average: " + str(mean(res)))
            res = self.massif_average(3)
            print(res)
            print("Average: " + str(mean(res)))
            print()
            break


class Sike_Reference_Implementation(Sike_Optimized_Implementation):
    def __init__(self):
        self.path = "Reference_Implementation"
        self.fun = "sidh_isogen"
        self.args = ""

class Sike_Optimized_Implementation_Compressed(Sike_Optimized_Implementation):
    def __init__(self):
        self.path = "Optimized_Implementation"
        self.fun = "EphemeralKeyGeneration_Compressed_A"
        self.args = "COMPRESSED=_compressed"

OI = Sike_Optimized_Implementation()
OI.get_statistics()

OI_compressed = Sike_Optimized_Implementation_Compressed()
OI_compressed.get_statistics()

RI = Sike_Reference_Implementation()
RI.get_statistics()