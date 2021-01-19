"""
Benchmarking CIRCL implementations.
"""
from src.base import BaseImplementation

curves = ["434", "503", "751"]


class CIRCL_Base(BaseImplementation):
    def __init__(self, count, path, args):
        super().__init__(count=count, path=path, args=args, callgrind_main="main.main", curves=curves)

    def map_functions(self, callgrind_result):
        res = {
            "PrivateKeyA": callgrind_result["main.privateKeyA"],
            "PublicKeyA": callgrind_result["main.publicKeyA"],
            "PrivateKeyB": callgrind_result["main.privateKeyB"],
            "PublicKeyB": callgrind_result["main.publicKeyB"],
            "SecretA": callgrind_result["main.sharedA"],
            "SecretB": callgrind_result["main.sharedB"]
        }
        return res


class CIRCL_x64(CIRCL_Base):
    def __init__(self, count):
        super().__init__(count=count, path="CIRCL/", args="ARCH=amd64")


class CIRCL_Generic(CIRCL_Base):
    def __init__(self, count):
        super().__init__(count=count, path="CIRCL/", args='ASM=noasm')
