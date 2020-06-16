
from src.base import Base_Implementation, bash, getCallgrindFunctionCalls


curves=["434" , "503", "610", "751"]

class Sike_Base(Base_Implementation):
    def __init(self):
        self.args = ""

    def get_statistics(self, count):
        print(type(self).__name__)

        result = []
        for curve in curves:
            print("Handling curve "+curve+"...")
            res = {}
            res["Curve"]= "p"+curve
            res.update(super().get_statistics(count, "{} PARAM={}".format(self.args, curve)))
            result.append(res)
        return result

class Sike_Optimized_Implementation(Sike_Base):
    def __init__(self):
        self.path = "SIKE/Optimized_Implementation"
        self.args = ""
    
    def map_functions(self, callgrind_result):
        res = {
            "PrivateKeyA": callgrind_result["random_mod_order_A"],
            "PublicKeyA": callgrind_result["EphemeralKeyGeneration_A"],
            "PrivateKeyB": callgrind_result["random_mod_order_B"],
            "PublicKeyB": callgrind_result["EphemeralKeyGeneration_B"],
            "SecretA": callgrind_result["EphemeralSecretAgreement_A"],
            "SecretB": callgrind_result["EphemeralSecretAgreement_B"]
        }
        return res

class Sike_Optimized_Implementation_Compressed(Sike_Base):
    def __init__(self):
        self.path = "SIKE/Optimized_Implementation"
        self.args = "COMPRESSED=_compressed"
    
        
    def map_functions(self, callgrind_result):
        res = {
            "PrivateKeyA": callgrind_result["random_mod_order_A"],
            "PublicKeyA": callgrind_result["EphemeralKeyGeneration_Compressed_A"],
            "PrivateKeyB": callgrind_result["random_mod_order_B"],
            "PublicKeyB": callgrind_result["EphemeralKeyGeneration_Compressed_B"],
            "SecretA": callgrind_result["EphemeralSecretAgreement_Compressed_A"],
            "SecretB": callgrind_result["EphemeralSecretAgreement_Compressed_B"]
        }
        return res

class Sike_x64_Implementation(Sike_Optimized_Implementation):
    def __init__(self):
        self.path = "SIKE/x64"
        self.args = ""

class Sike_x64_Implementation_Compressed(Sike_Optimized_Implementation_Compressed):
    def __init__(self):
        self.path = "SIKE/x64"
        self.args = "COMPRESSED=_compressed"


class Sike_Reference_Implementation(Sike_Base):
    def __init__(self):
        self.path = "SIKE/Reference_Implementation"
        self.args = ""

    def map_functions(self, callgrind_result):
        res = {
            "PrivateKeyA": callgrind_result["sidh_sk_keygen_A"],
            "PublicKeyA": callgrind_result["sidh_isogen_A"],
            "PrivateKeyB": callgrind_result["sidh_sk_keygen_B"],
            "PublicKeyB": callgrind_result["sidh_isogen_B"],
            "SecretA": callgrind_result["sidh_isoex_A"],
            "SecretB": callgrind_result["sidh_isoex_B"]
        }
        return res

    def callgrind_result(self):
        result = {}

        c1 = getCallgrindFunctionCalls(self.path+"/benchmarks/callgrind.out", "benchmark_keygen_A")
        c2 = getCallgrindFunctionCalls(self.path+"/benchmarks/callgrind.out", "benchmark_secret_A")
        c1.update(c2)
        for key in c1.keys():
            result[str(key) + "_A"] = c1[key]
    

        c1 = getCallgrindFunctionCalls(self.path+"/benchmarks/callgrind.out", "benchmark_keygen_B")
        c2 = getCallgrindFunctionCalls(self.path+"/benchmarks/callgrind.out", "benchmark_secret_B")
        c1.update(c2)
        for key in c1.keys():
            result[str(key) + "_B"] = c1[key]
        
        del result["gmp_init_A"]
        del result["gmp_init_B"]
        del result["fp2_Init_A"]
        del result["fp2_Init_B"]
        del result["public_key_init_A"]
        del result["public_key_init_B"]
        return self.map_functions(result)