"""
Helper functions to generate a html table and a latex table of the results of the benchmarking suite.
No tests are available for this function, since these functions simply create output tables.
"""
from pathlib import Path

from numpy import transpose
from prettytable import PrettyTable


def generate_table(results):
    generate_html_table(results)
    generate_latex_table(results)


def generate_html_table(results):
    with open('helper/pre.html', "r") as file:
        preHTML = file.read()

    Path("data").mkdir(parents=True, exist_ok=True)
    with open('data/result.html', 'w') as file:
        file.write(
            preHTML + "<p>All values (except Memory) are averages of absolute instruction counts. <br> All values in brackets are the standard derivation over N samples.</p>" + \
            "<p>*Maximum memory consumption in bytes.</p>")
        for name, impl in results.items():
            file.write("<h1>" + name + "</h1>")
            file.write(html_from_implementation(
                impl).replace("Memory", "Memory*"))
        file.write("</body></html>")


def generate_latex_table(results):
    Path("data").mkdir(parents=True, exist_ok=True)
    with open('data/result.tex', 'w') as file:
        for _, impl in results.items():
            file.write(latex_from_implementation(impl))


def latex_from_implementation(result):
    # Create table of the form
    # name | value1 | value2 | ...
    # tom  |   d    |   e    | ...
    # ...
    # pylint: disable=W1401

    table = [result.get_benchmark_names()]
    for curve in result.curves:
        table.append(curve.get_benchmark_values("\\\\"))

    # Inverse the table to obtain the form
    # name    |   tom  | ...
    # value1  |   d    |  
    # value2  |   e    |   
    # ...

    table = transpose(table)

    caption_short = caption_long = "Benchmarks for " + result.name.replace("_", " ")

    headers = table[0]
    headers = ["\\bfseries\makecell{" + str(val) + "}" for val in headers]

    pre_table = \
        "\subsection{" + caption_long + "}\n\\begin{table}[H]\n\t\\centering\n\t\\begin{tabular}{|" + len(
            headers) * r"K{2.5cm}|" + "}\n\t\\hline\n\t\\rowcolor{lightgray!50}\n\t" + \
        " & ".join(headers) + "\\\\\n"

    post_table = \
        "\n\t\hline\n\t\end{tabular}" + \
        "\n\t\caption[" + caption_short + "]{" + caption_long + "}" + \
        "\n\t\label{tab:benchmarks_" + result.name + "}" + \
        "\n\end{table}\n"

    table_str = pre_table
    for row in table[1:-1]:
        cells = [format_latex_cell(val) for val in row]
        row_str = "\t\hline\n\t" + " & ".join(cells) + "\\\\\n"
        table_str += row_str
    table_str += post_table
    return table_str + format_latex_hotspots(table[0], table[-1])


def format_latex_hotspots(heading, hotspots):
    res = ""
    for idx, name in enumerate(heading[1:]):
        res += "Execution hotspots parameter \\textit{" + name + "}:\n"
        res += "\\begin{enumerate}[noitemsep]"
        for hotspot in hotspots[idx + 1].split("\\\\"):
            fun = escape_latex(hotspot).split(" ")[0]
            percentage = escape_latex(hotspot).split(" ")[1]
            res += "\n\t\\item " + "\\texttt{" + fun + "} " + percentage
        res += "\n\\end{enumerate}\n"
    return res


def escape_latex(val):
    # pylint: disable=W1401
    con = val.replace("%", "\%")
    con = con.replace("_", "\_")
    return con


def format_latex_cell(val):
    # pylint: disable=W1401
    con = escape_latex(str(val))
    if (val == "Memory"):
        return "\makecell{" + con + "\\\\in bytes}"
    return "\makecell{" + con + "}"


def html_from_implementation(result):
    # result is instance of class BenchmarkImpl
    TABLE = PrettyTable()
    TABLE.field_names = result.get_benchmark_names()

    for curve in result.curves:
        values = curve.get_benchmark_values()
        TABLE.add_row(values)

    return TABLE.get_html_string()
