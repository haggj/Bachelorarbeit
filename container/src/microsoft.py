from src.base import Base_Implementation, bash, getCallgrindFunctionCalls, bcolors
import re


curves=["434", "503", "610", "751"]


def get_matching(dic, search):
    found = [dic[key] for key in dic if key.startswith(search)]
    if found:
        return found[0]
    return None

class Microsoft_Base(Base_Implementation):
    def __init(self):
        self.args = ""

    def get_statistics(self, count):
        print("\n" + bcolors.WARNING + type(self).__name__ + bcolors.ENDC)

        result = []
        for curve in curves:
            print(bcolors.BOLD + "Handling curve "+curve+"..." + bcolors.ENDC)
            res = {}
            res["Curve"]= "p"+curve
            res.update(super().get_statistics(count, "{} PARAM={}".format(self.args, curve)))
            result.append(res)
        return result

    def map_functions(self, callgrind_result):
        res = {
            "PrivateKeyA": get_matching(callgrind_result, "random_mod_order_A"),
            "PublicKeyA": get_matching(callgrind_result, "EphemeralKeyGeneration_A"),
            "PrivateKeyB": get_matching(callgrind_result, "random_mod_order_B"),
            "PublicKeyB": get_matching(callgrind_result, "EphemeralKeyGeneration_B"),
            "SecretA": get_matching(callgrind_result, "EphemeralSecretAgreement_A"),
            "SecretB": get_matching(callgrind_result, "EphemeralSecretAgreement_B"),
        }
        return res


class Microsoft_x64_Implementation(Microsoft_Base):
    def __init__(self):
        self.path = "Microsoft"
        self.args = ""
    

class Microsoft_x64_Implementation_Compressed(Microsoft_Base):
    def __init__(self):
        self.path = "Microsoft"
        self.args = "COMPRESSED=_compressed"
