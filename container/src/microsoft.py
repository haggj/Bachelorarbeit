from src.base import BaseImplementation


curves = ["434", "503", "610", "751"]


def get_matching(dic, search):
    found = [dic[key] for key in dic if key.startswith(search)]
    if found:
        return found[0]
    return None

class Microsoft_Base(BaseImplementation):
    def __init__(self, count, path, args):
        super().__init__(count=count, path=path, args=args,
                         callgrind_main="benchmark_keygen", curves=curves)

    def map_functions(self, callgrind_result: dict) -> dict:
        res = {
            "PrivateKeyA": get_matching(callgrind_result, "random_mod_order_A"),
            "PublicKeyA": get_matching(callgrind_result, "EphemeralKeyGeneration_A"),
            "PrivateKeyB": get_matching(callgrind_result, "random_mod_order_B"),
            "PublicKeyB": get_matching(callgrind_result, "EphemeralKeyGeneration_B"),
            "SecretA": get_matching(callgrind_result, "EphemeralSecretAgreement_A"),
            "SecretB": get_matching(callgrind_result, "EphemeralSecretAgreement_B"),
        }
        return res


class Microsoft_x64(Microsoft_Base):
    def __init__(self, count):
        super().__init__(count=count, path="Microsoft/", args="VERSION=x64/")


class Microsoft_x64_Compressed(Microsoft_Base):
    def __init__(self, count):
        super().__init__(count=count, path="Microsoft/",
                         args="COMPRESSED=_compressed VERSION=x64/")


class Microsoft_Generic(Microsoft_Base):
    def __init__(self, count):
        super().__init__(count=count, path="Microsoft/", args="VERSION=generic/")


class Microsoft_Generic_Compressed(Microsoft_Base):
    def __init__(self, count):
        super().__init__(count=count, path="Microsoft/",
                         args="COMPRESSED=_compressed VERSION=generic/")
