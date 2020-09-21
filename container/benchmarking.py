from src.ecdh import ECDH_Implementation

from src.sike import Sike_Optimized_Implementation, Sike_Optimized_Implementation_Compressed
from src.sike import Sike_x64_Implementation, Sike_x64_Implementation_Compressed
from src.sike import Sike_Reference_Implementation

from src.circl import CIRCL_x64_Implementation

from src.microsoft import Microsoft_x64_Implementation, Microsoft_x64_Implementation_Compressed

from src.utils.plot_graph import generate_graph
from src.utils.plot_table import generate_table
from src.utils.caching import load_from_json, save_as_json

import signal
import sys

COUNT = 1
RESULTS = {}


def SIKE():
    # Sike Optimization
    if "Sike Optimized" not in RESULTS:
        OI = Sike_Optimized_Implementation(COUNT)
        RESULTS["Sike Optimized"] = OI.get_statistics()

    # Sike Optimization Compressed
    if "Sike Optimized Compressed" not in RESULTS:
        OI_compressed = Sike_Optimized_Implementation_Compressed(COUNT)
        RESULTS["Sike Optimized Compressed"] = OI_compressed.get_statistics()

    # Sike x64
    if "Sike x64" not in RESULTS:
        x64 = Sike_x64_Implementation(COUNT)
        RESULTS["Sike x64"] = x64.get_statistics()

    # Sike x64 Compressed
    if "Sike x64 Compressed" not in RESULTS:
        x64_compressed = Sike_x64_Implementation_Compressed(COUNT)
        RESULTS["Sike x64 Compressed"] = x64_compressed.get_statistics()

    # Sike Reference Implementation
    if "Sike Reference" not in RESULTS:
        RI = Sike_Reference_Implementation(COUNT)
        RESULTS["Sike Reference"] = RI.get_statistics()


def ECDH():
    # Default ECDH with Curve25519
    if "ECDH" not in RESULTS:
        ECDH = ECDH_Implementation(COUNT)
        RESULTS["ECDH"] = ECDH.get_statistics()


def CIRCL():
    # CIRCL Implementation, supporting p434, p503, p751
    if "CIRCL x64" not in RESULTS:
        CIRCL = CIRCL_x64_Implementation(COUNT)
        RESULTS["CIRCL x64"] = CIRCL.get_statistics()

def MICROSOFT():
    if "Microsoft x64" not in RESULTS:
        MS_x64 = Microsoft_x64_Implementation(COUNT)
        RESULTS["Microsoft x64"] = MS_x64.get_statistics()

    if "Microsoft x64 Compressed" not in RESULTS:
        MS_x64_compressed = Microsoft_x64_Implementation_Compressed(COUNT)
        RESULTS["Microsoft x64 Compressed"] = MS_x64_compressed.get_statistics()

def signal_handler(sig,frame):
    save_as_json(RESULTS)
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    RESULTS = load_from_json()

    ECDH()
    SIKE()
    CIRCL()
    MICROSOFT()
    save_as_json(RESULTS)
    generate_graph(RESULTS)
    generate_table(RESULTS)
