from src.ecdh import ECDH_Implementation

from src.sike import Sike_Optimized_Implementation, Sike_Optimized_Implementation_Compressed
from src.sike import Sike_x64_Implementation, Sike_x64_Implementation_Compressed
from src.sike import Sike_Reference_Implementation

from src.circl import CIRCL_x64_Implementation

from src.microsoft import Microsoft_x64_Implementation, Microsoft_x64_Implementation_Compressed

from src.plot import generatePlot, generateTable, saveAsJson, loadFromJson

import signal
import sys

COUNT = 100
RESULTS = {}


def SIKE():
    # Sike Optimization
    if "Sike Optimized" not in RESULTS:
        OI = Sike_Optimized_Implementation()
        RESULTS["Sike Optimized"] = OI.get_statistics(COUNT)

    # Sike Optimization Compressed
    if "Sike Optimized Compressed" not in RESULTS:
        OI_compressed = Sike_Optimized_Implementation_Compressed()
        RESULTS["Sike Optimized Compressed"] = OI_compressed.get_statistics(COUNT)

    # Sike x64
    if "Sike x64" not in RESULTS:
        x64 = Sike_x64_Implementation()
        RESULTS["Sike x64"] = x64.get_statistics(COUNT)

    # Sike x64 Compressed
    if "Sike x64 Compressed" not in RESULTS:
        x64_compressed = Sike_x64_Implementation_Compressed()
        RESULTS["Sike x64 Compressed"] = x64_compressed.get_statistics(COUNT)

    # Sike Reference Implementation
    if "Sike Reference" not in RESULTS:
        RI = Sike_Reference_Implementation()
        RESULTS["Sike Reference"] = RI.get_statistics(COUNT)


def ECDH():
    # Default ECDH with Curve25519
    if "ECDH" not in RESULTS:
        ECDH = ECDH_Implementation()
        RESULTS["ECDH"] = ECDH.get_statistics(COUNT)


def CIRCL():
    # CIRCL Implementation, supporting p434, p503, p751
    if "CIRCL x64" not in RESULTS:
        CIRCL = CIRCL_x64_Implementation()
        RESULTS["CIRCL x64"] = CIRCL.get_statistics(COUNT)

def MICROSOFT():
    if "Microsoft x64" not in RESULTS:
        MS_x64 = Microsoft_x64_Implementation()
        RESULTS["Microsoft x64"] = MS_x64.get_statistics(COUNT)

    if "Microsoft x64 Compressed" not in RESULTS:
        MS_x64_compressed = Microsoft_x64_Implementation_Compressed()
        RESULTS["Microsoft x64 Compressed"] = MS_x64_compressed.get_statistics(COUNT)

def signal_handler(sig,frame):
    saveAsJson(RESULTS)
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    RESULTS = loadFromJson()

    ECDH()
    SIKE()
    CIRCL()
    MICROSOFT()

    saveAsJson(RESULTS)
    
    

    generatePlot(RESULTS)
    generateTable(RESULTS)
