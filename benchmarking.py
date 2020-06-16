
import os
from src.ecdh import ECDH_Implementation
from src.sike import *
from src.base import print_statistics

COUNT = 100


def SIKE():
    #Sike Optimization
    OI = Sike_Optimized_Implementation()
    print_statistics(OI.get_statistics(COUNT))

    #Sike Optimization Compressed
    OI_compressed = Sike_Optimized_Implementation_Compressed()
    print_statistics(OI_compressed.get_statistics(COUNT))

    #Sike x64
    x64 = Sike_x64_Implementation()
    print_statistics(x64.get_statistics(COUNT))

    #Sike x64 Compressed
    x64_compressed = Sike_x64_Implementation_Compressed()
    print_statistics(x64_compressed.get_statistics(COUNT))

    #Sike Reference Implementation
    RI = Sike_Reference_Implementation()
    print_statistics(RI.get_statistics(COUNT))

def ECDH():
    #Default ECDH with Curve25519
    ECDH = ECDH_Implementation()
    print_statistics(ECDH.get_statistics(COUNT))



if __name__ == "__main__":

    import time

    print("Count: " + str(COUNT))
    start = time.time()
    ECDH()
    SIKE()
    end = time.time()
    print(str(round(end - start,1)) + " Sekunden")

