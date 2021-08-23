"""This subpackage contains modules to use various APIs."""
import os
import csv

# make logs directory if it does not exist
try:
    os.mkdir("./logs")
except:
    pass

# make ADS log file if it does not exist
if "ads.csv" not in os.listdir("./logs"):
    with open("./logs/ads.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "URL"])
