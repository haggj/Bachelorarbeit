import statistics

def format_number(number):
    try:
        rounded = round(number) if isinstance(number, float) else round(int(number))
        return format(rounded, ",").replace(",", ".")
    except Exception:
        return number

class BenchmarkImpl:
    def __init__(self, description):
        self.name = description
        self.curves = []

    def add_curve(self, curve):
        # Save a reference to this implementation within the curve
        curve.impl = self
        self.curves.append(curve)
    
    def get_benchmark_names(self):
        if len(self.curves) == 0:
            return []
        return self.curves[0].get_benchmark_names()
    
    def get_curve_by_name(self, name):
        for curve in self.curves:
            if curve.name == name:
                return curve
        return None
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
        return ["Parameter"] + [benchmark.name for benchmark in self.benchmarks] + ["Hotspots"]
    
    def get_benchmark_values(self, newline="\n"):
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
    
    def get_benchmarks_for_plot(self):
        """Summarizes benchmarking values. Keygen is the sum of public key generation +
        private key generation. 

        Returns:
            list: [[Keygen A], [Keygen B], [Secret A], [Secret B]]
        """

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
        """Returns average of benchmark specified by name. If benchmark is not found,
        alternative is returned

        Args:
            name (str): Name of wanted benchmark.
            alternative: Alternative to return, if name is not a valid benchmark.

        Returns:
            Average of benchmark or alternative.
        """
        for benchmark in self.benchmarks:
            if benchmark.name == name:
                return benchmark.get_average()
        return alternative

class Benchmark:
    def __init__(self, description, values):
        self.name = description
        self.values = values
    def get_minimum(self):
        return min(self.values)
    def get_maximum(self):
        return max(self.values)
    def get_average(self):
        return round(statistics.mean(self.values))
    def get_stdev(self):
        if len(self.values) < 2:
            return 0
        return statistics.stdev(self.values)
    def __str__(self):
         return self.name + ": " + str(self.get_average())