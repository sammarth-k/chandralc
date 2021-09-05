"""The future of CXO Lightcurve Analysis."""

# PSL modules
import os
import inspect

# chandralc modules
from chandralc import download

clc_path = os.path.dirname(inspect.getfile(download))

# config files
try:
    os.mkdir(clc_path + "/config")
except:
    pass

if "mpl_backend.chandralc" not in os.listdir(clc_path + "/config"):
    with open(clc_path + "/config/mpl_backend.chandralc", "w") as f:
        f.write("False")

from chandralc.chandra_lightcurve import *

# Download Database Indices
download.download_db()
