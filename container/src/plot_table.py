from pathlib import Path
from prettytable import PrettyTable


def format_number(number):
    return format(round(int(number)), ",").replace(",", ".")


def generate_table(results):
    with open('pre.html', "r") as file:
        preHTML = file.read()

    Path("data").mkdir(parents=True, exist_ok=True)
    with open('data/result.html', 'w') as file:
        file.write(
            preHTML + "<p>All values (except memory) are absolute instruction counts.</p><p>*Maximum memory consumption in bytes.</p>")
        for name, impl in results.items():
            file.write("<h1>" + name + "</h1>")
            file.write(table_from_implementation(
                impl).replace("Memory", "Memory*"))
        file.write("</body></html>")


def table_from_implementation(result):
    # result is instance of class BenchmarkImpl
    TABLE = PrettyTable()
    TABLE.field_names = result.get_benchmark_names()

    for curve in result.curves:
        values = curve.get_benchmark_values()
        values = [format_number(val) for val in values]
        TABLE.add_row(values)

    return TABLE.get_html_string()
