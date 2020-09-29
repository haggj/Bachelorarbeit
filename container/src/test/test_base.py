from unittest import TestCase
from unittest.mock import MagicMock, patch, Mock
from src.base import bash, BaseImplementation
from src.utils.benchmarks import Benchmark, BenchmarkCurve, BenchmarkImpl


class TestBash(TestCase):

    def test_successful_command(self):
        command = "This is a test command"
        with patch("src.base.subprocess.Popen", autospec=True) as mock_popen:
            with patch("src.base.subprocess.PIPE") as mock_PIPE:
                obj = MagicMock()
                obj.returncode = 0
                mock_popen.return_value = obj
                bash(command)
        mock_popen.assert_called_once_with(command.split(), stdout=mock_PIPE)

    def test_error_command(self):
        command = "This is a test command"
        with patch("src.base.subprocess.Popen", autospec=True) as mock_popen:
            with patch("src.base.subprocess.PIPE") as mock_PIPE:
                obj = MagicMock()
                obj.returncode = 1
                self.assertRaises(Exception, bash, command)
        mock_popen.assert_called_once_with(command.split(), stdout=mock_PIPE)


class TestBaseImplementation(TestCase):
    def setUp(self):
        self.count = 5
        self.args = MagicMock()
        self.path = MagicMock()
        self.callgrind_main = MagicMock()
        self.curves = MagicMock()
        self.implementation = BaseImplementation(
            self.count, self.path, self.args, self.callgrind_main, self.curves)

    def test_map_functions(self):
        self.assertRaises(NotImplementedError,
                          self.implementation.map_functions, MagicMock())

    def test_callglrind_result(self):
        fake_calls = MagicMock()
        with patch("src.base.extract_function_calls", return_value=fake_calls) as mock_extract:
            with patch("src.base.BaseImplementation.map_functions") as mock_map:
                self.implementation.callgrind_result()

        mock_extract.assert_called_once()
        mock_map.assert_called_once_with(fake_calls)

    def test_callgrind(self):

        dic = {"PrivateKeyA": 2, "PublicKeyA": 2,  "PrivateKeyB": 2,
               "PublicKeyB": 2, "SecretA": 2, "SecretB": 2}

        with patch("src.base.bash") as mock_bash:
            with patch("src.base.BaseImplementation.callgrind_result", return_value=dic) as mock_result:
                result = self.implementation.callgrind()

        self.assertEqual(mock_bash.call_count, self.count)
        self.assertEqual(mock_result.call_count, self.count)
        self.assertEqual(len(result), 6)
        for benchmark in result:
            self.assertEqual(type(benchmark), Benchmark)
            self.assertEqual(benchmark.values, self.count *
                             [dic[benchmark.name]])

    def test_callgrind_exception(self):

        with patch("src.base.bash") as mock_bash:
            with patch("src.base.BaseImplementation.callgrind_result") as mock_result:
                mock_result.side_effect = Exception()
                result = self.implementation.callgrind()
        self.assertEqual(mock_bash.call_count, self.count*10)
        self.assertEqual(mock_result.call_count, self.count*10)
        self.assertEqual(result, [])

    def test_hotspots(self):

        fake_hotspots = [MagicMock(), MagicMock(), MagicMock()]

        with patch("src.base.extract_hotspots", return_value=fake_hotspots) as mock_hotspots:
            result = self.implementation.hotspots()
        mock_hotspots.assert_called_once()
        self.assertEqual(result, fake_hotspots)

    def test_massif_result(self):
        fake_snapshot = {"mem_heap": "3",
                         "mem_heap_extra": "3", "mem_stack": "3"}
        fake_data = {"peak_snapshot_index": 1,
                     "snapshots": [None, fake_snapshot, None]}

        with patch("src.base.msparser.parse_file", return_value=fake_data) as mock_parser:
            result = self.implementation.massif_result()
        self.assertEqual(result, 9)
        mock_parser.assert_called_once()

    def test_massif(self):

        fake_memory = 3

        with patch("src.base.bash") as mock_bash:
            with patch("src.base.BaseImplementation.massif_result", return_value=fake_memory) as mock_result:
                result = self.implementation.massif()

        self.assertEqual(mock_bash.call_count, self.count)
        self.assertEqual(mock_result.call_count, self.count)
        self.assertEqual(result.name, "Memory")
        self.assertEqual(result.values, self.count*[fake_memory])

    def test_benchmark_curve(self):

        fake_massif = MagicMock()
        fake_callgrind = [MagicMock(), MagicMock()]
        fake_hotspots = MagicMock()
        with patch("src.base.bash") as mock_bash:
            with patch("src.base.BaseImplementation.massif", return_value=fake_massif) as mock_massif:
                with patch("src.base.BaseImplementation.callgrind", return_value=fake_callgrind) as mock_callgrind:
                    with patch("src.base.BaseImplementation.hotspots", return_value=fake_hotspots) as mock_hotspots:
                        result = self.implementation.benchmark_curve(
                            MagicMock())
        self.assertEqual(type(result), BenchmarkCurve)
        self.assertEqual(result.benchmarks, fake_callgrind + [fake_massif])
        self.assertEqual(result.hotspots, fake_hotspots)
        mock_bash.assert_called_once()

    def test_get_statistics(self):
        self.implementation.curves = [1,2,3,4]
        fake_benchmark = MagicMock()
        with patch('builtins.print'):
            with patch("src.base.BaseImplementation.benchmark_curve", return_value=fake_benchmark) as mock_benchmark:
                result = self.implementation.get_statistics()

        self.assertEqual(mock_benchmark.call_count, len(self.implementation.curves))
        self.assertEqual(type(result), BenchmarkImpl)
        self.assertEqual(result.name, BaseImplementation.__name__)
        self.assertEqual(result.curves, len(self.implementation.curves) * [fake_benchmark])
