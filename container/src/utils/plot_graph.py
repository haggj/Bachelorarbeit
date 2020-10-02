import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from multiprocessing import Process
from pathlib import Path

def map_round(x):
    scaled = float(x)/1000000
    if scaled < 1:
        return round(scaled, 1)
    return int(scaled)

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
    title = 'Maximum memory consumption in kilobytes for p' + str(curve) + "\n\n"
    y_axis = 'Memory in Kilobytes\n'

    font = {'size': 18}
    matplotlib.rc('font', **font)

    number_of_implementations = len(benchmarks) + (1 if ecdh_compare else 0)
    
    x = np.arange(len(labels))
    width = 0.8/number_of_implementations
    offset = -width*(number_of_implementations/2)

    fig, ax = plt.subplots()

    count = 0


    for benchmark in benchmarks:
        values = [round(benchmark.find_benchmark(
            "Memory", "not found")/1000, 1)]
        rec = ax.bar(x + width*count + offset, values,
                     width, label=benchmark.impl.name)
        autolabel(rec, ax)
        count += 1

    if ecdh_compare:
        values = [round(ecdh_compare.find_benchmark(
            "Memory", "not found")/1000, 1)]
        ecdh = ax.bar(x + width*count + offset, values, width,
                      label = 'ECDH '+ecdh_compare.name+' (Reference value)')
        autolabel(ecdh, ax)
        count += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel(y_axis)
    #ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels([])
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, ncol=6)
    ax.set_ylim(bottom=0)
    fig.set_size_inches(20, 10)

    Path("data").mkdir(parents=True, exist_ok=True)
    fig.savefig('data/' + str(curve) + '_mem.png', dpi=100, bbox_inches='tight')


def plot_instructions(curve, benchmarks, ecdh_compare=None):
    # benchmarks is list of BenchmarkCurve objects
    labels = ['Keygen A', 'Keygen B', 'Secret A', 'Secret B']
    title = 'Overall Instructions for p' + str(curve) + '\n\n'
    y_axis = 'Overall Instructions in 1.000.000\n'

    number_of_implementations = len(benchmarks) + (1 if ecdh_compare else 0)
    
    x = np.arange(len(labels))
    width = 0.8/number_of_implementations
    offset = -width*(number_of_implementations/2)

    fig, ax = plt.subplots()

    count = 0

    for benchmark in benchmarks:
        values = list(map(map_round, benchmark.get_benchmarks_for_plot()))
        rec = ax.bar(x + width*count + offset, values,
                     width, label=benchmark.impl.name)
        autolabel(rec, ax)
        count += 1

    if ecdh_compare:
        values = list(map(map_round, ecdh_compare.get_benchmarks_for_plot()))
        ecdh = ax.bar(x + width*count + offset, values, width,
                      label='ECDH '+ecdh_compare.name+' (Reference value)')
        autolabel(ecdh, ax)
        count += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    #ax.set_title(title)
    # Logarithmic y-axis
    plt.yscale("log")
    plt.gca().yaxis.set_major_formatter(ScalarFormatter())
    ax.set_ylabel(y_axis)
    # X-axis
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    # Legend
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, ncol=6)
    # size
    fig.set_size_inches(20, 10)

    # Save as file
    Path("data").mkdir(parents=True, exist_ok=True)
    fig.savefig('data/' + str(curve) + '.png', dpi=100, bbox_inches='tight')

def map_to_ecdh(curve):
    if curve == "434":
        return "secp256"
    if curve == "503":
        return "secp384"
    if curve == "751":
        return "secp521"
    return None

def generate_graph(result):
    curves = ["434", "503", "610", "751"]
    implementations =[
        #SIKE
        #"Sike_Reference",
        #"Sike_Generic",
        #"Sike_Generic_Compressed",
        #"Sike_x64",
        #"Sike_x64_Compressed",

        #MICROSOFT
        "Microsoft_Generic",
        "Microsoft_Generic_Compressed",
        "Microsoft_x64",
        "Microsoft_x64_Compressed",

        #CIRCL
        #"CIRCL_x64",

        #ECDH
        #"ECDH",
    ]
    processes = []
    font = {'size': 18}
    matplotlib.rc('font', **font)
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=['#F9C74F', '#577590', '#F94144', '#43AA8B', '#F3722C', '#90BE6D'])
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=['#1F77B4', '#FF7F0E', '#2CA02C', '#D62728', '#9467BD', '#ffdd00'])

    for curve in curves:
        # 1. Collect all benchmarks for specific curve
        benchmarks = []
        for name in implementations:
            # Ignore these implementations
            impl = result.get(name)
            if not impl:
                continue
            found = impl.get_curve_by_name(curve)
            if found:
                benchmarks.append(found)
        # 2. Choose ECDH as comparision
        ecdh = None
        if "ECDH" in implementations and "ECDH" in result:
            if map_to_ecdh(curve):
                ecdh = result["ECDH"].get_curve_by_name(map_to_ecdh(curve))
        # 3. Generate plots
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
