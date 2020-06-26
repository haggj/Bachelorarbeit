
import os
from src.ecdh import ECDH_Implementation
from src.sike import *
from src.circl import CIRCL_Implementation
from src.plot import generatePlot, generateTable

COUNT = 3
RESULTS = {}
    

def SIKE():
    #Sike Optimization
    OI = Sike_Optimized_Implementation()
    RESULTS["Sike Optimized"] = OI.get_statistics(COUNT)

    #Sike Optimization Compressed
    OI_compressed = Sike_Optimized_Implementation_Compressed()
    RESULTS["Sike Optimized Compressed"] = OI_compressed.get_statistics(COUNT)

    #Sike x64
    x64 = Sike_x64_Implementation()
    RESULTS["Sike x64"] = x64.get_statistics(COUNT)

    #Sike x64 Compressed
    x64_compressed = Sike_x64_Implementation_Compressed()
    RESULTS["Sike x64 Compressed"] = x64_compressed.get_statistics(COUNT)

    #Sike Reference Implementation
    RI = Sike_Reference_Implementation()
    RESULTS["Sike Reference Implementation"] = RI.get_statistics(COUNT)

def ECDH():
    #Default ECDH with Curve25519
    ECDH = ECDH_Implementation()
    RESULTS["ECDH"] = ECDH.get_statistics(COUNT)

def CIRCL():
    #CIRCL Implementation, supporting p434, p503, p751
    CIRCL = CIRCL_Implementation()
    RESULTS["CIRCL"] = CIRCL.get_statistics(COUNT)

if __name__ == "__main__":

    ECDH()
    SIKE()
    CIRCL()
   
    generatePlot(RESULTS)
    generateTable(RESULTS)

