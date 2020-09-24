from pathlib import Path
from prettytable import PrettyTable



def generate_table(results):
    generate_html_table(results)
    generate_latex_table(results)

def generate_html_table(results):
    with open('pre.html', "r") as file:
        preHTML = file.read()

    Path("data").mkdir(parents=True, exist_ok=True)
    with open('data/result.html', 'w') as file:
        file.write(
            preHTML + "<p>All values (except memory) are absolute instruction counts.</p><p>*Maximum memory consumption in bytes.</p>")
        for name, impl in results.items():
            file.write("<h1>" + name + "</h1>")
            file.write(html_from_implementation(
                impl).replace("Memory", "Memory*"))
        file.write("</body></html>")

def generate_latex_table(results):

    Path("data").mkdir(parents=True, exist_ok=True)
    with open('data/result.tex', 'w') as file:
        for name, impl in results.items():
            file.write(latex_from_implementation(impl))

   


def latex_from_implementation(result):

    caption_short = caption_long = result.name.replace("_", " ")

    headers = result.get_benchmark_names()
    headers = ["\\bfseries\makecell{" + str(val)+ "}"  for val in headers]

    pre_table = \
        "\\begin{table}[htpb]\n\t\\centering\n\t\\begin{tabular}{|" + len(headers)*r"K{1cm}|" +"}\n\t\\hline\n\t\\rowcolor{lightgray!50}\n\t" + \
        " & ".join(headers) + "\\\\\n"

    post_table = \
        "\n\t\end{tabular}\n\t\caption[" + caption_short + "]{" + caption_long + "}\n\end{table}\n"

    table = pre_table
    for curve in result.curves:
        cells = ["\makecell{" + str(val).replace("%", "\%").replace("_", "\_") + "}" for val in curve.get_benchmark_values(newline="\\\\")]
        row = "\t\hline\n\t" + " & ".join(cells) + "\\\\\n"
        table+=row
    table += post_table
    return table
    


def html_from_implementation(result):
    # result is instance of class BenchmarkImpl
    TABLE = PrettyTable()
    TABLE.field_names = result.get_benchmark_names()

    for curve in result.curves:
        values = curve.get_benchmark_values()
        TABLE.add_row(values)

    return TABLE.get_html_string()
