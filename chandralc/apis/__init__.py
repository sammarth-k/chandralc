"""This subpackage contains modules to use various APIs."""

# PSL Modules
import os
import csv
import inspect

# chandralc modules
from chandralc import convert

clc_path = os.path.dirname(inspect.getfile(convert))

# make logs directory if it does not exist
try:
    os.mkdir(clc_path + "/logs")
except:
    pass

# make ADS log file if it does not exist
if "ads.csv" not in os.listdir(clc_path + "/logs"):
    with open(clc_path + "/logs/ads.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "URL"])
