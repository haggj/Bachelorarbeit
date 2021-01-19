import statistics
from unittest import TestCase
from unittest.mock import MagicMock, patch

from src.utils.benchmarks import Benchmark, BenchmarkCurve, BenchmarkImpl, format_number


class TestBenchmark(TestCase):
    def setUp(self):
        self.values = [1, 2, 3]
        self.name = "test"
        self.benchmark = Benchmark(self.name, self.values)

    def test_get_minimum(self):
        result = self.benchmark.get_minimum()
        self.assertEqual(result, 1)

    def test_get_maximum(self):
        result = self.benchmark.get_maximum()
        self.assertEqual(result, 3)

    def test_get_average(self):
        result = self.benchmark.get_average()
        self.assertEqual(result, 2)

    def test_get_stdev(self):
        result = self.benchmark.get_stdev()
        self.assertEqual(result, 1)

        benchmark = Benchmark("test", [])
        result = benchmark.get_stdev()
        self.assertEqual(result, 0)

    def test_str(self):
        result = str(self.benchmark)
        self.assertTrue(self.benchmark.name in result)
        self.assertTrue(len(self.benchmark.name) < len(result))


class TestBenchmarkCurve(TestCase):
    def setUp(self):
        self.name = "test"
        self.benchmark = BenchmarkCurve(self.name)

    def test_add_benchmarks(self):
        self.benchmark.add_benchmarks(MagicMock())
        self.assertEqual(len(self.benchmark.benchmarks), 1)
        self.benchmark.add_benchmarks([MagicMock()] * 3)
        self.assertEqual(len(self.benchmark.benchmarks), 4)

    def test_hotspot(self):
        hotspot = MagicMock()
        self.benchmark.set_hotspots(hotspot)
        self.assertEqual(self.benchmark.hotspots, hotspot)
        self.assertEqual(self.benchmark.get_hotspots(), hotspot)

    def test_get_benchmark_names(self):
        self.benchmark.add_benchmarks([MagicMock()] * 5)
        self.assertEqual(len(self.benchmark.get_benchmark_names()), 7)

    def test_get_benchmark_values(self):
        benchmark = MagicMock()
        self.benchmark.add_benchmarks([benchmark] * 5)
        self.benchmark.set_hotspots(MagicMock())
        with patch("src.utils.benchmarks.format_number"):
            result = self.benchmark.get_benchmark_values()
        self.assertTrue(isinstance(result, list))
        self.assertEqual(len(result), 7)
        self.assertEqual(benchmark.get_average.call_count, 5)
        self.assertEqual(benchmark.get_stdev.call_count, 5)

    def test_benchmark_values(self):
        test_list = [3, 4]
        self.benchmark.add_benchmarks(Benchmark("Test", test_list))
        ret = self.benchmark.benchmark_values("Test")
        self.assertCountEqual(ret, test_list)
        ret = self.benchmark.benchmark_values("Not existing")
        self.assertCountEqual(ret, [])

    def test_benchmark_average(self):
        test_list = [3, 3]
        self.benchmark.add_benchmarks(Benchmark("Test", test_list))
        ret = self.benchmark.benchmark_average("Test")
        self.assertEqual(ret, round(statistics.mean(test_list)))

        self.benchmark.add_benchmarks(Benchmark("Test2", []))
        ret = self.benchmark.benchmark_average("Test2")
        self.assertEqual(ret, 0)

        ret = self.benchmark.benchmark_average("Not existing")
        self.assertEqual(ret, 0)

    def test_benchmark_stdev(self):
        test_list = [3, 3]
        self.benchmark.add_benchmarks(Benchmark("Test", test_list))
        ret = self.benchmark.benchmark_stdev("Test")
        self.assertEqual(ret, round(statistics.stdev(test_list)))

        self.benchmark.add_benchmarks(Benchmark("Test2", [1]))
        ret = self.benchmark.benchmark_stdev("Test2")
        self.assertEqual(ret, 0)

        ret = self.benchmark.benchmark_stdev("Not existing")
        self.assertEqual(ret, 0)

    def test_get_benchmarks_for_plot(self):
        # Test for valid benchmarks
        self.benchmark.add_benchmarks(Benchmark("PublicKeyA", [3, 3]))
        self.benchmark.add_benchmarks(Benchmark("PublicKeyB", [1, 3]))
        self.benchmark.add_benchmarks(Benchmark("PrivateKeyA", [3, 3]))
        self.benchmark.add_benchmarks(Benchmark("PrivateKeyB", [1, 3]))
        self.benchmark.add_benchmarks(Benchmark("SecretA", [2, 4]))
        self.benchmark.add_benchmarks(Benchmark("SecretB", [2, 4]))

        result = self.benchmark.get_benchmarks_for_plot(mapping=lambda x: x)
        self.assertEqual(result, ([6, 4, 3, 3], [0, 3, 1, 1]))

    def test_find_benchmark(self):
        # Test for empty benchmarks
        result = self.benchmark.find_benchmark("not_existing")
        self.assertEqual(result, None)

        bench = Benchmark("test", [3, 5])
        self.benchmark.add_benchmarks(bench)
        result = self.benchmark.find_benchmark("test")
        self.assertEqual(result, bench)


class TestBenchmarkImpl(TestCase):
    def setUp(self):
        self.name = "test"
        self.impl = BenchmarkImpl(self.name)

    def test_add_curve(self):
        curve = MagicMock()
        self.impl.add_curve(curve)
        self.assertEqual(len(self.impl.curves), 1)
        self.assertEqual(self.impl.curves[0].impl, self.impl)

    def test_get_benchmark_names(self):
        result = self.impl.get_benchmark_names()
        self.assertEqual(result, [])

        curve = MagicMock()
        self.impl.add_curve(curve)
        result = self.impl.get_benchmark_names()
        self.assertEqual(result, curve.get_benchmark_names())

    def test_get_curve_by_name(self):
        result = self.impl.get_curve_by_name("not_existing")
        self.assertEqual(result, None)

        curve = MagicMock()
        curve.name = "test"
        self.impl.add_curve(curve)
        result = self.impl.get_curve_by_name("test")
        self.assertEqual(result, curve)


class TestFormatNumber(TestCase):
    def test_all(self):
        # Int as  input
        self.assertEqual(format_number(3), "3")

        # String as input
        self.assertEqual(format_number("3"), "3")

        # Round value
        self.assertEqual(format_number(3.6), "4")

        # Add thousand seperator
        self.assertEqual(format_number(3000000.6), "3.000.001")

        # Invalid input
        self.assertEqual(format_number("abc"), "abc")
