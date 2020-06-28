from src.base import Base_Implementation, getCallgrindFunctionCalls, bash, bcolors
import progressbar
import pandas

curves = ["434","503","751"]

class CIRCL_x64_Implementation(Base_Implementation):

    def __init__(self):
        self.path = "CIRCL/"
        self.args = ""

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

    def callgrind_result(self):
        calls = getCallgrindFunctionCalls(self.path+"/benchmarks/callgrind.out", "main.main")
        return self.map_functions(calls)

    def callgrind_average(self, count):
        results = []
        for i in progressbar.progressbar(range(count), redirect_stdout=True, prefix="    Callgrind "):
            count = 0
            while True:
                try:
                    bash('make callgrind -C {}'.format(self.path))
                    break
                except Exception as e:
                    count +=1
                    if count == 10:
                        print("Callgrind for CIRCL failed 3 times, exiting...")
                        exit(0)
                    
            res = self.callgrind_result()
            results.append(res)

        df = pandas.DataFrame(results)
        average = dict(df.mean())
        return average