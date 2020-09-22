import statistics

def format_number(number):
    try:    
        return format(round(int(number)), ",").replace(",", ".")
    except Exception:
        return number

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
        return ["Parameter"] + [benchmark.name for benchmark in self.benchmarks] + ["Hotspots"]
    
    def get_benchmark_values(self):
        final = []
        final.append(self.name)
        for benchmark in self.benchmarks:
            app = "{}\n({})".format( format_number(benchmark.get_average()), 
                                    format_number(benchmark.get_stdev()))
            final.append(app)
        
        final.append(self.hotspots)
        return final
    
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