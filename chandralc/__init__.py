"""The future of CXO Lightcurve Analysis."""

# PSL modules
import os
import inspect

# chandralc modules
from chandralc import download
from chandralc.chandra_lightcurve import *

clc_path = os.path.dirname(inspect.getfile(download))

# config files
if os.path.isdir(os.path.join(clc_path, "config")) is False:
    os.mkdir(os.path.join(clc_path, "config"))

if "mpl_backend.chandralc" not in os.listdir(clc_path + "/config"):
    with open(clc_path + "/config/mpl_backend.chandralc", "w", encoding="utf-8") as f:
        f.write("False")

# Download Database Indices
download.download_db()
