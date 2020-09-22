from src.base import BaseImplementation


curves = ["283", "409", "571"]
class ECDH_Implementation(BaseImplementation):
    def __init__(self, count):
        super().__init__(count=count, path="ECDH/", args="", callgrind_main="benchmark", curves=curves)

    def map_functions(self, callgrind_result):
        res = {
            "PublicKeyA": int(callgrind_result["keygen_A"]/2),
            "PublicKeyB": int(callgrind_result["keygen_B"]/2),
            "PrivateKeyA": 0,
            "PrivateKeyB": 0,
            "SecretA": int(callgrind_result["derive_A"]),
            "SecretB": int(callgrind_result["derive_B"]),
        }
        return res
