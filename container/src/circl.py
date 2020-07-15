from src.base import Base_Implementation


curves = ["434","503","751"]

class CIRCL_x64_Implementation(Base_Implementation):

    def __init__(self, count):
        super().__init__(count=count, path="CIRCL/", args="", callgrind_main="main.main", curves=curves)


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