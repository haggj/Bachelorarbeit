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
from src.output.plot_graph import generate_graphs, generate_graph_for
from src.output.plot_table import generate_table
from src.sike import Sike_Generic, Sike_Generic_Compressed
from src.sike import Sike_Reference
from src.sike import Sike_x64, Sike_x64_Compressed

RESULTS = {}

def benchmark(impl, N):
    name = impl.__name__

    if name not in RESULTS:
        instance = impl(N)
        RESULTS[name] = instance.get_statistics()


def signal_handler(sig, frame):
    save_as_json(RESULTS)
    sys.exit(0)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-N', dest='repetitions', action='store', type=int, default=100, help='repetitions of measurements')
    parser.add_argument('--no-cache', dest='cache', action='store_false', help='disable the use of cached data')
    return parser.parse_args()

def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is a negative number" % value)
    return ivalue


if __name__ == "__main__":
    # Register signal handler
    signal.signal(signal.SIGINT, signal_handler)

    # Parse arguments
    args = parse_arguments()
    N = args.repetitions
    print("\nInvoked benchmarking suites with following arguments:")
    print("N\t=\t{}".format(N))
    print("Cache\t=\t{}".format(args.cache))
    
    # Load cached data if requested
    RESULTS = {}
    if args.cache:
        RESULTS = load_from_json()

    # Implementations to benchmark
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

    # Execute benchmarks
    for implementation in implementations:
        benchmark(implementation, N)

    # Generate output files
    save_as_json(RESULTS)
    generate_table(RESULTS)
    generate_graphs(RESULTS)
