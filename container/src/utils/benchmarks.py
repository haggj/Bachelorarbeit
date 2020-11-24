import statistics

def format_number(number):
    try:
        rounded = round(number) if isinstance(number, float) else round(int(number))
        return format(rounded, ",").replace(",", ".")
    except Exception:
        return number

def map_round(x):
    scaled = float(x)/1000000
    if scaled < 1:
        return round(scaled,1)
    return int(scaled)

class Benchmark:
    def __init__(self, description, values):
        self.name = description
        self.values = values
    def get_minimum(self) -> int:
        return min(self.values)
    def get_maximum(self) -> int:
        return max(self.values)
    def get_average(self) -> float:
        return round(statistics.mean(self.values))
    def get_stdev(self) -> float:
        if len(self.values) < 2:
            return 0
        return statistics.stdev(self.values)
    def __str__(self):
         return self.name + ": " + str(self.get_average())

class BenchmarkCurve:
    """BenchmarkCurve saves benchmarks for a specific curve. It manages a list of benchmarks.
    """
    def __init__(self, description):
        self.name = description
        self.benchmarks = []
        self.hotspots = None

    def add_benchmarks(self, append):
        if isinstance(append, list):
            self.benchmarks = self.benchmarks + append
        else:
            self.benchmarks.append(append)

    def set_hotspots(self, hotspots: list):
        self.hotspots = hotspots

    def get_hotspots(self) -> list:
        return self.hotspots

    def get_benchmark_names(self) -> list:
        """Returns all benchmarks found in the underlaying benchmark objects.

        Returns:
            list: List of all benchmark names.
        """
        return ["Parameter"] + [benchmark.name for benchmark in self.benchmarks] + ["Hotspots"]
    
    def get_benchmark_values(self, newline="\n") -> list:
        """Returns a list of all benchmarking values. Each list element is a string of the form:
        "[average]
        ([standard derivation])"

        Args:
            newline (str, optional): Newline character. Defaults to "\n".

        Returns:
            list: List of benchmaring values.
        """
        final = []
        final.append(self.name)
        for benchmark in self.benchmarks:
            app = "{}{}({})".format(format_number(benchmark.get_average()),
                                    newline,
                                    format_number(benchmark.get_stdev()))
            final.append(app)
        
        final.append(newline.join(self.hotspots))
        return final
    
    def get_benchmarks_for_plot(self) -> list:
        """Summarizes benchmarking values. Keygen is the sum of public key generation +
        private key generation. 

        Returns:
            list: [[Keygen A], [Keygen B], [Secret A], [Secret B]]
        """

        # Calculate average values

        averages = []
        #KeyGenA
        val = self.benchmark_average("PublicKeyA")
        val += self.benchmark_average("PrivateKeyA")
        averages.append(val if val != 0 else "no values")
        #KeyGenB
        val = self.benchmark_average("PublicKeyB")
        val += self.benchmark_average("PrivateKeyB")
        averages.append(val if val != 0 else "no values")
        #SecretA
        val = self.benchmark_average("SecretA")
        averages.append(val if val != 0 else "no values")
        #SecretB
        val = self.benchmark_average("SecretB")
        averages.append(val if val != 0 else "no values")

        # Calculate standard deviation
        deviations = []
        # KeyGenA
        pub_key = self.benchmark_values("PublicKeyA")
        prv_key = self.benchmark_values("PrivateKeyA")
        added = list(map(sum, zip(pub_key,prv_key)))
        dev = round(statistics.stdev(added))
        deviations.append(dev)
        # KeyGenB
        pub_key = self.benchmark_values("PublicKeyB")
        prv_key = self.benchmark_values("PrivateKeyB")
        added = list(map(sum, zip(pub_key,prv_key)))
        dev = round(statistics.stdev(added))
        deviations.append(dev)
         #SecretA
        dev = round(statistics.stdev(self.benchmark_values("SecretA")))
        deviations.append(dev)
        #SecretB
        val = round(statistics.stdev(self.benchmark_values("SecretB")))
        deviations.append(dev)


        return list(map(map_round, averages)), list(map(map_round, deviations))

    def find_benchmark(self, name):
        """Returns average of benchmark specified by name. If benchmark is not found,
        None is returned

        Args:
            name (str): Name of wanted benchmark.

        Returns:
            Average of benchmark or None.
        """
        benchmark = None
        for benchmark in self.benchmarks:
            if benchmark.name == name:
                return benchmark

    def benchmark_average(self, name):
        benchmark = self.find_benchmark(name)
        if benchmark:
            return benchmark.get_average()
        return 0

    def benchmark_stdev(self, name):
        benchmark = self.find_benchmark(name)
        if benchmark:
            return benchmark.get_stdev()
        return 0
    
    def benchmark_values(self, name):
        benchmark = self.find_benchmark(name)
        if benchmark:
            return benchmark.values
        return []
                
class BenchmarkImpl:
    """BenchmarkImpl saves benchmarks for a specific implementation. It manages a list of benchmarked curves.
    """
    def __init__(self, description):
        self.name = description
        self.curves = []

    def add_curve(self, curve: BenchmarkCurve):
        """Adds a benchmarked curve to this implementation

        Args:
            curve (BenchmarkCurve): Curve to add
        """
        # Save a reference to this implementation within the curve
        curve.impl = self
        self.curves.append(curve)
    
    def get_benchmark_names(self):
        """Returns the names of all benchmarks found in the underlaying curves

        Returns:
            list: List of names
        """
        if len(self.curves) == 0:
            return []
        return self.curves[0].get_benchmark_names()
    
    def get_curve_by_name(self, name:str) -> BenchmarkCurve:
        """Search for a specific name within all benchmarked curves.

        Args:
            name (str): Name of the curve

        Returns:
            BenchmarkCurve: The benchmarked curve with the specified name, or None if the curve was not found.
        """
        for curve in self.curves:
            if curve.name == name:
                return curve
        return None