""" Contains the main class BaseImplementation as well as some shared common functions.
"""
import re
import subprocess

import msparser
import progressbar
from src.utils.benchmarks import BenchmarkImpl, BenchmarkCurve, Benchmark
from src.utils.callgrind import extract_function_calls, extract_hotspots


class bcolors:
    """
    Human meaningful colors
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def bash(command):
    """Executes a command in a new process.

    Args:
        command (string): Command to execute

    Raises:
        Exception: Exception is raised if command does not return with 0
    """
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    out, err = process.communicate()
    return_code = process.returncode
    if return_code != 0:
        print("Error during command: " + command)
        raise Exception(err)
    return out


class BaseImplementation:
    """
    This class is the base class of the benchmarking suite. Each concrete SIDH implementation inherits from this base
    class which provides all the functionality needed to measure benchmarks.
    """

    def __init__(self, count, path, args, callgrind_main, curves):
        self.path = path
        self.args = args
        self.curves = curves
        self.callgrind_main = callgrind_main
        self.count = count

    def map_functions(self, callgrind_result: dict) -> dict:  # pylint: disable=W0613:
        """Maps the incoming dictionary to a default output dictionary which is expected for further analysis.

        Args:
            callgrind_result ([type]): Dictionary, which is mapped to the default dictionary.

        Raises:
            NotImplementedError: Raises, if subclass has not implemented this function.

        return {
            "PrivateKeyA": 0,
            "PublicKeyA": 0,
            "PrivateKeyB": 0,
            "PublicKeyB": 0,
            "SecretA": 0,
            "SecretB": 0
        }
        """
        raise NotImplementedError("Mapping not implemented")

    def callgrind_result(self) -> dict:
        """Opens the callgrind file and returns the relevant data for benchmarking.

        Returns:
            Dict containing the interesting benchmarking statistics.
        """
        calls = extract_function_calls(
            self.path + "/benchmarks/callgrind.out", self.callgrind_main)
        return self.map_functions(calls)

    def callgrind(self) -> list:
        """Calls self.count times callgrind and extracts the results.

        Returns:
            List of Benchmark objects, containing the benchmarks of multiple callgrind runs.
        """
        results = []

        for _ in progressbar.progressbar(range(self.count), redirect_stdout=True, prefix="    Callgrind "):
            fails = 0
            while True:
                try:
                    bash('make callgrind -C {}'.format(self.path))
                    res = self.callgrind_result()
                    results.append(res)
                    break
                except Exception:
                    fails += 1
                    if fails == 10:
                        print("Callgrind failed 10 times...")
                        break

        # Combine single benchmarks to a common result
        benchmarks = []
        for description in ["PrivateKeyA", "PublicKeyA", "PrivateKeyB", "PublicKeyB", "SecretA", "SecretB"]:
            values = [res[description] for res in results]
            if values:
                benchmark = Benchmark(description, values)
                benchmarks.append(benchmark)

        return benchmarks

    def perf(self):
        """Calls self.count times perf and extracts the results.
        The returned benchmarks are: Cycles, GHZ and instructions per cycle.

        Returns:
            List of Benchmark objects, containing the benchmarks of multiple perf runs.
        """
        list_ins_per_sec = []
        list_cycles = []
        list_ghz = []

        for _ in range(5):
            command = "perf stat -o tmp.txt ./{path}/build/benchmark".format(path=self.path)
            bash(command)
            out = open("tmp.txt").read()

            ins_per_sec = float(re.findall("(?<=#)(.*)(?= {2}insn per cycle)", out)[0].replace(",", "."))
            cycles = int(re.findall("(?<=\n)(.*)(?= {6}cycles)", out)[0].replace(".", ""))
            ghz = float(re.findall("(?<=#)(.*)(?= GHz)", out)[0].replace(",", "."))

            list_ins_per_sec.append(ins_per_sec)
            list_cycles.append(cycles)
            list_ghz.append(ghz)

        return [Benchmark("IPC", list_ins_per_sec),
                Benchmark("Cycles", list_cycles),
                Benchmark("GHZ", list_ghz), ]

    def hotspots(self) -> list:
        """Extracts the most expensive functions during callgrind execution.

        Returns:
            List of strings, representing the execution hotspots.
        """
        return extract_hotspots(self.path + "/benchmarks/callgrind.out", 3)

    def massif_result(self) -> int:
        """Opens the massif file and calculates the peak memory consumption.

        Returns:
            Peak memory consuption as integer.
        """
        data = msparser.parse_file(self.path + "/benchmarks/massif.out")
        peak = data["peak_snapshot_index"]
        peak_data = data["snapshots"][peak]
        peak_mem = int(peak_data["mem_heap"]) + \
                   int(peak_data["mem_heap_extra"]) + \
                   int(peak_data["mem_stack"])
        return peak_mem

    def massif(self) -> list:
        """Calls self.count times massif and extracts the results.

        Returns:
            List of Benchmark objects, containing the benchmarks of multiple massif runs.
        """
        values = []
        for _ in progressbar.progressbar(range(self.count), redirect_stdout=True, prefix="    Massif    "):
            bash('make massif -C {}'.format(self.path))
            res = self.massif_result()
            values.append(res)
        return Benchmark("Memory", values)

    def benchmark_curve(self, curve: str) -> BenchmarkCurve:
        """Compilation and benchmarking for a specific curve

        Args:
            curve (string): String representing the curve to benchmark

        Returns:
            BenchmarkCurve: Contains all benchmarks for the curve
        """
        # compile and generate benchmark outputs for specific curve
        args = "{} {} PARAM={}".format(self.path, self.args, curve)
        bash('make build -B -C {}'.format(args))

        benchmark_curve = BenchmarkCurve(curve)
        benchmark_curve.add_benchmarks(self.callgrind())
        benchmark_curve.add_benchmarks(self.massif())
        benchmark_curve.add_benchmarks(self.perf())
        benchmark_curve.set_hotspots(self.hotspots())

        return benchmark_curve

    def get_statistics(self):
        """Runs benchmark for all curves specified in self.curves.

        Returns:
            BenchmarkImpl: Benchmarking object, that contains benchmarks for all defined curves.
        """
        print("\n" + bcolors.WARNING + type(self).__name__ + bcolors.ENDC)

        benchmark = BenchmarkImpl(type(self).__name__)

        for curve in self.curves:
            print(bcolors.BOLD + "Handling curve " +
                  str(curve) + "..." + bcolors.ENDC)
            benchmark.add_curve(self.benchmark_curve(curve))

        return benchmark
