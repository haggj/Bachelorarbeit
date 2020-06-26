
from prettytable import PrettyTable
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from multiprocessing import Process


def autolabel(rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


def plotCurve(result, name, memory=False):
    
    labels = []
    if not memory:
        labels = ['PrivateKeyA', 'PublicKeyA', 'PrivateKeyB', 'PublicKeyB', 'SecretA', 'SecretB']
        #ecdh_means = list(result["ECDH"][0].values())[1:-1]
        n = 4
        title = 'Instructions by Implementation for SIKE '
        y_axis = 'Overall Instructions in 1.000.000'
    else:
        labels = ["Memory"]
        #ecdh_means = list(result["ECDH"][0].values())[-1]
        n = 1
        title = 'Maximum Memory by Implementation for SIKE '
        y_axis = 'Memory in Kilobytes'



    x = np.arange(len(labels)) + 20 # the label locations
    width = 0.2  # the width of the bars   

    ###### p434 Plot ######
    fig, ax = plt.subplots()
    #rects1 = ax.bar(x - width/2, ecdh_means, width, label='ECDH')

    count = 0

    for implementation, list_of_results in result.items():
        #print(implementation)
        for curve in list_of_results:
            #print(curve)
            if name == curve['Curve']:
                if not memory:
                    mean = list(map(lambda x: int(int(x.replace(".", ""))/1000000), list(curve.values())[1:-1]))
                    rec = ax.bar(x + width*count - width*n/2 + width/2, mean, width, label=implementation)
                else:
                    mean = list(curve.values())[-1]
                    mean = [round(int(mean.replace(".", ""))/1000,1)]
                    rec = ax.bar(x + width*count - width*n/2 + width/2, mean, width, label=implementation)

                
                autolabel(rec, ax)
                count += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel(y_axis)
    ax.set_title(title + name)
    ax.set_xticks(x)
    ax.set_xticklabels([] if memory else labels)
    ax.legend()
    ax.set_ylim(bottom=0)
    fig.set_size_inches(15, 8)

    if not memory:
        fig.savefig('diagrams/' + name +'.png', dpi=100)
    else:
        fig.savefig('diagrams/' + name + '_mem.png', dpi=100)


def generatePlot(result):
    # Compare Curves regarding absolut Instructions
    curves = ["p434", "p503" , "p610", "p751"]
    processes = []
    for curve in curves:
        r = result
        p1 = Process(target=plotCurve, args=(r, curve, False))
        p1.start()
        p2 = Process(target=plotCurve, args=(r, curve, True))
        p2.start()
        processes.append(p1)
        processes.append(p2)
    
    for p in processes:
        p.join()
    
    # Compare Curves regarding Memory

        
    


def print_statistics(result):
    #result is list of dictionaries
    TABLE = PrettyTable()
    TABLE.field_names = list(result[0].keys())

    for r in result:
        TABLE.add_row(list(r.values()))

    print(TABLE)