import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from multiprocessing import Process
from pathlib import Path

def autolabel(rects, ax):
    """
    Attach a text label above each bar displaying its height
    """

    data_line, capline, barlinecols = rects.errorbar

    for err_segment, rect in zip(barlinecols[0].get_segments(), rects):
        height = err_segment[1][1]  # Use height of error bar

        ax.text(rect.get_x() + rect.get_width() / 2, 
                1.01 * height,
                f'{height:.0f}',
                ha='center', va='bottom')

def plot_any(data, labels, file=None, title=None, y_axis="", log=False):
    # data = [
    #     {name:"sike generic",
    #     averages: [2,3,4,5],
    #     deviations: [0,0,0,0]},
    #     {name:"sike generic",
    #     averages: [2,3,4,5],
    #     deviations: [0,0,0,0]},
    #     {name:"sike generic",
    #     averages: [2,3,4,5],
    #     deviations: [0,0,0,0]},
    # ]
    # labels = ["keygena", "keygenb", "keygenc", "keygend"]


    number_of_implementations = len(data)
    
    x = np.arange(len(labels))
    width = 0.8/number_of_implementations
    offset = -width*(number_of_implementations/2)

    fig, ax = plt.subplots()

    count = 0

    for date in data:
        averages = date["values"]
        deviations = date.get("deviations")
        if deviations:
            rec = ax.bar(x + width*count + offset, 
                        averages,
                        width, 
                        label=date["name"],
                        yerr=deviations, 
                        capsize=10)
        else:
            rec = ax.bar(x + width*count + offset, 
                        averages,
                        width, 
                        label=date["name"])
        autolabel(rec, ax)
        count += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    if title:
        ax.set_title(title)
    # Logarithmic y-axis
    if log:
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
    if file:
        Path("data").mkdir(parents=True, exist_ok=True)
        fig.savefig('data/' + file + '.png', dpi=100, bbox_inches='tight')

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
        "Sike_Generic",
        #"Sike_Generic_Compressed",
        "Sike_x64",
        #"Sike_x64_Compressed",

        #MICROSOFT
        "Microsoft_Generic",
        #"Microsoft_Generic_Compressed",
        "Microsoft_x64",
        #"Microsoft_x64_Compressed",

        #CIRCL
        "CIRCL_Generic",
        "CIRCL_x64",

        #ECDH
        "ECDH",
    ]
    
    font = {'size': 18}
    matplotlib.rc('font', **font)
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=['#F9C74F', '#577590', '#F94144', '#43AA8B', '#F3722C', '#90BE6D'])
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=['#1F77B4', '#FF7F0E', '#2CA02C', '#D62728', '#9467BD', '#ffdd00'])

    
    for curve in curves:
        # 1. Collect all benchmarks for specific curve
        data_instructions = []
        data_memory = []
        for name in implementations:
            impl = result.get(name)
            if not impl:
                print("Could not find " + name)
                continue
            found = impl.get_curve_by_name(map_to_ecdh(curve) if impl.name == "ECDH" else curve)
            if found:
                # Instructions
                values, deviations = found.get_benchmarks_for_plot()
                dic = {
                    "name": impl.name + ("(Reference Value)" if impl.name == "ECDH" else ""),
                    "values": values,
                    "deviations": deviations,
                }
                data_instructions.append(dic)

                # Memory
                values = [round(found.benchmark_average("Memory")/1000, 1)]
                deviations = [round(found.benchmark_stdev("Memory")/1000, 1)]
                dic = {
                    "name": impl.name + ("(Reference Value)" if impl.name == "ECDH" else ""),
                    "values": values,
                    "deviations": deviations,
                }
                data_memory.append(dic)

        plot_any(   data=data_instructions, 
                    labels=['Keygen A', 'Keygen B', 'Secret A', 'Secret B'],
                    log=True,
                    file= str(curve),
                    y_axis="Overall Instructions in 1.000.000\n")

        plot_any(   data=data_memory, 
                    labels=[''],
                    log=False,
                    file= str(curve) +"mem",
                    y_axis="Memory in Kilobytes")
    
    # Compare parameters among Microsoft_x64
    name = "Sike_x64"
    data_instructions = []
    data_memory = []
    for curve in curves:
        impl = result.get(name)
        if not impl:
            break
        found = impl.get_curve_by_name(curve)
         # Instructions
        values, deviations = found.get_benchmarks_for_plot()
        dic = {
            "name": "p" + curve,
            "values": values,
            "deviations": deviations,
        }
        data_instructions.append(dic)

        # Memory
        values = [round(found.benchmark_average("Memory")/1000, 1)]
        deviations = [round(found.benchmark_stdev("Memory")/1000, 1)]
        dic = {
            "name": "p" + curve,
            "values": values,
            "deviations": deviations,
        }
        data_memory.append(dic)


    plot_any(   data=data_instructions, 
            labels=['Keygen A', 'Keygen B', 'Secret A', 'Secret B'],
            log=False,
            file="SIKE_x64",
            y_axis="Overall Instructions in 1.000.000\n")

    plot_any(   data=data_memory, 
                labels=[''],
                log=False,
                file="SIKE_x64_mem",
                y_axis="Memory in Kilobytes")