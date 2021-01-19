"""
Entrypoint of the benchmarking suite.
"""
import signal
import sys
import argparse

from src.circl import CIRCL_x64, CIRCL_Generic
from src.ecdh import ECDH
from src.microsoft import Microsoft_Generic, Microsoft_Generic_Compressed
from src.microsoft import Microsoft_x64, Microsoft_x64_Compressed
from src.output.caching import load_from_json, save_as_json
from src.output.plot_graph import generate_graph
from src.output.plot_table import generate_table
from src.sike import Sike_Generic, Sike_Generic_Compressed
from src.sike import Sike_Reference
from src.sike import Sike_x64, Sike_x64_Compressed

# Number of repetitions for each benchmark (N>=2)
N = 1
RESULTS = {}


def benchmark(impl):
    name = impl.__name__

    if name not in RESULTS:
        instance = impl(N)
        RESULTS[name] = instance.get_statistics()


def signal_handler(sig, frame):
    save_as_json(RESULTS)
    sys.exit(0)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-cache', dest='cache', action='store_false')
    parser.set_defaults(cache=True)
    return parser.parse_args()


if __name__ == "__main__":
    # Register signal handler
    signal.signal(signal.SIGINT, signal_handler)

    # Parse arguments
    args = parse_arguments()

    RESULTS = {}
    if args.cache:
        RESULTS = load_from_json()

    implementations = [
        # ECDH
        ECDH,

        # #SIKE
        Sike_Reference,
        Sike_Generic,
        Sike_Generic_Compressed,
        Sike_x64,
        Sike_x64_Compressed,

        # CIRCL
        CIRCL_x64,
        CIRCL_Generic,

        # #MICROSOFT
        Microsoft_Generic,
        Microsoft_Generic_Compressed,
        Microsoft_x64,
        Microsoft_x64_Compressed,
    ]

    for implementation in implementations:
        benchmark(implementation)

    save_as_json(RESULTS)

    generate_table(RESULTS)
    generate_graph(RESULTS)
