"""
Benchmarking openssl ECDH implementations.
"""
from src.base import BaseImplementation

curves = ["secp256", "secp384", "secp521"]


class ECDH(BaseImplementation):
    def __init__(self, count):
        super().__init__(count=count, path="ECDH/", args="", callgrind_main="benchmark", curves=curves)

    def map_functions(self, callgrind_result):
        res = {
            "PublicKeyA": callgrind_result["keygen_A"],
            "PublicKeyB": callgrind_result["keygen_B"],
            "PrivateKeyA": 0,
            "PrivateKeyB": 0,
            "SecretA": callgrind_result["derive_A"],
            "SecretB": callgrind_result["derive_B"],
        }
        return res
