
import os
from src.ecdh import ECDH_Implementation
from src.sike import *
from src.circl import CIRCL_Implementation
from src.plot import generatePlot, print_statistics

COUNT = 1
RESULTS = {}
    

def SIKE():
    #Sike Optimization
    OI = Sike_Optimized_Implementation()
    RESULTS["Sike Optimized"] = OI.get_statistics(COUNT)
    print_statistics(RESULTS["Sike Optimized"])

    #Sike Optimization Compressed
    OI_compressed = Sike_Optimized_Implementation_Compressed()
    RESULTS["Sike Optimized Compressed"] = OI_compressed.get_statistics(COUNT)
    print_statistics(RESULTS["Sike Optimized Compressed"])

    #Sike x64
    x64 = Sike_x64_Implementation()
    RESULTS["Sike x64"] = x64.get_statistics(COUNT)
    print_statistics(RESULTS["Sike x64"])

    #Sike x64 Compressed
    x64_compressed = Sike_x64_Implementation_Compressed()
    RESULTS["Sike x64 Compressed"] = x64_compressed.get_statistics(COUNT)
    print_statistics(RESULTS["Sike x64 Compressed"])

    #Sike Reference Implementation
    RI = Sike_Reference_Implementation()
    RESULTS["Sike Reference Implementation"] = RI.get_statistics(COUNT)
    print_statistics(RESULTS["Sike Reference Implementation"])

def ECDH():
    #Default ECDH with Curve25519
    ECDH = ECDH_Implementation()
    RESULTS["ECDH"] = ECDH.get_statistics(COUNT)
    print_statistics(RESULTS["ECDH"])

def CIRCL():
    CIRCL = CIRCL_Implementation()
    print_statistics(CIRCL.get_statistics(COUNT))

if __name__ == "__main__":

    #ECDH()
    SIKE()
    CIRCL()

    #RESULTS = {'ECDH': [{'Curve': '25519', 'KeysA': '569.279', 'KeysB': '546.487', 'SecretA': '512.759', 'SecretB': '512.759', 'Memory': '13.576'}], 'Sike Optimized': [{'Curve': 'p434', 'PrivateKeyA': '90', 'PublicKeyA': '195.766.407', 'PrivateKeyB': '57', 'PublicKeyB': '216.548.718', 'SecretA': '158.715.898', 'SecretB': '182.403.124', 'Memory': '8.008'}, {'Curve': 'p503', 'PrivateKeyA': '95', 'PublicKeyA': '300.960.599', 'PrivateKeyB': '57', 'PublicKeyB': '331.368.751', 'SecretA': '245.139.361', 'SecretB': '279.727.050', 'Memory': '7.928'}, {'Curve': 'p610', 'PrivateKeyA': '96', 'PublicKeyA': '617.632.135', 'PrivateKeyB': '53', 'PublicKeyB': '615.248.913', 'SecretA': '514.833.551', 'SecretB': '521.242.325', 'Memory': '11.704'}, {'Curve': 'p751', 'PrivateKeyA': '97', 'PublicKeyA': '988.815.348', 'PrivateKeyB': '59', 'PublicKeyB': '1.110.622.514', 'SecretA': '812.990.929', 'SecretB': '946.083.828', 'Memory': '13.496'}], 'Sike Optimized Compressed': [{'Curve': 'p434', 'PrivateKeyA': '97', 'PublicKeyA': '509.975.819', 'PrivateKeyB': '150', 'PublicKeyB': '430.175.223', 'SecretA': '180.544.696', 'SecretB': '221.013.601', 'Memory': '16.536'}, {'Curve': 'p503', 'PrivateKeyA': '95', 'PublicKeyA': '773.503.930', 'PrivateKeyB': '147', 'PublicKeyB': '647.334.203', 'SecretA': '278.056.844', 'SecretB': '342.165.876', 'Memory': '19.096'}, {'Curve': 'p610', 'PrivateKeyA': '99', 'PublicKeyA': '1.479.028.321', 'PrivateKeyB': '187', 'PublicKeyB': '1.214.366.601', 'SecretA': '574.094.144', 'SecretB': '635.236.948', 'Memory': '23.896'}, {'Curve': 'p751', 'PrivateKeyA': '107', 'PublicKeyA': '2.701.802.180', 'PrivateKeyB': '202', 'PublicKeyB': '2.172.068.479', 'SecretA': '916.339.774', 'SecretB': '1.127.268.504', 'Memory': '27.768'}], 'Sike x64': [{'Curve': 'p434', 'PrivateKeyA': '90', 'PublicKeyA': '18.331.210', 'PrivateKeyB': '57', 'PublicKeyB': '20.387.082', 'SecretA': '14.850.647', 'SecretB': '17.182.025', 'Memory': '8.104'}, {'Curve': 'p503', 'PrivateKeyA': '95', 'PublicKeyA': '25.466.692', 'PrivateKeyB': '57', 'PublicKeyB': '28.206.470', 'SecretA': '20.731.488', 'SecretB': '23.829.301', 'Memory': '8.088'}, {'Curve': 'p610', 'PrivateKeyA': '96', 'PublicKeyA': '47.045.492', 'PrivateKeyB': '53', 'PublicKeyB': '47.165.758', 'SecretA': '39.194.638', 'SecretB': '39.988.742', 'Memory': '11.808'}, {'Curve': 'p751', 'PrivateKeyA': '97', 'PublicKeyA': '68.209.369', 'PrivateKeyB': '59', 'PublicKeyB': '77.081.514', 'SecretA': '56.041.244', 'SecretB': '65.709.246', 'Memory': '13.648'}], 'Sike x64 Compressed': [{'Curve': 'p434', 'PrivateKeyA': '97', 'PublicKeyA': '48.942.221', 'PrivateKeyB': '142', 'PublicKeyB': '41.763.644', 'SecretA': '17.186.082', 'SecretB': '21.161.586', 'Memory': '18.600'}, {'Curve': 'p503', 'PrivateKeyA': '95', 'PublicKeyA': '67.680.640', 'PrivateKeyB': '142', 'PublicKeyB': '56.569.898', 'SecretA': '23.902.389', 'SecretB': '29.558.508', 'Memory': '21.368'}, {'Curve': 'p610', 'PrivateKeyA': '99', 'PublicKeyA': '124.505.612', 'PrivateKeyB': '172', 'PublicKeyB': '94.864.240', 'SecretA': '44.261.467', 'SecretB': '49.850.293', 'Memory': '26.976'}, {'Curve': 'p751', 'PrivateKeyA': '107', 'PublicKeyA': '190.382.854', 'PrivateKeyB': '188', 'PublicKeyB': '152.550.839', 'SecretA': '63.925.947', 'SecretB': '79.133.373', 'Memory': '31.664'}]}
    print(RESULTS)

    generatePlot(RESULTS)

