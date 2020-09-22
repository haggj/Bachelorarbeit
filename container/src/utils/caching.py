import json
import os

from src.base import bcolors, BenchmarkCurve, BenchmarkImpl, Benchmark


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        dic = dict(obj.__dict__)
        if "impl" in dic:
            del dic["impl"]
        return dic


def save_as_json(result):
    if os.path.isfile("cached.json"):
        with open('data/cached.json', 'a') as f:
            json.dump(result, f, cls=MyEncoder)
    else:
        with open('data/cached.json', 'w+') as f:
            json.dump(result, f,  cls=MyEncoder)


def deserialize_impl(dic):
    if "curves" in dic and "name" in dic:
        if isinstance(dic["curves"], list):
            impl = BenchmarkImpl(dic["name"])
            for curve in dic["curves"]:
                impl.add_curve(deserialize_curve(curve))
            return impl
    return None


def deserialize_curve(dic):
    if "benchmarks" in dic and "name" in dic:
        if isinstance(dic["benchmarks"], list):
            curve = BenchmarkCurve(dic["name"])
            for benchmark in dic["benchmarks"]:
                curve.add_benchmarks(deserialize_benchmarks(benchmark))
                curve.set_hotspots(dic["hotspots"])
            return curve
    return None


def deserialize_benchmarks(dic):
    if "values" in dic and "name" in dic:
        if isinstance(dic["values"], list):
            return Benchmark(dic["name"], dic["values"])


def load_from_json():
    if os.path.isfile("data/cached.json"):
        with open('data/cached.json', 'r') as f:
            cached = json.load(f)
            serialized = {}
            for name, dic in cached.items():
                serialized[name] = deserialize_impl(dic)

            print("\nUsing cached data for:\n" + bcolors.WARNING +
                  "\t\n".join(cached.keys()) + bcolors.ENDC)
            return serialized
    return {}
