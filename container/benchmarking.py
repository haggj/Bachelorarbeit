from src.ecdh import ECDH

from src.sike import Sike_Generic, Sike_Generic_Compressed
from src.sike import Sike_x64, Sike_x64_Compressed
from src.sike import Sike_Reference

from src.circl import CIRCL_x64

from src.microsoft import Microsoft_x64, Microsoft_x64_Compressed
from src.microsoft import Microsoft_Generic, Microsoft_Generic_Compressed

from src.utils.plot_graph import generate_graph
from src.utils.plot_table import generate_table
from src.utils.caching import load_from_json, save_as_json

import signal
import sys

COUNT = 100
RESULTS = {}

def benchmark(Class):
    name = Class.__name__
    if name not in RESULTS:
        instance = Class(COUNT)
        RESULTS[name] = instance.get_statistics()

def signal_handler(sig,frame):
    save_as_json(RESULTS)
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    RESULTS = load_from_json()

    implementations =[
        #ECDH
        ECDH,

        # #SIKE
        Sike_Reference,
        Sike_Generic,
        Sike_Generic_Compressed,
        Sike_x64,
        Sike_x64_Compressed,

        #CIRCL
        CIRCL_x64,

        # #MICROSOFT
        Microsoft_Generic,
        Microsoft_Generic_Compressed,
        Microsoft_x64,
        Microsoft_x64_Compressed,
    ]

    for implementation in implementations:
        benchmark(implementation)

    save_as_json(RESULTS)
    generate_graph(RESULTS)
    generate_table(RESULTS)
