"""Module to view chandra logs."""

# PSL
import csv
import os
import inspect

# external modules
from prettytable import PrettyTable

# chandralc modules
from chandralc import convert

# get path of installation
clc_path = os.path.dirname(inspect.getfile(convert))


def _csv2ascii(reader):
    """Convert CSV to ASCII Table."""

    reader = list(reader)

    x = PrettyTable()

    # add filed names to table
    x.field_names = reader[0]

    # add table content
    for row in reader[1:]:
        x.add_row(row)

    return x.get_string()


def _display(log):
    with open(f"{clc_path}/logs/{log}.csv", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        print(_csv2ascii(reader))
