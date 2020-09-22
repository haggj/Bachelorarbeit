
from src.base import BaseImplementation
from src.utils.callgrind import extract_function_calls


curves = ["434", "503", "610", "751"]

def sike_map_functions(callgrind_result, compressed):
    add = ""
    if compressed:
        add = "Compressed_"
    res = {
            "PrivateKeyA": callgrind_result["random_mod_order_A"],
            "PublicKeyA": callgrind_result["EphemeralKeyGeneration_" + add + "A"],
            "PrivateKeyB": callgrind_result["random_mod_order_B"],
            "PublicKeyB": callgrind_result["EphemeralKeyGeneration_" + add + "B"],
            "SecretA": callgrind_result["EphemeralSecretAgreement_" + add + "A"],
            "SecretB": callgrind_result["EphemeralSecretAgreement_" + add + "B"]
        }
    return res

class Sike_Optimized_Implementation(BaseImplementation):
    def __init__(self, count):
        super().__init__(count=count, path="SIKE/Optimized_Implementation",
                         args="", callgrind_main="benchmark_keygen", curves=curves)

    def map_functions(self, callgrind_result):
        return sike_map_functions(callgrind_result, False)


class Sike_Optimized_Implementation_Compressed(BaseImplementation):
    def __init__(self, count):
        super().__init__(count=count, path="SIKE/Optimized_Implementation",
                         args="COMPRESSED=_compressed", callgrind_main="benchmark_keygen", curves=curves)

    def map_functions(self, callgrind_result):
        return sike_map_functions(callgrind_result, True)


class Sike_x64_Implementation(BaseImplementation):
    def __init__(self, count):
        super().__init__(count=count, path="SIKE/x64",
                         args="", callgrind_main="benchmark_keygen", curves=curves)

    def map_functions(self, callgrind_result):
        return sike_map_functions(callgrind_result, False)


class Sike_x64_Implementation_Compressed(BaseImplementation):
    def __init__(self, count):
        super().__init__(count=count, path="SIKE/x64",
                         args="COMPRESSED=_compressed", callgrind_main="benchmark_keygen", curves=curves)

    def map_functions(self, callgrind_result):
        return sike_map_functions(callgrind_result, True)


class Sike_Reference_Implementation(BaseImplementation):
    def __init__(self, count):
        super().__init__(count=count, path="SIKE/Reference_Implementation",
                         args="", callgrind_main="benchmark_keygen", curves=curves)

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

        c1 = extract_function_calls(
            self.path+"/benchmarks/callgrind.out", "benchmark_keygen_A")
        c2 = extract_function_calls(
            self.path+"/benchmarks/callgrind.out", "benchmark_secret_A")
        c1.update(c2)
        for key in c1.keys():
            result[str(key) + "_A"] = c1[key]

        c1 = extract_function_calls(
            self.path+"/benchmarks/callgrind.out", "benchmark_keygen_B")
        c2 = extract_function_calls(
            self.path+"/benchmarks/callgrind.out", "benchmark_secret_B")
        c1.update(c2)
        for key in c1.keys():
            result[str(key) + "_B"] = c1[key]

        return self.map_functions(result)
