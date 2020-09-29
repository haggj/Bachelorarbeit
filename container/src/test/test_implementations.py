from src.ecdh import ECDH

from src.sike import Sike_Generic, Sike_Generic_Compressed
from src.sike import Sike_x64, Sike_x64_Compressed
from src.sike import Sike_Reference, Sike_Base

from src.circl import CIRCL_x64, CIRCL_Base

from src.microsoft import Microsoft_x64, Microsoft_x64_Compressed
from src.microsoft import Microsoft_Generic, Microsoft_Generic_Compressed
from src.microsoft import Microsoft_Base, get_matching

from src.utils.benchmarks import Benchmark

from unittest import TestCase
from unittest.mock import MagicMock, patch
import logging
import sys
import os, os.path


logger = logging.getLogger()

class TestImplementations(TestCase):
    def test_init(self):
        implementations =[
            #ECDH
            ECDH,

            # #SIKE
            Sike_Reference,
            Sike_Generic,
            Sike_Generic_Compressed,
            Sike_x64,
            Sike_x64_Compressed,

            #CIRCL
            CIRCL_x64,

            # #MICROSOFT
            Microsoft_Generic,
            Microsoft_Generic_Compressed,
            Microsoft_x64,
            Microsoft_x64_Compressed,
        ]
        for impl in implementations:
            # Init implementation
            obj = impl(5)
            self.assertEqual(type(obj), impl)

            # Compile
            with patch("src.base.BaseImplementation.callgrind", return_value=Benchmark("",0)):
                with patch("src.base.BaseImplementation.massif", return_value=Benchmark("",0)):
                    with patch("src.base.BaseImplementation.hotspots", return_value = []):
                        logger.info("Testing compilation for " + impl.__name__)
                        for curve in obj.curves:
                            logger.info("\tHandle parameter" + str(curve))
                            obj.benchmark_curve(curve)
                            self.assertTrue(os.path.isfile(obj.path + "/build/benchmark"))
                            os.remove(obj.path + "/build/benchmark")


class TestECDH(TestCase):
    def test_map_functions(self):
        val = MagicMock()
        dic = {
            "keygen_A": val,
            "derive_A": val,
            "keygen_B": val,
            "derive_B": val,
        }
        base = ECDH(5)
        result = base.map_functions(dic)
        self.assertEqual(len(result), 6)
        self.assertEqual(result["PublicKeyA"], val)
        self.assertEqual(result["PublicKeyB"], val)
        self.assertEqual(result["SecretA"], val)
        self.assertEqual(result["SecretB"], val)
        self.assertEqual(result["PrivateKeyA"], 0)
        self.assertEqual(result["PrivateKeyB"], 0)

class TestCIRCL(TestCase):
    def test_map_functions(self):
        val = MagicMock()
        dic = {
            "main.privateKeyA": val,
            "main.publicKeyA": val,
            "main.privateKeyB": val,
            "main.publicKeyB": val,
            "main.sharedA": val,
            "main.sharedB": val,
        }
        base = CIRCL_Base(5, "path", "args")
        result = base.map_functions(dic)
        self.assertEqual(len(result), 6)
        self.assertEqual(result["PublicKeyA"], val)
        self.assertEqual(result["PublicKeyB"], val)
        self.assertEqual(result["SecretA"], val)
        self.assertEqual(result["SecretB"], val)
        self.assertEqual(result["PrivateKeyA"], val)
        self.assertEqual(result["PrivateKeyB"], val)

class TestMicrosoft(TestCase):
    def test_map_functions(self):
        val = MagicMock()
        dic = {
            "random_mod_order_A": val,
            "EphemeralKeyGeneration_A": val,
            "random_mod_order_B": val,
            "EphemeralKeyGeneration_B": val,
            "EphemeralSecretAgreement_A": val,
            "EphemeralSecretAgreement_B": val,
        }
        base = Microsoft_Base(5, "path", "args")
        result = base.map_functions(dic)
        self.assertEqual(len(result), 6)
        for key, value in result.items():
            self.assertEqual(value, val)
    
    def test_get_matching(self):
        dic ={
            "a":1,
            "b":2,
            "bb":3,
            "cb": 4
        }
        self.assertEqual(get_matching(dic, "a"), 1)
        self.assertEqual(get_matching(dic, "b"), 2)
        self.assertEqual(get_matching(dic, "c"), 4)
        self.assertEqual(get_matching(dic, "d"), None)


class TestSIKE(TestCase):
    def test_map_functions(self):
        base = Sike_Base(MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock())

        val = MagicMock()
        dic = {
            "random_mod_order_A": val,
            "EphemeralKeyGeneration_A": val,
            "random_mod_order_B": val,
            "EphemeralKeyGeneration_B": val,
            "EphemeralSecretAgreement_A": val,
            "EphemeralSecretAgreement_B": val,
        }
        result = base.sike_map_functions(dic, False)
        self.assertEqual(len(result), 6)
        self.assertEqual(result["PublicKeyA"], val)
        self.assertEqual(result["PublicKeyB"], val)
        self.assertEqual(result["SecretA"], val)
        self.assertEqual(result["SecretB"], val)
        self.assertEqual(result["PrivateKeyA"], val)
        self.assertEqual(result["PrivateKeyB"], val)

        # Compressed
        dic = {
            "random_mod_order_A": val,
            "EphemeralKeyGeneration_Compressed_A": val,
            "random_mod_order_B": val,
            "EphemeralKeyGeneration_Compressed_B": val,
            "EphemeralSecretAgreement_Compressed_A": val,
            "EphemeralSecretAgreement_Compressed_B": val,
        }
        result = base.sike_map_functions(dic, True)
        self.assertEqual(len(result), 6)
        self.assertEqual(result["PublicKeyA"], val)
        self.assertEqual(result["PublicKeyB"], val)
        self.assertEqual(result["SecretA"], val)
        self.assertEqual(result["SecretB"], val)
        self.assertEqual(result["PrivateKeyA"], val)
        self.assertEqual(result["PrivateKeyB"], val)

    def test_sike_reference_test_functions(self):
        val = MagicMock()
        dic = {
            "sidh_sk_keygen_A": val,
            "sidh_isogen_A": val,
            "sidh_sk_keygen_B": val,
            "sidh_isogen_B": val,
            "sidh_isoex_A": val,
            "sidh_isoex_B": val,
        }
        base = Sike_Reference(5)
        result = base.map_functions(dic)
        self.assertEqual(len(result), 6)
        self.assertEqual(result["PublicKeyA"], val)
        self.assertEqual(result["PublicKeyB"], val)
        self.assertEqual(result["SecretA"], val)
        self.assertEqual(result["SecretB"], val)
        self.assertEqual(result["PrivateKeyA"], val)
        self.assertEqual(result["PrivateKeyB"], val)