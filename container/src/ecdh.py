from src.base import Base_Implementation, bash, bcolors

from prettytable import PrettyTable
from statistics import mean

class ECDH_Implementation(Base_Implementation):
    def __init__(self):
        self.path = "ECDH/"
        self.args = ""

    def map_functions(self, callgrind_result):
        res = {
            "KeysA": int(callgrind_result["keygen_A"]/2),
            "KeysB": int(callgrind_result["keygen_B"]/2),
            "SecretA": int(callgrind_result["derive_A"]),
            "SecretB": int(callgrind_result["derive_B"]),
        }
        return res
    
    def get_statistics(self, count):
        print("\n" + bcolors.WARNING + type(self).__name__ + bcolors.ENDC)
        ret = {"Curve": "25519"}
        ret.update(super().get_statistics(count, self.args))

        return [ret]