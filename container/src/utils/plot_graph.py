import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Process
from pathlib import Path


def map_float(x): return float(x.replace(".", ""))


def map_round(x): return round(float(x)/1000000, 1)


def autolabel(rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


def plot_memory(curve, benchmarks, ecdh_compare=None):
    # benchmarks is list of BenchmarkCurve objects
    labels = ["Memory"]
    title = 'Maximum memory consumption in kilobytes for p' + str(curve)
    y_axis = 'Memory in Kilobytes'

    number_of_implementations = len(benchmarks) + (1 if ecdh_compare else 0)
    
    x = np.arange(len(labels))
    width = 0.8/number_of_implementations
    offset = -width*(number_of_implementations/2)

    fig, ax = plt.subplots()

    count = 0

    if ecdh_compare:
        values = [round(ecdh_compare.find_benchmark(
            "Memory", "not found")/1000, 1)]
        ecdh = ax.bar(x + offset + 0.1 , values, width,
                      label='ECDH (Reference value)')
        autolabel(ecdh, ax)
        count += 1


    for benchmark in benchmarks:
        values = [round(benchmark.find_benchmark(
            "Memory", "not found")/1000, 1)]
        rec = ax.bar(x + width*count + offset, values,
                     width, label=benchmark.impl.name)
        autolabel(rec, ax)
        count += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel(y_axis)
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels([])
    ax.legend()
    ax.set_ylim(bottom=0)
    fig.set_size_inches(18, 8)

    Path("data").mkdir(parents=True, exist_ok=True)
    fig.savefig('data/' + str(curve) + '_mem.png', dpi=100)


def plot_instructions(curve, benchmarks, ecdh_compare=None):
    # benchmarks is list of BenchmarkCurve objects
    labels = ['Keygen A', 'Keygen B', 'Secret A', 'Secret B']
    title = 'Overall Instructions for Parameters ' + str(curve)
    y_axis = 'Overall Instructions in 1.000.000'

    number_of_implementations = len(benchmarks) + (1 if ecdh_compare else 0)
    
    x = np.arange(len(labels))
    width = 0.8/number_of_implementations
    offset = -width*(number_of_implementations/2)

    fig, ax = plt.subplots()

    count = 0
    if ecdh_compare:
        values = list(map(map_round, ecdh_compare.get_benchmarks_for_plot()))
        ecdh = ax.bar(x + offset, values, width,
                      label='ECDH (Reference value)')
        autolabel(ecdh, ax)
        count += 1

    for benchmark in benchmarks:
        values = list(map(map_round, benchmark.get_benchmarks_for_plot()))
        rec = ax.bar(x + width*count + offset, values,
                     width, label=benchmark.impl.name)
        autolabel(rec, ax)
        count += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel(y_axis)
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.set_ylim(bottom=0)
    fig.set_size_inches(18, 8)

    Path("data").mkdir(parents=True, exist_ok=True)
    fig.savefig('data/' + str(curve) + '.png', dpi=100)


def generate_graph(result):
    curves = ["434", "503", "610", "751"]
    processes = []
    if "ECDH" in result:
        ecdh = result["ECDH"].curves[0]
    else:
        ecdh = None
    ecdh = None

    for curve in curves:
        # 1. Collect all benchmarks for specific curve
        benchmarks = []
        implementations = [
            "CIRCL_x64_Implementation",
            #"Microsoft_x64_Implementation",
            #"Microsoft_x64_Implementation_Compressed",
            "Sike_Optimized_Implementation",
            "Sike_Optimized_Implementation_Compressed",
            "Sike_x64_Implementation",
            #"Sike_x64_Implementation_Compressed",
            #"Sike_Reference_Implementation",
            #"ECDH_Implementation"
        ]
        for name, impl in result.items():
            # Ignore these implementations
            if impl.name not in implementations:
                continue
            found = impl.get_benchmarks_of_curve(curve)
            if found:
                benchmarks.append(found)
        # 2. Generate plots
        if benchmarks:
            # 2.1 Generates plots regarding instructions
            p1 = Process(target=plot_instructions, args=(curve, benchmarks, ecdh))
            p1.start()
            # 2.2 Generate plots regarding memory
            p2 = Process(target=plot_memory, args=(curve, benchmarks, ecdh))
            p2.start()
            processes.append(p1)
            processes.append(p2)
    for p in processes:
        p.join()
