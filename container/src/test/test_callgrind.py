from unittest import TestCase
from unittest.mock import MagicMock, patch, Mock
from src.utils.callgrind import extract_function_calls, extract_hotspots


class TestExtractHotspots(TestCase):
    def test(self):
        callgrind = MagicMock()
        count = 2
        
        # Fake CallgrindParser internals
        event1 = MagicMock()
        event1.name = "Time ratio"

        event2 = MagicMock()
        event2.name = "Samples"

        fun1 = MagicMock()
        fun1.events = MagicMock()
        fun1.events.items.return_value = [(event1, 0.1), (event2, 1)]

        fun2 = MagicMock()
        fun2.events = MagicMock()
        fun2.events.items.return_value = [(event1, 0.2), (event2, 1)]

        fun3 = MagicMock()
        fun3.events = MagicMock()
        fun3.events.items.return_value = [(event1, 0.3), (event2, 1)]

        fake_functions = {  "name1": fun1,
                            "name2": fun2,
                            "name3": fun3,}

        profile = MagicMock()
        profile.functions = fake_functions

        parser = MagicMock()
        parser.parse.return_value = profile

        with patch("src.utils.callgrind.open"):
            with patch("src.utils.callgrind.gprof2dot.CallgrindParser") as mock_parser:
               
                mock_parser.return_value = parser
                result = extract_hotspots(callgrind, count)
        
        self.assertEqual(len(result), 2)
        print(result)
        self.assertTrue("name3" in result[0] and "30.0%" in result[0])
        self.assertTrue("name2" in result[1] and "20.0%" in result[1])

class TestExtractFunctionCalls(TestCase):
    def test(self):
        callgrind = MagicMock()
        count = 2

        # Fake CallgrindParser internals
        event = MagicMock()
        event.name = "Samples"

        call1 = MagicMock()
        call1.callee_id = "name2"
        call1.events = {event:5}

        call2 = MagicMock()
        call2.callee_id = "name3"
        call2.events = {event:6}

        caller = MagicMock()
        caller.calls = {"key": call1, "another_key": call2}

        callee1 = MagicMock()
        callee1.name = "function2"

        callee2 = MagicMock()
        callee2.name = "function3"


        fake_functions = {"name1": caller,
                          "name2": callee1,
                          "name3": callee2}

        profile = MagicMock()
        profile.functions = fake_functions

        parser = MagicMock()
        parser.parse.return_value = profile

        with patch("src.utils.callgrind.open"):
            with patch("src.utils.callgrind.gprof2dot.CallgrindParser") as mock_parser:
               
                mock_parser.return_value = parser
                result = extract_function_calls(callgrind, "name1")
        
        #self.assertEqual(len(result), 2)
        print(result)
        self.assertEqual(result["function2"], 5)
        self.assertEqual(result["function3"], 6)
